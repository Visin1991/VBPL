bl_info = {
    "name": "Bake Selected Image",
    "author": "Fahad Hasan Pathik CGVIRUS",
    "version": (0, 2),
    "blender": (2, 80, 0),
    "location": "Toolshelf > Layers Tab",
    "description": "Bake Texture Easily with Selected Image",
    "warning": "",
    "wiki_url": "https://github.com/cgvirus/Blender-Bake-Selected-Image-Addon",
    "category": "Bake",
    }


import bpy
from bpy.props import *
from bpy.app.handlers import persistent

class Bake_OT_InputImage(bpy.types.Operator):
    """Input selected image as Image Texture in Material Editor"""
    bl_idname = "obj.image_input"
    bl_label = "Input Selected Image"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def execute(self, context):        
        for o in context.selected_objects:
            if o.type == 'MESH':
                for m in bpy.data.objects[o.name].material_slots:
                    m.material.use_nodes = True
                    node_tree = bpy.data.materials[m.material.name].node_tree


                    img_name = bpy.context.texture.image


                    node = node_tree.nodes.new("ShaderNodeTexImage")
                    node.name = "BakeTex"

                    node.image = img_name

                    node.select = True
                    

                    node_tree.nodes.active = node



            else:
                pass


        return {'FINISHED'}



class Bake_OT_SelectedImage(bpy.types.Operator):
    """Bake image textures of selected objects"""
    bl_idname = "obj.bake_image"
    bl_label = "Bake"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def execute(self, context):
        bake_type = context.scene.cycles.bake_type
        bpy.ops.object.bake('INVOKE_DEFAULT',type = bake_type)


        return {'FINISHED'}




class BAKESELECTED_PT_Panel(bpy.types.Panel):
    
    bl_idname = "BAKESELECTED_PT_Panel"
    bl_label = "Bake Selcted Image"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'CYCLES'}




    def draw(self, context):
        layout = self.layout

        col = layout.column()

        # https://docs.blender.org/manual/en/latest/render/materials/legacy_textures/index.html
        # 检测是否设置了Procedual Texture
        if context.texture_user:
            propname = context.texture_user_property.identifier
            col.template_ID(context.texture_user, propname, new="texture.new")

        # 选择Procedual Texture Type
        if context.texture:
            col.separator()
            split = col.split(factor=0.2)
            split.label(text="Type")
            split.prop(context.texture, "type", text="")

        layout = self.layout

        row = col.row(align=True)
        row = col.row(align=True)
        row.operator("obj.image_input",icon='TRACKING_FORWARDS')

        row = col.row(align=True)
        row = col.row(align=True)
        row.operator("obj.bake_image",icon='RENDER_STILL')

        row = col.row(align=True)

        if context.texture:  
            if type(context.texture) == bpy.types.ImageTexture:
                # Link to a ImageUser......
                layout.template_image(context.texture, "image", context.texture.image_user)
            else:
                layout.label(text="Texture No ImageUser!!!")

# -------------------------------------------------------------------------------------------------------

classes = (
    Bake_OT_InputImage,
    Bake_OT_SelectedImage,
    BAKESELECTED_PT_Panel,
    )


def register():
    # add operator
    from bpy.utils import register_class
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    # remove operator and preferences
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

if __name__ == "__main__":
    register()