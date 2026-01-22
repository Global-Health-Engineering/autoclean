"""
Canonical: Select the canonical (standard) name for a specific cluster
The canonical name is one value / string out of the specific cluster
All other values in that specific cluster will be mapped to this canonical name

Available methods:
    - most_frequent: Choose the most frequent value as the canonical name
    - llm_selection: Use LLM to intelligently select the canonical name

For further information, see look at Structural_errors.md in the folder Additional_Information
"""

# Imported libraries
from openai import OpenAI
from pydantic import BaseModel

# Needed to load API Key from .env 
import os
from dotenv import load_dotenv

# =============================================================================
# Pydantic Schema for Method 2 
# =============================================================================

class CanonicalSelection(BaseModel):
    """Structured output for LLM canonical selection"""
    index: int  # 1-based index of selected value

# =============================================================================
# Method 1: Most Frequent
# =============================================================================

def most_frequent(cluster_values: list, value_counts: dict) -> str:
    """
    Select the most frequently occurring value of a specific cluster as canonical name.

    Input: 
        - cluster_values: List of values grouped to one specific cluster
        - value_counts: Dictionary showing how often each value appears in original data (includes all unique values)

    """
    best_value = None
    best_count = 0
    
    # If cluster contains only one value, return it
    if len(cluster_values) == 1:
        return cluster_values[0]
    
    # Find the most frequent value of a specific cluster 
    for value in cluster_values:
        count = value_counts.get(value, 0)
        # Note: dict.get(key,0) search for key in dict and returns its value if found otherwise 0

        if count > best_count:
            best_count = count
            best_value = value
    
    # Raise ValueError if best_value stays None
    if best_value == None:
        raise ValueError(f"No values from cluster found in value_counts. Cluster values = {cluster_values}")
    
    return best_value

# =============================================================================
# Method 2: LLM Selection
# =============================================================================

def llm_selection(cluster_values: list, column_name: str) -> str:
    """
    Use LLM to select the best canonical name.
    
    Input: 
        - cluster_values: List of values grouped to one specific cluster
        - column_name: Name of the column (provides context)
    """
    # If cluster contains only one value, return it
    if len(cluster_values) == 1:
        return cluster_values[0]
    
    # Get API key from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    # Raise ValueError if api_key is not found (api_key == None) or if api_key is empty (api_key == "")
    if api_key == None or api_key == "":
        raise ValueError("OPENAI_API_KEY was not found or is empty in .env")

    # Build numbered list of values from the specific cluster as a string
    values_list = ""
    for i, v in enumerate(cluster_values):
        values_list += f"{i+1}. {v}\n"
    
    # Build prompt message for LLM 
    prompt = f"""Select the best canonical name from these values (column: {column_name}):
{values_list}
Consider: completeness, correct spelling, readability, standard format, proper casing (title case preferred, never all caps), frequency (as tiebreaker only)

Return the index (1-based) of your choice."""

    # Create OpenAi client 
    client = OpenAI(api_key = api_key)

    # Get response from LLM (with structured output)
    response = client.beta.chat.completions.parse(model = "gpt-4.1-mini",
                                                  temperature = 0.0,
                                                  seed = 42,
                                                  messages = [{"role": "user", "content": prompt}],
                                                  response_format = CanonicalSelection)

    # Get selected index (1-based from LLM) and convert to 0-based (python indexing)
    index = response.choices[0].message.parsed.index - 1
    
    # Return selected value (with safety check)
    if 0 <= index < len(cluster_values):
        return cluster_values[index]
    
    # Fallback
    print(f"Warning: LLM returned invalid response: {response}, using fallback: {cluster_values[0]}")
    return cluster_values[0]