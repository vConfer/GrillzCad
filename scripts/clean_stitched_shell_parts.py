from pathlib import Path
import trimesh

ROOT = Path(__file__).resolve().parents[1]

src = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell.stl"
out = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_clean.stl"

m = trimesh.load(src)
parts = m.split(only_watertight=False)

# Keep only real shell bodies
parts = [p for p in parts if len(p.faces) > 1000]

clean = trimesh.util.concatenate(parts)
clean.remove_unreferenced_vertices()
clean.process(validate=True)
clean.fix_normals()

clean.export(out)

print("Exported:", out)
print("Bodies:", len(clean.split(only_watertight=False)))
print("Faces:", len(clean.faces))
print("Watertight:", clean.is_watertight)
print("Volume:", clean.volume)