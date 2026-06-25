import numpy as np
import trimesh


def make_stone_marker(point, normal, diameter=1.0, height=0.25):
    radius = diameter / 2.0

    marker = trimesh.creation.cylinder(
        radius=radius,
        height=height,
        sections=24,
    )

    z_axis = np.array([0.0, 0.0, 1.0])

    normal = np.array(normal, dtype=float)
    normal /= np.linalg.norm(normal)

    transform = trimesh.geometry.align_vectors(z_axis, normal)
    marker.apply_transform(transform)

    point = np.array(point, dtype=float)
    marker.apply_translation(point + normal * (height / 2))

    return marker


def export_stone_markers(stones, path):
    markers = []

    for stone in stones:
        marker = make_stone_marker(
            point=[stone["x"], stone["y"], stone["z"]],
            normal=[stone["nx"], stone["ny"], stone["nz"]],
            diameter=stone.get("diameter", 1.0),
        )
        markers.append(marker)

    if not markers:
        return

    combined = trimesh.util.concatenate(markers)
    combined.export(path)