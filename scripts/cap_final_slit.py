from pathlib import Path
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]

src = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_final.stl"
out = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_final.stl"

mesh = trimesh.load(src)

faces = mesh.faces.tolist()
faces.append([13218, 20385, 40690])

fixed = trimesh.Trimesh(
    vertices=mesh.vertices,
    faces=np.array(faces),
    process=False,
)

fixed.fix_normals()
fixed.export(out)

print("Exported:", out)
print("Watertight:", fixed.is_watertight)
print("Bodies:", len(fixed.split(only_watertight=False)))
print("Volume:", fixed.volume)