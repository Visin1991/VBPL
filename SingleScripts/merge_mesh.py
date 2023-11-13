import bpy
import bmesh

def get_uv_coordinates(obj_name):
    obj = bpy.data.objects[obj_name]
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    uv_layer = bm.loops.layers.uv.active

    uv_coordinates = []
    for face in bm.faces:
        coords = [loop[uv_layer].uv.copy() for loop in face.loops]
        uv_coordinates.append(coords)
    
    return uv_coordinates

def calculate_aabb(uv_coords):
    aabb_list = []
    for coords in uv_coords:
        min_x = min([uv.x for uv in coords])
        max_x = max([uv.x for uv in coords])
        min_y = min([uv.y for uv in coords])
        max_y = max([uv.y for uv in coords])
        aabb_list.append(((min_x, min_y), (max_x, max_y)))
    return aabb_list

def is_overlapping(aabb1, aabb2):
    return (aabb1[0][0] < aabb2[1][0] and aabb1[1][0] > aabb2[0][0] and
            aabb1[0][1] < aabb2[1][1] and aabb1[1][1] > aabb2[0][1])

def merge_aabb(aabb1, aabb2):
    min_x = min(aabb1[0][0], aabb2[0][0])
    min_y = min(aabb1[0][1], aabb2[0][1])
    max_x = max(aabb1[1][0], aabb2[1][0])
    max_y = max(aabb1[1][1], aabb2[1][1])
    return ((min_x, min_y), (max_x, max_y))

def merge_overlapping_aabb(aabb_list):
    merged_aabb = aabb_list.copy()
    i = 0
    while i < len(merged_aabb):
        has_merged = False
        j = i + 1
        while j < len(merged_aabb):
            if is_overlapping(merged_aabb[i], merged_aabb[j]):
                new_aabb = merge_aabb(merged_aabb[i], merged_aabb[j])
                merged_aabb[i] = new_aabb
                del merged_aabb[j]
                has_merged = True
            else:
                j += 1
        if not has_merged:
            i += 1
    return merged_aabb

def create_plane_from_aabb(aabb, name):
    vertices = [(aabb[0][0], aabb[0][1], 0),  # Bottom left
                (aabb[1][0], aabb[0][1], 0),  # Bottom right
                (aabb[1][0], aabb[1][1], 0),  # Top right
                (aabb[0][0], aabb[1][1], 0)]  # Top left

    faces = [(0, 1, 2, 3)]

    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)

    bpy.context.collection.objects.link(obj)

    mesh.from_pydata(vertices, [], faces)
    mesh.update()

#--------------------------------------------------------------------------

selected_objects = bpy.context.selected_objects

for obj in selected_objects:
    if obj.type == 'MESH':
        uv_coords = get_uv_coordinates(obj.name)
        aabb_list = calculate_aabb(uv_coords)
        merged_aabb = merge_overlapping_aabb(aabb_list)
        print('----------------------------------------------------')
        for i, aabb in enumerate(merged_aabb):
            create_plane_from_aabb(aabb, f"AABB_{i}")      
    else:
        continue

