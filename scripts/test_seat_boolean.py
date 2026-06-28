from pathlib import Path
import trimesh

ROOT = Path(__file__).resolve().parents[1]

shell_path = ROOT / "outputs_shell_boolean" / "grill_shell_clean.stl"
seats_path = ROOT / "outputs_per_tooth_pave" / "round_stone_seats.stl"
shell_path = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_final.stl"

out_dir = ROOT / "outputs_seat_boolean"
out_dir.mkdir(exist_ok=True)

shell = trimesh.load(shell_path)
seats = trimesh.load(seats_path)

print("Shell faces:", len(shell.faces), "watertight:", shell.is_watertight)
print("Seats faces:", len(seats.faces), "watertight:", seats.is_watertight)

result = trimesh.boolean.difference(
    [shell, seats],
    engine=None,
)

if result is None:
    print("Seat boolean failed.")
else:
    out = out_dir / "grill_with_seats.stl"
    result.export(out)

    print("Exported:", out)
    print("Faces:", len(result.faces))
    print("Watertight:", result.is_watertight)
    print("Volume:", result.volume)