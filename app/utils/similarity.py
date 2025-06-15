import numpy as np

def cosine_similarity(vec1, vec2) -> float:
    """
    Compute the cosine similarity between two vectors.

    Args:
        vec1 (List[float] or np.ndarray): First vector.
        vec2 (List[float] or np.ndarray): Second vector.

    Returns:
        float: Cosine similarity score between -1 and 1. Returns 0.0 if either vector is zero.
    """
    vec1 = np.asarray(vec1, dtype=float)
    vec2 = np.asarray(vec2, dtype=float)

    # Compute norms
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    if norm_vec1 == 0 or norm_vec2 == 0:
        # At least one vector is all zeros, cosine similarity undefined
        return 0.0

    dot_product = np.dot(vec1, vec2)
    similarity = dot_product / (norm_vec1 * norm_vec2)

    return similarity