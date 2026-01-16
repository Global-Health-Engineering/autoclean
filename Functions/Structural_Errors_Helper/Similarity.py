# Imported libraries
import numpy as np
from rapidfuzz import fuzz
from openai import OpenAI

# Needed to load API Key from .env 
import os
from dotenv import load_dotenv

"""
Similarity: Compute similarity matrix between string values 
Returns a similarity matrix (n x n) for n unique values, where cell [i,j] = similarity between value i and j
Values range from 0 (different) to 1 (identical)

Available methods:
    - rapidfuzz_similarity: Character-based (typos, case, spacing, word order differences)
    - embedding_similarity: Semantic (abbreviations, synonyms, semantic variations)

For further information, see look at Structural_errors.md in the folder Additional_Information
"""

# =============================================================================
# Method 1: RapidFuzz Similarity
# =============================================================================

def rapidfuzz_similarity(values: list) -> np.ndarray:
    """
    From list values compute similarity matrix using RapidFuzz token_sort_ratio
    """
    # Get the # of unique values (values = list of unique values)
    n = len(values)

    # Create n x n zero matrix 
    similarity_matrix = np.zeros((n, n))
    
    # Compute for each pair of values their similarity and add to similarity matrix
    # Note: As similarity matrix is symmetric, only upper triangle needs to be computed (hence range(i,n) instead of range(n) for j) 
    #       & can be mirrored along diagonal to lower triangle  
    for i in range(n):
        for j in range(i, n):
            if i == j:
                similarity_matrix[i, j] = 1.0 # Diagonal is always 1
            else:
                # token_sort_ratio returns score between 0-100, normalize to 0-1 by /100.0
                score = fuzz.token_sort_ratio(str(values[i]).lower(), str(values[j]).lower()) / 100.0 
                # Note: str() is for safety, in case not already string

                similarity_matrix[i, j] = score
                similarity_matrix[j, i] = score  # Mirror the score along diagonal 
    
    return similarity_matrix

# =============================================================================
# Method 2: Embedding Similarity (OpenAI)
# =============================================================================

def embedding_similarity(values: list, model: str) -> np.ndarray:
    """
    From list values compute similarity matrix using OpenAI embeddings and cosine similarity
    
    Available OpenAI model: 
    - "text-embedding-3-small" (best for Everyday language)
    - "text-embedding-3-large" (best for Specialized/technical vocabulary) 
    """
    # Get API key from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    # Raise ValueError if api_key is not found (api_key == None) or if api_key is empty (api_key == "")
    if api_key == None or api_key == "":
        raise ValueError("OPENAI_API_KEY was not found or is empty in .env")
    
    # Create OpenAi client 
    client = OpenAI(api_key = api_key)

    # Get the embeddings as np array (each row == embeding)
    response = client.embeddings.create(input=[str(v) for v in values], model = model)
    # Note: str() is for safety, in case not already string
    embeddings = np.array([item.embedding for item in response.data])
    
    # Compute cosine similarities (which are simply dot products between embeddings, as embeddings are allready normalized)
    similarity_matrix = np.dot(embeddings, embeddings.T)
    
    # Safety checks for floating point errors (set diagonal = 1, clip / limit values to [0,1])
    np.fill_diagonal(similarity_matrix, 1.0)
    similarity_matrix = np.clip(similarity_matrix, 0, 1)
    
    return similarity_matrix