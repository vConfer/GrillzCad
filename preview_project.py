from pathlib import Path
import argparse
import pyvista as pv


def add_if_exists(plotter, path, color, opacity=1.0):
    path = Path(path)

    if not path.exists():
        print(f"Missing: {path.name}")
        return

    print(f"Loading: {path.name}")

    mesh = pv.read(str(path))

    plotter.add_mesh(
        mesh,
        color=color,
        opacity=opacity,
        show_edges=False,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="outputs_project")
    args = parser.parse_args()

    out = Path(args.output)

    plotter = pv.Plotter(window_size=(1400, 900))
    plotter.set_background("black")

    add_if_exists(plotter, out / "facial_full.stl", "white", 0.25)
    add_if_exists(plotter, out / "design_safe_region.stl", "green", 0.75)
    add_if_exists(plotter, out / "stone_markers.stl", "cyan", 1.0)
    add_if_exists(plotter, out / "round_stone_seats.stl", "red", 1.0)

    shell = out / "offset_shell_0.60mm.stl"
    if shell.exists():
        add_if_exists(plotter, shell, "gold", 0.35)

    plotter.add_axes()
    plotter.show_grid()

    print("Opening viewer...")
    plotter.show()


if __name__ == "__main__":
    main()