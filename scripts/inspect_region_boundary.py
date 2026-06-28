import trimesh
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

mesh = trimesh.load(ROOT / "outputs_region_shell" / "region_inner.stl")

edge_count = defaultdict(int)

for face in mesh.faces:
    a, b, c = map(int, face)
    for u, v in ((a, b), (b, c), (c, a)):
        key = tuple(sorted((u, v)))
        edge_count[key] += 1

boundary_edges = [
    edge for edge, count in edge_count.items()
    if count == 1
]

print("Faces:", len(mesh.faces))
print("Vertices:", len(mesh.vertices))
print("Boundary edges:", len(boundary_edges))
print("Watertight:", mesh.is_watertight)