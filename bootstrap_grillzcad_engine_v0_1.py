
from pathlib import Path

ROOT = Path.cwd()

FILES = {}

FILES["requirements.txt"] = """numpy
scipy
trimesh
networkx
rtree
"""

FILES[".gitignore"] = """.venv/
__pycache__/
*.pyc
outputs/
*.log
.DS_Store
"""

FILES["engine/__init__.py"] = ""

FILES["engine/mesh_loader.py"] = """
from pathlib import Path
import trimesh


def load_mesh(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Mesh file not found: {path}")

    mesh = trimesh.load_mesh(path, force="mesh")

    if not isinstance(mesh, trimesh.Trimesh):
        raise ValueError("File could not be loaded as a single mesh.")

    if mesh.vertices.size == 0 or mesh.faces.size == 0:
        raise ValueError("Mesh has no vertices or faces.")

    return mesh
"""

FILES["engine/mesh_cleaner.py"] = """
import trimesh


def clean_mesh(mesh):
    mesh = mesh.copy()

    for fn in [
        "remove_duplicate_faces",
        "remove_degenerate_faces",
        "remove_unreferenced_vertices",
        "merge_vertices",
        "fix_normals",
    ]:
        try:
            getattr(mesh, fn)()
        except Exception:
            pass

    return mesh
"""

FILES["engine/adjacency.py"] = """
from dataclasses import dataclass


@dataclass
class EdgeRecord:
    edge_key: tuple
    faces: list
    vertices: tuple


def build_edge_to_faces(mesh):
    edge_map = {}

    for face_index, face in enumerate(mesh.faces):
        a, b, c = map(int, face)

        for u, v in ((a, b), (b, c), (c, a)):
            key = tuple(sorted((u, v)))

            if key not in edge_map:
                edge_map[key] = EdgeRecord(edge_key=key, faces=[], vertices=(u, v))

            edge_map[key].faces.append(face_index)

    return edge_map


def build_face_graph(mesh, blocked_edges=None):
    blocked_edges = blocked_edges or set()
    edge_map = build_edge_to_faces(mesh)

    adjacency = [[] for _ in range(len(mesh.faces))]

    for key, record in edge_map.items():
        if key in blocked_edges:
            continue

        if len(record.faces) == 2:
            f1, f2 = record.faces
            adjacency[f1].append(f2)
            adjacency[f2].append(f1)

    return adjacency
"""

FILES["engine/crease_detection.py"] = """
from dataclasses import dataclass
import math
import numpy as np

from .adjacency import build_edge_to_faces


@dataclass
class CreaseEdge:
    edge_key: tuple
    face_a: int
    face_b: int
    angle_degrees: float
    strength: float
    is_valley: bool


def detect_crease_edges(mesh, angle_threshold_degrees=35.0, valleys_only=False):
    edge_map = build_edge_to_faces(mesh)
    normals = mesh.face_normals
    centers = mesh.triangles_center
    cos_threshold = math.cos(math.radians(angle_threshold_degrees))

    creases = []

    for key, record in edge_map.items():
        if len(record.faces) != 2:
            continue

        f1, f2 = record.faces
        n1 = normals[f1]
        n2 = normals[f2]

        dot = float(np.clip(np.dot(n1, n2), -1.0, 1.0))

        if dot > cos_threshold:
            continue

        angle = math.degrees(math.acos(dot))
        strength = 1.0 - dot

        v0, v1 = mesh.vertices[list(key)]
        edge_mid = (v0 + v1) / 2.0
        avg_center = (centers[f1] + centers[f2]) / 2.0

        avg_normal = n1 + n2
        norm = np.linalg.norm(avg_normal)

        if norm > 1e-9:
            avg_normal = avg_normal / norm

        center_dir = avg_center - edge_mid
        is_valley = float(np.dot(center_dir, avg_normal)) > 0

        if valleys_only and not is_valley:
            continue

        creases.append(
            CreaseEdge(
                edge_key=key,
                face_a=f1,
                face_b=f2,
                angle_degrees=angle,
                strength=strength,
                is_valley=is_valley,
            )
        )

    return creases


def crease_edge_keys(creases):
    return {c.edge_key for c in creases}
"""

FILES["engine/segmentation.py"] = """
from collections import deque

from .adjacency import build_face_graph


def segment_faces(mesh, blocked_edges=None, min_faces=100):
    adjacency = build_face_graph(mesh, blocked_edges=blocked_edges)
    visited = set()
    regions = []

    for start in range(len(mesh.faces)):
        if start in visited:
            continue

        queue = deque([start])
        visited.add(start)
        region = []

        while queue:
            face = queue.popleft()
            region.append(face)

            for neighbor in adjacency[face]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        if len(region) >= min_faces:
            regions.append(region)

    regions.sort(key=len, reverse=True)
    return regions


def submesh_from_faces(mesh, face_indices):
    sub = mesh.submesh([face_indices], append=True, repair=False)

    try:
        sub.remove_unreferenced_vertices()
    except Exception:
        pass

    return sub
"""

