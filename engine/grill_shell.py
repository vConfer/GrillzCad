from pathlib import Path
import trimesh


def make_offset_shell(mesh, offset_mm=0.4):
    shell = mesh.copy()
    shell.vertices = shell.vertices + shell.vertex_normals * offset_mm

    try:
        shell.fix_normals()
    except Exception:
        pass

    return shell


def export_offset_shell(mesh, path, offset_mm=0.4):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    shell = make_offset_shell(mesh, offset_mm=offset_mm)
    shell.export(path)

    return path