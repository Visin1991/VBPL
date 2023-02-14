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

# NPR material can be find in https://github.com/kents00/NprEevee/blob/main/resources/__init__.py

def find_first_socket(sockets,name)->bpy.types.NodeSocket:
    for socket in sockets:
        if socket.name == name:
            return socket


class ShaderMainPanel(bpy.types.Panel):
    bl_label = "Shader Library"
    bl_idname = "SHADER_PT_MAINPANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Shader Library"
    
    def draw(self,context):
        layout = self.layout
        
        row = layout.row()
        # row.label(text="Select a shader to be added.")
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

# =======================================================================================================
# Blender Material Functions

class Material_PT_Function(bpy.types.Panel):
    bl_label = "Material Functions"
    bl_idname = "MATERIAL_FUNCTION_PL"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Material Functions"
    
    def draw(self,context):
        layout = self.layout  
        row = layout.row()
        row.label(text="UV_Tile")
        row.operator("mf.uv_tile")
        self.layout.operator("mf.brick_operator")
        self.layout.operator("mf.uv_loop")
        self.layout.operator("mf.uv_pingpong_loop")


class Material_Function_OT_UV_Tile(bpy.types.Operator):
    bl_label = "UV_Tile"
    bl_idname = "mf.uv_tile"
    
    def execute(self,context):    
        print("Hello World")
        return {'FINISHED'}

# -----------------------------Brick----------------------------------------------------
class Material_Function_OT_Brick(bpy.types.Operator):
    bl_label = "Add Brick"
    bl_idname = "mf.brick_operator"
    
    def apply_new_material(self,context:bpy.context):
        # Make a new Material & delete BSDF
        bpy.ops.object.material_slot_add()
        brick_mat = bpy.data.materials.new(name="Brick")
        brick_mat.use_nodes = True
        brick_mat.node_tree.nodes.remove(brick_mat.node_tree.nodes.get('Principled BSDF'))
        
        # Delete all Materials in the mesh & apped brick material to it
        mesh = bpy.types.Mesh(context.object.data)
        mesh.materials.clear()
        mesh.materials.append(brick_mat)

        return brick_mat

    def create_brick_mat_group(self,context:bpy.context):
        # Create Group
        brick_group = bpy.data.node_groups.new(name="Brick Group",type="ShaderNodeTree")

        # Define Group Input
        group_in = brick_group.nodes.new("NodeGroupInput")
        group_in.location = (0,350)
        # Add Input to group
        input_scale = brick_group.inputs.new('NodeSocketFloatFactor','Scale') # https://docs.blender.org/api/current/bpy.types.html  "NodeSocketColor, NodeSocketFloat, ...... check out socket types"
        input_scale.default_value = 2
        input_scale.min_value = -20
        input_scale.max_value = 20
        
        # Inout for link to other node 
        inout_scale = find_first_socket(group_in.outputs,"Scale")
        

        #---------------------------------------------------
        # Define Group Output
        group_out = brick_group.nodes.new("NodeGroupOutput")
        group_out.location = (650,400)
        # Add Output to group
        brick_group.outputs.new('NodeSocketColor','Color')
        output_color = find_first_socket(group_out.inputs,'Color')

        
        #---------------------------------------------------
        # bpy.ops.node.add_node(type="ShaderNodeUVMap", use_transform=True)
        uv_map = brick_group.nodes.new("ShaderNodeUVMap")
        uv_map.location = (260,339)

        # bpy.ops.node.add_node(type="ShaderNodeVectorMath", use_transform=True)
        vector_scale = brick_group.nodes.new("ShaderNodeVectorMath")
        vector_scale.operation = 'SCALE'
        vector_scale.location = (604,314)
        vector_scale_scale = find_first_socket(vector_scale.inputs,'Scale')

        vector_fraction = brick_group.nodes.new("ShaderNodeVectorMath")
        vector_fraction.operation = 'FRACTION'
        vector_fraction.location = (894,253)
        
        # ---------------------------------------------------
        # Link
        link = brick_group.links.new

        
        link(uv_map.outputs[0], vector_scale.inputs[0])
        link(inout_scale, vector_scale_scale)
        link(vector_scale.outputs[0],vector_fraction.inputs[0])
        link(vector_fraction.outputs[0], output_color)

        
        # ----------------------------------------------------
        # Add to Active Material
        tree = bpy.context.object.active_material.node_tree
        group_node = tree.nodes.new("ShaderNodeGroup")
        group_node.node_tree = brick_group
        group_node.location = (-40, 300)
        group_node.use_custom_color = True
        group_node.color = (0,0,0)
        group_node.width = 250


    def execute(self,context):
        self.create_brick_mat_group(context)
        return {'FINISHED'}

