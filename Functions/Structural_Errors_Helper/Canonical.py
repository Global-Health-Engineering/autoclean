# Imported libraries
from openai import OpenAI

"""
Canonical: Select the canonical (standard) name for each cluster
All other values in the cluster will be mapped to this canonical name

Available methods:
    - most_frequent: Choose the most common value
    - llm_selection: Use LLM to intelligently select
"""


# =============================================================================
# Method 1: Most Frequent
# =============================================================================

def most_frequent(cluster_values: list, value_counts: dict) -> str:
    """
    Select the most frequently occurring value as canonical name.
    
    Parameters:
        cluster_values: List of values in this cluster
        value_counts: Dict mapping each value to its count in original data
    
    Returns:
        str: The most frequent value in the cluster
    """
    best_value = None
    best_count = -1
    
    for value in cluster_values:
        count = value_counts.get(value, 0)
        if count > best_count:
            best_count = count
            best_value = value
    
    return best_value


# =============================================================================
# Method 2: LLM Selection
# =============================================================================

def llm_selection(cluster_values: list, column_name: str) -> str:
    """
    Use LLM to select the best canonical name.
    
    Parameters:
        cluster_values: List of values in this cluster
        column_name: Name of the column (provides context)
    
    Returns:
        str: The LLM-selected canonical value
    
    Requires:
        OPENAI_API_KEY environment variable
    """
    # Single value = return it
    if len(cluster_values) == 1:
        return cluster_values[0]
    
    # Build prompt
    values_list = "\n".join([f"{i+1}. {v}" for i, v in enumerate(cluster_values)])
    prompt = f"""Select the best canonical form from these values in column "{column_name}":

{values_list}

Consider: completeness, correct spelling/capitalization, standard usage.
Reply with ONLY the exact value from the list. No explanation."""

    # Call LLM
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    selected = response.choices[0].message.content.strip()
    
    # Validate response
    if selected in cluster_values:
        return selected
    
    # Try to match (LLM might add quotes)
    selected_clean = selected.lower().strip('"\'')
    for value in cluster_values:
        if value.lower() == selected_clean:
            return value
    
    # Fallback to first value
    return cluster_values[0]
