import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.mesh_loader import load_mesh
from engine.mesh_cleaner import clean_mesh
from engine.surface_classifier import classify_surfaces
from engine.segmentation import submesh_from_faces


def export_class(mesh, faces, out_path):
    if not faces:
        print(f"Skipped empty class: {out_path.name}")
        return

    sub = submesh_from_faces(mesh, faces)
    sub.export(out_path)
    print(f"Exported {out_path} | faces: {len(faces)}")


def main():
    print("=== Grill Surface Classifier Test ===")

    if len(sys.argv) < 2:
        print("Usage: python scripts/test_surface_classifier.py path/to/grill.stl")
        return

    mesh = clean_mesh(load_mesh(sys.argv[1]))
    classes = classify_surfaces(mesh)

    out_dir = ROOT / "outputs_surface_classes"
    out_dir.mkdir(exist_ok=True)

    for name, faces in classes.items():
        export_class(mesh, faces, out_dir / f"{name}.stl")

    print("Surface class counts:")
    for name, faces in classes.items():
        print(f"{name}: {len(faces)}")


if __name__ == "__main__":
    main()