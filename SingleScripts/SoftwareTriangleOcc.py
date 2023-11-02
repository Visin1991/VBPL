import bpy
import bmesh
import math
from mathutils.bvhtree import BVHTree
from mathutils import Vector

def cull_hidden_faces_by_camera(obj, camera, resolution=100):
    # Setup BVH tree from object
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bvh = BVHTree.FromBMesh(bm)

    visible_faces = set()

    # Setup for camera space rays
    cam_matrix_inv = camera.matrix_world.inverted()

    # Iterate over a grid of rays from the camera
    for x in range(resolution):
        for y in range(resolution):
            # Convert grid coordinate to -1..1 range
            px = x / (resolution - 1) * 2 - 1
            py = y / (resolution - 1) * 2 - 1
            
            # Create start and end points for ray in camera space
            start = Vector((px, py, -1))
            end = Vector((px, py, 1))
            
            # Convert start and end points to world space
            start_world = camera.matrix_world @ start
            end_world = camera.matrix_world @ end
            
            direction = (end_world - start_world).normalized()

            hit, normal, index, distance = bvh.ray_cast(start_world, direction)

            if hit:
                print(f"hit index : {index}")
                visible_faces.add(index)
            else:
                print("miss......")

    # Select all faces except the visible ones
    # for face in bm.faces:
    #     face.select = face.index not in visible_faces

    # Delete hidden faces
    # bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.select], context='FACES')
    # bm.to_mesh(obj.data)
    # bm.free()
    for face in visible_faces:
        print(face)

# Assuming the active object is your mesh and you have a camera named "Camera"
# obj = bpy.context.active_object
# camera = bpy.data.objects["Camera"]
# cull_hidden_faces_by_camera(obj, camera)


# 绘制Debug射线 ......Todo: 后续可以奖这些Debug射线转为Python GPU 进行绘制
def visualize_rays(camera, resolution=100, ray_length=10):
    # Create a new mesh object to visualize the rays
    mesh = bpy.data.meshes.new(name="Rays")
    obj = bpy.data.objects.new("Rays", mesh)
    bpy.context.collection.objects.link(obj)

    verts = []
    edges = []

    # Iterate over a grid of rays from the camera
    for x in range(resolution):
        for y in range(resolution):
            # Convert grid coordinate to -1..1 range
            px = x / (resolution - 1) * 2 - 1
            py = y / (resolution - 1) * 2 - 1
            
            # Create start and end points for ray in camera space
            start = Vector((px, py, -1))
            end = Vector((px, py, 1))
            
            # Convert start and end points to world space
            start_world = camera.matrix_world @ start
            end_world = camera.matrix_world @ start + ray_length * (camera.matrix_world @ end - camera.matrix_world @ start).normalized()

            # Append the vertices and edge
            verts.append(start_world)
            verts.append(end_world)
            edges.append([len(verts)-2, len(verts)-1])

    mesh.from_pydata(verts, edges, [])

# Use this function after setting up your camera and object
visualize_rays(bpy.data.objects["Camera"])
