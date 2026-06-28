from pathlib import Path
from collections import defaultdict
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]

src = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_clean.stl"
out = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_repaired.stl"

mesh = trimesh.load(src)
parts = mesh.split(only_watertight=False)
parts = sorted(parts, key=lambda p: len(p.faces), reverse=True)

repaired_parts = []

for idx, part in enumerate(parts):
    edge_count = defaultdict(int)

    for face in part.faces:
        a, b, c = map(int, face)
        for u, v in ((a, b), (b, c), (c, a)):
            edge_count[tuple(sorted((u, v)))] += 1

    boundary_edges = [edge for edge, count in edge_count.items() if count == 1]
    boundary_vertices = sorted(set(v for edge in boundary_edges for v in edge))

    print(f"Part {idx}: boundary edges={len(boundary_edges)}, boundary vertices={len(boundary_vertices)}")

    if len(boundary_vertices) >= 3:
        center = part.vertices[boundary_vertices].mean(axis=0)
        center_index = len(part.vertices)

        vertices = np.vstack([part.vertices, center])
        faces = part.faces.tolist()

    for a, b in boundary_edges:
        faces.append([a, b, center_index])

    part = trimesh.Trimesh(
        vertices=vertices,
        faces=np.array(faces),
        process=True,
    )

    part.fix_normals()

    repaired_parts.append(part)

combined = trimesh.util.concatenate(repaired_parts)
combined.merge_vertices()
combined.remove_unreferenced_vertices()
combined.process(validate=True)
combined.fix_normals()

combined.export(out)

print("Exported:", out)
print("Bodies:", len(combined.split(only_watertight=False)))
print("Watertight:", combined.is_watertight)
print("Volume:", combined.volume)