import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.mesh_loader import load_mesh
from engine.mesh_cleaner import clean_mesh
from engine.tooth_analyzer import detect_teeth
from engine.facial_surface import detect_facial_faces
from engine.segmentation import submesh_from_faces


def main():
    print("=== Facial Surface Test ===")

    if len(sys.argv) < 2:
        print("Usage:")
        print("python scripts/test_facial_surface.py model.stl")
        return

    mesh = clean_mesh(load_mesh(sys.argv[1]))

    teeth, creases = detect_teeth(
        mesh,
        crease_angle=12,
        min_faces=1000,
        keep_largest=2,
    )

    out_dir = ROOT / "outputs_facial"
    out_dir.mkdir(exist_ok=True)

    print(f"Detected {len(teeth)} teeth")

    for tooth in teeth:
        facial_faces = detect_facial_faces(mesh, tooth.face_indices)

        facial_mesh = submesh_from_faces(mesh, facial_faces)

        filename = out_dir / f"tooth_{tooth.id:03d}.stl"

        facial_mesh.export(filename)

        print(filename)

    print("Done.")


if __name__ == "__main__":
    main()