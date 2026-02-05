# Structural Errors

## 1. Problem

### What are Structural Errors?

Structural errors are inconsistencies in categorical columns of a DataFrame where the same real-world entity is represented differently as text. The values refer to the same category, but the strings are different.

### Examples

| Type | Example |
|------|---------|
| Case | "New York" vs "new york" vs "NEW YORK" |
| Typos | "Hospital" vs "Hosptial" vs "Hospitla" |
| Abbreviations | "NYC" vs "New York City" vs "N.Y.C." |
| Spacing | "bore hole" vs "borehole" |
| Word order | "Health Center" vs "Center Health" |
| Synonyms | "tap water" vs "municipal water" |

### Goal

Group (cluster) similar values together and replace them with one canonical (standard) form. This results in a cleaned categorical column with standardized and consistent values.

---

## 2. Pipeline Overview

**Step 1 - Similarity:** Compute a similarity matrix that shows how similar each pair of values is. Different techniques available: character-based (RapidFuzz) or semantic (Embeddings).

**Step 2 - Clustering:** Group values that are similar enough into clusters. Different clustering methods available: Hierarchical, Connected Components, or Affinity Propagation.

**Step 3 - Canonical Selection:** For each cluster, select one value as the canonical (standard) name. All other values in the cluster will be mapped to this canonical name.

**Step 4 - Apply Mapping:** Replace all values in the DataFrame column with their canonical names. The result is a cleaned categorical column with standardized and consistent values.

---

## 3. Step 1: Similarity

### What is a Similarity Matrix?

A similarity matrix shows how similar every value is to every other value. For n unique values, we get an n × n matrix.

**Example** (4 unique values):
```
              Value A   Value B   Value C   Value D
Value A        1.00      0.85      0.20      0.15
Value B        0.85      1.00      0.25      0.18
Value C        0.20      0.25      1.00      0.90
Value D        0.15      0.18      0.90      1.00
```

**Properties:**
- Diagonal is always 1.0 (a value is identical to itself)
- Matrix is symmetric (similarity A→B equals similarity B→A)
- Values range from 0 (completely different) to 1 (identical)

---

### Method A: RapidFuzz (Character-Based)

RapidFuzz compares strings character by character. We use `token_sort_ratio` which works in two steps:

**1. Token Sort**

Split each string into words (tokens), sort them alphabetically, then join back together. This handles word order differences.

```
"Health Center" → ["Health", "Center"] → ["Center", "Health"] → "Center Health"
"Center Health" → ["Center", "Health"] → ["Center", "Health"] → "Center Health"

After sorting, both strings are identical.
```

**2. Ratio Calculation**

Compare the sorted strings character by charcter and calculate the similarity ratio: `(matching characters * 2 ) / (total characters in both strings)`. 

```
"Center Health" vs "Centre Health"
→ Most characters match → High similarity (~0.92)
```

**Best for:** Typos, case differences, spacing issues, word order differences

**Limitation:** Cannot understand meaning. "NYC" and "New York City" have low character similarity because they share few characters. But obviously they are meant to be the same thing. 

---

### Method B: Embeddings (Semantic)

Embeddings convert text into numerical vectors that capture semantic meaning. Each word or phrase becomes a vector of numbers.

#### Text to Vector

Each string is converted to a high-dimensional vector. The embedding model (from OpenAI) learns to point words with similar meaning in similar **directions** in  the vector space. Note that OpenAI embeddings are normalized (all vectors have length 1), so lenght carries no meaning, only the direction.

```
"New York"  →  [0.12, -0.34, 0.56, 0.78, ...]
"NYC"       →  [0.11, -0.33, 0.55, 0.77, ...]   ← similar to "New York"!
"Boston"    →  [0.45, 0.23, -0.12, 0.34, ...]   ← different direction
```


#### Cosine Similarity

Cosine similarity measures the angle between two vectors. A smaller angle means the vectors point in more similar directions, which means the texts have more similar meanings.

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

**Result:** We compute similarity between all pairs to create the similarity matrix:
```
              New York   new york   NYC     NY    Boston   boston
New York        1.00       0.95    0.88   0.85    0.45     0.44
new york        0.95       1.00    0.87   0.84    0.44     0.46
NYC             0.88       0.87    1.00   0.90    0.42     0.41
NY              0.85       0.84    0.90   1.00    0.43     0.42
Boston          0.45       0.44    0.42   0.43    1.00     0.96
boston          0.44       0.46    0.41   0.42    0.96     1.00
```

