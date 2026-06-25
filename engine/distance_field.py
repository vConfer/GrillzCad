from collections import deque


def boundary_faces(face_indices, adjacency):
    face_set = set(face_indices)
    boundary = set()

    for face in face_indices:
        for neighbor in adjacency[face]:
            if neighbor not in face_set:
                boundary.add(face)
                break

    return boundary


def face_distance_steps(face_indices, adjacency):
    """
    Graph-distance from each face to nearest boundary face.
    This is step distance, not mm yet.
    """
    face_set = set(face_indices)
    boundary = boundary_faces(face_indices, adjacency)

    distances = {face: None for face in face_indices}
    queue = deque()

    for face in boundary:
        distances[face] = 0
        queue.append(face)

    while queue:
        face = queue.popleft()

        for neighbor in adjacency[face]:
            if neighbor not in face_set:
                continue

            if distances[neighbor] is None:
                distances[neighbor] = distances[face] + 1
                queue.append(neighbor)

    return distances