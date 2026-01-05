# Imported libraries
from openai import OpenAI

# Needed to load API Key from .env 
import os
from dotenv import load_dotenv

"""
Canonical: Select the canonical (standard) name for a specific cluster
The canonical name is one value / string out of the specific cluster
All other values in that specific cluster will be mapped to this canonical name

Available methods:
    - most_frequent: Choose the most frequent value as the canonical name
    - llm_selection: Use LLM to intelligently select the canonical name

For further information, see look at Structural_errors.md in the folder Additional_Information
"""

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
    prompt = f"""Select the best canonical name of the following listed values:
{values_list}
For your information, these values are from a column named: {column_name}
Consider: completeness, correct spelling/capitalization, standard usage.
Reply only with the corresponding number from the list above. Only one integer nothing else!"""

    # Create OpenAi client 
    client = OpenAI(api_key = api_key)

    # Get response from LLM 
    response_total = client.chat.completions.create(model = "gpt-5-nano",
                                              messages=[{"role": "user", "content": prompt}],
                                              temperature = 0)
    response = response_total.choices[0].message.content.strip() # Remove possible leading and trailing whitespaces from response with .strip() 
    # Note: response is still a string

    # Validate response: check if it's a number in valid range
    if response.isdigit():
        # Note: .isdigit() checks if all characters in the string are digits, if so True is returned otherwise False 
        
        # Adapt response to python indexing
        index = int(response) - 1

        # Check that index is in the right range
        if 0 <= index < len(cluster_values):
            return cluster_values[index]
    
    # Fallback
    print(f"Warning: LLM returned invalid response: {response}, using fallback: {cluster_values[0]}")
    return cluster_values[0]