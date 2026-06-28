import trimesh

m = trimesh.load("outputs_shell_boolean/grill_shell_clean.stl")

print("Watertight:", m.is_watertight)

broken = m.edges_boundary

print("Boundary edges:", len(broken))

if len(broken) > 0:
    print("Shell has open boundaries")
else:
    print("No open boundaries found")