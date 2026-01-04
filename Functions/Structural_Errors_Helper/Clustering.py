# Imported libraries
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from sklearn.cluster import AffinityPropagation

"""
Clustering: Group similar values into clusters
Takes a similarity matrix and returns cluster labels (which cluster each value belongs to)

Available methods:
    - hierarchical_clustering: Industry standard, threshold-based
    - connected_components_clustering: Simplest, graph-based
    - affinity_propagation_clustering: Auto-finds number of clusters
"""

# =============================================================================
# Method 1: Hierarchical Clustering
# =============================================================================

def hierarchical_clustering(similarity_matrix: np.ndarray, threshold: float = 0.85) -> np.ndarray:
    """
    Cluster values using hierarchical agglomerative clustering.
    
    Parameters:
        similarity_matrix: Square matrix (n x n) with similarity scores 0-1
        threshold: Minimum similarity to be in same cluster (default: 0.85)
    
    Returns:
        np.ndarray: Cluster labels (array of integers, one per value)
    """
    # Convert similarity to distance (scipy needs distance)
    distance_matrix = 1 - similarity_matrix
    
    # Convert to condensed form (upper triangle as 1D array)
    n = len(distance_matrix)
    condensed = []
    for i in range(n):
        for j in range(i + 1, n):
            condensed.append(distance_matrix[i, j])
    condensed = np.array(condensed)
    
    # Perform hierarchical clustering
    Z = linkage(condensed, method="average")
    
    # Cut tree at threshold
    distance_threshold = 1 - threshold
    labels = fcluster(Z, t=distance_threshold, criterion='distance')
    
    # Convert to 0-indexed
    labels = labels - 1
    
    return labels


# =============================================================================
# Method 2: Connected Components Clustering
# =============================================================================

def connected_components_clustering(similarity_matrix: np.ndarray, threshold: float = 0.85) -> np.ndarray:
    """
    Cluster values using graph connected components.
    
    Parameters:
        similarity_matrix: Square matrix (n x n) with similarity scores 0-1
        threshold: Minimum similarity to connect two values (default: 0.85)
    
    Returns:
        np.ndarray: Cluster labels (array of integers, one per value)
    """
    # Create adjacency matrix (1 if similar enough, 0 otherwise)
    adjacency = (similarity_matrix >= threshold).astype(int)
    
    # Find connected components
    n_clusters, labels = connected_components(csr_matrix(adjacency), directed=False)
    
    return labels


# =============================================================================
# Method 3: Affinity Propagation Clustering
# =============================================================================

def affinity_propagation_clustering(similarity_matrix: np.ndarray, damping: float = 0.7) -> np.ndarray:
    """
    Cluster values using Affinity Propagation.
    
    Parameters:
        similarity_matrix: Square matrix (n x n) with similarity scores 0-1
        damping: Damping factor (0.5-1.0, default: 0.7)
                 Higher = more stable, slower convergence
    
    Returns:
        np.ndarray: Cluster labels (array of integers, one per value)
    
    Note:
        Affinity Propagation automatically determines the number of clusters.
        It finds "exemplars" (representative points) that best represent clusters.
    """
    # Run Affinity Propagation (uses similarity matrix directly)
    af = AffinityPropagation(affinity='precomputed', damping=damping, random_state=42)
    labels = af.fit_predict(similarity_matrix)
    
    return labels