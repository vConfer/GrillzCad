import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.mesh_loader import load_mesh
from engine.mesh_cleaner import clean_mesh
from engine.surface_classifier import classify_surfaces
from engine.adjacency import build_face_graph
from engine.distance_field import face_distance_steps
from engine.segmentation import submesh_from_faces


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_design_region.py model.stl")
        return

    print("Loading mesh...")
    mesh = clean_mesh(load_mesh(sys.argv[1]))

    print("Classifying surfaces...")
    classes = classify_surfaces(mesh)

    facial_faces = classes["facial"]

    print("Building face graph...")
    adjacency = build_face_graph(mesh)

    print("Computing distance field...")
    distances = face_distance_steps(facial_faces, adjacency)

    safe_faces = [
        face
        for face, dist in distances.items()
        if dist is not None and dist >= 4
    ]

    out_dir = ROOT / "outputs_design_region"
    out_dir.mkdir(exist_ok=True)

    submesh_from_faces(mesh, facial_faces).export(out_dir / "facial_full.stl")
    submesh_from_faces(mesh, safe_faces).export(out_dir / "design_safe_region.stl")

    print(f"Facial faces: {len(facial_faces)}")
    print(f"Safe region faces: {len(safe_faces)}")
    print("Done.")


if __name__ == "__main__":
    main()