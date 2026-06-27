import numpy as np


def split_faces_by_x(mesh, face_indices):
    """
    Simple v0: split selected faces into left/right tooth regions by X center.
    Later we'll replace this with true tooth numbering.
    """
    if not face_indices:
        return []

    face_indices = list(face_indices)
    centers = mesh.triangles_center[face_indices]

    x_values = centers[:, 0]
    median_x = float(np.median(x_values))

    left = []
    right = []

    for face, x in zip(face_indices, x_values):
        if x <= median_x:
            left.append(face)
        else:
            right.append(face)

    regions = []
    if left:
        regions.append(left)
    if right:
        regions.append(right)

    return regions