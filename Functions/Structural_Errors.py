"""
Structural Errors Module
========================
Handle inconsistent categorical values through string similarity clustering.

This module addresses common structural errors in categorical data:
- Case variations: "New York", "new york", "NEW YORK"
- Typos: "Boston", "Bosotn", "Bostno"
- Abbreviations: "N.Y.", "NYC", "New York"
- Trailing/leading whitespace: "Chicago  ", " Chicago"

Approach:
---------
1. Calculate pairwise string similarity between all unique values
2. Use hierarchical clustering to group similar values
3. Select canonical (standard) value for each cluster
4. Map all variations to their canonical form

Dependencies:
-------------
- pandas
- numpy
- rapidfuzz (for string similarity)
- scipy (for hierarchical clustering)
"""

import pandas as pd
import numpy as np
from rapidfuzz import fuzz
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
from typing import Optional


def handle_structural_errors(
    df: pd.DataFrame,
    columns: Optional[list] = None,
    similarity_threshold: float = 80.0,
    similarity_method: str = 'ratio',
    canonical_method: str = 'frequency',
    alias_map: Optional[dict] = None,
    exclude_pairs: Optional[dict] = None,
    show_mappings: bool = True
) -> pd.DataFrame:
    """
    Main function to clean structural errors in categorical columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe to clean
        
    columns : list, optional
        List of column names to process. If None, processes all object/string columns.
        
    similarity_threshold : float, default=85.0
        Minimum similarity score (0-100) to consider two values as the same.
        - Higher (e.g., 90): Only very similar strings grouped (strict)
        - Lower (e.g., 70): More variations grouped together (lenient)
        NOTE: Default is 85 to avoid grouping "Active"/"Inactive" (similarity=85.7)
        
    similarity_method : str, default='ratio'
        RapidFuzz method to calculate similarity:
        - 'ratio': Simple Levenshtein ratio (good for typos)
        - 'partial_ratio': Best partial match (good for substrings)
        - 'token_sort_ratio': Ignores word order (good for "New York" vs "York New")
        - 'token_set_ratio': Ignores duplicates and order (most lenient)
        - 'WRatio': Weighted combination (good general-purpose)
        
    canonical_method : str, default='frequency'
        How to select the canonical (standard) value for each cluster:
        - 'frequency': Most frequent value in original data
        - 'longest': Longest string (usually most complete)
        - 'shortest': Shortest string (usually abbreviation - not recommended)
        - 'alphabetical': First alphabetically (deterministic)
        
    alias_map : dict, optional
        Manual mapping for abbreviations and semantic equivalents that string
        similarity cannot detect. Applied BEFORE clustering.
        Format: {column_name: {alias: canonical, ...}, ...}
        Example:
            {
                'city': {'NYC': 'New York', 'N.Y.': 'New York', 'LA': 'Los Angeles'},
                'department': {'HR': 'Human Resources', 'IT': 'Information Technology'}
            }
            
    exclude_pairs : dict, optional
        Values that should NEVER be merged, even if similarity is high.
        Use this for semantically different but textually similar values.
        Format: {column_name: [list of values to keep separate], ...}
        Example:
            {
                'status': ['Active', 'Inactive'],  # These are opposites!
                'result': ['Pass', 'Fail']
            }
        
    show_mappings : bool, default=True
        If True, print the mappings applied to each column
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with standardized categorical values
        
    Example:
    --------
    >>> alias_map = {
    ...     'city': {'NYC': 'New York', 'N.Y.': 'New York'},
    ...     'department': {'HR': 'Human Resources', 'IT': 'Information Technology'}
    ... }
    >>> df = handle_structural_errors(
    ...     df, 
    ...     columns=['city', 'department'],
    ...     similarity_threshold=85.0,
    ...     alias_map=alias_map
    ... )
    """
    # Create a copy to avoid modifying original
    df_cleaned = df.copy()
    
    # If no columns specified, use all object/string columns
    if columns is None:
        columns = df_cleaned.select_dtypes(include=['object', 'string']).columns.tolist()
    
    print(f"\n{'='*60}")
    print(f"STRUCTURAL ERRORS CLEANING")
    print(f"{'='*60}")
    print(f"Columns to process: {columns}")
    print(f"Similarity threshold: {similarity_threshold}")
    print(f"Similarity method: {similarity_method}")
    print(f"Canonical selection: {canonical_method}")
    if alias_map:
        print(f"Alias maps provided for: {list(alias_map.keys())}")
    if exclude_pairs:
        print(f"Exclude pairs provided for: {list(exclude_pairs.keys())}")
    print(f"{'='*60}\n")
    
    # Process each column
    for col in columns:
        if col not in df_cleaned.columns:
            print(f"  Warning: Column '{col}' not found in DataFrame. Skipping.")
            continue
            
        print(f"\nProcessing column: '{col}'")
        print(f"-" * 40)
        
        # Step 1: Apply alias map FIRST (for abbreviations/semantic equivalents)
        if alias_map and col in alias_map:
            col_aliases = alias_map[col]
            print(f"  Applying {len(col_aliases)} manual aliases...")
            
            # Create case-insensitive mapping
            alias_applied = {}
            for original_val in df_cleaned[col].dropna().unique():
                # Check if this value matches any alias (case-insensitive)
                original_lower = str(original_val).lower().strip()
                for alias, canonical in col_aliases.items():
                    if original_lower == alias.lower().strip():
                        alias_applied[original_val] = canonical
                        break
            
            if alias_applied:
                df_cleaned[col] = df_cleaned[col].map(lambda x: alias_applied.get(x, x))
                print(f"  Aliases applied:")
                for orig, canon in alias_applied.items():
                    print(f"    → \"{canon}\" ← \"{orig}\"")
            print()
        
        # Step 2: Apply clustering for remaining variations (typos, case differences)
        # Get mapping for this column
        mapping = _cluster_column_values(
            df_cleaned[col],
            similarity_threshold=similarity_threshold,
            similarity_method=similarity_method,
            canonical_method=canonical_method
        )
        
        # Step 3: Handle excluded pairs specially
        # Values in exclude_pairs should only merge with case-variations of themselves
        if exclude_pairs and col in exclude_pairs:
            excluded_values = exclude_pairs[col]
            
            # Build a map: for each excluded value, find its case variations in data
            # and map them to the "canonical" form (the one specified in exclude_pairs)
            exclude_canonical_map = {}
            for excluded_val in excluded_values:
                excluded_lower = excluded_val.lower().strip()
                exclude_canonical_map[excluded_lower] = excluded_val
            
            # Filter the mapping
            filtered_mapping = {}
            for original, canonical in mapping.items():
                orig_lower = str(original).lower().strip()
                canon_lower = str(canonical).lower().strip()
                
                # Check if original matches any excluded value (case-insensitive)
                if orig_lower in exclude_canonical_map:
                    # This original is a variation of an excluded value
                    # It should only map to ITS OWN canonical form
                    filtered_mapping[original] = exclude_canonical_map[orig_lower]
                else:
                    # Not an excluded value - use the cluster-determined mapping
                    # BUT check if canonical is excluded
                    if canon_lower in exclude_canonical_map:
                        # Don't map to an excluded value from a non-excluded original
                        filtered_mapping[original] = original
                    else:
                        filtered_mapping[original] = canonical
            
            mapping = filtered_mapping
            print(f"  (Excluded pairs protected: {excluded_values})")
        
        # Apply mapping if any clusters were found
        if mapping:
            df_cleaned[col] = df_cleaned[col].map(lambda x: mapping.get(x, x))
            
            if show_mappings:
                _print_mapping(mapping)
        else:
            print(f"  No clustering needed - all values are distinct")
    
    print(f"\n{'='*60}")
    print(f"STRUCTURAL ERRORS CLEANING COMPLETE")
    print(f"{'='*60}\n")
    
    return df_cleaned


