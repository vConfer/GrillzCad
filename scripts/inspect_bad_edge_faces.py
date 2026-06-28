from pathlib import Path
from collections import defaultdict
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]

mesh = trimesh.load(
    ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_final_clean.stl"
)

edge_faces = defaultdict(list)

for face_index, face in enumerate(mesh.faces):
    a, b, c = map(int, face)

    for u, v in ((a, b), (b, c), (c, a)):
        edge_faces[tuple(sorted((u, v)))].append(face_index)

bad_edges = [
    (edge, faces)
    for edge, faces in edge_faces.items()
    if len(faces) != 2
]

print("Bad edges:", len(bad_edges))

for edge, faces in bad_edges:
    print()
    print("EDGE:", edge)
    print("Face count:", len(faces))

    for f in faces:
        face = mesh.faces[f]
        verts = mesh.vertices[face]
        area = trimesh.triangles.area([verts])[0]
        normal = mesh.face_normals[f]
        center = verts.mean(axis=0)

        print(
            f"  face {f}: "
            f"verts={face.tolist()} "
            f"area={area:.8f} "
            f"normal={np.round(normal, 4).tolist()} "
            f"center={np.round(center, 4).tolist()}"
        )