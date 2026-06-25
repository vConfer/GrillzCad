import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.stone_markers import export_stone_markers
from engine.mesh_loader import load_mesh
from engine.mesh_cleaner import clean_mesh
from engine.surface_classifier import classify_surfaces
from engine.adjacency import build_face_graph
from engine.distance_field import face_distance_steps
from engine.stone_layout import generate_hex_layout, save_stone_layout
from engine.seat_cutters import export_seat_cutters
from engine.seat_generator import export_round_stone_seats

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_stone_layout.py model.stl")
        return

    mesh = clean_mesh(load_mesh(sys.argv[1]))

    classes = classify_surfaces(mesh)
    facial_faces = classes["facial"]

    adjacency = build_face_graph(mesh)
    distances = face_distance_steps(facial_faces, adjacency)

    safe_faces = [
        face
        for face, dist in distances.items()
        if dist is not None and dist >= 4
    ]

    stones = generate_hex_layout(
        mesh,
        safe_faces,
        stone_diameter=1.0,
        spacing=0.15,
    )

    out_dir = ROOT / "outputs_stone_layout"
    out_dir.mkdir(exist_ok=True)

    save_stone_layout(stones, out_dir / "stone_centers.json")
    export_stone_markers(stones, out_dir / "stone_markers.stl")
    export_seat_cutters(stones, out_dir / "seat_cutters.stl", depth=0.6)
    export_round_stone_seats(stones, out_dir / "round_stone_seats.stl", total_depth=0.65)
    print(f"Exported: {out_dir / 'round_stone_seats.stl'}")
    print(f"Exported: {out_dir / 'seat_cutters.stl'}")
    print(f"Exported: {out_dir / 'stone_markers.stl'}")

    print(f"Safe faces: {len(safe_faces)}")
    print(f"Generated stones: {len(stones)}")
    print(f"Exported: {out_dir / 'stone_centers.json'}")


if __name__ == "__main__":
    main()