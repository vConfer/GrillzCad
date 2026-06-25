from pathlib import Path
import trimesh


def load_mesh(path: str | Path) -> trimesh.Trimesh:
    """Load an STL/mesh file as a single Trimesh object."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Mesh file not found: {path}")

    mesh = trimesh.load_mesh(path, force="mesh")

    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError(f"Could not load file as a single mesh: {path}")

    if mesh.vertices.size == 0 or mesh.faces.size == 0:
        raise ValueError("Mesh has no vertices or faces.")

    return mesh