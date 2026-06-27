import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.mesh_loader import load_mesh
from engine.mesh_cleaner import clean_mesh
from engine.tooth_analyzer import detect_teeth
from engine.visibility_classifier import visible_faces_from_camera
from engine.tooth_anatomy import filter_design_region_by_uv
from engine.segmentation import submesh_from_faces


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_tooth_safe_faces.py model.stl")
        return

    mesh = clean_mesh(load_mesh(sys.argv[1]))

    teeth, creases = detect_teeth(
        mesh,
        crease_angle=12.0,
        min_faces=1000,
    )

    print(f"Detected teeth: {len(teeth)}")

    out_dir = ROOT / "outputs_tooth_safe_faces"
    out_dir.mkdir(exist_ok=True)

    all_safe_faces = []

    for i, tooth in enumerate(teeth):
        tooth_faces = list(tooth.face_indices)

        # Use all detected tooth faces first, then anatomy-trim them.
        safe_faces = filter_design_region_by_uv(
            mesh,
            tooth_faces,
            u_min_ratio=0.16,
            u_max_ratio=0.84,
            v_min_ratio=0.42,
            v_max_ratio=0.92,
        )

        print(f"Tooth {i + 1}: {len(tooth_faces)} faces -> {len(safe_faces)} safe faces")

        if safe_faces:
            submesh_from_faces(mesh, safe_faces).export(
                out_dir / f"tooth_{i + 1}_safe.stl"
            )
            all_safe_faces.extend(safe_faces)

    if all_safe_faces:
        submesh_from_faces(mesh, all_safe_faces).export(
            out_dir / "all_tooth_safe_faces.stl"
        )

    print(f"Output: {out_dir}")


if __name__ == "__main__":
    main()