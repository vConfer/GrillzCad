from dataclasses import dataclass
import math
import numpy as np
import trimesh

from .adjacency import build_edge_to_faces


@dataclass
class CreaseEdge:
    edge_key: tuple[int, int]
    face_a: int
    face_b: int
    angle_degrees: float
    strength: float
    is_valley: bool


def detect_crease_edges(
    mesh: trimesh.Trimesh,
    angle_threshold_degrees: float = 35.0,
    valleys_only: bool = False,
) -> list[CreaseEdge]:
    """
    Detect crease edges using dihedral angle between adjacent face normals.

    This is a first-pass method:
    - high angle = sharp crease/ridge
    - valley/ridge classification is approximate
    """
    edge_map = build_edge_to_faces(mesh)
    normals = mesh.face_normals
    centers = mesh.triangles_center

    creases: list[CreaseEdge] = []
    cos_threshold = math.cos(math.radians(angle_threshold_degrees))

    for key, rec in edge_map.items():
        if len(rec.faces) != 2:
            continue

        f1, f2 = rec.faces
        n1 = normals[f1]
        n2 = normals[f2]

        dot = float(np.clip(np.dot(n1, n2), -1.0, 1.0))
        if dot > cos_threshold:
            continue

        angle = math.degrees(math.acos(dot))
        strength = 1.0 - dot

        v0, v1 = mesh.vertices[list(key)]
        edge_mid = (v0 + v1) / 2.0
        avg_center = (centers[f1] + centers[f2]) / 2.0
        avg_normal = n1 + n2
        norm = np.linalg.norm(avg_normal)
        if norm > 1e-9:
            avg_normal = avg_normal / norm

        # Approximate valley heuristic.
        # On many scanned surfaces, concave grooves produce a positive relation here.
        center_dir = avg_center - edge_mid
        is_valley = float(np.dot(center_dir, avg_normal)) > 0

        if valleys_only and not is_valley:
            continue

        creases.append(
            CreaseEdge(
                edge_key=key,
                face_a=f1,
                face_b=f2,
                angle_degrees=angle,
                strength=strength,
                is_valley=is_valley,
            )
        )

    return creases


def crease_edge_keys(creases: list[CreaseEdge]) -> set[tuple[int, int]]:
    return {c.edge_key for c in creases}