
"""
Categorical Data Cleaning with Affinity Propagation (AP)
Supervisor's Approach: Vectorization + Standardization
"""

import numpy as np
import pandas as pd
from sklearn.cluster import AffinityPropagation
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer


def clean_categorical_column_vectorized(column_data, preference=-10000, damping=0.5):
    """
    Clean categorical column using vectorization approach
    
    Steps:
    1. Convert strings to numerical vectors (TF-IDF)
    2. Standardize with StandardScaler
    3. Apply Affinity Propagation
    
    Parameters:
    -----------
    column_data : array-like
        The categorical column to clean
    preference : float
        Controls number of clusters (in this approach, typically -10 to -100)
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
    
    # Step 1: Convert strings to numerical vectors using TF-IDF
    # This creates a matrix where each string is represented by word frequencies
    vectorizer = TfidfVectorizer(
        lowercase=True,           # Handle case variations
        analyzer='char_wb',       # Character n-grams (better for typos)
        ngram_range=(2, 3),       # Use 2 and 3 character combinations
    )
    
    X = vectorizer.fit_transform(unique_values)
    
    # Step 2: Standardize the data
    scaler = StandardScaler(with_mean=False)  # with_mean=False for sparse matrices
    X_std = scaler.fit_transform(X)
    
    # Step 3: Apply Affinity Propagation
    ap = AffinityPropagation(
        preference=preference,
        damping=damping,
        random_state=42,
        max_iter=500
    )
    
    ap.fit(X_std)
    
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
# EXAMPLE: Same city data as before
# ============================================================================

raw_data = [
    'New York',
    'new york',
    'NEW YORK',
    'New York City',
    'New York, NY',
    'downtown new york',
    'Boston',
    'boston',
    'BOSTON',
    'Boston MA',
    'Boston, MA',
    'Chicago',
    'chicago',
    'CHICAGO',
    'Chicago IL',
    'Chicago, Illinois',
    'Los Angeles',
    'los angeles',
    'LOS ANGELES',
    'Los Angeles CA',
    'Los Angeles, California',
    'cali los angeles',
    'Miami',
    'miami',
    'miomi',
    'MIAMI',
    'Miami FL',
    'Miami, Florida',
]


# Clean the data with vectorization approach
cleaned_data, mapping = clean_categorical_column_vectorized(
    raw_data,
    preference=-50,  # Different scale than custom similarity approach
    damping=0.9
)

# Get final clusters
final_clusters = set(cleaned_data)
n_clusters = len(final_clusters)

# Print results
# Print results
print("\n" + "=" * 70)
print(f"FINAL CLUSTERS: {n_clusters}")
print("=" * 70)
for i, cluster in enumerate(sorted(final_clusters), 1):
    count = sum(1 for x in cleaned_data if x == cluster)
    print(f"{i}. '{cluster}' ({count} items)")