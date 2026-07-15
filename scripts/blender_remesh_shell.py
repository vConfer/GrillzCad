from pathlib import Path
import bpy

ROOT = Path(__file__).resolve().parents[1]

src_path = ROOT / "outputs_stitched_region_shell" / "stitched_region_shell_clean.stl"
out_dir = ROOT / "outputs_watertight_shell"
out_dir.mkdir(exist_ok=True)
out_path = out_dir / "grill_shell_remesh.stl"

bpy.ops.object.delete()

bpy.ops.wm.stl_import(filepath=str(src_path))
obj = bpy.context.object
obj.name = "GrillShell"

obj.data = obj.data.copy()

bpy.context.view_layer.objects.active = obj
obj.select_set(True)

remesh = obj.modifiers.new(name="VoxelRemesh", type="REMESH")
remesh.mode = "VOXEL"
remesh.voxel_size = 0.08
remesh.use_smooth_shade = False

bpy.ops.object.modifier_apply(modifier=remesh.name)

bpy.ops.object.select_all(action="DESELECT")
obj.select_set(True)
bpy.context.view_layer.objects.active = obj

bpy.ops.export_mesh.stl(filepath=str(out_path), use_selection=True)

print(f"Exported: {out_path}")