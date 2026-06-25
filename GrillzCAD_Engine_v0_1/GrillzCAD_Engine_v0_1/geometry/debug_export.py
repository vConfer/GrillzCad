from pathlib import Path
import json
import numpy as np
import trimesh

from .segmentation import submesh_from_faces


def export_cleaned_mesh(mesh: trimesh.Trimesh, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    mesh.export(out_dir / "cleaned_mesh.stl")


def export_regions(mesh: trimesh.Trimesh, regions: list[list[int]], out_dir: Path):
    region_dir = out_dir / "regions"
    region_dir.mkdir(parents=True, exist_ok=True)

    paths = []
    for i, faces in enumerate(regions, start=1):
        sub = submesh_from_faces(mesh, faces)
        path = region_dir / f"region_{i:03d}.stl"
        sub.export(path)
        paths.append(str(path))
    return paths


def export_crease_lines_obj(mesh: trimesh.Trimesh, creases, out_dir: Path):
    """Export crease edges as OBJ line segments."""
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

    with open(path, "w", encoding="utf-8") as f:
        f.write("# GrillzCAD crease lines\n")
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for a, b in lines:
            f.write(f"l {a} {b}\n")

    return path


def export_report(
    mesh: trimesh.Trimesh,
    creases,
    regions: list[list[int]],
    out_dir: Path,
    settings: dict,
):
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
            {
                "id": i + 1,
                "face_count": len(region),
            }
            for i, region in enumerate(regions)
        ],
    }

    path = out_dir / "report.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return path