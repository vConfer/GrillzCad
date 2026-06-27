import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.mesh_loader import load_mesh
from engine.mesh_cleaner import clean_mesh
from engine.tooth_analyzer import detect_teeth
from engine.tooth_anatomy import filter_design_region_by_uv
from engine.uv_hex_sampler import sample_uv_hex
from engine.stone_layout import save_stone_layout
from engine.stone_markers import export_stone_markers
from engine.seat_generator import export_round_stone_seats
from engine.segmentation import submesh_from_faces


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_per_tooth_pave.py model.stl")
        return

    mesh = clean_mesh(load_mesh(sys.argv[1]))

    teeth, creases = detect_teeth(
        mesh,
        crease_angle=12.0,
        min_faces=1000,
    )

    out_dir = ROOT / "outputs_per_tooth_pave"
    out_dir.mkdir(exist_ok=True)

    all_safe_faces = []
    all_stones = []

    for i, tooth in enumerate(teeth):
        safe_faces = filter_design_region_by_uv(
            mesh,
            list(tooth.face_indices),
            u_min_ratio=0.16,
            u_max_ratio=0.84,
            v_min_ratio=0.42,
            v_max_ratio=0.92,
        )

        stones = sample_uv_hex(
            mesh,
            safe_faces,
            stone_diameter=1.0,
            spacing=0.15,
        )

        print(f"Tooth {i + 1}: safe faces {len(safe_faces)}, stones {len(stones)}")

        all_safe_faces.extend(safe_faces)
        all_stones.extend(stones)

    submesh_from_faces(mesh, all_safe_faces).export(out_dir / "design_safe_region.stl")
    save_stone_layout(all_stones, out_dir / "stone_centers.json")
    export_stone_markers(all_stones, out_dir / "stone_markers.stl")
    export_round_stone_seats(all_stones, out_dir / "round_stone_seats.stl")

    print(f"Total stones: {len(all_stones)}")
    print(f"Output: {out_dir}")


if __name__ == "__main__":
    main()