# -----------------------------Gradient loop----------------------------------------------------
def create_UV_Loop_group(context:bpy.context,is_pingpong:bool):
        # Create Group
        group_name = "UV Loop"
        if is_pingpong:
            group_name = "UV PingPong Loop"
        brick_group = bpy.data.node_groups.new(name=group_name,type="ShaderNodeTree")
        link = brick_group.links.new

        # Define Group Input
        group_in = brick_group.nodes.new("NodeGroupInput")
        group_in.location = (0,350)
        # Add Input to group
        input_scale = brick_group.inputs.new('NodeSocketFloatFactor','ScaleX') # https://docs.blender.org/api/current/bpy.types.html  "NodeSocketColor, NodeSocketFloat, ...... check out socket types"
        input_scale.default_value = 2
        input_scale.min_value = -20
        input_scale.max_value = 20
        input_scale = brick_group.inputs.new('NodeSocketFloatFactor','ScaleY') # https://docs.blender.org/api/current/bpy.types.html  "NodeSocketColor, NodeSocketFloat, ...... check out socket types"
        input_scale.default_value = 2
        input_scale.min_value = -20
        input_scale.max_value = 20
        
        # Inout for link to other node 
        inout_scale_X = find_first_socket(group_in.outputs,"ScaleX")
        inout_scale_Y = find_first_socket(group_in.outputs,"ScaleY")
        

        #---------------------------------------------------
        # Define Group Output
        group_out = brick_group.nodes.new("NodeGroupOutput")
        group_out.location = (1200,400)
        # Add Output to group
        brick_group.outputs.new('NodeSocketColor','Color')
        output_color = find_first_socket(group_out.inputs,'Color')

        
        #---------------------------------------------------
        # U Dir
        # bpy.ops.node.add_node(type="ShaderNodeUVMap", use_transform=True)
        uv_map = brick_group.nodes.new("ShaderNodeUVMap")
        uv_map.location = (260,339)

        # bpy.ops.node.add_node(type="ShaderNodeSeparateXYZ", use_transform=True)
        separate_xyz = brick_group.nodes.new("ShaderNodeSeparateXYZ")
        separate_xyz.location = (300,339)

        # bpy.ops.node.add_node(type="ShaderNodeVectorMath", use_transform=True)
        multiplay = brick_group.nodes.new("ShaderNodeMath")
        multiplay.operation = 'MULTIPLY'
        multiplay.location = (604,314)

        fraction = brick_group.nodes.new("ShaderNodeMath")
        fraction.operation = 'FRACT'
        fraction.location = (894,253)
        # Link U
        link(uv_map.outputs[0], separate_xyz.inputs[0])
        link(separate_xyz.outputs[0], multiplay.inputs[0])
        link(inout_scale_X, multiplay.inputs[1])
        link(multiplay.outputs[0],fraction.inputs[0])
        pingpong = None
        if is_pingpong:
            pingpong = brick_group.nodes.new("ShaderNodeMath")
            pingpong.operation = 'PINGPONG'
            pingpong.location = (1000,253)
            link(fraction.outputs[0],find_first_socket(pingpong.inputs,'Value'))


        #---------------------------------------------------
        # V Dir
        # bpy.ops.node.add_node(type="ShaderNodeSeparateXYZ", use_transform=True)
        separate_xyz_v = brick_group.nodes.new("ShaderNodeSeparateXYZ")
        separate_xyz_v.location = (200,239)

        multiplay_v = brick_group.nodes.new("ShaderNodeMath")
        multiplay_v.operation = 'MULTIPLY'
        multiplay_v.location = (580,214)

        fraction_v = brick_group.nodes.new("ShaderNodeMath")
        fraction_v.operation = 'FRACT'
        fraction_v.location = (870,153)

        # Link V 
        link(uv_map.outputs[0], separate_xyz_v.inputs[0])
        link(separate_xyz_v.outputs[1], multiplay_v.inputs[0])
        link(inout_scale_Y, multiplay_v.inputs[1])
        link(multiplay_v.outputs[0],fraction_v.inputs[0])
        pingpong_v = None
        if is_pingpong:
            pingpong_v = brick_group.nodes.new("ShaderNodeMath")
            pingpong_v.operation = 'PINGPONG'
            pingpong_v.location = (1000,153)
            link(fraction_v.outputs[0],find_first_socket(pingpong_v.inputs,'Value'))

        #------------------------------------------------------
        combine_color_final = brick_group.nodes.new("ShaderNodeCombineColor")
        combine_color_final.location = (1100,314)

        if not is_pingpong:
            link(fraction.outputs[0],combine_color_final.inputs[0])
            link(fraction_v.outputs[0],combine_color_final.inputs[1])
        else:
            link(pingpong.outputs[0],combine_color_final.inputs[0])
            link(pingpong_v.outputs[0],combine_color_final.inputs[1])
        
        link(combine_color_final.outputs[0], output_color)
        
               
        # ----------------------------------------------------
        # Add to Active Material
        tree = bpy.context.object.active_material.node_tree
        group_node = tree.nodes.new("ShaderNodeGroup")
        group_node.node_tree = brick_group
        group_node.location = (-40, 300)
        group_node.use_custom_color = True
        group_node.color = (0,0,0)
        group_node.width = 250

class Material_Function_OT_UV_Loop(bpy.types.Operator):
    bl_label = "UV Loop"
    bl_idname = "mf.uv_loop"
    def execute(self,context):
        create_UV_Loop_group(context,is_pingpong=False)
        return {'FINISHED'}

class Material_Function_OT_UV_PingPong_Loop(bpy.types.Operator):
    bl_label = "UV PingPong Loop"
    bl_idname = "mf.uv_pingpong_loop"
    def execute(self,context):
        create_UV_Loop_group(context,is_pingpong=True)
        return {'FINISHED'}
