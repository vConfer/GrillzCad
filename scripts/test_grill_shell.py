import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.mesh_loader import load_mesh
from engine.mesh_cleaner import clean_mesh
from engine.grill_shell import export_offset_shell


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_grill_shell.py model.stl")
        return

    mesh = clean_mesh(load_mesh(sys.argv[1]))

    out_dir = ROOT / "outputs_shell"
    out_dir.mkdir(exist_ok=True)

    export_offset_shell(mesh, out_dir / "offset_shell_04mm.stl", offset_mm=0.4)
    export_offset_shell(mesh, out_dir / "offset_shell_08mm.stl", offset_mm=0.8)

    print(f"Exported shell previews to {out_dir}")


if __name__ == "__main__":
    main()