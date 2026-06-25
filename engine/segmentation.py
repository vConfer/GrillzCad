from collections import deque
import trimesh

from .adjacency import build_face_graph


def segment_faces(
    mesh: trimesh.Trimesh,
    blocked_edges: set[tuple[int, int]] | None = None,
    min_faces: int = 100,
) -> list[list[int]]:
    """Segment mesh faces into connected components, optionally separated by blocked crease edges."""
    adjacency = build_face_graph(mesh, blocked_edges=blocked_edges)

    visited = set()
    regions: list[list[int]] = []

    for start in range(len(mesh.faces)):
        if start in visited:
            continue

        queue = deque([start])
        visited.add(start)
        region = []

        while queue:
            f = queue.popleft()
            region.append(f)

            for nb in adjacency[f]:
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)

        if len(region) >= min_faces:
            regions.append(region)

    regions.sort(key=len, reverse=True)
    return regions


def submesh_from_faces(mesh: trimesh.Trimesh, face_indices: list[int]) -> trimesh.Trimesh:
    """Extract a region as a new Trimesh."""
    sub = mesh.submesh([face_indices], append=True, repair=False)
    try:
        sub.remove_unreferenced_vertices()
    except Exception:
        pass
    return sub