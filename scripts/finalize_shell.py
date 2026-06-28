from pathlib import Path
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]

src = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_repaired.stl"
out = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_final_clean.stl"

mesh = trimesh.load(src)

faces = mesh.faces.tolist()
faces.append([13218, 20385, 40690])

fixed = trimesh.Trimesh(
    vertices=mesh.vertices,
    faces=np.array(faces),
    process=False,
)

parts = fixed.split(only_watertight=False)
largest = max(parts, key=lambda p: len(p.faces))

largest.merge_vertices()
largest.remove_unreferenced_vertices()
largest.process(validate=True)
largest.fix_normals()

largest.export(out)

print("Exported:", out)
print("Faces:", len(largest.faces))
print("Watertight:", largest.is_watertight)
print("Bodies:", len(largest.split(only_watertight=False)))
print("Volume:", largest.volume)