from pathlib import Path
from collections import defaultdict
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]
src = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell.stl"
out = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_capped.stl"

mesh = trimesh.load(src)

edge_count = defaultdict(int)
for face in mesh.faces:
    a, b, c = map(int, face)
    for u, v in ((a, b), (b, c), (c, a)):
        edge_count[tuple(sorted((u, v)))] += 1

boundary_edges = [edge for edge, count in edge_count.items() if count == 1]
boundary_vertices = sorted(set(v for edge in boundary_edges for v in edge))

print("Boundary edges:", len(boundary_edges))
print("Boundary vertices:", len(boundary_vertices))

if len(boundary_vertices) >= 3:
    center = mesh.vertices[boundary_vertices].mean(axis=0)
    center_index = len(mesh.vertices)

    vertices = np.vstack([mesh.vertices, center])
    faces = mesh.faces.tolist()

    for a, b in boundary_edges:
        faces.append([a, b, center_index])

    capped = trimesh.Trimesh(vertices=vertices, faces=np.array(faces), process=True)
    capped.fix_normals()
    capped.export(out)

    print("Exported:", out)
    print("Watertight:", capped.is_watertight)
    print("Volume:", capped.volume)
else:
    print("Not enough boundary vertices to cap.")