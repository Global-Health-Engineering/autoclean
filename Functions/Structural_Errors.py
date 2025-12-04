"""
LLM-Powered Data Cleaning with Affinity Propagation

Cleans messy string data using semantic embeddings and clustering.
"""

import numpy as np
from pydantic import BaseModel, Field
from sklearn.cluster import AffinityPropagation
from sklearn.metrics.pairwise import cosine_similarity
import instructor
from openai import OpenAI


# =============================================================================
# Pydantic Models for Structured Output
# =============================================================================

class ClusterEvaluation(BaseModel):
    """LLM's evaluation of clustering quality."""
    is_satisfactory: bool = Field(description="Whether clustering is good enough")
    num_clusters: int = Field(description="Number of clusters found")
    issues: list[str] = Field(default_factory=list, description="Issues with current clustering")
    suggested_preference: float = Field(description="New preference value to try (between -1.0 and 0)")
    reasoning: str = Field(description="Explanation for the suggestion")


class CanonicalName(BaseModel):
    """Canonical name for a cluster."""
    cluster_id: int = Field(description="Cluster identifier")
    members: list[str] = Field(description="All strings in this cluster")
    canonical_form: str = Field(description="The standardized form")
    confidence: float = Field(ge=0, le=1, description="Confidence score")
    reasoning: str = Field(description="Why this form was chosen")


class CleaningResult(BaseModel):
    """Complete cleaning result."""
    mappings: dict[str, str] = Field(description="Original → canonical mappings")
    clusters: list[CanonicalName] = Field(description="Cluster details")
    stats: dict = Field(default_factory=dict, description="Process statistics")


# =============================================================================
# Main Cleaner Class
# =============================================================================