FILES["engine/debug_export.py"] = """
from pathlib import Path
import json

from .segmentation import submesh_from_faces


def export_cleaned_mesh(mesh, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "cleaned_mesh.stl"
    mesh.export(path)
    return path


def export_regions(mesh, regions, out_dir):
    out_dir = Path(out_dir)
    region_dir = out_dir / "regions"
    region_dir.mkdir(parents=True, exist_ok=True)

    paths = []

    for i, faces in enumerate(regions, start=1):
        sub = submesh_from_faces(mesh, faces)
        path = region_dir / f"region_{i:03d}.stl"
        sub.export(path)
        paths.append(path)

    return paths


def export_crease_lines_obj(mesh, creases, out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "crease_lines.obj"

    vertices = []
    lines = []

    for crease in creases:
        a_idx, b_idx = crease.edge_key
        a = mesh.vertices[a_idx]
        b = mesh.vertices[b_idx]

        vertices.append(a)
        vertices.append(b)

        n = len(vertices)
        lines.append((n - 1, n))

    with open(path, "w", encoding="utf-8") as file:
        file.write("# GrillzCAD crease lines\\n")

        for v in vertices:
            file.write(f"v {v[0]} {v[1]} {v[2]}\\n")

        for a, b in lines:
            file.write(f"l {a} {b}\\n")

    return path


def export_report(mesh, creases, regions, out_dir, settings):
    out_dir = Path(out_dir)

    report = {
        "vertices": int(len(mesh.vertices)),
        "faces": int(len(mesh.faces)),
        "is_watertight": bool(mesh.is_watertight),
        "bounds": mesh.bounds.tolist(),
        "settings": settings,
        "crease_count": len(creases),
        "valley_crease_count": sum(1 for c in creases if c.is_valley),
        "region_count": len(regions),
        "regions": [
            {"id": i + 1, "face_count": len(region)}
            for i, region in enumerate(regions)
        ],
    }

    path = out_dir / "report.json"

    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    return path
"""

FILES["run_segmentation.py"] = """
from pathlib import Path
import argparse

from engine.mesh_loader import load_mesh
from engine.mesh_cleaner import clean_mesh
from engine.crease_detection import detect_crease_edges, crease_edge_keys
from engine.segmentation import segment_faces
from engine.debug_export import (
    export_cleaned_mesh,
    export_crease_lines_obj,
    export_regions,
    export_report,
)


def main():
    parser = argparse.ArgumentParser(description="GrillzCAD engine segmentation runner")
    parser.add_argument("input_stl", help="Input STL file")
    parser.add_argument("output_dir", help="Output folder")
    parser.add_argument("--crease-angle", type=float, default=35.0)
    parser.add_argument("--min-faces", type=int, default=100)
    parser.add_argument("--valleys-only", action="store_true")
    args = parser.parse_args()

    input_path = Path(args.input_stl)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/6] Loading mesh: {input_path}")
    mesh = load_mesh(input_path)

    print("[2/6] Cleaning mesh")
    mesh = clean_mesh(mesh)

    print("[3/6] Detecting creases")
    creases = detect_crease_edges(
        mesh,
        angle_threshold_degrees=args.crease_angle,
        valleys_only=args.valleys_only,
    )

    blocked_edges = crease_edge_keys(creases)

    print("[4/6] Segmenting mesh")
    regions = segment_faces(mesh, blocked_edges=blocked_edges, min_faces=args.min_faces)

    print("[5/6] Exporting debug files")
    export_cleaned_mesh(mesh, output_dir)
    export_crease_lines_obj(mesh, creases, output_dir)
    export_regions(mesh, regions, output_dir)

    print("[6/6] Writing report")
    report = export_report(
        mesh,
        creases,
        regions,
        output_dir,
        settings={
            "input_stl": str(input_path),
            "crease_angle": args.crease_angle,
            "min_faces": args.min_faces,
            "valleys_only": args.valleys_only,
        },
    )

    print("\\nDone.")
    print(f"Creases: {len(creases)}")
    print(f"Regions: {len(regions)}")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
"""

FILES["README.md"] = """# GrillzCAD

GrillzCAD is a CAD tool for creating custom grillz with pave, prong, and invisible stone settings.

## Current milestone

Engine v0.1:

- Load STL
- Clean mesh
- Detect crease edges
- Segment mesh into regions
- Export debug STLs/OBJ/report

## Setup

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run segmentation

```powershell
python run_segmentation.py "C:\\path\\to\\your_model.stl" outputs --crease-angle 35 --min-faces 100
```
"""


def main():
    for relative, content in FILES.items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content.strip() + "\n", encoding="utf-8")

    print("Created GrillzCAD Engine v0.1 files in:", ROOT)
    print("Next commands:")
    print("  git add .")
    print('  git commit -m "Add engine v0.1 segmentation pipeline"')


if __name__ == "__main__":
    main()
