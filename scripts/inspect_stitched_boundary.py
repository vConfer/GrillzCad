import trimesh
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

mesh = trimesh.load(
    ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_clean.stl"
)

edge_count = defaultdict(int)

for face in mesh.faces:
    a, b, c = map(int, face)
    for u, v in ((a, b), (b, c), (c, a)):
        edge_count[tuple(sorted((u, v)))] += 1

boundary_edges = [
    edge for edge, count in edge_count.items()
    if count == 1
]

print("Watertight:", mesh.is_watertight)
print("Boundary edges:", len(boundary_edges))
print("Faces:", len(mesh.faces))
print("Vertices:", len(mesh.vertices))
print("Volume:", mesh.volume)