def _cluster_column_values(
    series: pd.Series,
    similarity_threshold: float,
    similarity_method: str,
    canonical_method: str
) -> dict:
    """
    Cluster similar values in a single column and return mapping to canonical values.
    
    Parameters:
    -----------
    series : pd.Series
        Column data to cluster
        
    similarity_threshold : float
        Minimum similarity (0-100) to group values
        
    similarity_method : str
        RapidFuzz method name
        
    canonical_method : str
        How to pick the canonical value
        
    Returns:
    --------
    dict
        Mapping from original values to canonical values
        Example: {'new york': 'New York', 'NYC': 'New York', ...}
    """
    # Get unique values (excluding NaN)
    unique_values = series.dropna().unique().tolist()
    n_unique = len(unique_values)
    
    print(f"  Unique values: {n_unique}")
    
    # If only 0 or 1 unique values, nothing to cluster
    if n_unique <= 1:
        return {}
    
    # Step 1: Build similarity matrix
    # --------------------------------
    # Create n x n matrix where matrix[i][j] = similarity between value i and value j
    similarity_matrix = _build_similarity_matrix(unique_values, similarity_method)
    
    # Convert similarity (0-100) to distance (100-0) for clustering
    # Clustering algorithms minimize distance, so similar items should have LOW distance
    distance_matrix = 100 - similarity_matrix
    
    # Step 2: Perform hierarchical clustering
    # ----------------------------------------
    # Convert full matrix to condensed form (upper triangle only)
    # Required format for scipy's linkage function
    condensed_distance = squareform(distance_matrix)
    
    # Perform hierarchical clustering using average linkage
    # 'average' = UPGMA: uses average distance between all pairs in clusters
    # Other options: 'single' (minimum), 'complete' (maximum), 'ward' (minimize variance)
    linkage_matrix = linkage(condensed_distance, method='average')
    
    # Step 3: Cut dendrogram at threshold to get clusters
    # ---------------------------------------------------
    # Convert similarity threshold to distance threshold
    distance_threshold = 100 - similarity_threshold
    
    # fcluster assigns each value to a cluster ID based on threshold
    # criterion='distance' means cut where distance exceeds threshold
    cluster_labels = fcluster(linkage_matrix, t=distance_threshold, criterion='distance')
    
    # Step 4: Group values by cluster
    # --------------------------------
    clusters = {}  # {cluster_id: [list of values in cluster]}
    for value, cluster_id in zip(unique_values, cluster_labels):
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(value)
    
    # Count clusters with multiple values (actual groupings found)
    n_clusters_with_groups = sum(1 for vals in clusters.values() if len(vals) > 1)
    print(f"  Clusters found: {len(clusters)} ({n_clusters_with_groups} with multiple values)")
    
    # Step 5: Build mapping from variations to canonical values
    # ---------------------------------------------------------
    mapping = {}
    
    # Get value frequencies for 'frequency' method
    value_counts = series.value_counts()
    
    for cluster_id, cluster_values in clusters.items():
        if len(cluster_values) > 1:
            # Multiple values in cluster - need to pick canonical
            canonical = _select_canonical(cluster_values, value_counts, canonical_method)
            
            # Map all values in cluster to canonical
            for value in cluster_values:
                mapping[value] = canonical
        else:
            # Single value - maps to itself (no change needed, but include for completeness)
            mapping[cluster_values[0]] = cluster_values[0]
    
    return mapping


