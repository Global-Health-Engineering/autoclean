"""
Similarity: Compute similarity matrix between string values 

Returns a similarity matrix (n x n) for n unique values, where cell [i,j] = similarity between value i and j.
Values range from 0 (different) to 1 (identical).

Available methods:
    - rapidfuzz_similarity: Character-based (typos, case, spacing, word order differences)
    - embedding_similarity: Embedding-based (abbreviations, synonyms, semantic variations)
    - llm_similarity: LLM-based (complex equivalences beyond embeddings)

For further information, see look at Structural_errors.md in the folder Additional_Information
"""

# Imported libraries
import numpy as np
from rapidfuzz import fuzz
from openai import OpenAI
from pydantic import BaseModel, Field
from itertools import combinations
import json

# =============================================================================
# Pydantic Schema for Method 3 
# =============================================================================

class SimilarityScore(BaseModel):
    """Single pair score"""
    index: int = Field(ge = 0, description = "Index of the pair in given list") 
    similarity: float = Field(ge = 0.0, le = 1.0, description = "Similarity score between the two values")

class SimilarityResponse(BaseModel):
    """Structured output for LLM similarity scoring"""
    scores: list[SimilarityScore] = Field(description = "Scores for all pairs in input list")

# =============================================================================
# Method 1: RapidFuzz Similarity
# =============================================================================

def rapidfuzz_similarity(values: list) -> np.ndarray:
    """
    From list of values (input) compute similarity matrix using RapidFuzz token_sort_ratio
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

def embedding_similarity(values: list, embedding_model: str, client: OpenAI) -> np.ndarray:
    """
    From list of values (input) compute similarity matrix using OpenAI embeddings and cosine similarity
    
    Parameters:
        - values: List of values to compare
        - embedding_model: "text-embedding-3-small" (best for Everyday language) or "text-embedding-3-large" (best for Specialized/technical vocabulary)
        - client: OpenAI client for API calls
    """
    # Get the embeddings as np array (each row == embeding)
    response = client.embeddings.create(input=[str(v) for v in values], model = embedding_model)
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
                   llm_context: str,
                   llm_mode: str,
                   client: OpenAI) -> np.ndarray:
    """
    From list of values (input) compute similarity matrix using LLM
    
    Parameters:
        - values: List of values to compare
        - llm_context: Description of column, to provide context to LLM
        - llm_mode: Mode for LLM similarity scoring
            'strict': Binary scoring (0 or 1), best for unit standardization
            'fast': Range scoring (0 to 1) with gpt-4.1, faster but less accurate
            'reliable': Range scoring (0 to 1) with gpt-5-mini, slower but more accurate
        - client: OpenAI client for API calls
    """
    # Get the # of unique values
    n_unique_values = len(values)

    # Initialize n x n matrix with diagonal = 1.0 (self-similarity)
    similarity_matrix = np.eye(n_unique_values)

    # Generate all pairs (upper triangle only, will mirror later)
    pairs = list(combinations(range(n_unique_values), 2))
    # Note: combinations(range(n), 2) generates all unique pairs (i, j) where i < j
    
    # Get model, model parameters & system prompt for strict mode
    if llm_mode == 'strict': 
        system_prompt = f"""
For each pair (a vs b): Do these two values represent the same quantity?

Similarity scoring:
- 1.0 = Same quantity (different format/unit allowed)
- 0.0 = Different quantity

Convert to base unit if needed, then compare.

Context: {llm_context}

Return similarity score and index as given in input. 
""".strip()

        model = 'gpt-5-mini'
        model_parameters = {'reasoning_effort': 'low', 'seed': 42}

    # Get model, model parameters & system prompt for fast and reliable mode 
    elif llm_mode == 'fast' or llm_mode == 'reliable': 
        system_prompt = f"""
Score similarity for each pair (a vs b).

Scoring:
- 1.0 = Definitely same entity
- 0.8-0.9 = Very likely same
- 0.5-0.7 = Possibly related
- 0.1-0.4 = Weak relation
- 0.0 = Definitely different

Be precise: scoring different entities too high is worse than scoring same entities too low.

Context: {llm_context}

Return similarity score and index as given in input. 
""".strip()
        
        model = 'gpt-4.1' if llm_mode == 'fast' else 'gpt-5-mini'
        model_parameters = {'temperature': 0.0, 'seed': 42} if llm_mode == 'fast' else {'reasoning_effort': 'low', 'seed': 42}

    else:
        raise ValueError(f"Invalid llm_mode: {llm_mode}. Must be 'strict', 'fast', or 'reliable'.")

    # Get right batch size, depending on number of unique values
    batch_size = _get_batch_size(n_unique_values)

    # Process pairs in batches
    for batch_start in range(0, len(pairs), batch_size):
        batch = pairs[batch_start:batch_start + batch_size]
        
        # Build list of pairs for this batch with their indices
        pairs_json = json.dumps([{"index": idx, "a": str(values[i]), "b": str(values[j])} for idx, (i, j) in enumerate(batch)])
        
        # Call OpenAI API for this batch (with structured output)
        response = client.beta.chat.completions.parse(model = model,
                                                      **model_parameters, 
                                                      messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": pairs_json}],
                                                      response_format = SimilarityResponse)

        # Extract scores and fill matrix
        for score_item in response.choices[0].message.parsed.scores:
            i, j = batch[score_item.index]
            
            # Print with aligned formatting
            print(f"{values[i]:30} ↔ {values[j]:30} → {score_item.similarity:.2f}")

            # Fill both [i,j] and [j,i] (symmetric matrix)
            similarity_matrix[i, j] = score_item.similarity
            similarity_matrix[j, i] = score_item.similarity

    return similarity_matrix

# =============================================================================
# Helper Functions (Private)
# =============================================================================

def _get_batch_size(n_unique_values: int) -> int:
    """
    Get batch size depending on number of unique values (n_unique_values)
    """
    if n_unique_values <= 10:
        return 15
    elif n_unique_values <= 30:
        return 20
    elif n_unique_values <= 75:
        return 30
    elif n_unique_values <= 100:
        return 40
    else:
        return 50