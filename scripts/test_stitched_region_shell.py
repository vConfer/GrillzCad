from pathlib import Path
from collections import defaultdict
import numpy as np
import trimesh

ROOT = Path(__file__).resolve().parents[1]

inner = trimesh.load(ROOT / "outputs_region_shell" / "region_inner.stl")
outer = trimesh.load(ROOT / "outputs_region_shell" / "region_outer.stl")

out_dir = ROOT / "outputs_stitched_region_shell"
out_dir.mkdir(exist_ok=True)


def boundary_loops(mesh):
    edge_count = defaultdict(int)

    for face in mesh.faces:
        a, b, c = map(int, face)
        for u, v in ((a, b), (b, c), (c, a)):
            edge_count[tuple(sorted((u, v)))] += 1

    boundary_edges = [edge for edge, count in edge_count.items() if count == 1]

    vertex_neighbors = defaultdict(list)
    for a, b in boundary_edges:
        vertex_neighbors[a].append(b)
        vertex_neighbors[b].append(a)

    visited = set()
    loops = []

    for a, b in boundary_edges:
        key = tuple(sorted((a, b)))
        if key in visited:
            continue

        loop = [a, b]
        visited.add(key)

        prev = a
        current = b

        while True:
            candidates = [v for v in vertex_neighbors[current] if v != prev]
            if not candidates:
                break

            nxt = candidates[0]
            edge_key = tuple(sorted((current, nxt)))

            if edge_key in visited:
                break

            loop.append(nxt)
            visited.add(edge_key)

            prev = current
            current = nxt

            if current == loop[0]:
                break

        loops.append(loop)

    return sorted(loops, key=len, reverse=True)


inner_loops = boundary_loops(inner)

vertices = np.vstack([inner.vertices, outer.vertices])
offset = len(inner.vertices)

faces = []
faces.extend(inner.faces.tolist())
faces.extend((outer.faces + offset).tolist())

for loop in inner_loops:
    n = len(loop)

    for i in range(n):
        a = loop[i]
        b = loop[(i + 1) % n]

        ao = a + offset
        bo = b + offset

        faces.append([a, bo, b])
        faces.append([a, ao, bo])

stitched = trimesh.Trimesh(vertices=vertices, faces=np.array(faces), process=True)

stitched.invert()
stitched.fix_normals()

stitched.fill_holes()
stitched.merge_vertices()
stitched.remove_unreferenced_vertices()
stitched.process(validate=True)
stitched.fix_normals()
stitched.remove_unreferenced_vertices()
stitched.process(validate=True)

stitched.export(out_dir / "stitched_region_shell.stl")

print("Loops stitched:", len(inner_loops))
print("Faces:", len(stitched.faces))
print("Watertight:", stitched.is_watertight)
print("Volume:", stitched.volume)
print("Output:", out_dir)