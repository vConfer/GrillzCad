import argparse

from engine.grill_project import GrillProject


def main():
    parser = argparse.ArgumentParser(description="Run GrillzCAD project workflow.")
    parser.add_argument("input_stl")
    parser.add_argument("--output", default="outputs_project")
    parser.add_argument("--stone-diameter", type=float, default=1.0)
    parser.add_argument("--spacing", type=float, default=0.15)
    parser.add_argument("--border-mm", type=float, default=0.5)
    parser.add_argument("--shell-offset", type=float, default=0.6)

    args = parser.parse_args()

    project = GrillProject(args.input_stl)

    project.build_preview(
        output_dir=args.output,
        stone_diameter=args.stone_diameter,
        spacing=args.spacing,
        border_mm=args.border_mm,
    )

    project.export_shell(offset_mm=args.shell_offset)

    print("Done.")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()