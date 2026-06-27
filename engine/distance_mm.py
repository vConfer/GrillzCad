import numpy as np

from engine.distance_field import boundary_faces


def face_distance_mm(mesh, face_indices, adjacency):
    face_set = set(face_indices)
    boundary = boundary_faces(face_indices, adjacency)
    centers = mesh.triangles_center

    if not boundary:
        return {face: 0.0 for face in face_indices}

    boundary_centers = np.array([centers[f] for f in boundary])

    distances = {}

    for face in face_indices:
        if face in boundary:
            distances[face] = 0.0
            continue

        point = centers[face]
        dists = np.linalg.norm(boundary_centers - point, axis=1)
        distances[face] = float(np.min(dists))

    return distances


def safe_faces_by_mm(mesh, face_indices, adjacency, border_mm=0.5):
    distances = face_distance_mm(mesh, face_indices, adjacency)

    return [
        face
        for face, dist in distances.items()
        if dist >= border_mm
    ]