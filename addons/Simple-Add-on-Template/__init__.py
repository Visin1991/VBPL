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
    bl_context = "objectmode"

    def draw(self, context):
        self.layout.operator("object.simple_operator",
        text="Print Encouraging Message")
        self.layout.prop(context.scene, 'encouraging_message')

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
   SimpleOperator,
   SimplePanel,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
   register()