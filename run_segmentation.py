from pathlib import Path
import argparse

from engine.mesh_loader import load_mesh
from engine.mesh_cleaner import clean_mesh
from engine.crease_detection import detect_crease_edges, crease_edge_keys
from engine.segmentation import segment_faces
from engine.debug_export import (
    export_cleaned_mesh,
    export_crease_lines_obj,
    export_regions,
    export_report,
)


def main():
    parser = argparse.ArgumentParser(description="GrillzCAD Engine v0.1 segmentation runner")
    parser.add_argument("input_stl", help="Input STL file")
    parser.add_argument("output_dir", help="Output folder")
    parser.add_argument("--crease-angle", type=float, default=35.0, help="Crease angle threshold in degrees")
    parser.add_argument("--min-faces", type=int, default=100, help="Minimum faces per exported region")
    parser.add_argument("--valleys-only", action="store_true", help="Only use likely valley creases")
    args = parser.parse_args()

    input_path = Path(args.input_stl)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/6] Loading mesh: {input_path}")
    mesh = load_mesh(input_path)

    print("[2/6] Cleaning mesh")
    mesh = clean_mesh(mesh)

    print("[3/6] Detecting creases")
    creases = detect_crease_edges(
        mesh,
        angle_threshold_degrees=args.crease_angle,
        valleys_only=args.valleys_only,
    )
    blocked = crease_edge_keys(creases)

    print("[4/6] Segmenting mesh")
    regions = segment_faces(mesh, blocked_edges=blocked, min_faces=args.min_faces)

    print("[5/6] Exporting debug files")
    export_cleaned_mesh(mesh, out_dir)
    export_crease_lines_obj(mesh, creases, out_dir)
    export_regions(mesh, regions, out_dir)

    print("[6/6] Writing report")
    report_path = export_report(
        mesh,
        creases,
        regions,
        out_dir,
        settings={
            "input_stl": str(input_path),
            "crease_angle": args.crease_angle,
            "min_faces": args.min_faces,
            "valleys_only": args.valleys_only,
        },
    )

    print("\nDone.")
    print(f"Creases: {len(creases)}")
    print(f"Regions: {len(regions)}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
