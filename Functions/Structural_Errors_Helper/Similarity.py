# Imported libraries
import numpy as np
from rapidfuzz import fuzz
from openai import OpenAI
from pydantic import BaseModel
from itertools import combinations
import json

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
    - llm_similarity: Reasoning-based (unit conversions, number words, complex abbreviations)

For further information, see look at Structural_errors.md in the folder Additional_Information
"""

# =============================================================================
# Pydantic Schema for Method 3 
# =============================================================================

class SimilarityScore(BaseModel):
    """Single pair score"""
    index: int                  # Index of the pair in the batch
    similarity: float           # Score between 0.0 and 1.0

class SimilarityResponse(BaseModel):
    """Structured output for Phase 2: Pair scores"""
    scores: list[SimilarityScore]

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

# =============================================================================
# Method 3: LLM Similarity (OpenAI)
# =============================================================================

def llm_similarity(values: list,
                   context: str,
                   model: str = "gpt-4o",
                   temperature: float = 0.0,
                   batch_size: int = 50) -> np.ndarray:
    """
    From list values compute similarity matrix using LLM reasoning.
    
    This is one step above embedding similarity - it uses LLM reasoning to understand
    complex equivalences that embeddings miss:
    - Unit conversions: "500L" ↔ "500000ml"
    - Number words: "25" ↔ "twenty-five"  
    - Complex abbreviations: "WHO" ↔ "World Health Organization"
    - Boolean variations: "Yes" ↔ "Y" ↔ "1" ↔ "true"
    
    Parameters:
        values: List of unique string values to compare
        context: Description of the column (e.g., "City names with abbreviations")
        model: OpenAI model to use (default: "gpt-4o")
        temperature: Controls randomness, 0.0 = deterministic (default: 0.0)
        batch_size: Number of pairs per API call (default: 50)
    
    Returns:
        np.ndarray: Similarity matrix of shape (n, n)
    """
    # Get API key from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    # Raise ValueError if api_key is not found or empty
    if not api_key:
        raise ValueError("OPENAI_API_KEY was not found or is empty in .env")
    
    # Create OpenAI client 
    client = OpenAI(api_key=api_key)

    # Get the # of unique values
    n = len(values)

    # Initialize n x n matrix with diagonal = 1.0 (self-similarity)
    similarity_matrix = np.eye(n)

    # Generate all pairs (upper triangle only, will mirror later)
    pairs = list(combinations(range(n), 2))
    # Note: combinations(range(n), 2) generates all unique pairs (i, j) where i < j

    # System prompt - provides context for all batches
    system_prompt = f"""You are a data cleaning expert helping standardize a dataset column.

COLUMN CONTEXT: {context}

YOUR TASK: Score similarity between value pairs. These scores will be used to cluster similar values and replace them with one canonical form.

SCORING GUIDE:
- 1.0 = Definitely the same entity → will be merged
- 0.8-0.9 = Very likely same (typo, abbreviation, format variation)
- 0.5-0.7 = Possibly related, uncertain
- 0.1-0.4 = Weak relation, probably different
- 0.0 = Definitely different → will NOT be merged

Consider: typos, case differences, abbreviations, synonyms, unit conversions, number words.

IMPORTANT: Be precise. False merges (scoring different entities high) are worse than missed merges (scoring same entities low)."""

    # Process pairs in batches
    for batch_start in range(0, len(pairs), batch_size):
        batch = pairs[batch_start:batch_start + batch_size]
        
        # Build list of pairs for this batch with their indices
        pairs_json = json.dumps([
            {"index": idx, "a": str(values[i]), "b": str(values[j])}
            for idx, (i, j) in enumerate(batch)
        ])
        
        # Call OpenAI API for this batch (with structured output)
        response = client.beta.chat.completions.parse(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": pairs_json}
            ],
            response_format=SimilarityResponse
        )
        
        # Extract scores and fill matrix
        for score_item in response.choices[0].message.parsed.scores:
            i, j = batch[score_item.index]
            similarity = max(0.0, min(1.0, score_item.similarity))  # Clip to [0, 1]
            
            # Fill both [i,j] and [j,i] (symmetric matrix)
            similarity_matrix[i, j] = similarity
            similarity_matrix[j, i] = similarity
    
    return similarity_matrix