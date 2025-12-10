# Imported libraries
import pandas as pd
import numpy as np
from rapidfuzz import fuzz
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

"""
Handle structural errors in categorical columns (Simple Method)

Groups similar categorical values (case variations, typos, misspellings) and 
replaces them with a canonical (standard) form using string similarity clustering.

Method: RapidFuzz string similarity + Hierarchical Clustering

Parameters:
    - column: Name of categorical column to clean
    - threshold: Distance threshold for clustering (0-100)
        - 10-15: Very strict (only near-identical strings)
        - 20-30: Moderate (catches typos and case variations) [default: 20]
        - 40-50: Loose (catches more distant variations)
    - method: Linkage method for hierarchical clustering ('average', 'complete', 'single')

Example:
    Input:  ["Hospital", "hospital", "HOSPITAL", "Clinic", "clinic"]
    Output: ["Hospital", "Hospital", "Hospital", "Clinic", "Clinic"]

Note: This method works well for case variations and typos, but cannot understand 
      semantic meaning (e.g., "NYC" will NOT be grouped with "New York").
      For semantic understanding, use Structural_Errors_LLM.py
"""

# ============================================================================
# Main Function (Public)
# ============================================================================

def handle_structural_errors_simple(df: pd.DataFrame, 
                                     column: str, 
                                     threshold: float = 20.0,
                                     method: str = 'average') -> pd.DataFrame:
    """
    Cluster similar categorical values and replace with canonical form.
    """
    
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
    
    print(f"Clustering column '{column}' with {n_unique} unique values (threshold={threshold})")
    
    # Step 1: Create distance matrix using RapidFuzz string similarity
    distance_matrix = _create_distance_matrix(unique_values)
    
    # Step 2: Perform hierarchical clustering
    clusters = _hierarchical_clustering(distance_matrix, threshold, method)
    
    # Step 3: Create mapping from each value to its canonical form
    mapping = _create_canonical_mapping(unique_values, clusters)
    
    # Step 4: Apply mapping to dataframe
    if len(mapping) > 0:
        df[column] = df[column].replace(mapping)
        print(f"Replaced {len(mapping)} values with canonical forms")
    else:
        print(f"No similar values found to cluster")
    
    return df


# ============================================================================
# Helper Functions (Private)
# ============================================================================

def _create_distance_matrix(values: list) -> np.ndarray:
    """
    Create a distance matrix using RapidFuzz string similarity.
    
    RapidFuzz ratio returns similarity (0-100), we convert to distance (100 - similarity).
    Comparison is case-insensitive.
    """
    
    n = len(values)
    distance_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i + 1, n):
            # Calculate string similarity (0-100), case-insensitive
            similarity = fuzz.ratio(values[i].lower(), values[j].lower())
            # Note: fuzz.ratio compares two strings and returns similarity score 0-100
            #       100 = identical, 0 = completely different
            
            # Convert similarity to distance (0 = identical, 100 = completely different)
            distance = 100 - similarity
            
            # Fill both sides of matrix (symmetric)
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance
    
    return distance_matrix


def _hierarchical_clustering(distance_matrix: np.ndarray, 
                              threshold: float, 
                              method: str) -> np.ndarray:
    """
    Perform hierarchical clustering on the distance matrix.
    
    Returns array of cluster labels (1-indexed).
    """
    
    # Convert square distance matrix to condensed form (required by scipy linkage)
    condensed_dist = squareform(distance_matrix)
    # Note: squareform converts NxN matrix to 1D array of upper triangle values
    #       This is the format scipy.cluster.hierarchy.linkage expects
    
    # Perform hierarchical clustering
    linkage_matrix = linkage(condensed_dist, method=method)
    # Note: linkage builds the hierarchical cluster tree
    #       method='average' uses average distance between clusters (UPGMA)
    
    # Cut tree at threshold to get flat cluster assignments
    clusters = fcluster(linkage_matrix, t=threshold, criterion='distance')
    # Note: fcluster cuts the dendrogram at height 'threshold'
    #       Returns array where clusters[i] is the cluster ID for values[i]
    
    return clusters


