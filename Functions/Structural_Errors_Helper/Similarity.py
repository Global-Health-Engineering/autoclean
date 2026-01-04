# Imported libraries
import numpy as np
from rapidfuzz import fuzz
from openai import OpenAI

"""
Similarity: Compute similarity matrix between string values
Returns a similarity matrix (n x n) where cell [i,j] = similarity between value i and j
Values range from 0 (different) to 1 (identical)

Available methods:
    - rapidfuzz_similarity: Character-based (typos, case, spacing)
    - embedding_similarity: Semantic (abbreviations, synonyms)
"""


# =============================================================================
# Method 1: RapidFuzz Similarity
# =============================================================================

def rapidfuzz_similarity(values: list) -> np.ndarray:
    """
    Compute similarity matrix using RapidFuzz token_sort_ratio.
    
    Parameters:
        values: List of unique string values to compare
    
    Returns:
        np.ndarray: Similarity matrix (n x n) with values 0-1
    """
    n = len(values)
    similarity_matrix = np.zeros((n, n))
    
    # Compare each pair of values
    for i in range(n):
        for j in range(i, n):
            if i == j:
                similarity_matrix[i, j] = 1.0
            else:
                # RapidFuzz returns 0-100, normalize to 0-1
                score = fuzz.token_sort_ratio(str(values[i]), str(values[j])) / 100.0
                similarity_matrix[i, j] = score
                similarity_matrix[j, i] = score  # Matrix is symmetric
    
    return similarity_matrix


# =============================================================================
# Method 2: Embedding Similarity (OpenAI)
# =============================================================================

def embedding_similarity(values: list) -> np.ndarray:
    """
    Compute similarity matrix using OpenAI embeddings and cosine similarity.
    
    Parameters:
        values: List of unique string values to compare
    
    Returns:
        np.ndarray: Similarity matrix (n x n) with values 0-1
    
    Requires:
        OPENAI_API_KEY environment variable
    """
    # Get embeddings from OpenAI
    client = OpenAI()
    response = client.embeddings.create(
        input=[str(v) for v in values],
        model="text-embedding-3-small"
    )
    embeddings = np.array([item.embedding for item in response.data])
    
    # Compute cosine similarity: normalize then dot product
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    normalized = embeddings / norms
    similarity_matrix = np.dot(normalized, normalized.T)
    
    # Clean up: diagonal = 1, clip to [0,1]
    np.fill_diagonal(similarity_matrix, 1.0)
    similarity_matrix = np.clip(similarity_matrix, 0, 1)
    
    return similarity_matrix
