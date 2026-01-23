"""
Semantic Outliers: Detect semantically invalid values using LLM

This function checks if values in a column make semantic sense given the context.
For each value, the LLM returns its confidence between 0.0 & 1.0, where 0.0 means the value does definitely not belong in this column and 1.0 means the value definitely belongs in the column. Values with confidence below (provided) threshold are then either set to np.nan or the whole row is deleted. 

Example of semantic outliers:
- Column country: 28.1 -> not a country
- Column age: -5 -> physically impossible
- Column name: lkajdsfl -> nonsense

Parameters:
    - df: DataFrame to clean 
    - column: Name of column, for which handle_semantic_outliers needs to be applied 
    - context: Description of column, to provide context to LLM
    - threshold: Values with confidence below this are considered semantic outliers (default: 0.3)
    - action: 'nan' (replace with semantic outlier with np.nan, default) or 'delete' (remove semantic outlier and its entire row)

Returns:
    Cleaned dataframe and report (as tuple)
"""

# Imported libraries
import pandas as pd
import numpy as np
from openai import OpenAI
from pydantic import BaseModel, Field
import json

# Needed to load API Key from .env
import os
from dotenv import load_dotenv

# =============================================================================
# Pydantic Schema for Structured Output
# =============================================================================

class SemanticScore(BaseModel):
    """Single value score"""
    index: int = Field(ge = 0, description = "Index of value in the input list")
    confidence: float = Field(ge = 0.0, le = 1.0, description = "Confidence score of the value") 

class SemanticResponse(BaseModel):
    """Structured output for semantic validation"""
    scores: list[SemanticScore] = Field(description = "Scores for all items in input list")

# =============================================================================
# Main Function (Public)
# =============================================================================

def handle_semantic_outliers(df: pd.DataFrame,
                             column: str,
                             context: str,
                             threshold: float = 0.3,
                             action: str = 'nan') -> tuple:
    # Terminal output: start
    print(f"Detecting semantic outliers ({column})... ", end="", flush=True)

    # Work with copy, to not modify input df
    df_work = df.copy()

    # Initialize report
    report = {'column': column,
              'context': context,
              'threshold': threshold,
              'action': action,
              'unique_values_checked': 0,
              'outliers_detected': 0,
              'rows_affected': 0, # Number of rows containing outliers 
              'rows_deleted': 0,
              'outliers': []}

    # Get unique values (excluding NaN)
    unique_values = df_work[column].dropna().unique().tolist()
    report['unique_values_checked'] = len(unique_values)

    # Edge case: no values to check
    if len(unique_values) == 0:
        print("✓")
        return df_work, report

    # Get API key from .env file
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY was not found or is empty in .env")

    # Create OpenAI client
    client = OpenAI(api_key=api_key)

    # System prompt
    system_prompt = f"""
How confident are you these values belong in a column of: {context}?

Scoring:
- 1.0 = Definitely belongs
- 0.0 = Definitely does not belong

Judge absolute plausibility, not statistical rarity.

Return confidence score and index as given in the input.
""".strip()
    
    # Process unique values in batches
    batch_size = _get_batch_size(len(unique_values))
    value_confidence = {}  # {value: confidence}

    for batch_start in range(0, len(unique_values), batch_size):
        batch = unique_values[batch_start:batch_start + batch_size]

        # Build list of values for prompt
        values_json = json.dumps([
            {"index": idx, "value": str(v)}
            for idx, v in enumerate(batch)
        ])

        # Call OpenAI API
        response = client.beta.chat.completions.parse(
            model = 'gpt-5-mini',
            seed = 42,
            reasoning_effort = "minimal",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": values_json}
            ],
            response_format=SemanticResponse
        )

        # Extract scores
        for score_item in response.choices[0].message.parsed.scores:
            value = batch[score_item.index]
            value_confidence[value] = score_item.confidence
            
    # Find outliers (confidence < threshold)
    outlier_values = {v: c for v, c in value_confidence.items() if c < threshold}

    # Build outliers list for report and track affected rows
    rows_to_delete = []

    for value, confidence in outlier_values.items():
        # Find rows with this value
        affected_rows = df_work[df_work[column] == value].index.tolist()

        report['outliers'].append({
            'value': value,
            'confidence': confidence,
            'n_affected_rows': len(affected_rows)
        })

        report['outliers_detected'] += 1
        report['rows_affected'] += len(affected_rows)

        # Apply action
        if action == 'nan':
            df_work.loc[df_work[column] == value, column] = np.nan
        elif action == 'delete':
            rows_to_delete.extend(affected_rows)

    # Delete rows if action is 'delete'
    if action == 'delete' and rows_to_delete:
        df_work = df_work.drop(rows_to_delete).reset_index(drop=True)
        report['rows_deleted'] = len(rows_to_delete)

    # Terminal output: end
    print("✓")

    return df_work, report

# =============================================================================
# Helper Functions (Private)
# =============================================================================

def _get_batch_size(n_unique_values: int) -> int:
    """
    Get batch size depending on number of unique values (n_unique_values)
    """
    if n_unique_values <= 20:
        return 20
    elif n_unique_values <= 300:
        return 30
    else:
        return 50