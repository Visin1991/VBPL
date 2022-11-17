
import bpy
from .ShaderLibrary import *

bl_info = {
    "name": "Shader Library",
    "author": "Visin",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Toolshelf",
    "description": "Adds a new shader to your Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Shader",
}


classes = (
   ShaderMainPanel, 
   SHADER_OT_DIAMOND,
   Material_PT_Function,
   Material_Function_OT_UV_Tile
)

register, unregister = bpy.utils.register_classes_factory(classes)
    
if __name__ == "__main__":
    register()