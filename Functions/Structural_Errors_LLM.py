# Imported libraries
import pandas as pd
import numpy as np
from sklearn.cluster import AffinityPropagation
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from pydantic import BaseModel
import instructor
from openai import OpenAI
import os

"""
Handle structural errors in categorical columns (LLM-Powered Method)

Groups similar categorical values using semantic understanding and replaces 
them with a canonical (standard) form.

Method: OpenAI Embeddings + Affinity Propagation (with cosine similarity) + LLM Canonical Name Selection

Pipeline:
    Step 1: Convert strings → embeddings (numerical vectors capturing meaning)
    Step 2: Cluster embeddings with Affinity Propagation using cosine similarity
    Step 3: LLM proposes canonical name for each cluster
    Step 4: Output structured mapping with Pydantic

Parameters:
    - column: Name of categorical column to clean
    - preference: Affinity Propagation preference parameter
                  Lower values = fewer clusters, higher = more clusters
                  For cosine similarity (0 to 1): typical range is -0.5 to 0.5
    - damping: Damping factor for AP (default: 0.9, range: 0.5-1.0)

Example:
    Input:  ["New York", "new york", "NYC", "NY", "Boston", "boston"]
    Output: ["New York", "New York", "New York", "New York", "Boston", "Boston"]

Note: This method understands semantic meaning (e.g., "NYC" = "New York").
      For simple case/typo corrections without API, use Structural_Errors_Simple.py
"""

# ============================================================================
# Pydantic Models for Structured LLM Output
# ============================================================================

class CanonicalName(BaseModel):
    """LLM's choice for canonical name of a cluster."""
    canonical: str
    reasoning: str


# ============================================================================
# Main Function (Public)
# ============================================================================

def handle_structural_errors_llm(df: pd.DataFrame, 
                                  column: str,
                                  preference: float = None,
                                  damping: float = 0.9,
                                  context: str = None) -> pd.DataFrame:
    """
    Cluster similar categorical values using embeddings + Affinity Propagation,
    then use LLM to propose canonical names.
    
    Parameters:
        df: DataFrame to clean
        column: Name of categorical column to cluster
        preference: AP preference parameter (None = auto based on similarity median)
                    For cosine similarity: range is roughly -0.5 to 0.5
                    Lower = fewer clusters, Higher = more clusters
        damping: AP damping factor (0.5-1.0, higher = more stable)
        context: Optional context for LLM (e.g., "These are WASH facility types")
    
    Returns:
        DataFrame with clustered values replaced by canonical form
    """
    
    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file")
        return df
    
    # Check if column exists
    if column not in df.columns:
        print(f"Column '{column}' not found in dataframe")
        return df
    
    # Get unique values from column (excluding NaN)
    unique_values = df[column].dropna().unique().tolist()
    n_unique = len(unique_values)
    
    # Check if clustering is needed
    if n_unique <= 1:
        print(f"Column '{column}' has {n_unique} unique value(s) - no clustering needed")
        return df
    
    print(f"Clustering column '{column}' with {n_unique} unique values using LLM")
    print("-" * 60)
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Step 1: Convert strings to embeddings
    print("Step 1: Generating embeddings...")
    embeddings = _get_embeddings(unique_values, client)
    
    # Step 2: Cluster with Affinity Propagation using cosine similarity
    print("Step 2: Clustering with Affinity Propagation (cosine similarity)...")
    cluster_labels = _cluster_affinity_propagation(embeddings, preference, damping)
    
    # Group values by cluster
    cluster_groups = _group_by_cluster(unique_values, cluster_labels)
    n_clusters = len(cluster_groups)
    n_multi = sum(1 for v in cluster_groups.values() if len(v) > 1)
    print(f"       Found {n_clusters} clusters ({n_multi} with multiple values)")
    
    # Step 3: LLM proposes canonical names for each cluster
    print("Step 3: LLM selecting canonical names...")
    instructor_client = instructor.from_openai(client)
    mapping = _get_canonical_mapping(cluster_groups, instructor_client, context)
    
    # Step 4: Apply mapping to dataframe
    print("-" * 60)
    if len(mapping) > 0:
        df[column] = df[column].replace(mapping)
        print(f"Replaced {len(mapping)} values with canonical forms")
    else:
        print(f"No values needed replacement")
    
    return df


# ============================================================================
# Helper Functions (Private)
# ============================================================================

def _get_embeddings(values: list, client: OpenAI) -> np.ndarray:
    """
    Convert strings to embeddings using OpenAI's embedding API.
    
    Uses 'text-embedding-3-small' model - fast and cost-effective.
    """
    
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=values
    )
    # Note: OpenAI returns embeddings in the same order as input
    
    # Extract embedding vectors from response
    embeddings = [item.embedding for item in response.data]
    
    # Convert to numpy array
    embeddings_array = np.array(embeddings)
    
    print(f"       Generated {len(embeddings)} embeddings (dimension: {len(embeddings[0])})")
    
    return embeddings_array


