import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.grill_engine import GrillEngine
from engine.tooth_regions import split_faces_by_x
from engine.uv_hex_sampler import sample_uv_hex
from engine.stone_layout import save_stone_layout
from engine.stone_markers import export_stone_markers
from engine.seat_generator import export_round_stone_seats


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_uv_hex_per_tooth.py model.stl")
        return

    out_dir = ROOT / "outputs_uv_hex_teeth"
    out_dir.mkdir(exist_ok=True)

    engine = (
        GrillEngine(sys.argv[1])
        .load()
        .classify_surfaces()
        .compute_design_region(border_mm=0)
    )

    regions = split_faces_by_x(engine.mesh, engine.safe_faces)

    stones = []
    for i, region in enumerate(regions):
        region_stones = sample_uv_hex(
            engine.mesh,
            region,
            stone_diameter=1.0,
            spacing=0.15,
        )
        print(f"Tooth region {i}: {len(region)} faces, {len(region_stones)} stones")
        stones.extend(region_stones)

    save_stone_layout(stones, out_dir / "stone_centers.json")
    export_stone_markers(stones, out_dir / "stone_markers.stl")
    export_round_stone_seats(stones, out_dir / "round_stone_seats.stl")

    print(f"Total stones: {len(stones)}")
    print(f"Output: {out_dir}")


if __name__ == "__main__":
    main()