import bpy
import bmesh

def compute_mesh_surface_area(obj):
    # 确保它是一个网格对象
    if obj.type != 'MESH':
        raise ValueError("Object is not a mesh")

    # 从对象网格数据创建一个bmesh
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # 计算表面积
    surface_area = sum(face.calc_area() for face in bm.faces)

    # 清理
    bm.free()

    return surface_area

# 假设活跃对象是你感兴趣的网格
obj = bpy.context.active_object
surface_area = compute_mesh_surface_area(obj)
print(f"Surface area of the object: {surface_area:.4f} square units")
