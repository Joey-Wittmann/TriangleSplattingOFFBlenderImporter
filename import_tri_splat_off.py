import bpy
import os
import bmesh



def load_off_with_colors(filepath):
    with open(filepath, 'r') as f:
        # Skip comments and look for OFF header
        while True:
            header = f.readline().strip()
            if header == 'OFF':
                break
            elif header == 'COFF':
                break
            elif header.startswith('#') or header == '':
                continue
            else:
                raise ValueError("Invalid OFF header")

        # Read vertex/face counts
        while True:
            counts_line = f.readline()
            if counts_line.strip() and not counts_line.startswith('#'):
                break
        num_verts, num_faces, _ = map(int, counts_line.strip().split())

        vertices = []
        colors = []
        for _ in range(num_verts):
            while True:
                line = f.readline()
                if line.strip() and not line.startswith('#'):
                    break
            parts = list(map(float, line.strip().split()))
            x, y, z = parts[:3]
            vertices.append((x, y, z))
            colors.append((1.0, 1.0, 1.0, 1.0))
        
        print(str(len(colors)))
        faces = []
        for _ in range(num_faces):
            while True:
                line = f.readline()
                if line.strip() and not line.startswith('#'):
                    break
            parts = list(map(int, line.strip().split()))
            face = parts[1:1+parts[0]]
            if len(parts) >= 6:
                r, g, b = parts[4:7]
                r /= 255.0
                g /= 255.0
                b /= 255.0
                for index in face:
                    colors[index] = (r, g, b, 1.0)
            faces.append(face)

    return vertices, colors, faces

def create_mesh_with_vertex_colors(name, vertices, colors, faces):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    # Add vertex color layer
    color_layer = mesh.vertex_colors.new(name="Col")
    loop_colors = color_layer.data

    # Assign vertex colors per face loop
    color_dict = {i: col for i, col in enumerate(colors)}
    for poly in mesh.polygons:
        for loop_index in poly.loop_indices:
            vert_index = mesh.loops[loop_index].vertex_index
            loop_colors[loop_index].color = color_dict[vert_index]

    return obj

# Replace this with the path to your .off file
off_file_path = bpy.path.abspath("C:/Users/Desktop06/Downloads/garden.off")

if os.path.exists(off_file_path):
    verts, cols, faces = load_off_with_colors(off_file_path)
    create_mesh_with_vertex_colors("OFF_Colored", verts, cols, faces)
    print("OFF file with vertex colors imported successfully.")
else:
    print(f"File not found: {off_file_path}")
    

