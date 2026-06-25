import numpy as np


def estimate_front_direction(mesh):
    vertices = mesh.vertices
    centered = vertices - vertices.mean(axis=0)

    cov = np.cov(centered.T)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)

    main_axis = eigenvectors[:, np.argmax(eigenvalues)]
    return main_axis / np.linalg.norm(main_axis)


def detect_facial_faces(mesh, face_indices, front_direction=None, normal_threshold=0.25):
    if front_direction is None:
        front_direction = estimate_front_direction(mesh)

    normals = mesh.face_normals
    centers = mesh.triangles_center
    region_center = centers[face_indices].mean(axis=0)

    facial = []

    for face_index in face_indices:
        normal = normals[face_index]
        center = centers[face_index]

        outward_score = float(np.dot(normal, front_direction))
        position_score = float(np.dot(center - region_center, front_direction))

        if outward_score > normal_threshold and position_score > 0:
            facial.append(face_index)

    return facial