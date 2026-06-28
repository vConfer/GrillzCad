import trimesh

m = trimesh.load("outputs_stitched_region_shell/stitched_region_shell.stl")
parts = m.split(only_watertight=False)
parts = sorted(parts, key=lambda p: len(p.faces), reverse=True)

print("Parts:", len(parts))

for i, p in enumerate(parts[:20]):
    print(i, "faces:", len(p.faces), "watertight:", p.is_watertight, "volume:", p.volume)