def _cluster_affinity_propagation(embeddings: np.ndarray, 
                                   preference: float,
                                   damping: float) -> np.ndarray:
    """
    Cluster embeddings using Affinity Propagation with COSINE SIMILARITY.
    
    Key insight: Text embeddings work much better with cosine similarity
    than Euclidean distance. Cosine similarity measures the angle between
    vectors, which captures semantic similarity better.
    
    Cosine similarity ranges from 0 (different) to 1 (identical).
    """
    
    # Compute cosine similarity matrix
    # This is the KEY FIX - using cosine similarity instead of Euclidean distance
    similarity_matrix = cosine_similarity(embeddings)
    # Note: similarity_matrix[i][j] = cosine similarity between embedding i and j
    #       Values range from ~0 (different) to 1 (identical)
    
    # Print some similarity stats for debugging
    # Get upper triangle (excluding diagonal)
    upper_tri = similarity_matrix[np.triu_indices(len(similarity_matrix), k=1)]
    print(f"       Similarity stats: min={upper_tri.min():.3f}, max={upper_tri.max():.3f}, mean={upper_tri.mean():.3f}")
    
    # If preference not set, use a value that encourages meaningful clusters
    if preference is None:
        # Use a value below the median similarity - this tends to create reasonable clusters
        preference = np.median(upper_tri) - 0.1
        print(f"       Auto preference: {preference:.3f}")
    
    # Run Affinity Propagation with precomputed similarity matrix
    ap = AffinityPropagation(
        preference=preference,
        damping=damping,
        affinity='precomputed',  # KEY: Use our cosine similarity matrix
        random_state=42,
        max_iter=500
    )
    cluster_labels = ap.fit_predict(similarity_matrix)
    
    n_clusters = len(set(cluster_labels))
    print(f"       Affinity Propagation found {n_clusters} clusters")
    
    return cluster_labels


def _group_by_cluster(values: list, cluster_labels: np.ndarray) -> dict:
    """
    Group values by their cluster label.
    
    Returns:
        Dictionary: {cluster_id: [list of values in that cluster]}
    """
    
    cluster_groups = {}
    
    for value, cluster_id in zip(values, cluster_labels):
        if cluster_id not in cluster_groups:
            cluster_groups[cluster_id] = []
        cluster_groups[cluster_id].append(value)
    
    return cluster_groups


def _get_canonical_mapping(cluster_groups: dict, 
                            client: instructor.Instructor,
                            context: str = None) -> dict:
    """
    Use LLM to propose canonical name for each cluster.
    
    Returns:
        Dictionary: {original_value: canonical_value} for values that need replacing
    """
    
    mapping = {}
    
    for cluster_id, values in cluster_groups.items():
        if len(values) == 1:
            # Single value cluster - no need for LLM
            print(f"  Cluster {cluster_id}: '{values[0]}' (single value)")
            continue
        
        # Ask LLM to choose canonical name
        canonical = _llm_choose_canonical(values, client, context)
        
        print(f"  Cluster {cluster_id}: {values} → '{canonical}'")
        
        # Create mapping for non-canonical values
        for value in values:
            if value != canonical:
                mapping[value] = canonical
    
    return mapping


def _llm_choose_canonical(values: list, 
                           client: instructor.Instructor,
                           context: str = None) -> str:
    """
    Ask LLM to choose the canonical (standard) form from a list of similar values.
    """
    
    context_str = f"\nContext: {context}" if context else ""
    
    prompt = f"""These values all refer to the same thing. Choose the most appropriate canonical (standard) form.
{context_str}

Values: {values}

Choose the canonical form that is:
1. Most complete and descriptive (prefer "New York" over "NYC")
2. Properly capitalized
3. Most commonly accepted/official spelling

IMPORTANT: Choose ONE canonical form. If the values include a full name and abbreviations, prefer the full name."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_model=CanonicalName
    )
    
    return response.canonical


# ============================================================================
# Utility Function: Preview Clusters (Public)
# ============================================================================

def preview_clusters_llm(df: pd.DataFrame, 
                          column: str,
                          preference: float = None,
                          damping: float = 0.9) -> dict:
    """
    Preview what clusters would be formed WITHOUT modifying the dataframe.
    Shows embeddings + AP clustering results before LLM canonical selection.
    
    Useful for exploring different preference values.
    """
    
    # Load API key
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("Error: OPENAI_API_KEY not found in .env file")
        return {}
    
    if column not in df.columns:
        print(f"Column '{column}' not found in dataframe")
        return {}
    
    unique_values = df[column].dropna().unique().tolist()
    
    if len(unique_values) <= 1:
        print(f"Column '{column}' has {len(unique_values)} unique value(s)")
        return {}
    
    print(f"Previewing LLM clusters for column '{column}'")
    print("-" * 60)
    
    # Get embeddings and cluster
    client = OpenAI(api_key=api_key)
    embeddings = _get_embeddings(unique_values, client)
    cluster_labels = _cluster_affinity_propagation(embeddings, preference, damping)
    cluster_groups = _group_by_cluster(unique_values, cluster_labels)
    
    # Print results
    print("-" * 60)
    print("Clusters (before LLM canonical selection):")
    for cluster_id, values in sorted(cluster_groups.items()):
        if len(values) > 1:
            print(f"  Cluster {cluster_id}: {values}")
        else:
            print(f"  Cluster {cluster_id}: '{values[0]}' (single)")
    
    return cluster_groups