import numpy as np


def estimate_visibility_axis(mesh):
    vertices = mesh.vertices
    centered = vertices - vertices.mean(axis=0)

    cov = np.cov(centered.T)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)

    axis = eigenvectors[:, np.argmin(eigenvalues)]
    return axis / np.linalg.norm(axis)


def visible_faces_from_direction(mesh, direction,samples_u=25, samples_v=25):
    centers = mesh.triangles_center
    origin = centers.mean(axis=0)

    bbox = mesh.bounds
    size = np.linalg.norm(bbox[1] - bbox[0])

    direction = np.array(direction, dtype=float)
    direction /= np.linalg.norm(direction)

    camera = origin + direction * size * 3.0

    up = np.array([0.0, 0.0, 1.0])
    u_axis = np.cross(direction, up)

    if np.linalg.norm(u_axis) < 1e-6:
        up = np.array([0.0, 1.0, 0.0])
        u_axis = np.cross(direction, up)

    u_axis /= np.linalg.norm(u_axis)
    v_axis = np.cross(u_axis, direction)
    v_axis /= np.linalg.norm(v_axis)

    rel = centers - origin
    u_vals = rel @ u_axis
    v_vals = rel @ v_axis

    ray_origins = []
    ray_dirs = []

    for u in np.linspace(u_vals.min(), u_vals.max(), samples_u):
        for v in np.linspace(v_vals.min(), v_vals.max(), samples_v):
            ray_origins.append(camera + u * u_axis + v * v_axis)
            ray_dirs.append(-direction)

    ray_origins = np.array(ray_origins)
    ray_dirs = np.array(ray_dirs)

    locations, index_ray, index_tri = mesh.ray.intersects_location(
        ray_origins=ray_origins,
        ray_directions=ray_dirs,
        multiple_hits=False,
    )

    return list(set(int(i) for i in index_tri))


def visible_faces_from_camera(mesh, samples_u=25, samples_v=25):
    axis = estimate_visibility_axis(mesh)

    faces_a = visible_faces_from_direction(
        mesh,
        axis,
        samples_u=samples_u,
        samples_v=samples_v,
    )

    faces_b = visible_faces_from_direction(
        mesh,
        -axis,
        samples_u=samples_u,
        samples_v=samples_v,
    )

    print(f"Visibility side A faces: {len(faces_a)}")
    print(f"Visibility side B faces: {len(faces_b)}")

    return faces_a if len(faces_a) >= len(faces_b) else faces_b