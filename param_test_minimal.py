"""
Extended Parameter Selection Test
Now includes: similarity_method, clustering_method, threshold
"""

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Literal
import os
from dotenv import load_dotenv


class CleaningParams(BaseModel):
    """Constrained parameters for structural error cleaning"""
    
    similarity_method: Literal["rapidfuzz", "embeddings"] = Field(
        description="rapidfuzz for typos/character errors, embeddings for semantic/abbreviations"
    )
    
    clustering_method: Literal["hierarchical", "connected_components", "affinity_propagation"] = Field(
        description="hierarchical is safest (no chaining), connected_components is aggressive (chains similar values), affinity_propagation auto-detects clusters (no threshold needed)"
    )
    
    threshold: float = Field(
        ge=0.5, le=1.0,
        description="Similarity threshold. Higher=stricter/fewer merges, Lower=looser/more merges. Not used if affinity_propagation."
    )
    
    reasoning: str = Field(
        description="Explain your choice based on the patterns you see in the data"
    )


def suggest_params(unique_values: list) -> CleaningParams:
    """Give LLM the unique values, get parameters back"""
    
    # Get API key from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Raise ValueError if api_key is not found or empty
    if api_key == None or api_key == "":
        raise ValueError("OPENAI_API_KEY was not found or is empty in .env")
    
    client = instructor.from_openai(OpenAI(api_key=api_key))
    
    return client.chat.completions.create(
        model="gpt-5",
        response_model=CleaningParams,
        messages=[{
            "role": "user",
            "content": f"""Analyze these {len(unique_values)} unique values from a data column:

{unique_values}

I need to merge duplicates/variants into canonical forms. Choose parameters:

1. SIMILARITY METHOD:
   - "rapidfuzz": Character-level comparison. Good for typos (Hosptial→Hospital), case variants (BOSTON→Boston), whitespace issues.
   - "embeddings": Semantic comparison. Good for abbreviations (NYC→New York City), synonyms (WHO→World Health Organization), different names for same thing.

2. CLUSTERING METHOD:
   - "hierarchical": SAFEST. Only merges values that are directly similar. Use when you want to avoid wrong merges.
   - "connected_components": AGGRESSIVE. If A~B and B~C, then A,B,C all merge even if A≠C. Can cause chain reactions.
   - "affinity_propagation": AUTO-DETECTION. Finds natural clusters automatically. Good when you're unsure about threshold. No threshold needed.

3. THRESHOLD (0.5-1.0):
   - 0.90+: Very strict, only nearly identical strings merge
   - 0.80-0.90: Balanced, catches typos but avoids wrong merges
   - 0.70-0.80: Loose, good for abbreviations with embeddings
   - 0.60-0.70: Very loose, risk of wrong merges
   - (ignored if using affinity_propagation)

What parameters should I use for this column?"""
        }]
    )


if __name__ == "__main__":
    # Test cases with different patterns
    test_cases = {
        "city": [
            'New York', 'new york', 'NYC', 'NY', 'New York City', 
            'Boston', 'boston', 'BOSTON', 
            'Los Angeles', 'LA', 'L.A.', 'los angeles', 
            'Chicago', 'chicago', 'CHICAGO', 
            'Seattle', 'seattle', 'SEATTLE', 
            'Denver', 'denver', 'DENVER'
        ],
        
        "Facility Type": [
            'Hospital', 'hospital', 'HOSPITAL', 'Hosptial', 'hosptial', 
            'Clinic', 'clinic', 'CLINIC', 'Clnic', 
            'Health Center', 'health center', 'Health centre', 'Helth Center'
        ],
        
        "Funding_Organization": [
            'WHO', 'World Health Organization', 'W.H.O.', 
            'UNICEF', "United Nations Children's Fund", 'United Nations Childrens Fund',
            'Scottish Government', 'The Scottish Government', 'Scottish Gov'
        ],
        
        # Harder case: mixed patterns
        "drilling_contractor": [
            'Blue Water Drilling Ltd', 'Blue Water Drilling Company', 'Blue water',
            'OG Madzi', 'OG Madzi Drilling', 'OG MADZI', 'OG Madzi Drillers',
            'Saifro Limited', 'Saifro Ltd', 'Saifro Malawi',
            'China Gansu', 'China Gansu Engineering Co.',
            'Nditha Drilling and Civil Contractors', 'Nditha Civil and Drilling Contractors',
            'GIMM', 'GIMME', 'GIMM water experts'
        ]
    }
    
    print("="*70)
    print("EXTENDED PARAMETER SELECTION TEST")
    print("="*70)
    
    for col_name, unique_vals in test_cases.items():
        print(f"\n{'='*70}")
        print(f"Column: {col_name}")
        print(f"Values ({len(unique_vals)}): {unique_vals[:5]}..." if len(unique_vals) > 5 else f"Values: {unique_vals}")
        print("="*70)
        
        params = suggest_params(unique_vals)
        
        print(f"""
LLM Suggestion:
  Similarity: {params.similarity_method}
  Clustering: {params.clustering_method}
  Threshold:  {params.threshold}
  
Reasoning: {params.reasoning}
""")

