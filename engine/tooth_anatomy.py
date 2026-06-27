import numpy as np


def compute_local_uv(mesh, face_indices):
    centers = mesh.triangles_center[face_indices]
    origin = centers.mean(axis=0)

    centered = centers - origin
    cov = np.cov(centered.T)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)

    order = np.argsort(eigenvalues)[::-1]

    u_axis = eigenvectors[:, order[0]]
    v_axis = eigenvectors[:, order[1]]

    u_axis = u_axis / np.linalg.norm(u_axis)
    v_axis = v_axis / np.linalg.norm(v_axis)

    uv = []

    for c in centers:
        rel = c - origin
        uv.append([
            float(np.dot(rel, u_axis)),
            float(np.dot(rel, v_axis)),
        ])

    uv = np.array(uv)

    return uv


def filter_design_region_by_uv(
    mesh,
    face_indices,
    u_min_ratio=0.12,
    u_max_ratio=0.88,
    v_min_ratio=0.18,
    v_max_ratio=0.72,
):
    if not face_indices:
        return []

    uv = compute_local_uv(mesh, face_indices)

    u_values = uv[:, 0]
    v_values = uv[:, 1]

    u_min = u_values.min()
    u_max = u_values.max()
    v_min = v_values.min()
    v_max = v_values.max()

    u_low = u_min + (u_max - u_min) * u_min_ratio
    u_high = u_min + (u_max - u_min) * u_max_ratio

    v_low = v_min + (v_max - v_min) * v_min_ratio
    v_high = v_min + (v_max - v_min) * v_max_ratio

    filtered = []

    for face, (u, v) in zip(face_indices, uv):
        if u_low <= u <= u_high and v_low <= v <= v_high:
            filtered.append(face)

    return filtered