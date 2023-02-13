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


def main(context):
    '''obj = context.active_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)a

    uv_layer = bm.loops.layers.uv.verify()

    # adjust uv coordinates
    for face in bm.faces:
        for loop in face.loops:
            loop_uv = loop[uv_layer]
            # use xy position of the vertex as a uv coordinate
            loop_uv.uv = loop.vert.co.xy

    bmesh.update_edit_mesh(me)'''
    
    bpy.context.active_object.data.uv_layers.new(name='uv_02')
    context = bpy.context
    ob = context.edit_object
    if ob is None:
        print("Not in selected mode")
        return

    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    
    uv02 = bm.loops.layers.uv.get("uv_02")

    for f in bm.faces:
        for loop in f.loops:
            print(loop[uv02].uv)
            loop[uv02].uv = mathutils.Vector((0,0))

    print(uv02)


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