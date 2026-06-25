# GrillzCAD Engine Architecture

## Goal

Separate geometry from the UI.

The Electron/Three.js frontend should eventually call this engine to process STL files.

## Pipeline

```text
STL
 ↓
mesh_loader.py
 ↓
mesh_cleaner.py
 ↓
adjacency.py
 ↓
crease_detection.py
 ↓
segmentation.py
 ↓
debug_export.py
```

## Future modules

```text
boundary_offset.py
surface_parameterization.py
hex_packing.py
seat_generation.py
boolean_cut.py
```