**Parameters (Models):**

| Model | Dimensions of Vector | Use Case |
|-------|------------|----------|
| `text-embedding-3-small` | 1536 | Everyday language |
| `text-embedding-3-large` | 3072 | Specialized/technical vocabulary |

**Best for:** Abbreviations, synonyms, semantic variations

**Limitation:** Requires API call, slower, costs money.

---

## 4. Step 2: Clustering

### What is Clustering?

Clustering groups similar values together based on the similarity matrix. Each group (cluster) contains values that should be standardized to the same canonical name.

### Available Methods

| Method | Threshold? | Best For |
|--------|------------|----------|
| **Hierarchical** | Yes | All-rounder. You directly control how strict the grouping is via the threshold. Most predictable behavior and good default choice.|
| **Connected Components** | Yes | Simple and fast. Best when similar values should always be grouped together, even indirectly (if A~B and B~C, then A,B,C grouped). |
| **Affinity Propagation** | No (auto) | When you don't know what threshold to use. Automatically finds the optimal number of clusters. Good for exploring data or mixed error types. |

### Method Details


**Hierarchical Clustering**

Starts with each value in its own cluster. Repeatedly finds the two most similar clusters and merges them. When clusters merge, their similarity to other clusters is calculated as the average of all pairwise similarities (average linkage). Stops when the similarity between clusters drops below the threshold. You control how aggressive the grouping is via the threshold parameter.

**Connected Components Clustering**

Builds a graph where each value is a node. Draws a connection between two nodes if their similarity is above the threshold. Values that are connected (directly or through other values) form a cluster. Simple and very fast.

**Affinity Propagation Clustering**

The algorithm maintains two values for every pair of points (i, k):
- **Responsibility r(i,k):** "How much does value i want k to be its representative?" (high if k is similar to i and i has no better options)
- **Availability a(i,k):** "How good of a representative would k be for i?" (high if many others also want k to represent them)

The iteration process:
1. Compute all responsibilities based on similarities
2. Compute all availabilities based on responsibilities
3. Update responsibilities using new availabilities
4. Update availabilities using new responsibilities
5. Repeat until values stop changing
6. Form clusters with final responsibilities & availabilities 

For more details: https://en.wikipedia.org/wiki/Affinity_propagation

### Parameters

**Hierarchical:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| threshold | 0.85 | Minimum similarity to merge clusters (0-1). Higher = stricter, fewer merges. |

**Connected Components:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| threshold | 0.85 | Minimum similarity to connect values (0-1). Higher = stricter, fewer connections. |

**Affinity Propagation:**
| Parameter | Default | Description |
|-----------|---------|-------------|
| damping | 0.7 | Controls how values update each round. Without damping, the algorithm replaces old values completely with new computed values. This can cause oscillation where preferences flip back and forth forever. With damping = 0.7, the new value is blended: 70% old value + 30% newly computed value. This gradual change ensures the algorithm converges to a stable solution. |

---

## 5. Step 3: Canonical Selection

### What is a Canonical Name?

The canonical name is the standardized form that will represent all values in a cluster. 

### Method A: Most Frequent

Picks the value that appears most often in the original data.

**Logic:** The correct spelling is usually more common than typos.

**Best for:** Typos, case errors where the correct form appears more frequently.

**Limitation:** Fails if errors are more common than the correct value.

### Method B: LLM Selection

Uses an LLM (GPT-4o-mini) to intelligently select the best canonical form.

**LLM preferences:**
- Prefers complete forms over abbreviations
- Prefers correct spelling and capitalization
- Prefers standard/official names over informal variants

**Best for:** Abbreviations, mixed error types, when frequency doesn't indicate correctness.

**Limitation:** Requires API call, slower, costs money.

---

## 6. Step 4: Apply Mapping

### What is the Mapping?

The mapping is a dictionary that connects each original value to its canonical name:

```
{
    "New York": "New York",    (canonical stays the same)
    "new york": "New York",    (mapped to canonical)
    "NEW YORK": "New York",    (mapped to canonical)
    "NYC": "New York"          (mapped to canonical)
}
```

### Applying to the DataFrame

Every value in the categorical column is replaced with its canonical name from the mapping. Values not in the mapping (e.g., NaN) remain unchanged.

**Result:** A cleaned DataFrame column with standardized and consistent categorical values.
