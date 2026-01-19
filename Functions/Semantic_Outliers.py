# Imported libraries
import pandas as pd
import numpy as np
from openai import OpenAI
from pydantic import BaseModel
import json

# Needed to load API Key from .env
import os
from dotenv import load_dotenv

"""
Semantic Outliers: Detect semantically invalid values using LLM reasoning

This function checks if values in a column make semantic sense given the context.
For example:
- Blood pressure of 0 → physically impossible
- Country "Freelance consultant" → not a country
- Age of -5 → impossible

Parameters:
    df: DataFrame to check
    column: Column to check for semantic outliers
    context: Description of what valid values look like (e.g., "Blood pressure in mmHg, valid range 60-180")
    threshold: Values with confidence below this are considered outliers (default: 0.5)
    action: 'nan' (replace with NaN) or 'delete' (remove entire row)

Returns:
    Cleaned dataframe and report (as tuple)
"""

# =============================================================================
# Pydantic Schema for Structured Output
# =============================================================================

class SemanticScore(BaseModel):
    """Single value score"""
    index: int          # Index of value in batch
    confidence: float   # 0.0 = invalid, 1.0 = valid

class SemanticResponse(BaseModel):
    """Structured output for semantic validation"""
    scores: list[SemanticScore]

# =============================================================================
# Main Function (Public)
# =============================================================================

def handle_semantic_outliers(df: pd.DataFrame,
                             column: str,
                             context: str,
                             threshold: float = 0.5,
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
              'total_rows': len(df_work),
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
    system_prompt = f"""You are a data quality expert checking if values are semantically valid.

COLUMN CONTEXT: {context}

Score each value's validity:
- 1.0 = Definitely valid
- 0.7-0.9 = Likely valid
- 0.4-0.6 = Uncertain
- 0.1-0.3 = Likely invalid
- 0.0 = Definitely invalid (impossible, nonsense, wrong data type)

Be strict. If a value doesn't make sense at all for this column, score it low."""

    # Process unique values in batches
    batch_size = 50
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
            model="gpt-4o",
            temperature=0.0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": values_json}
            ],
            response_format=SemanticResponse
        )

        # Extract scores
        for score_item in response.choices[0].message.parsed.scores:
            value = batch[score_item.index]
            confidence = max(0.0, min(1.0, score_item.confidence))
            value_confidence[value] = confidence

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
            'rows': affected_rows
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