class LLMDataCleaner:
    """
    Cleans messy string data using LLM embeddings and Affinity Propagation.
    
    Example:
        cleaner = LLMDataCleaner(api_key="sk-...")
        result = cleaner.clean(["New York", "new york", "NY", "Boston"])
        print(result.mappings)
    """
    
    def __init__(
        self,
        api_key: str,
        embedding_model: str = "text-embedding-3-small",
        chat_model: str = "gpt-4o-mini",
        max_iterations: int = 5,
        verbose: bool = True
    ):
        self.client = OpenAI(api_key=api_key)
        self.instructor_client = instructor.from_openai(self.client)
        self.embedding_model = embedding_model
        self.chat_model = chat_model
        self.max_iterations = max_iterations
        self.verbose = verbose
        
    def _log(self, msg: str):
        if self.verbose:
            print(msg)
    
    def get_embeddings(self, strings: list[str]) -> np.ndarray:
        """Convert strings to semantic embeddings."""
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=strings
        )
        return np.array([item.embedding for item in response.data])
    
    def cluster_with_ap(
        self,
        similarity_matrix: np.ndarray,
        preference: float = None,
        damping: float = 0.9
    ) -> np.ndarray:
        """
        Cluster using Affinity Propagation.
        
        Args:
            similarity_matrix: Precomputed cosine similarity matrix
            preference: Controls cluster count. If None, uses median similarity.
                       More negative = fewer clusters, less negative = more clusters.
                       Should be in range [-1, 0] for cosine similarity.
            damping: Damping factor (0.5-1.0)
        """
        if preference is None:
            preference = np.median(similarity_matrix)
        
        ap = AffinityPropagation(
            preference=preference,
            damping=damping,
            affinity='precomputed',
            max_iter=500,
            random_state=42
        )
        return ap.fit_predict(similarity_matrix)
    
    def evaluate_clusters(
        self,
        strings: list[str],
        labels: np.ndarray,
        preference: float,
        iteration: int,
        similarity_stats: dict
    ) -> ClusterEvaluation:
        """Use LLM to evaluate clustering and suggest adjustments."""
        clusters = {}
        for s, label in zip(strings, labels):
            clusters.setdefault(int(label), []).append(s)
        
        cluster_summary = "\n".join(
            f"Cluster {k}: {v}" for k, v in sorted(clusters.items())
        )
        
        prompt = f"""Evaluate these clusters for data cleaning.
Goal: Group strings referring to the SAME entity together, separate DIFFERENT entities.

Current clustering (iteration {iteration}):
{cluster_summary}

Current preference: {preference:.4f}
Similarity matrix stats: min={similarity_stats['min']:.3f}, max={similarity_stats['max']:.3f}, median={similarity_stats['median']:.3f}

IMPORTANT RULES:
1. Check if strings for the SAME entity (e.g., "New York" and "NY") are in the same cluster
2. Check if DIFFERENT entities (e.g., "New York" vs "Boston") are in SEPARATE clusters
3. Each distinct real-world entity should have its own cluster

If clustering is wrong, suggest a new preference value:
- Preference must be between -1.0 and 0.0 (cosine similarity scale)
- More negative (e.g., -0.8) → FEWER, larger clusters
- Less negative (e.g., -0.2) → MORE, smaller clusters
- If everything is in 1 cluster, try LESS negative (closer to 0)
- If too many clusters, try MORE negative (closer to -1)"""

        return self.instructor_client.chat.completions.create(
            model=self.chat_model,
            response_model=ClusterEvaluation,
            messages=[{"role": "user", "content": prompt}]
        )
    
    def find_optimal_clusters(
        self,
        strings: list[str],
        similarity_matrix: np.ndarray,
        initial_preference: float = None
    ) -> tuple[np.ndarray, list[ClusterEvaluation]]:
        """Iteratively find optimal clustering with LLM guidance."""
        
        # Compute similarity stats for LLM context
        sim_values = similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)]
        similarity_stats = {
            'min': float(np.min(sim_values)),
            'max': float(np.max(sim_values)),
            'median': float(np.median(sim_values))
        }
        
        # Start with a preference that should create multiple clusters
        if initial_preference is None:
            initial_preference = similarity_stats['median'] - 0.3
            initial_preference = max(-0.95, min(-0.05, initial_preference))
        
        preference = initial_preference
        history = []
        best_labels = None
        best_num_clusters = 0
        
        self._log(f"  Similarity stats: min={similarity_stats['min']:.3f}, "
                 f"max={similarity_stats['max']:.3f}, median={similarity_stats['median']:.3f}")
        
        for i in range(self.max_iterations):
            labels = self.cluster_with_ap(similarity_matrix, preference)
            num_clusters = len(set(labels))
            
            # Keep track of best result
            if num_clusters > best_num_clusters and num_clusters < len(strings):
                best_labels = labels.copy()
                best_num_clusters = num_clusters
            
            evaluation = self.evaluate_clusters(
                strings, labels, preference, i + 1, similarity_stats
            )
            history.append(evaluation)
            
            if evaluation.is_satisfactory:
                self._log(f"  ✓ Optimal at iteration {i+1}: {num_clusters} clusters")
                return labels, history
            
            self._log(f"  Iteration {i+1}: {num_clusters} clusters, "
                     f"preference {preference:.4f} → {evaluation.suggested_preference:.4f}")
            self._log(f"    Issues: {evaluation.issues}")
            
            # Clamp suggested preference to valid range
            preference = max(-0.99, min(-0.01, evaluation.suggested_preference))
        
        # If we never found good clusters, return the best we found
        if best_labels is not None and best_num_clusters > 1:
            self._log(f"  Using best result with {best_num_clusters} clusters")
            return best_labels, history
        
        return labels, history
    
    def propose_canonical_names(
        self,
        strings: list[str],
        labels: np.ndarray
    ) -> list[CanonicalName]:
        """Use LLM to select canonical names for each cluster."""
        clusters = {}
        for s, label in zip(strings, labels):
            clusters.setdefault(int(label), []).append(s)
        
        results = []
        for cluster_id, members in sorted(clusters.items()):
            prompt = f"""These variations all refer to the SAME entity:
{members}

Select the best canonical (standardized) form.
Rules:
1. Use proper capitalization
2. Prefer full names over abbreviations
3. Fix any typos
4. Use the official/formal form
5. Return ONLY the canonical name, nothing extra"""

            canonical = self.instructor_client.chat.completions.create(
                model=self.chat_model,
                response_model=CanonicalName,
                messages=[{"role": "user", "content": prompt}]
            )
            canonical.cluster_id = cluster_id
            canonical.members = members
            results.append(canonical)
        
        return results
    
    def clean(
        self,
        dirty_strings: list[str],
        initial_preference: float = None
    ) -> CleaningResult:
        """
        Clean a list of dirty strings.
        
        Args:
            dirty_strings: List of messy strings to clean
            initial_preference: Starting AP preference (between -1 and 0).
                               If None, automatically determined from data.
            
        Returns:
            CleaningResult with mappings and metadata
        """
        self._log(f"\n{'='*60}")
        self._log("LLM Data Cleaning Pipeline")
        self._log(f"{'='*60}")
        
        unique_strings = list(set(dirty_strings))
        self._log(f"Input: {len(dirty_strings)} total, {len(unique_strings)} unique")
        
        # Step 1: Embeddings
        self._log("\n[Step 1] Generating embeddings...")
        embeddings = self.get_embeddings(unique_strings)
        self._log(f"  ✓ {embeddings.shape[0]} embeddings (dim={embeddings.shape[1]})")
        
        # Step 1.5: Compute similarity matrix once
        self._log("\n[Step 1.5] Computing similarity matrix...")
        similarity_matrix = cosine_similarity(embeddings)
        self._log(f"  ✓ {similarity_matrix.shape[0]}x{similarity_matrix.shape[1]} similarity matrix")
        
        # Step 2: Optimal clustering
        self._log("\n[Step 2] Finding optimal clusters...")
        labels, history = self.find_optimal_clusters(
            unique_strings, similarity_matrix, initial_preference
        )
        
        num_clusters = len(set(labels))
        self._log(f"  Final: {num_clusters} clusters")
        
        # Step 3: Canonical names
        self._log("\n[Step 3] Selecting canonical names...")
        canonical_names = self.propose_canonical_names(unique_strings, labels)
        for cn in canonical_names:
            self._log(f"  {cn.members} → '{cn.canonical_form}'")
        
        # Step 4: Build mappings
        mappings = {}
        for cn in canonical_names:
            for member in cn.members:
                mappings[member] = cn.canonical_form
        
        return CleaningResult(
            mappings=mappings,
            clusters=canonical_names,
            stats={
                "input_count": len(dirty_strings),
                "unique_count": len(unique_strings),
                "cluster_count": len(canonical_names),
                "iterations": len(history)
            }
        )
