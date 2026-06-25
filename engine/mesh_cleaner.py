import trimesh


def clean_mesh(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """Basic mesh cleanup for scanned dental/grill models."""
    mesh = mesh.copy()

    # Older trimesh has these as methods; newer versions warn but still work.
    try:
        mesh.remove_duplicate_faces()
    except Exception:
        pass

    try:
        mesh.remove_degenerate_faces()
    except Exception:
        pass

    try:
        mesh.remove_unreferenced_vertices()
    except Exception:
        pass

    try:
        mesh.merge_vertices()
    except Exception:
        pass

    try:
        mesh.fix_normals()
    except Exception:
        pass

    return mesh