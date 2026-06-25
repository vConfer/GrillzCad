from pathlib import Path

from engine.grill_engine import GrillEngine
from engine.grill_shell import export_offset_shell


class GrillProject:
    def __init__(self, input_stl):
        self.input_stl = Path(input_stl)
        self.engine = GrillEngine(input_stl)
        self.output_dir = None

    def build_preview(
        self,
        output_dir="outputs_project",
        stone_diameter=1.0,
        spacing=0.15,
        border_mm=0.5,
    ):
        self.output_dir = Path(output_dir)

        (
            self.engine
            .load()
            .classify_surfaces()
            .compute_design_region(border_mm=border_mm)
            .generate_stones(
                stone_diameter=stone_diameter,
                spacing=spacing,
            )
        )

        self.engine.export_preview(self.output_dir)
        return self

    def export_shell(self, offset_mm=0.6):
        if self.output_dir is None:
            self.output_dir = Path("outputs_project")

        self.output_dir.mkdir(exist_ok=True)

        return export_offset_shell(
            self.engine.mesh,
            self.output_dir / f"offset_shell_{offset_mm:.2f}mm.stl",
            offset_mm=offset_mm,
        )