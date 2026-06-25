from collections import defaultdict
from dataclasses import dataclass
import numpy as np
import trimesh


@dataclass
class EdgeRecord:
    edge_key: tuple[int, int]
    faces: list[int]
    vertices: tuple[int, int]


def build_edge_to_faces(mesh: trimesh.Trimesh) -> dict[tuple[int, int], EdgeRecord]:
    """Map each undirected mesh edge to the faces sharing it."""
    edge_map: dict[tuple[int, int], EdgeRecord] = {}

    for face_index, face in enumerate(mesh.faces):
        a, b, c = map(int, face)
        for u, v in ((a, b), (b, c), (c, a)):
            key = tuple(sorted((u, v)))
            if key not in edge_map:
                edge_map[key] = EdgeRecord(edge_key=key, faces=[], vertices=(u, v))
            edge_map[key].faces.append(face_index)

    return edge_map


def build_face_graph(mesh: trimesh.Trimesh, blocked_edges: set[tuple[int, int]] | None = None):
    """Build face adjacency graph while optionally blocking traversal across crease edges."""
    blocked_edges = blocked_edges or set()
    edge_map = build_edge_to_faces(mesh)

    adjacency = [[] for _ in range(len(mesh.faces))]

    for key, rec in edge_map.items():
        if key in blocked_edges:
            continue
        if len(rec.faces) == 2:
            f1, f2 = rec.faces
            adjacency[f1].append(f2)
            adjacency[f2].append(f1)

    return adjacency