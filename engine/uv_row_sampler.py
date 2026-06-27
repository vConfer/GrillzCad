import numpy as np

from engine.surface_uv import faces_to_uv


def point_from_stone(stone):
    return np.array([stone["x"], stone["y"], stone["z"]], dtype=float)


def sample_uv_rows(mesh, face_indices, stone_diameter=1.0, spacing=0.15):
    if not face_indices:
        return []

    face_indices = list(face_indices)
    centers = mesh.triangles_center[face_indices]
    normals = mesh.face_normals[face_indices]

    uv, origin, u_axis, v_axis, n_axis = faces_to_uv(mesh, face_indices)

    pitch = stone_diameter + spacing
    row_height = pitch * 0.8660254
    min_distance = pitch

    v_min = uv[:, 1].min()
    v_max = uv[:, 1].max()

    stones = []
    row = 0
    v = v_min

    while v <= v_max:
        row_mask = np.abs(uv[:, 1] - v) <= row_height * 0.45

        if np.any(row_mask):
            row_indices = np.where(row_mask)[0]
            row_indices = row_indices[np.argsort(uv[row_indices, 0])]

            offset_toggle = row % 2

            for count, idx in enumerate(row_indices):
                if count % 2 != offset_toggle:
                    continue

                face = int(face_indices[idx])
                point = centers[idx]
                normal = normals[idx]

                keep = True
                for existing in stones:
                    if np.linalg.norm(point_from_stone(existing) - point) < min_distance:
                        keep = False
                        break

                if keep:
                    stones.append({
                        "face": face,
                        "x": float(point[0]),
                        "y": float(point[1]),
                        "z": float(point[2]),
                        "nx": float(normal[0]),
                        "ny": float(normal[1]),
                        "nz": float(normal[2]),
                        "diameter": float(stone_diameter),
                    })

        row += 1
        v += row_height

    return stones