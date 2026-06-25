import argparse

from engine.grill_engine import GrillEngine


def main():
    parser = argparse.ArgumentParser(description="Run GrillzCAD engine preview.")
    parser.add_argument("input_stl")
    parser.add_argument("--output", default="outputs_engine")
    parser.add_argument("--stone-diameter", type=float, default=1.0)
    parser.add_argument("--spacing", type=float, default=0.15)
    parser.add_argument("--border-steps", type=int, default=4)
    parser.add_argument("--border-mm", type=float, default=None)

    args = parser.parse_args()

    engine = (
        GrillEngine(args.input_stl)
        .load()
        .classify_surfaces()
        .compute_design_region(border_steps=args.border_steps, border_mm=args.border_mm)
        .generate_stones(
            stone_diameter=args.stone_diameter,
            spacing=args.spacing,
        )
    )

    output_dir = engine.export_preview(args.output)

    print("Done.")
    print(f"Safe faces: {len(engine.safe_faces)}")
    print(f"Stones: {len(engine.stones)}")
    print(f"Output: {output_dir}")


if __name__ == "__main__":
    main()