from pathlib import Path
from collections import defaultdict
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]

src = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_final_clean.stl"
out = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_manifold.stl"

mesh = trimesh.load(src)

edge_faces = defaultdict(list)

for face_index, face in enumerate(mesh.faces):
    a, b, c = map(int, face)

    for u, v in ((a, b), (b, c), (c, a)):
        edge_faces[tuple(sorted((u, v)))].append(face_index)

faces_to_remove = set()

for edge, faces in edge_faces.items():
    if len(faces) > 2:
        # Keep the first two faces, remove extras
        for f in faces[2:]:
            faces_to_remove.add(f)

print("Faces to remove:", len(faces_to_remove))
print("Removing:", sorted(faces_to_remove))

keep_faces = [
    face
    for i, face in enumerate(mesh.faces)
    if i not in faces_to_remove
]

fixed = trimesh.Trimesh(
    vertices=mesh.vertices,
    faces=np.array(keep_faces),
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