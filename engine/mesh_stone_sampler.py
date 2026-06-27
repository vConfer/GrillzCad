import numpy as np

from engine.surface_uv import faces_to_uv


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
    if not face_indices:
        return []

    face_indices = list(face_indices)

    centers = mesh.triangles_center[face_indices]
    normals = mesh.face_normals[face_indices]
    uv, origin, u_axis, v_axis, n_axis = faces_to_uv(mesh, face_indices)

    boundary_scores = compute_boundary_scores(mesh, face_indices)

    pitch = stone_diameter + spacing
    row_pitch = pitch * 0.8660254
    min_distance = pitch

    u_min, v_min = uv.min(axis=0)
    u_max, v_max = uv.max(axis=0)

    stones = []
    used_faces = set()

    row = 0
    v = v_min

    while v <= v_max:
        offset = pitch / 2.0 if row % 2 else 0.0
        u = u_min + offset

        while u <= u_max:
            target_uv = np.array([u, v])
            distances_uv = np.linalg.norm(uv - target_uv, axis=1)
            idx = int(np.argmin(distances_uv))

            if idx not in used_faces and boundary_scores[idx] >= min_boundary_score:
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
                    used_faces.add(idx)

            u += pitch

        row += 1
        v += row_pitch

    return stones