import numpy as np


def project_point_to_faces(mesh, face_indices, target_point):
    centers = mesh.triangles_center[face_indices]

    distances = np.linalg.norm(
        centers - target_point,
        axis=1,
    )

    idx = np.argmin(distances)

    face = int(face_indices[idx])

    return {
        "face": face,
        "point": centers[idx],
        "normal": mesh.face_normals[face],
    }