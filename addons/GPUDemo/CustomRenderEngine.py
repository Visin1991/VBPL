import bpy
import array
import gpu
from mathutils import Matrix
from gpu_extras.presets import draw_texture_2d
from gpu_extras.presets import draw_circle_2d
from gpu_extras.batch import batch_for_shader


class CustomRenderEngine(bpy.types.RenderEngine):
    # These three members are used by blender to set up the
    # RenderEngine; define its internal name, visible name and capabilities.
    bl_idname = "CUSTOM"
    bl_label = "Custom"
    bl_use_preview = True

    # Init is called whenever a new render engine instance is created. Multiple
    # instances may exist at the same time, for example for a viewport and final
    # render.
    def __init__(self):
        self.scene_data = None
        self.draw_data = None

    # When the render engine instance is destroy, this is called. Clean up any
    # render engine data here, for example stopping running render threads.
    def __del__(self):
        pass

    # This is the method called by Blender for both final renders (F12) and
    # small preview for materials, world and lights.
    def render(self, depsgraph):
        bpy.types.Depsgraph
        scene = depsgraph.scene
        scale = scene.render.resolution_percentage / 100.0
        self.size_x = int(scene.render.resolution_x * scale)
        self.size_y = int(scene.render.resolution_y * scale)

        # Fill the render result with a flat color. The framebuffer is
        # defined as a list of pixels, each pixel itself being a list of
        # R,G,B,A values.
        if self.is_preview:
            color = [0.1, 0.2, 0.1, 1.0]
        else:
            color = [0.2, 0.1, 0.1, 1.0]

        pixel_count = self.size_x * self.size_y
        rect = [color] * pixel_count

        # Here we write the pixel values to the RenderResult
        result = self.begin_result(0, 0, self.size_x, self.size_y)
        layer = result.layers[0].passes["Combined"]
        layer.rect = rect
        self.end_result(result)

    # For viewport renders, this method gets called once at the start and
    # whenever the scene or 3D viewport changes. This method is where data
    # should be read from Blender in the same thread. Typically a render
    # thread will be started to do the work while keeping Blender responsive.
    def view_update(self, context, depsgraph):
        region = context.region
        view3d = context.space_data
        scene = depsgraph.scene

        # Get viewport dimensions
        dimensions = region.width, region.height

        if not self.scene_data:
            # First time initialization
            self.scene_data = []
            first_time = True

            # Loop over all datablocks used in the scene.
            for datablock in depsgraph.ids:
                pass
        else:
            first_time = False

            # Test which datablocks changed
            for update in depsgraph.updates:
                print("Datablock updated: ", update.id.name)

            # Test if any material was added, removed or changed.
            if depsgraph.id_type_updated('MATERIAL'):
                print("Materials updated")

        # Loop over all object instances in the scene.
        if first_time or depsgraph.id_type_updated('OBJECT'):
            for instance in depsgraph.object_instances:
                pass

    # For viewport renders, this method is called whenever Blender redraws
    # the 3D viewport. The renderer is expected to quickly draw the render
    # with OpenGL, and not perform other expensive work.
    # Blender will draw overlays for selection and editing on top of the
    # rendered image automatically.
    def view_draw(self, context, depsgraph):
        region = context.region
        scene = depsgraph.scene

        # Get viewport dimensions
        dimensions = region.width, region.height

        # Bind shader that converts from scene linear to display space,
        gpu.state.blend_set('ALPHA_PREMULT')
        self.bind_display_space_shader(scene)

        if not self.draw_data or self.draw_data.dimensions != dimensions:
            self.draw_data = CustomDrawData(dimensions)

        self.draw_data.draw()

        self.unbind_display_space_shader()
        gpu.state.blend_set('NONE')


