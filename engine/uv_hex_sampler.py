import numpy as np

from engine.surface_uv import faces_to_uv


def point_from_stone(stone):
    return np.array([stone["x"], stone["y"], stone["z"]], dtype=float)


def sample_uv_hex(mesh, face_indices, stone_diameter=1.0, spacing=0.15):
    if not face_indices:
        return []

    face_indices = list(face_indices)

    centers = mesh.triangles_center[face_indices]
    normals = mesh.face_normals[face_indices]
    uv, origin, u_axis, v_axis, n_axis = faces_to_uv(mesh, face_indices)

    pitch = stone_diameter + spacing
    row_pitch = pitch * 0.8660254
    min_distance = pitch * 0.80

    u_min, v_min = uv.min(axis=0)
    u_max, v_max = uv.max(axis=0)

    v_range = v_max - v_min
    v_start = v_min + v_range * 0.08
    v_end = v_min + v_range * 0.92

    stones = []

    candidate_count = 0
    near_face_count = 0
    collision_reject_count = 0
    accepted_count = 0

    row = 0
    v = v_start

    while v <= v_end:
        offset = pitch / 2.0 if row % 2 else 0.0
        u = u_min + offset

        while u <= u_max:
            candidate_count += 1

            target_uv = np.array([u, v])
            uv_distances = np.linalg.norm(uv - target_uv, axis=1)
            idx = int(np.argmin(uv_distances))

            if uv_distances[idx] <= pitch * 1.10:
                near_face_count += 1

                face = int(face_indices[idx])
                point = centers[idx]
                normal = normals[idx]

                keep = True
                for existing in stones:
                    if np.linalg.norm(point_from_stone(existing) - point) < min_distance:
                        keep = False
                        collision_reject_count += 1
                        break

                if keep:
                    accepted_count += 1
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

            u += pitch

        row += 1
        v += row_pitch

    print(f"Candidate grid points: {candidate_count}")
    print(f"Near safe-face points: {near_face_count}")
    print(f"Collision rejections: {collision_reject_count}")
    print(f"Accepted stones: {accepted_count}")

    return stones