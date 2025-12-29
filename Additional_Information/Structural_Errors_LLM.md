# Structural Errors LLM 

## The Problem

Categorical columns often have inconsistent values referring to the same thing:

```
["New York", "new york", "NYC", "NY", "Boston", "boston"]
```

**Goal:** Group / cluster similar values and replace them with one canonical (standard) form.

---

## Pipeline Overview

```
Step 1: Text → Embeddings
Step 2: Calculate similarity between embeddings (Cosine Similarity)
Step 3: Cluster similar embeddings (Affinity Propagation)
Step 4: LLM selects canonical name per cluster
Step 5: Replace values in dataframe
```

---

## Example: Cities

**Input:**
```
["New York", "new york", "NYC", "NY", "Boston", "boston"]
```

---
### Step 1: Text → Embeddings

Embeddings convert text into numerical vectors that capture semantic meaning. Each word or phrase becomes a vector of numbers.
```
"New York"  →  [0.12, -0.34, 0.56, 0.78, ...]
"NYC"       →  [0.11, -0.33, 0.55, 0.77, ...]   ← similar to "New York"!
"Boston"    →  [0.45, 0.23, -0.12, 0.34, ...]   ← different direction
```

Words with similar meaning point in similar **directions** in vector space. Note that OpenAI embeddings are normalized (all vectors have length 1), so lenght carries no meaning, only the direction.

**Models available:**

| Model | Dimensions of Vector | Use Case |
|-------|------------|----------|
| `text-embedding-3-small` | 1536 | Everyday language |
| `text-embedding-3-large` | 3072 | Specialized/technical vocabulary |

---
### Step 2: Calculate similarity between embeddings (Cosine Similarity)

Cosine similarity measures the angle between two vectors. A smaller angle means the vectors point in more similar directions, which means the texts have more similar meanings.

**Formula:**

```
               A · B    
cos(θ)  =  ───────────── 
           ||A|| × ||B||      
```

- Numerator: Dot product of vectors A and B
- Denominator: Product of vector lengths (normalizes the result)

Note: Since OpenAI embeddings are already normalized (length = 1), the denominator equals 1, 
      so cosine similarity simplifies to just the dot product.

**Range of cosine similarity:** 0 to 1 

| Value | Meaning | Example |
|-------|---------|---------|
| 1.0 | Identical | "New York" vs "New York" |
| > 0.8 | Same thing | "New York" vs "NYC" |
| 0.5 | Somewhat related | "New York" vs "Boston" (both cities) |
| 0.0 | Unrelated | "New York" vs "Banana" |

**Result:** We compute similarity between all pairs to create a similarity matrix:
```
              New York   new york   NYC     NY    Boston   boston
New York        1.00       0.95    0.88   0.85    0.45     0.44
new york        0.95       1.00    0.87   0.84    0.44     0.46
NYC             0.88       0.87    1.00   0.90    0.42     0.41
NY              0.85       0.84    0.90   1.00    0.43     0.42
Boston          0.45       0.44    0.42   0.43    1.00     0.96
boston          0.44       0.46    0.41   0.42    0.96     1.00
```

---
### Step 3: Affinity Propagation Clustering

Affinity Propagation groups similar items into clusters using the similarity matrix.

**Principle:**

The algorithm starts by considering every point as a potential cluster center (exemplar). Then, through an iterative process, points "communicate" with each other to decide who should represent whom.

Each point looks at its similarity to all other points and asks: "Who is most similar to me and could represent me well?" At the same time, points that are similar to many others start accumulating "support" from those points.

After several iterations, natural exemplars emerge — these are points that are highly similar to many other points. The remaining points then cluster around their closest exemplar.

The key advantage over K-means: we don't need to specify the number of clusters beforehand. The algorithm discovers the natural groupings based on the similarity structure of the data.

**Parameters:**

| Parameter | What it controls | Default |
|-----------|------------------|---------|
| `preference` | How likely each point is to become an exemplar. Lower → fewer clusters, Higher → more clusters | Auto (median similarity) |
| `damping` | Smooths the iterative updates to prevent oscillation | 0.9 |

**Result for our example:**
```
Cluster 0 (exemplar: "New York"): ["New York", "new york", "NYC", "NY"]
Cluster 1 (exemplar: "Boston"):   ["Boston", "boston"]
```

"New York" emerged as exemplar because it has high similarity to "new york", "NYC", and "NY". Same for "Boston" with "boston".

---

### Step 4: LLM Selects Canonical Name

For each cluster with multiple values, the LLM is asked to choose the best standard form.

**Cluster 0:** ["New York", "new york", "NYC", "NY"]

The LLM evaluates:
- Completeness: "New York" is the full name (not an abbreviation like "NYC" or "NY")
- Capitalization: "New York" has proper capitalization (not "new york")
- Official usage: "New York" is the most commonly accepted form

**Selected canonical name:** "New York"

**Cluster 1:** ["Boston", "boston"]

**Selected canonical name:** "Boston"

The LLM response is structured using Pydantic to ensure we get exactly the format we need.

---

### Step 5: Apply Mapping

Create a mapping from original values to canonical names and apply it to the dataframe:

```python
mapping = {
    "new york": "New York",
    "NYC": "New York", 
    "NY": "New York",
    "boston": "Boston"
}

df[column] = df[column].replace(mapping)
```

**Output:**
```
["New York", "New York", "New York", "New York", "Boston", "Boston"]
```
