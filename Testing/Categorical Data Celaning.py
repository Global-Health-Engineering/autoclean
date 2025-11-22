"""
Categorical Data Cleaning with Affinity Propagation (AP)
"""

import numpy as np
import pandas as pd
from sklearn.cluster import AffinityPropagation
from sklearn.metrics import pairwise_distances

"""
Calculate similarity between two strings
Handles: typos, uppercase & lowercase, word order, extra information
Returns value between 0 (completely different) and 1 (identical)
"""


# Levenshtein distance (# of edits needed to turn one string into the other)
def levenshtein_similarity(a, b):
    # Swap them so 'a' is always the longer one
    if len(a) < len(b):
        a, b = b, a
    if len(b) == 0:
        return 0.0
    
    previous_row = range(len(b) + 1)
    for i, ca in enumerate(a):
        current_row = [i + 1]
        for j, cb in enumerate(b):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (ca != cb)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    distance = previous_row[-1]
    max_len = max(len(a), len(b))
    return 1 - (distance / max_len)

# Jaccard similarity (measure how similar two sets are)
def jaccard_similarity(a, b):
    # Remove commas (.replace()), split string into words by spaces (.split()) & convert to set (.set()) --> removes duplicates 
    s1 = set(a.replace(',', '').split())
    s2 = set(b.replace(',', '').split())

    if len(s1.union(s2)) > 0: # Both 
        jaccard = len(s1.intersection(s2)) / len(s1.union(s2))
        # jaccard = (# unique words that appear in both sets) / (# unique words of both sets) 

    else:
        jaccard = 0.0
        # If no words at all, similarity is 0 
    
    return jaccard

def string_similarity(s1, s2):
    # Convert to lowercase (.lower()) and remove whitespaces at front / end(.strip())
    s1_lower = s1.lower().strip()
    s2_lower = s2.lower().strip()
    
    # Check if strings are equivalent (similarity = 1)
    if s1_lower == s2_lower:
        return 1.0
    
    levenshtein = levenshtein_similarity(s1_lower, s2_lower)
    jaccard = jaccard_similarity(s1_lower, s2_lower)

    # Combine both metrics (weighted average)
    # Jaccard is better for word reordering, Levenshtein for typos
    similarity = 0.6 * jaccard + 0.4 * levenshtein
    
    return similarity


def build_similarity_matrix(values):
    """
    Build similarity matrix for all unique values in the column
    """
    n = len(values)
    similarity_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            similarity_matrix[i, j] = string_similarity(values[i], values[j])
    
    return similarity_matrix


def clean_categorical_column(column_data, preference=-0.5, damping=0.9):
    """
    Clean a categorical column by clustering similar values
    
    Parameters:
    -----------
    column_data : array-like
        The categorical column to clean
    preference : float
        Controls number of clusters (lower = fewer clusters)
        Adjust this based on your data
    damping : float
        Damping factor for stability (0.5 to 1.0)
    
    Returns:
    --------
    cleaned_data : array
        Cleaned categorical values (mapped to cluster exemplars)
    mapping : dict
        Dictionary showing original -> cleaned mapping
    """
    
    # Get unique values
    unique_values = list(set(column_data))
    
    # Build similarity matrix
    similarity_matrix = build_similarity_matrix(unique_values)
    
    # Convert similarity to affinity (negative distance)
    affinity_matrix = -((1 - similarity_matrix) ** 2)
    
    # Apply Affinity Propagation
    ap = AffinityPropagation(
        affinity='precomputed',
        preference=preference,
        damping=damping,
        random_state=42,
        max_iter=500
    )
    
    ap.fit(affinity_matrix)
    
    # Get cluster labels and exemplars
    labels = ap.labels_
    exemplar_indices = ap.cluster_centers_indices_
    
    # Create mapping from original values to exemplars
    mapping = {}
    for i, value in enumerate(unique_values):
        cluster_id = labels[i]
        exemplar_idx = exemplar_indices[cluster_id]
        exemplar_value = unique_values[exemplar_idx]
        mapping[value] = exemplar_value
    
    # Apply mapping to original data
    cleaned_data = np.array([mapping[val] for val in column_data])
    
    return cleaned_data, mapping


# ============================================================================
# EXAMPLE: Categorical column with structural errors
# ============================================================================

# Sample data: city names with various structural errors
raw_data = [ 
    # New York
    'New York',
    'new york',
    'NEW YORK',
    'New York City',
    'New York, NY',
    'downtown new york', 

    # Boston
    'Boston',
    'boston',
    'BOSTON',
    'Boston MA',
    'Boston, MA',

    # Chicago
    'Chicago',
    'chicago',
    'CHICAGO',
    'Chicago IL',
    'Chicago, Illinois',

    # Los Angeles
    'Los Angeles',
    'los angeles',
    'LOS ANGELES',
    'Los Angeles CA',
    'Los Angeles, California',
    'cali los angeles',

    # Miami
    'Miami',
    'miami',
    'miomi',  
    'MIAMI',
    'Miami FL',
    'Miami, Florida',

    # Zug 
    "zug", 
    "Zug"
]

# Clean the data
cleaned_data, mapping = clean_categorical_column(
    raw_data,
    preference=-0.24,  # Tune this parameter based on your data
    damping=0.9
)

# Get final clusters
final_clusters = set(cleaned_data)
n_clusters = len(final_clusters)

# Print results
print("\n" + "=" * 70)
print(f"FINAL CLUSTERS: {n_clusters}")
print("=" * 70)
for i, cluster in enumerate(sorted(final_clusters), 1):
    count = sum(1 for x in cleaned_data if x == cluster)
    print(f"{i}. '{cluster}' ({count} items)")
"""
print("\n" + "=" * 70)
print("MAPPING (Original → Cleaned)")
print("=" * 70)
for original, cleaned in sorted(mapping.items()):
    print(f"{original:<30} → {cleaned}")
"""


