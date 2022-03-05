bl_info = {
    "name": "Simple UV",
    "author": "Visin",
    "location": "",
    "version": (0, 0, 1),
    "blender": (2, 90, 1),
    "description": "Some UV tools",
    "wiki_url": "https://github.com/Visin1991/VBPL/tree/main/addons/SimpleUV",
    "category": "Development"
}

from enum import Enum
from bmesh.types import BMFace
import bpy
import bmesh
import bpy_extras
import bpy_extras.mesh_utils
import mathutils
from bl_ui.space_image import IMAGE_MT_uvs_context_menu

    
def LocalUnwrap_UV():
    context = bpy.context
    ob = context.edit_object
    if ob is None:
        print("Not in selected mode")
        return

    me = ob.data
    bm = bmesh.from_edit_mesh(me)

    # Get Selected Faces and uv layer name
    selfaces = [f for f in bm.faces if f.select]
    if len(selfaces) <= 0:
        return

    uv_layer = bm.loops.layers.uv.active

    # Get Selected UV data
    # uv_data = []
    uv_data_x =[]
    uv_data_y =[]
    for f in selfaces:
        for loop in f.loops:
            uv = loop[uv_layer].uv
            #uv_data.append(uv)
            uv_data_x.append(uv.x)
            uv_data_y.append(uv.y)
    
    # Calculate UV bounding box
    uv_data_x = sorted(uv_data_x)
    uv_data_y = sorted(uv_data_y)
    x_max = uv_data_x[0]
    x_min = uv_data_x[-1]
    y_max = uv_data_y[0]
    y_min = uv_data_y[-1]

    target_origin = mathutils.Vector((x_max,y_max))
    target_size = mathutils.Vector((x_max - x_min,y_max - y_min)) 

    print("target origin : {}".format(target_origin))
    print("target size : {}".format(target_size))
    
    # unwrap the uv
    """
    bpy.types.Scene.local_unwrap_method
    bpy.types.Scene.local_unwrap_fill_holes
    bpy.types.Scene.Scene.local_unwrap_correct_aspect
    bpy.types.Scene.Scene.local_unwrap_use_subsurf_data
    bpy.types.Scene.Scene.local_unwrap_margin
    """
    arg0 = context.scene.local_unwrap_method
    arg1 = context.scene.local_unwrap_fill_holes
    arg2 = context.scene.local_unwrap_correct_aspect
    arg3 = context.scene.local_unwrap_use_subsurf_data
    arg4 = context.scene.local_unwrap_margin
    bpy.ops.uv.unwrap(method=arg0,fill_holes=arg1,correct_aspect=arg2,use_subsurf_data=arg3,margin=arg4)

    new_uv_data_x =[]
    new_uv_data_y =[]
    for f in selfaces:
        for loop in f.loops:
            uv = loop[uv_layer].uv
            new_uv_data_x.append(uv.x)
            new_uv_data_y.append(uv.y)
    
    # Calculate NewUV bounding box
    new_uv_data_x = sorted(new_uv_data_x)
    new_uv_data_y = sorted(new_uv_data_y)
    x_max = new_uv_data_x[0]
    x_min = new_uv_data_x[-1]
    y_max = new_uv_data_y[0]
    y_min = new_uv_data_y[-1]

    new_model_space_origin = mathutils.Vector((x_max,y_max)) 
    new_model_space_size = mathutils.Vector((x_max - x_min,y_max - y_min)) 

    print("new model space origin : {}".format(new_model_space_origin))
    print("new model space size : {}".format(new_model_space_size))

    offset = target_origin - new_model_space_origin
    scale_x = (target_size.x) / (new_model_space_size.x)
    scale_y = (target_size.y) / (new_model_space_size.y)
    
    for f in selfaces:
        for loop in f.loops:
            new_world_space_uv = loop[uv_layer].uv
            new_model_space_uv = new_world_space_uv + new_model_space_origin
            target_space_uv_x = new_model_space_uv.x * scale_x + offset.x
            target_space_uv_y = new_model_space_uv.y * scale_y + offset.y
            loop[uv_layer].uv = mathutils.Vector((target_space_uv_x,target_space_uv_y))
            
#==================================================================================================================
class LocalUnwrapOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Local Unwrap UV"
 
    def execute(self, context):  
        LocalUnwrap_UV()
        return {'FINISHED'}

    @classmethod
    def register(cls): 
        # bpy.ops.uv.unwrap()
        #  [(identifier, name, description, icon, number), ...]
        selection_modes =[
            ("ANGLE_BASED", "Angle based", "", 0),
            ("CONFORMAL", "Conformal", "", 1),
        ]
        bpy.types.Scene.local_unwrap_method = bpy.props.EnumProperty(items=selection_modes, name="Method")
        bpy.types.Scene.local_unwrap_fill_holes = bpy.props.BoolProperty(name="fill holes",default=True)
        bpy.types.Scene.local_unwrap_correct_aspect = bpy.props.BoolProperty(name="correct aspect",default=True)
        bpy.types.Scene.local_unwrap_use_subsurf_data = bpy.props.BoolProperty(name="use subsurf data",default=False)
        bpy.types.Scene.local_unwrap_margin = bpy.props.FloatProperty(name="margin", default=0.01) 

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.local_unwrap_method
        del bpy.types.Scene.local_unwrap_fill_holes
        del bpy.types.Scene.Scene.local_unwrap_correct_aspect
        del bpy.types.Scene.Scene.local_unwrap_use_subsurf_data
        del bpy.types.Scene.Scene.local_unwrap_margin


def drawOperator(self, context):
    self.layout.operator("object.simple_operator",text="Local Unwrap UV")


# A simple button and input field in the Tools panel
class VBPL_PT_SampleUVPanel(bpy.types.Panel):
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Simple UV"
    bl_label = "Local Unwrap Operator"
    #bl_context = "objectmode"

    def draw(self, context):
        self.layout.prop(context.scene,'local_unwrap_method')
        self.layout.prop(context.scene,'local_unwrap_fill_holes')
        self.layout.prop(context.scene,'local_unwrap_correct_aspect')
        self.layout.prop(context.scene,'local_unwrap_use_subsurf_data')
        self.layout.prop(context.scene,'local_unwrap_margin')
        self.layout.operator("object.simple_operator",text="Local Unwrap UV")

    @classmethod
    def register(cls):     
        IMAGE_MT_uvs_context_menu.append(drawOperator)
        

    @classmethod
    def unregister(cls):
        IMAGE_MT_uvs_context_menu.remove(drawOperator)
        # Delete parameters related to the class here


classes = (
   LocalUnwrapOperator, 
   VBPL_PT_SampleUVPanel,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
   register()