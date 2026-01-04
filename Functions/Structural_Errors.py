# Imported libraries
import pandas as pd

# Import subfunctions
from Structural_Errors_Helper.Similarity import rapidfuzz_similarity, embedding_similarity
from Structural_Errors_Helper.Clustering import hierarchical_clustering, connected_components_clustering
from Structural_Errors_Helper.Canonical import most_frequent, llm_selection

"""
Structural Errors: Fix inconsistent string values in categorical columns
Examples: "New York" vs "new york" vs "NYC", "Hospital" vs "Hosptial"

This function orchestrates the pipeline:
    1. Similarity: Compute how similar each pair of values is
    2. Clustering: Group similar values into clusters
    3. Canonical: Select one value to represent each cluster
    4. Apply: Map all values to their canonical form
"""


# =============================================================================
# Main Function (Public)
# =============================================================================

def fix_structural_errors(
    df: pd.DataFrame,
    column: str,
    similarity: str = "rapidfuzz",
    clustering: str = "hierarchical",
    canonical: str = "most_frequent",
    threshold: float = 0.85
) -> tuple:
    """
    Fix structural errors in a categorical column.
    
    Parameters:
        df: DataFrame to clean
        column: Column name to fix
        similarity: "rapidfuzz" (character-based) or "embeddings" (semantic)
        clustering: "hierarchical" (standard) or "connected_components" (simple)
        canonical: "most_frequent" (simple) or "llm" (intelligent)
        threshold: Minimum similarity to group values (0-1, default: 0.85)
    
    Returns:
        tuple: (df_cleaned, report)
    """
    # Terminal output: start
    print(f"Fixing structural errors ({column})... ", end="", flush=True)
    
    # Make a copy
    df_clean = df.copy()
    
    # Initialize report
    report = {
        'column': column,
        'similarity': similarity,
        'clustering': clustering,
        'canonical': canonical,
        'threshold': threshold,
        'unique_before': df[column].nunique(),
        'unique_after': None,
        'mapping': {},
        'values_changed': 0
    }
    
    # Get unique values (excluding NaN)
    unique_values = df[column].dropna().unique().tolist()
    
    # Edge case: 0 or 1 unique values
    if len(unique_values) <= 1:
        report['unique_after'] = report['unique_before']
        print("✓")
        return df_clean, report
    
    # Get value counts for canonical selection
    value_counts = df[column].value_counts().to_dict()
    
    # =========================================================================
    # Step 1: Compute similarity matrix
    # =========================================================================
    if similarity == "rapidfuzz":
        similarity_matrix = rapidfuzz_similarity(unique_values)
    elif similarity == "embeddings":
        similarity_matrix = embedding_similarity(unique_values)
    else:
        raise ValueError(f"Unknown similarity: {similarity}")
    
    # =========================================================================
    # Step 2: Cluster similar values
    # =========================================================================
    if clustering == "hierarchical":
        labels = hierarchical_clustering(similarity_matrix, threshold)
    elif clustering == "connected_components":
        labels = connected_components_clustering(similarity_matrix, threshold)
    else:
        raise ValueError(f"Unknown clustering: {clustering}")
    
    # =========================================================================
    # Step 3: Build mapping (value → canonical)
    # =========================================================================
    
    # Group values by cluster
    clusters = {}
    for value, label in zip(unique_values, labels):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(value)
    
    # Select canonical name for each cluster
    mapping = {}
    for label, cluster_values in clusters.items():
        if canonical == "most_frequent":
            canonical_name = most_frequent(cluster_values, value_counts)
        elif canonical == "llm":
            canonical_name = llm_selection(cluster_values, column)
        else:
            raise ValueError(f"Unknown canonical: {canonical}")
        
        for value in cluster_values:
            mapping[value] = canonical_name
    
    report['mapping'] = mapping
    
    # =========================================================================
    # Step 4: Apply mapping
    # =========================================================================
    
    # Count values that will change
    for old_val, new_val in mapping.items():
        if old_val != new_val:
            report['values_changed'] += (df_clean[column] == old_val).sum()
    
    # Apply mapping
    df_clean[column] = df_clean[column].map(lambda x: mapping.get(x, x))
    
    # Update report
    report['unique_after'] = df_clean[column].nunique()
    
    # Terminal output: end
    print("✓")
    
    return df_clean, report
