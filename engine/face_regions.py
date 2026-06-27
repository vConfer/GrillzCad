from collections import deque


def connected_face_regions(face_indices, adjacency, min_faces=5):
    face_set = set(face_indices)
    visited = set()
    regions = []

    for start in face_indices:
        if start in visited:
            continue

        queue = deque([start])
        visited.add(start)
        region = []

        while queue:
            face = queue.popleft()
            region.append(face)

            for neighbor in adjacency[face]:
                if neighbor in face_set and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        if len(region) >= min_faces:
            regions.append(region)

    regions.sort(key=len, reverse=True)
    return regions
