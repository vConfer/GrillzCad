import numpy as np


def build_local_uv_frame(mesh, face_indices):
    centers = mesh.triangles_center[face_indices]
    origin = centers.mean(axis=0)

    centered = centers - origin
    cov = np.cov(centered.T)

    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    order = np.argsort(eigenvalues)[::-1]

    u_axis = eigenvectors[:, order[0]]
    v_axis = eigenvectors[:, order[1]]
    n_axis = np.cross(u_axis, v_axis)

    u_axis = u_axis / np.linalg.norm(u_axis)
    v_axis = v_axis / np.linalg.norm(v_axis)
    n_axis = n_axis / np.linalg.norm(n_axis)

    return origin, u_axis, v_axis, n_axis


def faces_to_uv(mesh, face_indices):
    origin, u_axis, v_axis, n_axis = build_local_uv_frame(mesh, face_indices)

    centers = mesh.triangles_center[face_indices]
    uv = []

    for center in centers:
        rel = center - origin
        uv.append([
            float(np.dot(rel, u_axis)),
            float(np.dot(rel, v_axis)),
        ])

    return np.array(uv), origin, u_axis, v_axis, n_axis
