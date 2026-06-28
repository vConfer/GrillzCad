from pathlib import Path
from collections import defaultdict
import trimesh

ROOT = Path(__file__).resolve().parents[1]

mesh = trimesh.load(
    ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_clean.stl"
)

parts = mesh.split(only_watertight=False)
parts = sorted(parts, key=lambda p: len(p.faces), reverse=True)

print("Parts:", len(parts))

for i, part in enumerate(parts):
    edge_count = defaultdict(int)

    for face in part.faces:
        a, b, c = map(int, face)
        for u, v in ((a, b), (b, c), (c, a)):
            edge_count[tuple(sorted((u, v)))] += 1

    boundary_edges = [
        edge for edge, count in edge_count.items()
        if count == 1
    ]

    print(
        f"Part {i}: faces={len(part.faces)}, "
        f"watertight={part.is_watertight}, "
        f"boundary_edges={len(boundary_edges)}, "
        f"volume={part.volume}"
    )