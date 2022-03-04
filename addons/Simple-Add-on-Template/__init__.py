bl_info = {
    "name": "Simple Add-on Template",
    "author": "",
    "location": "",
    "version": (1, 0, 0),
    "blender": (2, 90, 1),
    "description": "Starting point for new add-ons.",
    "wiki_url": "www.google.com",
    "category": "Development"
}

from bmesh.types import BMFace
import bpy
import bmesh
import bpy_extras
import bpy_extras.mesh_utils
import mathutils

def Test_Print_UV_MiniMax(context):
    # Get all UV Datas
    uv_data = []
    uv_data_x =[]
    uv_data_y =[]
    ob = bpy.context.object
    for face in ob.data.polygons:
        for vert_id, loop_id in zip(face.vertices, face.loop_indices):
            # normal = ob.data.vertices[vert_id].normal
            # coord = ob.data.vertices[vert_id].co
            uv = ob.data.uv_layers.active.data[loop_id].uv
            uv_data_x.append(uv.x)
            uv_data_y.append(uv.y)
            uv_data.append(uv)

    # Calculate UV bounding box
    uv_data_x = sorted(uv_data_x)
    uv_data_y = sorted(uv_data_y)
    x_max = uv_data_x[0]
    x_min = uv_data_x[-1]
    y_max = uv_data_y[0]
    y_min = uv_data_y[-1]
    print("UV bounding box : {},{},{},{}".format(x_max,x_min,y_max,y_min))

    
def Test_Unwrap_UV(context:bpy.context):
    context = bpy.context
    ob = context.edit_object
    if ob is None:
        print("Not in selected mode")
        return

    me = ob.data
    bm = bmesh.from_edit_mesh(me)

    # Get Selected Faces and uv layer name
    selfaces = [f for f in bm.faces if f.select]
    uv_layer = bm.loops.layers.uv.active

    # Get Selected UV data
    uv_data = []
    uv_data_x =[]
    uv_data_y =[]
    for f in selfaces:
        for loop in f.loops:
            uv = loop[uv_layer].uv
            uv_data.append(uv_data)
            uv_data_x.append(uv.x)
            uv_data_y.append(uv.y)
    
    # Calculate UV bounding box
    uv_data_x = sorted(uv_data_x)
    uv_data_y = sorted(uv_data_y)
    x_max = uv_data_x[0]
    x_min = uv_data_x[-1]
    y_max = uv_data_y[0]
    y_min = uv_data_y[-1]

    # Calculate UV size 
    x_size = x_max - x_min
    y_size = y_max - y_min
    x_center = x_min + x_size * 0.5
    y_center = y_min + y_size * 0.5


    # unwrap the uv
    bpy.ops.uv.unwrap()

    new_uv_data = []
    new_uv_data_x =[]
    new_uv_data_y =[]
    for f in selfaces:
        for loop in f.loops:
            uv = loop[uv_layer].uv
            new_uv_data.append(uv_data)
            new_uv_data_x.append(uv.x)
            new_uv_data_y.append(uv.y)
    
    # Calculate NewUV bounding box
    new_uv_data_x = sorted(new_uv_data_x)
    new_uv_data_y = sorted(new_uv_data_y)
    x_max = new_uv_data_x[0]
    x_min = new_uv_data_x[-1]
    y_max = new_uv_data_y[0]
    y_min = new_uv_data_y[-1]

    new_x_size = x_max - x_min
    new_y_size = y_max - y_min
    new_x_center = x_min + x_size * 0.5
    new_y_center = y_min + y_size * 0.5
            

def Test_Porcess_UV_Island(context):
    ob = context.object
    me = ob.data
    scene = context.scene

    bpy.ops.object.mode_set(mode ='EDIT') 
    bm = bmesh.from_edit_mesh(me)

    bm.select_mode = {'FACE'}
    faceGroups = []
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')

    
    save_sync = scene.tool_settings.use_uv_select_sync
    scene.tool_settings.use_uv_select_sync = True
    faces = set(bm.faces[:])
    bm.free()
    
    while faces:
        bpy.ops.mesh.select_all(action='DESELECT')  
        face = faces.pop() 
        face.select = True
        bpy.ops.uv.select_linked()
        selected_faces = {f for f in faces if f.select}
        selected_faces.add(face) # this or bm.faces above?
        faceGroups.append(selected_faces)
        faces -= selected_faces

    scene.tool_settings.use_uv_select_sync = save_sync

    for group in faceGroups:
        print("=============Process UV Island================")
        for face in group:
            print("Process a face......")
            #bmesh.types.BMesh.faces
            #bmesh.types.BMFace.loops
            #bmesh.types.BMLoop
            for bmloop in face.loops:
                print(bmloop.index)
    print("===================Done========================")

    bpy.ops.object.mode_set(mode ='OBJECT') 

#==================================================================================================================

class Print_UV_Island(bpy.types.Operator):
    bl_idname = "object.process_mesh"
    bl_label = "Process a mesh......"
    def execute(self,context):
        Test_Porcess_UV_Island(context)
        return {'FINISHED'}

class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Print an Encouraging Message"
    def execute(self, context):
        print("\n\n####################################################")
        print("# Add-on and Simple Operator executed successfully!")
        print("# " + context.scene.encouraging_message)
        print(bpy.context.active_object)
        Test_Unwrap_UV(context)
        print("####################################################")
        return {'FINISHED'}
    @classmethod
    def register(cls):
        print("Registered class: %s " % cls.bl_label)
        # Register properties related to the class here
        bpy.types.Scene.encouraging_message = bpy.props.StringProperty(
        name="",
        description="Message to print to user",
        default="Have a nice day!")
    @classmethod
    def unregister(cls):
        print("Unregistered class: %s " % cls.bl_label)
        # Delete parameters related to the class here
        del bpy.types.Scene.encouraging_message

# A simple button and input field in the Tools panel
class SimplePanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Simple Addon"
    bl_label = "Call Simple Operator"
    #bl_context = "objectmode"

    def draw(self, context):
        self.layout.operator("object.simple_operator",text="Print Encouraging Message")
        self.layout.prop(context.scene, 'encouraging_message')

        self.layout.split()
        self.layout.operator("object.process_mesh",text="Print all mesh island")



    @classmethod
    def register(cls):
        print("======================================")
        print("Registered class: %s " % cls.bl_label)
        # Register properties related to the class here.

    @classmethod
    def unregister(cls):
        print("Unregistered class: %s " % cls.bl_label)
        # Delete parameters related to the class here

classes = (
   Print_UV_Island, 
   SimpleOperator,
   SimplePanel,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
   register()