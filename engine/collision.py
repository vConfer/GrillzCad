import numpy as np


def stone_point(stone):
    return np.array([stone["x"], stone["y"], stone["z"]], dtype=float)


def stones_overlap(a, b, min_spacing=0.05):
    pa = stone_point(a)
    pb = stone_point(b)

    da = float(a.get("diameter", 1.0))
    db = float(b.get("diameter", 1.0))

    min_distance = (da / 2.0) + (db / 2.0) + min_spacing
    actual_distance = float(np.linalg.norm(pa - pb))

    return actual_distance < min_distance


def remove_colliding_stones(stones, min_spacing=0.05):
    kept = []

    for stone in stones:
        collides = False

        for existing in kept:
            if stones_overlap(stone, existing, min_spacing=min_spacing):
                collides = True
                break

        if not collides:
            kept.append(stone)

    return kept