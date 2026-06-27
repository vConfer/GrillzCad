from pathlib import Path

from engine.mesh_loader import load_mesh
from engine.mesh_cleaner import clean_mesh
from engine.visibility_classifier import visible_faces_from_camera
from engine.adjacency import build_face_graph
from engine.distance_field import face_distance_steps
from engine.distance_mm import safe_faces_by_mm
from engine.stone_layout import generate_hex_layout, save_stone_layout
from engine.collision import remove_colliding_stones
from engine.stone_markers import export_stone_markers
from engine.seat_cutters import export_seat_cutters
from engine.seat_generator import export_round_stone_seats
from engine.segmentation import submesh_from_faces
from engine.tooth_anatomy import filter_design_region_by_uv
from engine.mesh_stone_sampler import sample_stones_from_faces
from engine.face_regions import connected_face_regions


class GrillEngine:
    def __init__(self, input_path):
        self.input_path = Path(input_path)
        self.mesh = None
        self.classes = None
        self.safe_faces = None
        self.stones = None

    def load(self):
        self.mesh = clean_mesh(load_mesh(self.input_path))
        return self

    def classify_surfaces(self):
        visible_faces = visible_faces_from_camera(self.mesh)
        self.classes = {
            "facial": visible_faces,
            "back": [],
            "edge": [],
            "flat": [],
        }
        return self

    def compute_design_region(self, border_steps=4, border_mm=None):
        facial_faces = self.classes["facial"]
        adjacency = build_face_graph(self.mesh)

        if border_mm is not None and border_mm > 0:
            self.safe_faces = safe_faces_by_mm(
                self.mesh,
                facial_faces,
                adjacency,
                border_mm=border_mm,
            )
        else:
            self.safe_faces = list(facial_faces)

        self.safe_faces = filter_design_region_by_uv(
            self.mesh,
            self.safe_faces,
            u_min_ratio=0.16,
            u_max_ratio=0.84,
            v_min_ratio=0.42,
            v_max_ratio=0.92,
        )

        print(f"Safe faces after anatomy filter: {len(self.safe_faces)}")

        return self

    def generate_stones(self, stone_diameter=1.0, spacing=0.15):
        print(f"Safe faces: {len(self.safe_faces)}")

        self.stones = sample_stones_from_faces(
            self.mesh,
            self.safe_faces,
            stone_diameter=stone_diameter,
            spacing=spacing,
        )

        self.stones = remove_colliding_stones(
            self.stones,
            min_spacing=spacing,
        )

        print(f"Generated stones: {len(self.stones)}")

        return self

    def export_preview(self, output_dir):
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        submesh_from_faces(self.mesh, self.classes["facial"]).export(
            output_dir / "facial_full.stl"
        )

        submesh_from_faces(self.mesh, self.safe_faces).export(
            output_dir / "design_safe_region.stl"
        )

        save_stone_layout(self.stones, output_dir / "stone_centers.json")
        export_stone_markers(self.stones, output_dir / "stone_markers.stl")
        export_seat_cutters(self.stones, output_dir / "seat_cutters.stl", depth=0.6)
        export_round_stone_seats(self.stones, output_dir / "round_stone_seats.stl")

        return output_dir