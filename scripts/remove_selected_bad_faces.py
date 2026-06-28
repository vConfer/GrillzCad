from pathlib import Path
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]

src = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_final_clean.stl"
out = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_selected_fix.stl"

mesh = trimesh.load(src)

faces_to_remove = {55119, 55761, 55727}

faces = [
    face for i, face in enumerate(mesh.faces)
    if i not in faces_to_remove
]

fixed = trimesh.Trimesh(
    vertices=mesh.vertices,
    faces=np.array(faces),
    process=True,
)

fixed.merge_vertices()
fixed.remove_unreferenced_vertices()
fixed.process(validate=True)
fixed.fix_normals()

fixed.export(out)

print("Exported:", out)
print("Faces:", len(fixed.faces))
print("Watertight:", fixed.is_watertight)
print("Bodies:", len(fixed.split(only_watertight=False)))
print("Volume:", fixed.volume)