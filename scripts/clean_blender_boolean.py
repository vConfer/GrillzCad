from pathlib import Path
import trimesh

ROOT = Path(__file__).resolve().parents[1]

src = ROOT / "outputs_blender_boolean" / "grill_with_seats_blender.stl"
out = ROOT / "outputs_blender_boolean" / "grill_with_seats_clean.stl"

m = trimesh.load(src)
parts = m.split(only_watertight=False)

largest = max(parts, key=lambda p: len(p.faces))
largest.remove_unreferenced_vertices()
largest.process(validate=True)
largest.fix_normals()

largest.export(out)

print("Exported:", out)
print("Faces:", len(largest.faces))
print("Watertight:", largest.is_watertight)
print("Bodies:", len(largest.split(only_watertight=False)))
print("Volume:", largest.volume)