import sys
from pathlib import Path
import trimesh

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from engine.mesh_loader import load_mesh
from engine.mesh_cleaner import clean_mesh
from engine.tooth_analyzer import detect_teeth
from engine.tooth_anatomy import filter_design_region_by_uv
from engine.segmentation import submesh_from_faces


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_region_shell.py model.stl")
        return

    mesh = clean_mesh(load_mesh(sys.argv[1]))

    teeth, creases = detect_teeth(mesh, crease_angle=12.0, min_faces=1000)

    out_dir = ROOT / "outputs_region_shell"
    out_dir.mkdir(exist_ok=True)

    all_safe_faces = []

    for tooth in teeth:
        safe_faces = filter_design_region_by_uv(
            mesh,
            list(tooth.face_indices),
            u_min_ratio=0.16,
            u_max_ratio=0.84,
            v_min_ratio=0.42,
            v_max_ratio=0.92,
        )
        all_safe_faces.extend(safe_faces)

    region = submesh_from_faces(mesh, all_safe_faces)
    region.export(out_dir / "region_inner.stl")

    outer = region.copy()
    outer.vertices = outer.vertices + outer.vertex_normals * 0.60
    outer.export(out_dir / "region_outer.stl")

    combined = trimesh.util.concatenate([region, outer])
    combined.export(out_dir / "region_shell_unstitched.stl")

    print(f"Safe faces: {len(all_safe_faces)}")
    print(f"Inner watertight: {region.is_watertight}")
    print(f"Outer watertight: {outer.is_watertight}")
    print(f"Combined watertight: {combined.is_watertight}")
    print(f"Output: {out_dir}")


if __name__ == "__main__":
    main()