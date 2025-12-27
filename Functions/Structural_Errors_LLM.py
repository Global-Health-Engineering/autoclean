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
                                  context: str = None) -> tuple:
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
        (df, report): Cleaned DataFrame and report dict
    """
    
    # Terminal output: start
    print("Correcting structural errors (LLM)... ", end="", flush=True)
    
    # Initialize report
    report = {
        'column': column,
        'preference': preference,
        'damping': damping,
        'context': context,
        'clusters': []
    }
    
    # Load API key from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found")
        return df, report
    
    # Check if column exists
    if column not in df.columns:
        print(f"ERROR: Column '{column}' not found")
        return df, report
    
    # Get unique values from column (excluding NaN)
    unique_values = df[column].dropna().unique().tolist()
    n_unique = len(unique_values)
    
    # Check if clustering is needed
    if n_unique <= 1:
        print("✓")
        return df, report
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    # Step 1: Convert strings to embeddings
    embeddings = _get_embeddings(unique_values, client)
    
    # Step 2: Cluster with Affinity Propagation using cosine similarity
    cluster_labels, auto_preference = _cluster_affinity_propagation(embeddings, preference, damping)
    
    # Update report with auto preference if it was calculated
    if preference is None:
        report['preference'] = auto_preference
    
    # Group values by cluster
    cluster_groups = _group_by_cluster(unique_values, cluster_labels)
    
    # Step 3: LLM proposes canonical names for each cluster
    instructor_client = instructor.from_openai(client)
    mapping, cluster_info = _get_canonical_mapping(cluster_groups, instructor_client, context)
    
    # Update report with cluster info
    report['clusters'] = cluster_info
    
    # Step 4: Apply mapping to dataframe
    if len(mapping) > 0:
        df[column] = df[column].replace(mapping)
    
    # Terminal output: end
    print("✓")
    
    return df, report


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
    
    return embeddings_array


def _cluster_affinity_propagation(embeddings: np.ndarray, 
                                   preference: float,
                                   damping: float) -> tuple:
    """
    Cluster embeddings using Affinity Propagation with COSINE SIMILARITY.
    
    Returns:
        (cluster_labels, auto_preference): Labels and the preference used
    """
    
    # Compute cosine similarity matrix
    similarity_matrix = cosine_similarity(embeddings)
    # Note: similarity_matrix[i][j] = cosine similarity between embedding i and j
    #       Values range from ~0 (different) to 1 (identical)
    
    # Get upper triangle (excluding diagonal) for stats
    upper_tri = similarity_matrix[np.triu_indices(len(similarity_matrix), k=1)]
    
    # If preference not set, use a value that encourages meaningful clusters
    auto_preference = None
    if preference is None:
        # Use a value below the median similarity - this tends to create reasonable clusters
        auto_preference = np.median(upper_tri) - 0.1
        preference = auto_preference
    
    # Run Affinity Propagation with precomputed similarity matrix
    ap = AffinityPropagation(
        preference=preference,
        damping=damping,
        affinity='precomputed',  # KEY: Use our cosine similarity matrix
        random_state=42,
        max_iter=500
    )
    cluster_labels = ap.fit_predict(similarity_matrix)
    
    return cluster_labels, auto_preference if auto_preference else preference


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
                            context: str = None) -> tuple:
    """
    Use LLM to propose canonical name for each cluster.
    
    Returns:
        (mapping, cluster_info):
            - mapping: {original_value: canonical_value} for values that need replacing
            - cluster_info: list of dicts for report
    """
    
    mapping = {}
    cluster_info = []
    
    for cluster_id, values in cluster_groups.items():
        if len(values) == 1:
            # Single value cluster - no need for LLM
            continue
        
        # Ask LLM to choose canonical name
        canonical = _llm_choose_canonical(values, client, context)
        
        # Add to cluster info for report
        cluster_info.append({
            'values': values,
            'canonical': canonical
        })
        
        # Create mapping for non-canonical values
        for value in values:
            if value != canonical:
                mapping[value] = canonical
    
    return mapping, cluster_info


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
