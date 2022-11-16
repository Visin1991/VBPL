
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


def register():
    bpy.utils.register_class(ShaderMainPanel)
    bpy.utils.register_class(SHADER_OT_DIAMOND)
    
def unregister():
    bpy.utils.unregister_class(ShaderMainPanel)
    bpy.utils.unregister_class(SHADER_OT_DIAMOND)
    
if __name__ == "__main__":
    register()