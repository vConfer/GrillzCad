from engine.crease_detection import detect_crease_edges, crease_edge_keys
from engine.segmentation import segment_faces
from engine.tooth import Tooth


def detect_teeth(mesh, crease_angle=12.0, min_faces=1000, keep_largest=None):
    creases = detect_crease_edges(mesh, angle_threshold_degrees=crease_angle)

    regions = segment_faces(
        mesh,
        blocked_edges=crease_edge_keys(creases),
        min_faces=min_faces,
    )

    if keep_largest is not None:
        regions = regions[:keep_largest]

    teeth = [
        Tooth.from_region(mesh, tooth_id=i + 1, face_indices=region)
        for i, region in enumerate(regions)
    ]

    return teeth, creases