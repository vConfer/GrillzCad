import trimesh
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

m = trimesh.load(ROOT / "outputs_solid_shell" / "solid_shell.stl")
parts = m.split()

if len(parts) != 2:
    raise ValueError(f"Expected 2 shell parts, got {len(parts)}")

parts = sorted(parts, key=lambda p: p.volume)
inner = parts[0]
outer = parts[1]

out_dir = ROOT / "outputs_shell_boolean"
out_dir.mkdir(exist_ok=True)

inner.export(out_dir / "inner.stl")
outer.export(out_dir / "outer.stl")

print("Inner volume:", inner.volume)
print("Outer volume:", outer.volume)

result = trimesh.boolean.difference(
    [outer, inner],
    engine=None,
)

if result is None:
    print("Boolean failed.")
else:
    result.export(out_dir / "grill_shell_boolean.stl")
    print("Exported:", out_dir / "grill_shell_boolean.stl")
    print("Watertight:", result.is_watertight)
    print("Volume:", result.volume)