def _build_similarity_matrix(values: list, method: str) -> np.ndarray:
    """
    Build a symmetric similarity matrix for all pairs of values.
    
    Parameters:
    -----------
    values : list
        List of string values to compare
        
    method : str
        RapidFuzz similarity method
        
    Returns:
    --------
    np.ndarray
        n x n matrix where matrix[i][j] = similarity between values[i] and values[j]
    """
    n = len(values)
    matrix = np.zeros((n, n))
    
    # Get the appropriate similarity function from rapidfuzz
    similarity_func = _get_similarity_function(method)
    
    # Fill matrix (only need to compute upper triangle, then mirror)
    for i in range(n):
        matrix[i][i] = 100  # Perfect similarity with itself
        for j in range(i + 1, n):
            # Normalize strings for comparison: lowercase and strip whitespace
            str_i = str(values[i]).lower().strip()
            str_j = str(values[j]).lower().strip()
            
            # Calculate similarity (0-100 scale)
            similarity = similarity_func(str_i, str_j)
            
            # Fill both positions (symmetric matrix)
            matrix[i][j] = similarity
            matrix[j][i] = similarity
    
    return matrix


def _get_similarity_function(method: str):
    """
    Get the appropriate RapidFuzz similarity function.
    
    Parameters:
    -----------
    method : str
        Name of the similarity method
        
    Returns:
    --------
    function
        RapidFuzz similarity function
    """
    method_map = {
        'ratio': fuzz.ratio,
        'partial_ratio': fuzz.partial_ratio,
        'token_sort_ratio': fuzz.token_sort_ratio,
        'token_set_ratio': fuzz.token_set_ratio,
        'WRatio': fuzz.WRatio
    }
    
    if method not in method_map:
        print(f"  Warning: Unknown method '{method}'. Using 'ratio'.")
        return fuzz.ratio
    
    return method_map[method]


