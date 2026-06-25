import json
import numpy as np


def estimate_layout_axes(mesh, face_indices):
    centers = mesh.triangles_center[face_indices]
    centered = centers - centers.mean(axis=0)

    cov = np.cov(centered.T)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)

    order = np.argsort(eigenvalues)[::-1]
    u_axis = eigenvectors[:, order[0]]
    v_axis = eigenvectors[:, order[1]]

    u_axis = u_axis / np.linalg.norm(u_axis)
    v_axis = v_axis / np.linalg.norm(v_axis)

    return centers.mean(axis=0), u_axis, v_axis


def generate_hex_layout(mesh, face_indices, stone_diameter=1.0, spacing=0.15):
    centers = mesh.triangles_center[face_indices]
    origin, u_axis, v_axis = estimate_layout_axes(mesh, face_indices)

    pitch = stone_diameter + spacing
    row_pitch = pitch * 0.8660254

    uv = []
    for c in centers:
        rel = c - origin
        uv.append([np.dot(rel, u_axis), np.dot(rel, v_axis)])

    uv = np.array(uv)
    u_min, v_min = uv.min(axis=0)
    u_max, v_max = uv.max(axis=0)

    stones = []
    row = 0
    v = v_min

    while v <= v_max:
        offset = pitch / 2 if row % 2 else 0
        u = u_min + offset

        while u <= u_max:
            target = origin + u * u_axis + v * v_axis

            distances = np.linalg.norm(centers - target, axis=1)
            nearest_index = int(np.argmin(distances))

            if distances[nearest_index] <= pitch * 0.75:
                face_index = face_indices[nearest_index]
                point = centers[nearest_index]
                normal = mesh.face_normals[face_index]

                stones.append({
                    "face": int(face_index),
                    "x": float(point[0]),
                    "y": float(point[1]),
                    "z": float(point[2]),
                    "nx": float(normal[0]),
                    "ny": float(normal[1]),
                    "nz": float(normal[2]),
                    "diameter": float(stone_diameter),
                })

            u += pitch

        row += 1
        v += row_pitch

    return stones


def save_stone_layout(stones, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(stones, file, indent=2)