import os
import json
import time
from itertools import combinations
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import pandas as pd
from tqdm import tqdm


class SimilarityScore(BaseModel):
    index: int
    similarity: float

class SimilarityResponse(BaseModel):
    scores: list[SimilarityScore]

class DataAnalysis(BaseModel):
    data_type: str
    description: str
    rules: list[str]


def analyze_values(client: OpenAI, values: list[str]) -> DataAnalysis:
    sample = values[:20] if len(values) > 20 else values
    
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"""Analyze these values from a dataset column for data cleaning purposes.

Values: {json.dumps(sample)}

Determine:
1. What type of data is this? (e.g., boolean, volume, count, frequency, category, date, etc.)
2. Brief description of what you observe
3. Generate 4-6 specific rules for comparing pairs and scoring similarity (0.0-1.0)

Rules should handle: exact matches, format variations, unit conversions, and when values are different (0.0)."""
        }],
        response_format=DataAnalysis
    )
    
    return response.choices[0].message.parsed


def build_similarity_matrix(values: list[str], batch_size: int = 50) -> dict:
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print("  Analyzing data type...")
    analysis = analyze_values(client, values)
    
    print(f"  Detected: {analysis.data_type}")
    print(f"  {analysis.description}")
    print(f"  Rules:")
    for rule in analysis.rules:
        print(f"    • {rule}")
    print()
    
    n = len(values)
    matrix = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    pairs = list(combinations(range(n), 2))
    
    rules_text = "\n".join(f"- {rule}" for rule in analysis.rules)
    
    prompt_template = f"""You are a data cleaning expert comparing {analysis.data_type} values.

CONTEXT: {analysis.description}

RULES:
{rules_text}

Compare each pair and return similarity score (0.0-1.0).

Pairs:
{{comparisons}}"""

    with tqdm(total=len(pairs), desc="Comparing pairs", unit="pair", ncols=80) as pbar:
        for batch_start in range(0, len(pairs), batch_size):
            batch = pairs[batch_start:batch_start + batch_size]
            
            comparisons = [
                {"index": idx, "a": values[i], "b": values[j]}
                for idx, (i, j) in enumerate(batch)
            ]
            
            response = client.beta.chat.completions.parse(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": prompt_template.format(comparisons=json.dumps(comparisons))
                }],
                response_format=SimilarityResponse
            )
            
            for s in response.choices[0].message.parsed.scores:
                i, j = batch[s.index]
                matrix[i][j] = matrix[j][i] = s.similarity
            
            pbar.update(len(batch))
    
    return {"matrix": matrix, "labels": values, "analysis": analysis}


def save_results(result: dict, name: str):
    df = pd.DataFrame(result["matrix"], index=result["labels"], columns=result["labels"])
    
    csv_file = f"{name}_matrix.csv"
    df.to_csv(csv_file)
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    size = max(8, len(result["labels"]) * 0.5)
    plt.figure(figsize=(size, size * 0.8))
    sns.heatmap(df, annot=len(result["labels"]) <= 15, fmt=".2f", cmap="YlGnBu", vmin=0, vmax=1, annot_kws={"size": 8})
    plt.title(f"{name} ({result['analysis'].data_type})")
    plt.tight_layout()
    
    png_file = f"{name}_heatmap.png"
    plt.savefig(png_file, dpi=150)
    plt.close()
    
    print(f"  ✓ Saved: {csv_file}, {png_file}")


if __name__ == "__main__":
    datasets = {
        # Volume with unit variations
        "daily_usage": [
            "500L", "480 liters", "520000ml", "500 liters",
            "240L", "250000ml", "5000L", "200 liters"
        ],
        
        # Boolean variations
        "is_functional": [
            "Yes", "Y", "1", "true", "TRUE", "No", "N", "0", "false"
        ],
        
        # Frequency with typos
        "maintenance": [
            "Monthly", "monthly", "MONTHLY", "Mothly",
            "Quarterly", "quarterly", "QUARTERLY", "Quartely"
        ],
        
        # Numbers as digits and words
        "staff_count": [
            "25", "twenty-five", "26", "twelve", "12", "thirty-three", "33", "-5"
        ],
        
        # Dates in different formats
        "dates": [
            "2024-01-15", "15/01/2024", "Jan 15 2024", "01-15-2024",
            "2024-02-10", "10/02/2024", "Feb 10 2024", "2024-12-25"
        ],
        
        # Currency/prices
        "prices": [
            "$100", "100 USD", "$100.00", "100 dollars",
            "€85", "85 EUR", "$99.99", "100$"
        ],
        
        # Organization names
        "organizations": [
            "WHO", "World Health Organization", "W.H.O.",
            "UNICEF", "United Nations Children's Fund",
            "Scottish Government", "Scottish Gov", "The Scottish Government"
        ],
        
        # Cities/locations
        "cities": [
            "New York", "new york", "NYC", "NY", "New York City",
            "Los Angeles", "LA", "L.A.", "los angeles"
        ],
        
        # Facility types with typos
        "facility_type": [
            "Hospital", "hospital", "HOSPITAL", "Hosptial",
            "Clinic", "clinic", "CLINIC", "Clnic",
            "Health Center", "health center", "Health centre", "Helth Center"
        ],
        
        # Water sources
        "water_source": [
            "Borehole", "borehole", "bore hole", "Borehole well",
            "Hand pump", "hand pump", "handpump", "Hand Pump",
            "Piped water", "Piped Water", "piped water", "Tap water"
        ],
        
        # Percentages
        "percentages": [
            "50%", "50 percent", "0.5", "50/100", "half",
            "25%", "25 percent", "0.25", "one quarter"
        ],
        
        # Weights
        "weights": [
            "1kg", "1000g", "1 kilogram", "2.2 lbs",
            "500g", "0.5kg", "1.1 pounds", "500 grams"
        ],
    }
    
    start = time.time()
    
    for name, values in datasets.items():
        n_pairs = len(list(combinations(range(len(values)), 2)))
        print(f"\n{'='*60}")
        print(f"  {name.upper()} ({len(values)} values, {n_pairs} pairs)")
        print(f"{'='*60}")
        
        result = build_similarity_matrix(values)
        save_results(result, name)
    
    print(f"\n✅ Done! Total time: {time.time() - start:.1f}s")