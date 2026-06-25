import numpy as np
import trimesh


def make_round_stone_seat(
    point,
    normal,
    stone_diameter=1.0,
    total_depth=0.65,
    pilot_ratio=0.72,
    bearing_ratio=0.98,
):
    point = np.array(point, dtype=float)
    normal = np.array(normal, dtype=float)
    normal /= np.linalg.norm(normal)

    cut_dir = -normal

    bearing_diameter = stone_diameter * bearing_ratio
    pilot_diameter = stone_diameter * pilot_ratio

    bearing_depth = total_depth * 0.35
    cone_depth = total_depth * 0.40
    pilot_depth = total_depth * 0.25

    bearing = trimesh.creation.cylinder(
        radius=bearing_diameter / 2,
        height=bearing_depth,
        sections=32,
    )

    cone = trimesh.creation.cone(
        radius=bearing_diameter / 2,
        height=cone_depth,
        sections=32,
    )

    pilot = trimesh.creation.cylinder(
        radius=pilot_diameter / 2,
        height=pilot_depth,
        sections=32,
    )

    bearing.apply_translation([0, 0, -bearing_depth / 2])
    cone.apply_translation([0, 0, -bearing_depth - cone_depth / 2])
    pilot.apply_translation([0, 0, -bearing_depth - cone_depth - pilot_depth / 2])

    seat = trimesh.util.concatenate([bearing, cone, pilot])

    z_axis = np.array([0.0, 0.0, -1.0])
    transform = trimesh.geometry.align_vectors(z_axis, cut_dir)
    seat.apply_transform(transform)
    seat.apply_translation(point)

    return seat


def export_round_stone_seats(stones, path, total_depth=0.65):
    seats = []

    for stone in stones:
        seats.append(
            make_round_stone_seat(
                point=[stone["x"], stone["y"], stone["z"]],
                normal=[stone["nx"], stone["ny"], stone["nz"]],
                stone_diameter=stone.get("diameter", 1.0),
                total_depth=total_depth,
            )
        )

    if not seats:
        return None

    combined = trimesh.util.concatenate(seats)
    combined.export(path)
    return path