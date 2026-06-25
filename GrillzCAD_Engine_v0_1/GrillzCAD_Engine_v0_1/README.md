# GrillzCAD Engine v0.1

This is the first standalone Python geometry engine for GrillzCAD.

## What it does

Given an STL file, it will:

1. Load the mesh
2. Clean the mesh
3. Build triangle adjacency
4. Detect sharp crease/valley edges
5. Segment the mesh into connected regions
6. Export debug STL files:
   - cleaned mesh
   - crease lines
   - segmented region STLs

This is not the full pavé app yet. This is the foundation that will eventually power automatic tooth detection.

---

## Install

Open PowerShell in this folder:

```powershell
py -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Run

```powershell
python run_segmentation.py "C:\path\to\your_model.stl" outputs
```

Example:

```powershell
python run_segmentation.py examples/test.stl outputs
```

---

## Output

The engine creates:

```text
outputs/
├── cleaned_mesh.stl
├── crease_lines.obj
├── regions/
│   ├── region_001.stl
│   ├── region_002.stl
│   └── ...
└── report.json
```

Open the output STLs in Nomad, Blender, Meshmixer, or your slicer to inspect the segmentation.

---

## Tuning

Use CLI options:

```powershell
python run_segmentation.py input.stl outputs --crease-angle 35 --min-faces 100
```

- Increase `--crease-angle` if the engine detects too many creases.
- Decrease `--crease-angle` if it misses tooth grooves.
- Increase `--min-faces` to remove tiny fragments.
