# Imported libraries
import pandas as pd

# Import subfunctions
from Functions.Structural_Errors_Helper.Similarity import rapidfuzz_similarity, embedding_similarity
from Functions.Structural_Errors_Helper.Clustering import hierarchical_clustering, connected_components_clustering, affinity_propagation_clustering
from Functions.Structural_Errors_Helper.Canonical import most_frequent, llm_selection

"""
Structural Errors: Orchestrates all the subfunctions to handle structural errors. 

Pipeline: 
    Step 1: Compute Similarity Matrix 
    Step 2: Cluster similar values
    Step 3: Build mapping (value → canonical) by choosing canonical form 
    Step 4: Apply mapping

Parameters: 
    df: DataFrame to clean
    column: Name of column for which handle_structural_errors needs to be applied 
    similarity: "embeddings" or "rapidfuzz" (default)
    clustering: "connected_components", "affinity_propagation", "hierarchical" (default)
    canonical: "llm" or "most_frequent" (default)
    threshold_cc:  Threshold for connected components clustering (default = 0.85)
    threshold_h: Threshold for hierarchical clustering (default = 0.85)
    embedding_model: "text-embedding-3-large" or "text-embedding-3-small" (default)

Returns: 
    Cleaned dataframe and report (as tuple)

For further information, see look at Structural_errors.md in the folder Additional_Information
"""

# =============================================================================
# Main Function (Public)
# =============================================================================

def handle_structural_errors(df: pd.DataFrame,
                             column: str,
                             similarity: str = "rapidfuzz",
                             clustering: str = "hierarchical",
                             canonical: str = "most_frequent",
                             threshold_cc: float = 0.85,
                             threshold_h: float = 0.85, 
                             embedding_model: str = "text-embedding-3-small") -> tuple:
    # Terminal output: start
    print(f"Fixing structural errors ({column})... ", end = "", flush = True)
    # Note: With flush = True, print is immediately

    # Work with copy, to not modify input df 
    df_work = df.copy()
    
    # Initialize report
    report = {'column': column,
              'similarity': similarity,
              'clustering': clustering,
              'canonical': canonical,
              'threshold_cc': threshold_cc,
              'threshold_h': threshold_h,
              'embedding_model': embedding_model,
              'unique_values_before': df[column].nunique(), # .nunique() returns number of unique values (excluding missing values)
              'unique_values_after': None,
              'mapping': {},
              'values_changed': 0,
              'value_counts': {}}
    
    # Get unique values (excluding missing values)
    unique_values = list(df[column].dropna().unique())
    # Note: .dropna() removes missing values
    #       .unique() returns unique values as np array
    #       list() converts np array to list
    
    # Edge case: 1 unique values
    if len(unique_values) == 1:
        report['unique_values_after'] = report['unique_values_before']
        print("✓")
        return df_work, report
    
    # Get dictionary, where each unique value is a key and its value is the # it appears in the df[column] 
    value_counts = dict(df[column].value_counts())
    # Note: .value_counts() returns a pd series with index = unique values & data = count of the unique values
    #       dict() converts pd series to dict, where index -> key, data -> value

    # Update report
    report['value_counts'] = value_counts
    # =========================================================================
    # Step 1: Compute similarity matrix
    # =========================================================================
    
    if similarity == "rapidfuzz":
        similarity_matrix = rapidfuzz_similarity(unique_values)
    elif similarity == "embeddings":
        similarity_matrix = embedding_similarity(unique_values, embedding_model)
    else:
        raise ValueError(f"Unknown similarity: {similarity}")
    
    # =========================================================================
    # Step 2: Cluster similar values
    # =========================================================================
    
    if clustering == "hierarchical":
        labels = hierarchical_clustering(similarity_matrix, threshold_h)
    elif clustering == "connected_components":
        labels = connected_components_clustering(similarity_matrix, threshold_cc)
    elif clustering == "affinity_propagation":
        labels = affinity_propagation_clustering(similarity_matrix)
    else:
        raise ValueError(f"Unknown clustering: {clustering}")
    
    # =========================================================================
    # Step 3: Build mapping (value → canonical) by choosing canonical form 
    # =========================================================================
    
    # Create dictionary which stores all clusters
    # For each cluster: key = label, value = list of all unique values assigend to cluster 
    clusters = {}
    for value, label in zip(unique_values, labels):
        # If key (label) is not yet in dict clusters, add it
        if label not in clusters:
            clusters[label] = []

        # Add the unique_value to the label in the dict clusters
        clusters[label].append(value)
    
    # Create dictionary for mapping
    mapping = {}

    # Select canonical name for each cluster & fill dict mapping
    # Note: In dict mapping, each unique value is a key and the corresponding value is the matching canonical name
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
    # Note: In the dict report the value of the key 'mapping' is again a dictionary 

    # =========================================================================
    # Step 4: Apply mapping
    # =========================================================================
    
    # Count how many values in the column of df will change
    for old_val, new_val in mapping.items():
        if old_val != new_val:
            report['values_changed'] += (df_work[column] == old_val).sum()
            # Note: (df_work[column] == old_val) returns a boolean pd.series, with True if cell in df_work[column] == old_val else false 
            #       .sum() gets number of all cell marked True 
    
    # Apply mapping
    df_work[column] = df_work[column].map(lambda x: mapping.get(x, x))
    # Note: dict.get(x,x) search for key x in dict and returns its value if found otherwise 0
    #       .map(lambda...) applies lambda function do each cell

    # Update report
    report['unique_values_after'] = df_work[column].nunique() # .nunique() returns number of unique values (excluding missing values)
    
    # Terminal output: end
    print("✓")
    
    return df_work, report