import numpy as np


def point_from_stone(stone):
    return np.array([stone["x"], stone["y"], stone["z"]], dtype=float)


def compute_boundary_scores(mesh, face_indices):
    centers = mesh.triangles_center[face_indices]
    region_center = centers.mean(axis=0)

    distances = np.linalg.norm(centers - region_center, axis=1)
    max_distance = distances.max()

    if max_distance == 0:
        return np.ones(len(face_indices))

    return 1.0 - (distances / max_distance)


def sample_stones_from_faces(
    mesh,
    face_indices,
    stone_diameter=1.0,
    spacing=0.15,
    min_boundary_score=0.18,
):
    centers = mesh.triangles_center[face_indices]
    normals = mesh.face_normals[face_indices]

    boundary_scores = compute_boundary_scores(mesh, face_indices)

    min_distance = stone_diameter + spacing
    stones = []

    region_center = centers.mean(axis=0)
    order = np.argsort(np.linalg.norm(centers - region_center, axis=1))

    for idx in order:
        if boundary_scores[idx] < min_boundary_score:
            continue

        face = int(face_indices[idx])
        point = centers[idx]
        normal = normals[idx]

        candidate = {
            "face": face,
            "x": float(point[0]),
            "y": float(point[1]),
            "z": float(point[2]),
            "nx": float(normal[0]),
            "ny": float(normal[1]),
            "nz": float(normal[2]),
            "diameter": float(stone_diameter),
        }

        keep = True
        for existing in stones:
            if np.linalg.norm(point_from_stone(existing) - point) < min_distance:
                keep = False
                break

        if keep:
            stones.append(candidate)

    return stones