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

import bpy
import bmesh
import bpy_extras
import bpy_extras.mesh_utils

class ProcessMesh(bpy.types.Operator):
    bl_idname = "object.process_mesh"
    bl_label = "Process a mesh......"
    def execute(self,context):
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
            print("Process UV Island......")
            for face in group:
                print("Process a face......")
                #bmesh.types.BMesh.faces
                #bmesh.types.BMFace.loops
                #bmesh.types.BMLoop
                for bmloop in face.loops:
                    print(bmloop.index)

        bpy.ops.object.mode_set(mode ='OBJECT') 
        

        return {'FINISHED'}

class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Print an Encouraging Message"
    def execute(self, context):
        print("\n\n####################################################")
        print("# Add-on and Simple Operator executed successfully!")
        print("# " + context.scene.encouraging_message)
        print(bpy.context.active_object)
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
   ProcessMesh, 
   SimpleOperator,
   SimplePanel,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
   register()