class CustomDrawData:
    def __init__(self, dimensions):
        # Generate dummy float image buffer
        self.dimensions = dimensions
        width, height = dimensions

        self.offscreen = gpu.types.GPUOffScreen(512, 512)

        # Drawing the generated texture in 3D space
        #############################################

        vertex_shader = '''
            uniform mat4 modelMatrix;
            uniform mat4 viewProjectionMatrix;

            in vec2 position;
            in vec2 uv;

            out vec2 uvInterp;

            void main()
            {
                uvInterp = uv;
                gl_Position = viewProjectionMatrix * modelMatrix * vec4(position, 0.0, 1.0);
            }
        '''

        fragment_shader = '''
            uniform sampler2D image;

            in vec2 uvInterp;
            out vec4 FragColor;

            void main()
            {
                FragColor = texture(image, uvInterp);
            }
        '''

        self.shader = gpu.types.GPUShader(vertex_shader, fragment_shader)
        self.batch = batch_for_shader(
            self.shader, 'TRI_FAN',
            {
                "position": ((-1, -1), (1, -1), (1, 1), (-1, 1)),
                "uv": ((0, 0), (1, 0), (1, 1), (0, 1)),
            },
        )


        pixels = width * height * array.array('f', [0.1, 0.2, 0.1, 1.0])
        pixels = gpu.types.Buffer('FLOAT', width * height * 4, pixels)

        # Generate texture
        self.texture = gpu.types.GPUTexture((width, height), format='RGBA16F', data=pixels)

        # Note: This is just a didactic example.
        # In this case it would be more convenient to fill the texture with:
        # self.texture.clear('FLOAT', value=[0.1, 0.2, 0.1, 1.0])

    def __del__(self):
        del self.texture
        del self.batch
        del self.shader

    def draw(self):
        draw_texture_2d(self.texture, (0, 0), self.texture.width, self.texture.height)

        # Cache the default final frame buffer for our Render engine
        defaultfb = gpu.state.active_framebuffer_get()

        with self.offscreen.bind():
            fb = gpu.state.active_framebuffer_get()
            fb.clear(color=(0.0, 0.0, 0.0, 0.0))
            with gpu.matrix.push_pop():
                # reset matrices -> use normalized device coordinates [-1, 1]
                gpu.matrix.load_matrix(Matrix.Identity(4))
                gpu.matrix.load_projection_matrix(Matrix.Identity(4))

                amount = 10
                for i in range(-amount, amount + 1):
                    x_pos = i / amount
                    draw_circle_2d((x_pos, 0.0), (1, 1, 1, 1), 0.5, segments=200)

        # Restore to default final frame buffer
        defaultfb.bind()

        # Use Offscreen texture in our shader......
        self.shader.bind()
        self.shader.uniform_float("modelMatrix", Matrix.Translation((1, 2, 3)) @ Matrix.Scale(3, 4))
        self.shader.uniform_float("viewProjectionMatrix", bpy.context.region_data.perspective_matrix)
        self.shader.uniform_sampler("image", self.offscreen.texture_color)
        self.batch.draw(self.shader)


# RenderEngines also need to tell UI Panels that they are compatible with.
# We recommend to enable all panels marked as BLENDER_RENDER, and then
# exclude any panels that are replaced by custom panels registered by the
# render engine, or that are not supported.
def get_panels():
    exclude_panels = {
        'VIEWLAYER_PT_filter',
        'VIEWLAYER_PT_layer_passes',
    }

    panels = []
    for panel in bpy.types.Panel.__subclasses__():
        if hasattr(panel, 'COMPAT_ENGINES') and 'BLENDER_RENDER' in panel.COMPAT_ENGINES:
            if panel.__name__ not in exclude_panels:
                panels.append(panel)

    return panels


def register():
    # Register the RenderEngine
    bpy.utils.register_class(CustomRenderEngine)

    for panel in get_panels():
        panel.COMPAT_ENGINES.add('CUSTOM')


def unregister():
    bpy.utils.unregister_class(CustomRenderEngine)

    for panel in get_panels():
        if 'CUSTOM' in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove('CUSTOM')


if __name__ == "__main__":
    register()