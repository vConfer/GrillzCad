import numpy as np
import trimesh


def make_seat_cutter(point, normal, diameter=1.0, depth=0.6):
    radius = diameter / 2.0

    cutter = trimesh.creation.cylinder(
        radius=radius,
        height=depth,
        sections=32,
    )

    z_axis = np.array([0.0, 0.0, 1.0])
    normal = np.array(normal, dtype=float)
    normal /= np.linalg.norm(normal)

    # Cutter points inward, opposite the surface normal
    cut_direction = -normal

    transform = trimesh.geometry.align_vectors(z_axis, cut_direction)
    cutter.apply_transform(transform)

    point = np.array(point, dtype=float)
    cutter.apply_translation(point + cut_direction * (depth / 2.0))

    return cutter


def export_seat_cutters(stones, path, depth=0.6):
    cutters = []

    for stone in stones:
        cutters.append(
            make_seat_cutter(
                point=[stone["x"], stone["y"], stone["z"]],
                normal=[stone["nx"], stone["ny"], stone["nz"]],
                diameter=stone.get("diameter", 1.0),
                depth=depth,
            )
        )

    if not cutters:
        return None

    combined = trimesh.util.concatenate(cutters)
    combined.export(path)
    return path