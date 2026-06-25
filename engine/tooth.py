from dataclasses import dataclass
from pathlib import Path

import trimesh

from engine.segmentation import submesh_from_faces


@dataclass
class Tooth:
    id: int
    face_indices: list[int]
    mesh: trimesh.Trimesh

    @property
    def face_count(self):
        return len(self.face_indices)

    @classmethod
    def from_region(cls, source_mesh, tooth_id, face_indices):
        tooth_mesh = submesh_from_faces(source_mesh, face_indices)
        return cls(id=tooth_id, face_indices=face_indices, mesh=tooth_mesh)

    def export(self, path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.mesh.export(path)
        return path