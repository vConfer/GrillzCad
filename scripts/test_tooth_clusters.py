import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.tooth_analyzer import detect_teeth
from engine.grill_engine import GrillEngine
from engine.tooth_clusters import cluster_faces_by_position
from engine.uv_hex_sampler import sample_uv_hex
from engine.stone_layout import save_stone_layout
from engine.stone_markers import export_stone_markers
from engine.seat_generator import export_round_stone_seats
from engine.segmentation import submesh_from_faces


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_tooth_clusters.py model.stl")
        return

    out_dir = ROOT / "outputs_tooth_clusters"
    out_dir.mkdir(exist_ok=True)

    engine = (
        GrillEngine(sys.argv[1])
        .load()
        .classify_surfaces()
        .compute_design_region(border_mm=0)
    )

    submesh_from_faces(engine.mesh, engine.classes["facial"]).export(out_dir / "facial_full.stl")
    submesh_from_faces(engine.mesh, engine.safe_faces).export(out_dir / "design_safe_region.stl")

    detected_teeth, creases = detect_teeth(engine.mesh, crease_angle=12.0, min_faces=1000)

    print(f"Detected teeth: {len(detected_teeth)}")

    for i, tooth in enumerate(detected_teeth):
        print(
            f"Tooth {i + 1}: "
            f"{len(tooth.face_indices)} faces"
        )

    regions = []

    safe_set = set(engine.safe_faces)

    for i, tooth in enumerate(detected_teeth):
        overlap = [face for face in tooth.face_indices if face in safe_set]
        print(f"Tooth {i + 1} safe overlap: {len(overlap)} faces")

    for tooth in detected_teeth:
        tooth_faces = tooth.face_indices

        safe_set = set(engine.safe_faces)
        region = [face for face in tooth_faces if face in safe_set]

        if region:
            regions.append(region)

    stones = []

    for i, region in enumerate(regions):
        region_stones = sample_uv_hex(
            engine.mesh,
            region,
            stone_diameter=1.0,
            spacing=0.15,
        )
        print(f"Cluster {i}: {len(region)} faces, {len(region_stones)} stones")
        stones.extend(region_stones)

    save_stone_layout(stones, out_dir / "stone_centers.json")
    export_stone_markers(stones, out_dir / "stone_markers.stl")
    export_round_stone_seats(stones, out_dir / "round_stone_seats.stl")

    print(f"Total stones: {len(stones)}")
    print(f"Output: {out_dir}")


if __name__ == "__main__":
    main()