from pathlib import Path
import trimesh

ROOT = Path(__file__).resolve().parents[1]

src = ROOT / "outputs_shell_boolean" / "grill_shell_boolean.stl"
out_dir = ROOT / "outputs_shell_boolean"
out = out_dir / "grill_shell_clean.stl"

m = trimesh.load(src)
parts = m.split(only_watertight=False)

largest = max(parts, key=lambda p: len(p.faces))

largest.remove_unreferenced_vertices()
largest.process(validate=True)

largest.export(out)

print("Exported:", out)
print("Faces:", len(largest.faces))
print("Vertices:", len(largest.vertices))
print("Watertight:", largest.is_watertight)
print("Volume:", largest.volume)