def _create_canonical_mapping(values: list, clusters: np.ndarray) -> dict:
    """
    Create mapping from each value to its canonical (standard) form.
    
    The canonical form is chosen as the most "standard looking" value:
    1. Prefer Title Case versions
    2. If tied, prefer longer (more complete) version
    3. If still tied, use alphabetical order
    """
    
    # Group values by cluster ID
    cluster_groups = {}
    for value, cluster_id in zip(values, clusters):
        if cluster_id not in cluster_groups:
            cluster_groups[cluster_id] = []
        cluster_groups[cluster_id].append(value)
    
    # Create mapping for clusters with multiple values
    mapping = {}
    n_clusters_with_variations = 0
    
    for cluster_id, group in cluster_groups.items():
        if len(group) > 1:
            # This cluster has variations that need to be unified
            n_clusters_with_variations += 1
            
            # Choose the canonical (standard) form
            canonical = _choose_canonical(group)
            
            print(f"  Cluster: {group} → '{canonical}'")
            
            # Map all non-canonical values to the canonical form
            for value in group:
                if value != canonical:
                    mapping[value] = canonical
    
    print(f"Found {n_clusters_with_variations} clusters with variations")
    
    return mapping


def _choose_canonical(values: list) -> str:
    """
    Choose the canonical (standard) form from a list of similar values.
    
    Strategy:
    1. Prefer Title Case versions (e.g., "Hospital" over "hospital")
    2. If multiple title case, prefer longer (more complete) version
    3. If still tied, use alphabetical order for consistency
    """
    
    scored_values = []
    
    for v in values:
        score = 0
        
        # Prefer Title Case (first letter uppercase, rest lowercase per word)
        if v == v.title():
            score += 100
        # Also give some points for first letter uppercase
        elif len(v) > 0 and v[0].isupper():
            score += 50
            
        # Prefer longer strings (more complete/descriptive)
        score += len(v)
        
        scored_values.append((score, v))
    
    # Sort by score (descending), then alphabetically for consistency
    scored_values.sort(key=lambda x: (-x[0], x[1]))
    
    return scored_values[0][1]


# ============================================================================
# Utility Function: Preview Clusters (Public)
# ============================================================================

def preview_clusters(df: pd.DataFrame, 
                     column: str, 
                     threshold: float = 20.0,
                     method: str = 'average') -> dict:
    """
    Preview what clusters would be formed WITHOUT modifying the dataframe.
    Useful for exploring different threshold values before applying.
    
    Returns:
        Dictionary with cluster_id as key and list of values as value
    """
    
    # Check if column exists
    if column not in df.columns:
        print(f"Column '{column}' not found in dataframe")
        return {}
    
    unique_values = df[column].dropna().unique().tolist()
    n_unique = len(unique_values)
    
    if n_unique <= 1:
        print(f"Column '{column}' has {n_unique} unique value(s)")
        return {}
    
    # Create distance matrix and cluster
    distance_matrix = _create_distance_matrix(unique_values)
    clusters = _hierarchical_clustering(distance_matrix, threshold, method)
    
    # Group by cluster
    cluster_groups = {}
    for value, cluster_id in zip(unique_values, clusters):
        if cluster_id not in cluster_groups:
            cluster_groups[cluster_id] = []
        cluster_groups[cluster_id].append(value)
    
    # Print results
    print(f"\nColumn '{column}' - Threshold {threshold}:")
    print("-" * 50)
    
    n_with_variations = 0
    for cluster_id, group in sorted(cluster_groups.items()):
        if len(group) > 1:
            n_with_variations += 1
            canonical = _choose_canonical(group)
            print(f"  Cluster {cluster_id}: {group} → '{canonical}'")
        else:
            print(f"  Cluster {cluster_id}: '{group[0]}' (no variations)")
    
    print(f"\nTotal: {len(cluster_groups)} clusters, {n_with_variations} with variations")
    
    return cluster_groups