def _select_canonical(
    cluster_values: list,
    value_counts: pd.Series,
    method: str
) -> str:
    """
    Select the canonical (standard) value from a cluster.
    
    Parameters:
    -----------
    cluster_values : list
        All values in the cluster
        
    value_counts : pd.Series
        Frequency of each value in original data
        
    method : str
        Selection method: 'frequency', 'longest', 'shortest', 'alphabetical'
        
    Returns:
    --------
    str
        The selected canonical value
    """
    if method == 'frequency':
        # Pick most frequent value
        # Sort cluster values by their count in original data (descending)
        sorted_by_freq = sorted(
            cluster_values,
            key=lambda x: value_counts.get(x, 0),
            reverse=True
        )
        return sorted_by_freq[0]
    
    elif method == 'longest':
        # Pick longest string (usually most complete/formal)
        return max(cluster_values, key=len)
    
    elif method == 'shortest':
        # Pick shortest string
        return min(cluster_values, key=len)
    
    elif method == 'alphabetical':
        # Pick first alphabetically (deterministic)
        return sorted(cluster_values)[0]
    
    else:
        # Default to frequency
        print(f"  Warning: Unknown canonical method '{method}'. Using 'frequency'.")
        return _select_canonical(cluster_values, value_counts, 'frequency')


