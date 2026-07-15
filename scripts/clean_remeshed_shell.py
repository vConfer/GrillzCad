from pathlib import Path
import trimesh

ROOT = Path(__file__).resolve().parents[1]

src = ROOT / "outputs_watertight_shell" / "grill_shell_remesh.stl"
out = ROOT / "outputs_watertight_shell" / "grill_shell_remesh_clean.stl"

mesh = trimesh.load(src)
parts = mesh.split()

parts = sorted(parts, key=lambda part: abs(part.volume), reverse=True)

print(f"Parts before cleaning: {len(parts)}")

for i, part in enumerate(parts):
    print(
        f"Part {i}: "
        f"faces={len(part.faces)}, "
        f"volume={part.volume:.6f}, "
        f"watertight={part.is_watertight}"
    )

# Keep substantial bodies and discard tiny floating islands.
largest_volume = abs(parts[0].volume)
kept = [
    part
    for part in parts
    if abs(part.volume) >= largest_volume * 0.01
]

clean = trimesh.util.concatenate(kept)
clean.remove_unreferenced_vertices()
clean.fix_normals()
clean.export(out)

print(f"Kept bodies: {len(kept)}")
print(f"Exported: {out}")
print(f"Faces: {len(clean.faces)}")
print(f"Watertight: {clean.is_watertight}")
print(f"Bodies: {len(clean.split())}")
print(f"Volume: {clean.volume}")