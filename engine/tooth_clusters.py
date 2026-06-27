import numpy as np


def cluster_faces_by_position(mesh, face_indices, expected_teeth=2):
    """
    v0 true-ish clustering:
    Groups design faces into tooth regions using face-center positions.

    This is better than median-X because it clusters by spatial center,
    not just a hard left/right cut.
    """
    if not face_indices:
        return []

    face_indices = list(face_indices)
    centers = mesh.triangles_center[face_indices]

    # Use x/y/z centers, but scale by spread so one axis doesn't dominate.
    spread = centers.max(axis=0) - centers.min(axis=0)
    spread[spread == 0] = 1.0
    points = (centers - centers.mean(axis=0)) / spread

    # Initialize cluster centers by farthest points
    cluster_centers = [points[np.argmin(points[:, 0])], points[np.argmax(points[:, 0])]]

    for _ in range(20):
        assignments = []

        for p in points:
            distances = [np.linalg.norm(p - c) for c in cluster_centers]
            assignments.append(int(np.argmin(distances)))

        new_centers = []
        for cluster_id in range(expected_teeth):
            cluster_points = points[np.array(assignments) == cluster_id]

            if len(cluster_points) == 0:
                new_centers.append(cluster_centers[cluster_id])
            else:
                new_centers.append(cluster_points.mean(axis=0))

        cluster_centers = new_centers

    regions = [[] for _ in range(expected_teeth)]

    for face, cluster_id in zip(face_indices, assignments):
        regions[cluster_id].append(face)

    regions = [r for r in regions if r]
    regions.sort(key=len, reverse=True)

    return regions