from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import trimesh


@dataclass
class MeshStats:
    path: str | None
    vertices: int
    faces: int
    is_watertight: bool
    bounds_min: list[float]
    bounds_max: list[float]
    size: list[float]
    volume: float | None
    surface_area: float


class Mesh:
    """
    Core mesh wrapper for GrillzCAD.

    This class is intentionally small and stable. Every future engine module
    should use this instead of calling trimesh directly everywhere.
    """

    def __init__(self, mesh: trimesh.Trimesh, path: str | Path | None = None):
        if not isinstance(mesh, trimesh.Trimesh):
            raise TypeError("Mesh expects a trimesh.Trimesh object.")

        if mesh.vertices.size == 0 or mesh.faces.size == 0:
            raise ValueError("Mesh has no vertices or faces.")

        self.path = str(path) if path else None
        self.mesh = mesh

    @classmethod
    def load(cls, path: str | Path) -> "Mesh":
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Mesh file not found: {path}")

        loaded = trimesh.load_mesh(path, force="mesh")

        if not isinstance(loaded, trimesh.Trimesh):
            raise ValueError(f"Could not load as a single mesh: {path}")

        return cls(loaded, path=path)

    def copy(self) -> "Mesh":
        return Mesh(self.mesh.copy(), path=self.path)

    def clean(self) -> "Mesh":
        """
        Clean mesh in-place and return self for chaining.

        Example:
            mesh = Mesh.load("scan.stl").clean()
        """
        m = self.mesh

        cleanup_methods = [
            "remove_duplicate_faces",
            "remove_degenerate_faces",
            "remove_unreferenced_vertices",
            "merge_vertices",
        ]

        for method_name in cleanup_methods:
            method = getattr(m, method_name, None)
            if method:
                try:
                    method()
                except Exception:
                    pass

        try:
            m.fix_normals()
        except Exception:
            pass

        return self

    def centered(self) -> "Mesh":
        """
        Return a centered copy. Does not modify the original.
        Useful for viewer/debug exports.
        """
        new = self.copy()
        center = new.mesh.bounds.mean(axis=0)
        new.mesh.apply_translation(-center)
        return new

    def stats(self) -> MeshStats:
        bounds = self.mesh.bounds
        size = bounds[1] - bounds[0]

        volume = None
        try:
            if self.mesh.is_watertight:
                volume = float(self.mesh.volume)
        except Exception:
            volume = None

        return MeshStats(
            path=self.path,
            vertices=int(len(self.mesh.vertices)),
            faces=int(len(self.mesh.faces)),
            is_watertight=bool(self.mesh.is_watertight),
            bounds_min=[float(x) for x in bounds[0]],
            bounds_max=[float(x) for x in bounds[1]],
            size=[float(x) for x in size],
            volume=volume,
            surface_area=float(self.mesh.area),
        )

    def face_adjacency(self) -> np.ndarray:
        return self.mesh.face_adjacency

    def face_normals(self) -> np.ndarray:
        return self.mesh.face_normals

    def vertex_normals(self) -> np.ndarray:
        return self.mesh.vertex_normals

    def export(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.mesh.export(path)
        return path

    def to_trimesh(self) -> trimesh.Trimesh:
        return self.mesh
