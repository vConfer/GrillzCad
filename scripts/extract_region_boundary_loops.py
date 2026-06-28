import trimesh
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

mesh = trimesh.load(ROOT / "outputs_region_shell" / "region_inner.stl")

edge_count = defaultdict(int)

for face in mesh.faces:
    a, b, c = map(int, face)
    for u, v in ((a, b), (b, c), (c, a)):
        key = tuple(sorted((u, v)))
        edge_count[key] += 1

boundary_edges = [
    edge for edge, count in edge_count.items()
    if count == 1
]

vertex_to_edges = defaultdict(list)

for a, b in boundary_edges:
    vertex_to_edges[a].append(b)
    vertex_to_edges[b].append(a)

visited_edges = set()
loops = []

for start_a, start_b in boundary_edges:
    edge_key = tuple(sorted((start_a, start_b)))

    if edge_key in visited_edges:
        continue

    loop = [start_a, start_b]
    visited_edges.add(edge_key)

    prev = start_a
    current = start_b

    while True:
        neighbors = vertex_to_edges[current]
        next_candidates = [v for v in neighbors if v != prev]

        if not next_candidates:
            break

        next_v = next_candidates[0]
        next_edge = tuple(sorted((current, next_v)))

        if next_edge in visited_edges:
            break

        loop.append(next_v)
        visited_edges.add(next_edge)

        prev = current
        current = next_v

        if current == loop[0]:
            break

    loops.append(loop)

loops = sorted(loops, key=len, reverse=True)

print(f"Boundary edges: {len(boundary_edges)}")
print(f"Loops found: {len(loops)}")

for i, loop in enumerate(loops[:10]):
    print(f"Loop {i}: {len(loop)} vertices")