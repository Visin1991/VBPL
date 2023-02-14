bl_info = {
    "name": "Position to UV2",
    "author": "",
    "location": "",
    "version": (1, 0, 0),
    "blender": (2, 90, 1),
    "description": "Starting point for new add-ons.",
    "wiki_url": "www.google.com",
    "category": "Development"
}

import bpy
import bmesh
import mathutils

counter = 0

def main(context):
    print("------------------------------")
    global counter
    print(counter)
    counter += 1
    context = bpy.context
    ob = context.edit_object
    if ob is None:
        print("Not in selected mode")
        return


    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    # bm.normal_update()

    uv01 = bm.loops.layers.uv.get("uv_01")
    uv02 = bm.loops.layers.uv.get("uv_02")
    uv03 = bm.loops.layers.uv.get("uv_03")

    if uv01 is None:
        bpy.context.active_object.data.uv_layers.new(name='uv_01')
        uv01 = bm.loops.layers.uv.get("uv_01")
    if uv02 is None:
        bpy.context.active_object.data.uv_layers.new(name='uv_02')
        uv02 = bm.loops.layers.uv.get("uv_02")
    if uv03 is None:
        bpy.context.active_object.data.uv_layers.new(name='uv_03')
        uv03 = bm.loops.layers.uv.get("uv_03")

    wmtx = ob.matrix_world

    for f in bm.faces:
        # Convert normal from local space to World space
        local_face_normal = f.normal
        world_face_normal = wmtx.to_3x3().inverted().transposed() @ local_face_normal
        world_face_normal.normalize()
    
        # Save world position and normal to uvs
        for loop in f.loops:
            # 注意ob使用的是location, 并非Worldlocation, 因此注意Object不要有父子结构
            loop[uv01].uv = mathutils.Vector((ob.location.x,ob.location.y))
            loop[uv02].uv = mathutils.Vector((ob.location.z,world_face_normal.x))
            loop[uv03].uv = mathutils.Vector((world_face_normal.y,world_face_normal.z))
            
    # bm.free()



class MeshPositionToUV2Operator(bpy.types.Operator):
    """UV Operator description"""
    bl_idname = "object.mesh_position_to_uv2"
    bl_label = "Simple UV Operator"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        # return obj and obj.type == 'MESH' and obj.mode == 'EDIT'
        return True

    def execute(self, context):
        print("Start Action")
        main(context)
        print("End Action")
        return {'FINISHED'}

class VBPL_PT_PivotToUV(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Mesh UV"
    bl_label = "Transform Object Position to UV2"

    def draw(self, context):
        self.layout.operator("object.mesh_position_to_uv2",text="Position to UV2")

# Register and add to the "UV" menu (required to also use F3 search "Simple UV Operator" for quick access).
def register():
    bpy.utils.register_class(MeshPositionToUV2Operator)
    bpy.utils.register_class(VBPL_PT_PivotToUV)


def unregister():
    bpy.utils.unregister_class(MeshPositionToUV2Operator)
    bpy.utils.register_class(VBPL_PT_PivotToUV)


if __name__ == "__main__":
    register()