from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parents[1]

shell_path = (
    ROOT
    / "outputs_watertight_shell"
    / "grill_shell_remesh_clean.stl"
)

seats_path = (
    ROOT
    / "outputs_per_tooth_pave"
    / "round_stone_seats.stl"
)

out_dir = ROOT / "outputs_blender_boolean"
out_dir.mkdir(exist_ok=True)

out_path = out_dir / "grill_with_seats_blender.stl"


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def import_stl(path):
    before = set(bpy.context.scene.objects)

    bpy.ops.wm.stl_import(filepath=str(path))

    after = set(bpy.context.scene.objects)
    imported = list(after - before)

    if not imported:
        raise RuntimeError(f"No objects imported from {path}")

    return imported


def join_objects(objects, name):
    bpy.ops.object.select_all(action="DESELECT")

    for obj in objects:
        obj.select_set(True)

    active = objects[0]
    bpy.context.view_layer.objects.active = active

    if len(objects) > 1:
        bpy.ops.object.join()

    active = bpy.context.view_layer.objects.active
    active.name = name

    # Prevent Blender's multi-user-data modifier error.
    active.data = active.data.copy()

    return active


clear_scene()

shell_objects = import_stl(shell_path)
shell = join_objects(shell_objects, "GrillShell")

seat_objects = import_stl(seats_path)
seats = join_objects(seat_objects, "SeatCutters")

print(f"Shell polygons before boolean: {len(shell.data.polygons)}")
print(f"Cutter polygons: {len(seats.data.polygons)}")

if len(shell.data.polygons) == 0:
    raise RuntimeError("Shell imported empty.")

if len(seats.data.polygons) == 0:
    raise RuntimeError("Seat cutters imported empty.")

bpy.ops.object.select_all(action="DESELECT")
shell.select_set(True)
bpy.context.view_layer.objects.active = shell

modifier = shell.modifiers.new(
    name="SeatBoolean",
    type="BOOLEAN",
)
modifier.operation = "DIFFERENCE"
modifier.object = seats
modifier.solver = "FAST"

bpy.ops.object.modifier_apply(modifier=modifier.name)

polygon_count = len(shell.data.polygons)
print(f"Shell polygons after boolean: {polygon_count}")

if polygon_count == 0:
    raise RuntimeError(
        "Boolean erased the shell. Output was not exported."
    )

# Remove cutter geometry after applying the Boolean.
bpy.data.objects.remove(seats, do_unlink=True)

bpy.ops.object.select_all(action="DESELECT")
shell.select_set(True)
bpy.context.view_layer.objects.active = shell

bpy.ops.export_mesh.stl(
    filepath=str(out_path),
    use_selection=True,
)

seat_obj = bpy.data.objects.get("SeatCutters")

if seat_obj is not None:
    bpy.data.objects.remove(seat_obj, do_unlink=True)

bpy.ops.object.select_all(action="DESELECT")
shell.select_set(True)
bpy.context.view_layer.objects.active = shell

bpy.ops.export_mesh.stl(
    filepath=str(out_path),
    use_selection=True,
)

print(f"Exported: {out_path}")
print(f"Shell polygons after boolean: {len(shell.data.polygons)}")