bl_info = {
   'name': 'DebugpyVSCode',
   'author': 'VV',
   'version': (1, 0, 0),
   'blender': (2, 90, 0),
   "description": "Blender Remote debugpy for VS Code",
   'location': '',
   "warning": "",
   "wiki_url": "wwww.google.com",
   "tracker_url": "wwww.google.com",
   'category': 'Development',
}

import bpy
import debugpy

class DebugPyPreferences(bpy.types.AddonPreferences):
   bl_idname = __name__

   port: bpy.props.IntProperty(name="Port",min=0,max=65535,default=5678)

   def draw(self, context):
      layout = self.layout
      row_port = layout.split()
      row_port.prop(self, "port")
      row_port.label(text="port : Listen to VS Code Debug")

class DebugPyOperator(bpy.types.Operator):
   bl_idname = "debugpy.listen_vscode_debug"
   bl_label = "Debugpy: Listen VS Code Debug"
   bl_description = "Starts debugpy Listen VS Code Debug"
   
   @classmethod
   def register(cls):
      # Register properties related to the class here.
      print("Registered class: %s " % cls.bl_label)

   def execute(self, context):
      #get debugpy and import if exists
      prefs = bpy.context.preferences.addons[__name__].preferences
      debugpy_port = prefs.port

      try:
         print("Starting to listen Local Host......")
         debugpy.listen(("localhost", debugpy_port))
      except:
         print("Server already running.")

      return {"FINISHED"}

class DebugPyMenu(bpy.types.Menu):
   bl_label = "DebugPy"
   bl_idname = "view3D.DebugPy"
   
   def menu_func(self,context):
      layout = self.layout
      layout.operator("debugpy.listen_vscode_debug")
      
   @classmethod
   def register(cls):
      # Register properties related to the class here.
      bpy.types.VIEW3D_MT_object.append(cls.menu_func)
      print("======================================")
      print("Registered class: %s " % cls.bl_label)
   
   # Set the menu operators and draw functions
   def draw(self, context):
      self.menu_func(self,context)
      
classes = (
   DebugPyPreferences,
   DebugPyOperator,
   DebugPyMenu,
)

register, unregister = bpy.utils.register_classes_factory(classes)

if __name__ == "__main__":
   register()