def _print_mapping(mapping: dict) -> None:
    """
    Print the mapping in a readable format, grouped by canonical value.
    
    Parameters:
    -----------
    mapping : dict
        Mapping from original to canonical values
    """
    # Group by canonical value to show what maps to what
    canonical_groups = {}
    for original, canonical in mapping.items():
        if original != canonical:  # Only show actual changes
            if canonical not in canonical_groups:
                canonical_groups[canonical] = []
            canonical_groups[canonical].append(original)
    
    if canonical_groups:
        print(f"\n  Mappings applied:")
        for canonical, originals in sorted(canonical_groups.items()):
            originals_str = ', '.join(f'"{o}"' for o in sorted(originals))
            print(f"    → \"{canonical}\" ← [{originals_str}]")
    print()


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def preview_clusters(
    df: pd.DataFrame,
    column: str,
    similarity_threshold: float = 80.0,
    similarity_method: str = 'ratio'
) -> dict:
    """
    Preview what clusters would be formed WITHOUT applying changes.
    Useful for testing different thresholds.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input dataframe
        
    column : str
        Column name to analyze
        
    similarity_threshold : float
        Similarity threshold to test
        
    similarity_method : str
        Similarity method to use
        
    Returns:
    --------
    dict
        Dictionary of cluster_id -> list of values
    """
    series = df[column]
    unique_values = series.dropna().unique().tolist()
    n_unique = len(unique_values)
    
    print(f"\n{'='*60}")
    print(f"CLUSTER PREVIEW: '{column}'")
    print(f"{'='*60}")
    print(f"Unique values: {n_unique}")
    print(f"Threshold: {similarity_threshold}")
    print(f"Method: {similarity_method}")
    print(f"{'='*60}\n")
    
    if n_unique <= 1:
        print("Only 0 or 1 unique values - nothing to cluster")
        return {}
    
    # Build similarity matrix and cluster
    similarity_matrix = _build_similarity_matrix(unique_values, similarity_method)
    distance_matrix = 100 - similarity_matrix
    condensed_distance = squareform(distance_matrix)
    linkage_matrix = linkage(condensed_distance, method='average')
    distance_threshold = 100 - similarity_threshold
    cluster_labels = fcluster(linkage_matrix, t=distance_threshold, criterion='distance')
    
    # Group by cluster
    clusters = {}
    for value, cluster_id in zip(unique_values, cluster_labels):
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(value)
    
    # Print clusters
    print("Clusters found:\n")
    for cluster_id, values in sorted(clusters.items()):
        if len(values) > 1:
            print(f"  Cluster {cluster_id} ({len(values)} values):")
            for v in sorted(values):
                count = (series == v).sum()
                print(f"    - \"{v}\" (count: {count})")
            print()
        else:
            print(f"  Cluster {cluster_id}: \"{values[0]}\" (singleton)")
    
    return clusters


# =============================================================================
# MAIN EXECUTION (for testing)
# =============================================================================

if __name__ == "__main__":
    # Test with sample data
    test_data = {
        'name': ['John', 'Jane', 'Bob', 'Alice', 'John', 'Charlie', 'Diana', 'Eve', 
                 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack', 'Kate', 'Leo', 'Mary', 
                 'Nina', 'Oscar', 'John', 'Paul'],
        'city': ['New York', 'Boston', 'Chicago', 'new york', 'New York', 'boston',
                 '', 'New York', 'Chcago', 'New York  ', 'Bosotn', 'NEW YORK', 
                 'N.Y.', 'NYC', 'Miami', 'Los Angeles', 'Bostno', 'chicago', 
                 'New York', 'Mimai'],
        'department': ['Sales', 'sales', 'SALES', 'Marketing', 'marketing', 'Engineering',
                       'engineering', 'Enginnering', 'Sales', 'HR', 'Human Resources', 
                       'hr', 'Sale', 'Slaes', 'IT', 'Information Technology', 'I.T.',
                       'Mktg', 'Sales', 'Marketing'],
        'status': ['Active', 'active', 'Active', 'Inactive', 'inactive', 'Active',
                   'active', 'Inactive', 'active', 'Active', 'active', 'Inactive',
                   'Active', 'inactive', 'Active', 'active', 'Inactive', 'Active',
                   'active', 'Actve']
    }
    
    df = pd.DataFrame(test_data)
    
    print("\n" + "="*60)
    print("ORIGINAL DATA")
    print("="*60)
    print(f"\nUnique cities: {df['city'].unique().tolist()}")
    print(f"Unique departments: {df['department'].unique().tolist()}")
    print(f"Unique status: {df['status'].unique().tolist()}")
    
    # Preview clusters first
    preview_clusters(df, 'city', similarity_threshold=75)
    
    # Apply cleaning
    df_cleaned = handle_structural_errors(
        df,
        columns=['city', 'department', 'status'],
        similarity_threshold=75.0,
        similarity_method='ratio',
        canonical_method='frequency'
    )
    
    print("\n" + "="*60)
    print("CLEANED DATA")
    print("="*60)
    print(f"\nUnique cities: {df_cleaned['city'].unique().tolist()}")
    print(f"Unique departments: {df_cleaned['department'].unique().tolist()}")
    print(f"Unique status: {df_cleaned['status'].unique().tolist()}")
