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

**Example** (4 values):
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
```

After sorting, both strings are identical.

**2. Ratio Calculation**

Compare the sorted strings character by character and calculate the similarity ratio.

For single words:
```
"Hospital" vs "Hosptial"
→ Most characters match → High similarity (~0.88)
```

For multiple words (after token sort):
```
"Center Health" vs "Center Health"
→ All characters match → Similarity = 1.0

"Center Health" vs "Centre Health"
→ Most characters match (only e vs r differs) → High similarity (~0.92)
```

**Parameters:**
| Parameter | Value | Description |
|-----------|-------|-------------|
| method | `token_sort_ratio` | Sorts words alphabetically, then calculates character ratio |

**Best for:** Typos, case differences, spacing issues, word order differences

**Limitation:** Cannot understand meaning. "NYC" and "New York City" have low character similarity because they share few characters.

---

### Method B: Embeddings (Semantic)

Embeddings convert text into numerical vectors that capture meaning. Similar meanings → similar vectors.

#### Text to Vector

Each string is converted to a high-dimensional vector (list of numbers). The embedding model (trained on billions of texts) learns to place words with similar meanings close together in vector space.

```
"New York City"  →  [0.023, -0.041, 0.018, ..., 0.033]   (1536 numbers)
"NYC"            →  [0.025, -0.038, 0.021, ..., 0.031]   (1536 numbers)
"Los Angeles"    →  [-0.019, 0.052, -0.008, ..., -0.027] (1536 numbers)
```

These vectors are normalized (length = 1). Words with similar meaning point in similar directions in this high-dimensional space.

#### Cosine Similarity

We measure similarity by the angle between two vectors:

```
                    A · B
cosine(A, B) = ─────────────
               ||A|| × ||B||

Where:
- A · B = dot product (multiply corresponding elements, sum them)
- ||A|| = magnitude (length of vector)
```

- Vectors pointing in the same direction → cosine = 1 (identical meaning)
- Vectors perpendicular → cosine = 0 (unrelated meaning)

**Result:**
```
"NYC" vs "New York City"  →  cosine ≈ 0.92  (high - same meaning!)
"NYC" vs "Los Angeles"    →  cosine ≈ 0.45  (low - different cities)
```

**Parameters:**
| Parameter | Options | Description |
|-----------|---------|-------------|
| model | `text-embedding-3-small` | Faster, cheaper, 1536 dimensions |
| model | `text-embedding-3-large` | Better quality, 3072 dimensions |

**Best for:** Abbreviations, synonyms, semantic variations

**Limitation:** Requires API call (cost, latency). May over-group unrelated short strings.

---

## 4. Step 2: Clustering

### What is Clustering?

Clustering groups similar values together based on the similarity matrix. Each group (cluster) contains values that should be standardized to the same canonical name.

### Available Methods

| Method | Threshold? | Best For |
|--------|------------|----------|
| **Hierarchical** | Yes | Most cases. Best when you want control over how strict the grouping is. Good for typos, case errors, and spacing issues where you can set a clear similarity threshold. |
| **Connected Components** | Yes | Simple and fast. Best when similar values should always be grouped together, even indirectly. If A is similar to B, and B is similar to C, then A, B, and C are all grouped together. |
| **Affinity Propagation** | No (auto) | Best when you don't know what similarity threshold to use. The algorithm automatically determines the optimal number of clusters. Good for exploring data or when error types are mixed. |

### Method Details

**Hierarchical Clustering**

Starts with each value in its own cluster. Repeatedly finds the two most similar clusters and merges them. Stops when the similarity between clusters drops below the threshold. You control how aggressive the grouping is via the threshold parameter.

**Connected Components Clustering**

Builds a graph where each value is a node. Draws a connection between two nodes if their similarity is above the threshold. Values that are connected (directly or through other values) form a cluster. Simple and very fast.

**Affinity Propagation Clustering**

Values "vote" for which value should represent them (the exemplar). Through iterative message passing, the algorithm finds natural groupings and their representative values. No threshold needed - the algorithm decides the optimal grouping automatically.

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
| damping | 0.7 | Controls how much values update their preferences each iteration (0.5-1.0). Higher values make updates smaller, which helps the algorithm converge smoothly without oscillating. |

---

## 5. Step 3: Canonical Selection

### What is a Canonical Name?

The canonical name is the "correct" or "standard" form that will represent all values in a cluster.

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
    "NYC": "NYC"               (different cluster, own canonical)
}
```

### Applying to the DataFrame

Every value in the categorical column is replaced with its canonical name from the mapping. Values not in the mapping (e.g., NaN) remain unchanged.

**Result:** A cleaned DataFrame column with standardized categorical values, ready for analysis.
