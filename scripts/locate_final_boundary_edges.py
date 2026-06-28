from pathlib import Path
from collections import defaultdict
import trimesh

ROOT = Path(__file__).resolve().parents[1]
mesh = trimesh.load(ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_final.stl")

edge_count = defaultdict(int)

for face in mesh.faces:
    a, b, c = map(int, face)
    for u, v in ((a, b), (b, c), (c, a)):
        edge_count[tuple(sorted((u, v)))] += 1

boundary_edges = [edge for edge, count in edge_count.items() if count == 1]

print("Boundary edges:", len(boundary_edges))

for edge in boundary_edges:
    a, b = edge
    print(edge)
    print("A:", mesh.vertices[a])
    print("B:", mesh.vertices[b])