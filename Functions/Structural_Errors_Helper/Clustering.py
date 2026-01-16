# Imported libraries
import numpy as np
# Hierachical Clustering
from scipy.cluster.hierarchy import linkage, fcluster
# Connected Components Clustering
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
# Affinity Propagation
from sklearn.cluster import AffinityPropagation

"""
Clustering: Group similar values into clusters
Takes a similarity matrix and returns cluster labels (which cluster each value belongs to)

Available methods:
    - hierarchical_clustering: All-rounder. You directly control how strict the grouping is via the threshold. Most predictable behavior and good default choice.
    - connected_components_clustering: Simple and fast. Best when similar values should always be grouped together, even indirectly (if A~B and B~C, then A,B,C grouped).
    - affinity_propagation_clustering: When you don't know what threshold to use. Automatically finds the optimal number of clusters. Good for exploring data or mixed error types.

For further information, see look at Structural_errors.md in the folder Additional_Information
"""

# =============================================================================
# Method 1: Hierarchical Clustering
# =============================================================================

def hierarchical_clustering(similarity_matrix: np.ndarray, threshold: float) -> np.ndarray:
    """
    Cluster values using hierarchical clustering
    
    Parameter:
        threshold: Minimum similarity to merge clusters (0-1). Higher = stricter, fewer merges.
    """
    # Scipy expects distance (smaller = more similar) instead of similarity (larger = more similar)
    # Hence convert similarity matrix to distance matrix
    distance_matrix = 1 - similarity_matrix
    # Example: similarity 0.9 → distance 0.1 (very close)
    #          similarity 0.2 → distance 0.8 (far apart)

    # Convert similarity threshold to distance threshold
    distance_threshold = 1 - threshold

    # Scipy expects condensed form (upper triangle as 1D array) of distance_matrix 
    # Hence convert to condensed form 
    n = len(distance_matrix)
    condensed = []
    for i in range(n):
        for j in range(i + 1, n):
            condensed.append(distance_matrix[i, j])
    condensed = np.array(condensed)
    
    # Perform hierarchical clustering
    Z = linkage(condensed, method = "average") # Method = "average" --> average linkage (See Structural_Errors.md in Additional_Information)
    labels = fcluster(Z, t = distance_threshold, criterion = 'distance')
    
    # Convert to 0-indexed (meaning labels start with 0 instead of 1)
    labels = labels - 1
    
    return labels

# =============================================================================
# Method 2: Connected Components Clustering
# =============================================================================

def connected_components_clustering(similarity_matrix: np.ndarray, threshold: float) -> np.ndarray:
    """
    Cluster values using Connected Components Clustering
    
    Parameters:
        threshold: Minimum similarity to connect values (0-1). Higher = stricter, fewer connections. 
    """
    # Create adjacency matrix (1 if similar enough, 0 otherwise)
    adjacency = (similarity_matrix >= threshold).astype(int)
    # Note: Logical operator applied to np array are executed element wise 
    #       similarity_matrix >= threshold will become a boolean matrix
    #       With .astype(int) from Numpy the all values of the matrix are converted to int (True, False -> 1,0)
    
    # Perform Connected Components Clustering
    n_clusters, labels = connected_components(csr_matrix(adjacency), directed=False)
    # Note: n_cluster = # of clusters found (not used)
    #       csr_matrix() convertion to sparse matrix (required)

    return labels

# =============================================================================
# Method 3: Affinity Propagation Clustering
# =============================================================================

def affinity_propagation_clustering(similarity_matrix: np.ndarray, damping: float) -> np.ndarray:
    """
    Cluster values using Affinity Propagation
    
    Parameters:
        damping: Controls how values update each round. Without damping, the algorithm replaces old values completely with new computed values. 
                 This can cause oscillation  where preferences flip back and forth forever. 
                 With damping = 0.7, the new value is blended: 70% old value + 30% newly computed value. 
                 This gradual change ensures the algorithm converges to a stable solution.
    """
    # Perform Affinity Propagation
    af = AffinityPropagation(affinity = 'precomputed', damping = damping, random_state = 42)
    labels = af.fit_predict(similarity_matrix)
    
    return labels