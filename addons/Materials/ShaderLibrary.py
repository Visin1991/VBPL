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

import bpy

class ShaderMainPanel(bpy.types.Panel):
    bl_label = "Shader Library"
    bl_idname = "SHADER_PT_MAINPANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Shader Library"
    
    def draw(self,context):
        layout = self.layout
        
        row = layout.row()
        row.label(text="Select a shader to be added.")
        row.operator("shader.diamond_operator")
        
        
#Create a Custom Operator for Diamond Shader
class SHADER_OT_DIAMOND(bpy.types.Operator):
    bl_label = "Add Diamond"
    bl_idname = "shader.diamond_operator"
    
    def execute(self,context):
        #Create a new shader calling it Diamond
        material_diamond = bpy.data.materials.new(name="Diamond")
        
        
        material_diamond.use_nodes = True
        
        material_diamond.node_tree.nodes.remove(material_diamond.node_tree.nodes.get("Principled BSDF"))
        
        material_output = material_diamond.node_tree.nodes.get("Material Output")
        #set location of node
        material_output.location = (-400,0)
        
        #Adding Glass1 Node
        glass1_node = material_diamond.node_tree.nodes.new("ShaderNodeBsdfGlass")
        #Set location of node
        glass1_node.location=(-600,0)
        #set Default Color
        glass1_node.inputs[0].default_value = (1,0,0,1)
        #set Default IOR Value
        glass1_node.inputs[2].default_value = 1.446
        
        #Adding Glass2 Node
        glass2_node = material_diamond.node_tree.nodes.new("ShaderNodeBsdfGlass")
        #Set location of node
        glass2_node.location=(-600,-150)
        #set Default Color
        glass2_node.inputs[0].default_value = (0,1,0,1)
        #set Default IOR Value
        glass2_node.inputs[2].default_value = 1.446
        
         #Adding Glass Node
        glass3_node = material_diamond.node_tree.nodes.new("ShaderNodeBsdfGlass")
        #Set location of node
        glass3_node.location=(-600,-300)
        #set Default Color
        glass3_node.inputs[0].default_value = (0,1,0,1)
        #set Default IOR Value
        glass3_node.inputs[2].default_value = 1.446
        
        add1_node = material_diamond.node_tree.nodes.new("ShaderNodeAddShader")
        #setting the location
        add1_node.location = (-400,-50)
        #setting the Label
        add1_node.label = "Add 1"
        #Minimizes the Node
        add1_node.hide = True
        #deselect the node
        add1_node.select = False
        
        add2_node = material_diamond.node_tree.nodes.new("ShaderNodeAddShader")
        #setting the location
        add2_node.location = (-100,0)
        #setting the Label
        add2_node.label = "Add 2"
        #Minimizes the Node
        add2_node.hide = True
        #deselect the node
        add2_node.select = False
        
        #create the glass node and reference it as glass4
        glass4_node = material_diamond.node_tree.nodes.new("ShaderNodeBsdfGlass")
        #setting the location
        glass4_node.location = (-150,-150)
        
        glass4_node.inputs[0].default_value = (1,1,1,1)
        
        glass4_node.inputs[2].default_value = 1.450
        
        glass4_node.select = False
        
        
        #Create the Mix Shader Node and Reference it as Mix1
        mix1_node = material_diamond.node_tree.nodes.new("ShaderNodeMixShader")
        #Setting the Location
        mix1_node.location = (200,0)
        #Deselect the Node
        mix1_node.select = False
        
        
        material_diamond.node_tree.links.new(glass1_node.outputs[0], add1_node.inputs[0])
        material_diamond.node_tree.links.new(glass2_node.outputs[0], add1_node.inputs[1])
        
        material_diamond.node_tree.links.new(add1_node.outputs[0], add2_node.inputs[0])
        material_diamond.node_tree.links.new(glass3_node.outputs[0], add2_node.inputs[1])
        
        material_diamond.node_tree.links.new(add2_node.outputs[0], mix1_node.inputs[1])
        material_diamond.node_tree.links.new(glass4_node.outputs[0], mix1_node.inputs[2])
        
        material_diamond.node_tree.links.new(mix1_node.outputs[0], material_output.inputs[0])
        
        bpy.context.object.active_material = material_diamond
        
        return {'FINISHED'}
        
        
        
        

        
        
def register():
    bpy.utils.register_class(ShaderMainPanel)
    bpy.utils.register_class(SHADER_OT_DIAMOND)
    
def unregister():
    bpy.utils.unregister_class(ShaderMainPanel)
    bpy.utils.unregister_class(SHADER_OT_DIAMOND)
    
    
if __name__ == "__main__":
    register()