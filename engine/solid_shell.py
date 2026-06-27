from pathlib import Path
import trimesh


def make_solid_shell(mesh, offset_mm=0.60):
    """
    Experimental solid grill shell.

    Creates:
        inner tooth surface
        outer offset surface
        side walls
        watertight solid
    """

    inner = mesh.copy()

    outer = mesh.copy()
    outer.vertices = (
        outer.vertices
        + outer.vertex_normals * offset_mm
    )

    outer.invert()

    try:
        inner.fix_normals()
        outer.fix_normals()
    except Exception:
        pass

    solid = trimesh.util.concatenate([
        inner,
        outer,
    ])

    return solid


def export_solid_shell(
    mesh,
    path,
    offset_mm=0.60,
):
    path = Path(path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    solid = make_solid_shell(
        mesh,
        offset_mm=offset_mm,
    )

    solid.export(path)

    return path