from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parents[1]

shell_path = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_final_clean.stl"
seats_path = ROOT / "outputs_per_tooth_pave" / "round_stone_seats.stl"
out_dir = ROOT / "outputs_blender_boolean"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "grill_with_seats_blender.stl"

bpy.ops.object.delete()

bpy.ops.wm.stl_import(filepath=str(shell_path))
shell = bpy.context.object
shell.name = "Shell"
shell.data = shell.data.copy()

bpy.ops.wm.stl_import(filepath=str(seats_path))
seats = bpy.context.object
seats.name = "SeatCutters"
seats.data = seats.data.copy()

bpy.context.view_layer.objects.active = shell
shell.select_set(True)
seats.select_set(False)

modifier = shell.modifiers.new(name="SeatBoolean", type="BOOLEAN")
modifier.operation = "DIFFERENCE"
modifier.object = seats
modifier.solver = "FAST"

bpy.ops.object.modifier_apply(modifier=modifier.name)

bpy.data.objects.remove(seats, do_unlink=True)

bpy.ops.object.select_all(action="DESELECT")
shell.select_set(True)
bpy.context.view_layer.objects.active = shell

bpy.ops.export_mesh.stl(filepath=str(out_path), use_selection=True)

print(f"Exported: {out_path}")