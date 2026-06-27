import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.mesh_loader import load_mesh
from engine.mesh_cleaner import clean_mesh
from engine.solid_shell import export_solid_shell


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_solid_shell.py model.stl")
        return

    mesh = clean_mesh(load_mesh(sys.argv[1]))

    out_dir = ROOT / "outputs_solid_shell"
    out_dir.mkdir(exist_ok=True)

    export_solid_shell(
        mesh,
        out_dir / "solid_shell.stl",
        offset_mm=0.60,
    )

    print(f"Output: {out_dir}")


if __name__ == "__main__":
    main()