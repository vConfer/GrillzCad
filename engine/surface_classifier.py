import numpy as np


def estimate_design_direction(mesh):
    """
    Estimate the main visible/design direction of a grill mesh.
    For now, this uses PCA and chooses the smallest-thickness axis.
    Later we can let the user override this.
    """
    vertices = mesh.vertices
    centered = vertices - vertices.mean(axis=0)

    cov = np.cov(centered.T)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)

    # Smallest variance usually points front/back thickness direction.
    axis = eigenvectors[:, np.argmin(eigenvalues)]
    axis = axis / np.linalg.norm(axis)

    return axis


def classify_surfaces(mesh, design_direction=None, facial_threshold=0.25, edge_threshold=0.15):
    """
    Classify every face of a grill mesh.

    Returns:
        dict[str, list[int]]
    """
    if design_direction is None:
        design_direction = estimate_design_direction(mesh)

    normals = mesh.face_normals
    centers = mesh.triangles_center
    mesh_center = centers.mean(axis=0)

    classes = {
        "facial": [],
        "back": [],
        "edge": [],
        "flat": [],
    }

    for face_index, normal in enumerate(normals):
        center = centers[face_index]

        normal_score = float(np.dot(normal, design_direction))
        position_score = float(np.dot(center - mesh_center, design_direction))

        if normal_score > facial_threshold and position_score > 0:
            classes["facial"].append(face_index)
        elif normal_score < -facial_threshold and position_score < 0:
            classes["back"].append(face_index)
        elif abs(normal_score) < edge_threshold:
            classes["edge"].append(face_index)
        else:
            classes["flat"].append(face_index)

    return classes