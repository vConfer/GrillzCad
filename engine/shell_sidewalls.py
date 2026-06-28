import trimesh

m = trimesh.load("outputs_solid_shell/solid_shell.stl")

parts = m.split()

print(f"Parts: {len(parts)}")

for i, p in enumerate(parts):
    print()
    print(f"Part {i}")
    print(f"Faces: {len(p.faces)}")
    print(f"Vertices: {len(p.vertices)}")
    print(f"Volume: {p.volume}")
    print(f"Watertight: {p.is_watertight}")