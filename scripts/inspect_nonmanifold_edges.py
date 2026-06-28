from pathlib import Path
from collections import defaultdict
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

for edge, faces in bad_edges[:20]:
    print(edge, "face_count:", len(faces), "faces:", faces[:10])