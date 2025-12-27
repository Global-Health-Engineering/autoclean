# Imported libraries
import pandas as pd
import numpy as np

"""
Post-Processing: Polish data after cleaning pipeline

This function is the LAST step after all cleaning.
It rounds numeric columns to match original precision.

Steps applied:
    1. Round numeric columns to match original decimal places
    2. Restore integers (1.0 → 1)

Usage:
    df_final, report = postprocess_data(df_cleaned, df_original)
"""


def postprocess_data(df_cleaned: pd.DataFrame, 
                     df_original: pd.DataFrame) -> tuple:
    """
    Polish cleaned data to match original formatting.
    
    Parameters:
        df_cleaned: DataFrame after cleaning pipeline
        df_original: Original DataFrame (from preprocess_data)
    
    Returns:
        (df, report): Polished DataFrame and report dict
    """
    
    # Terminal output: start
    print("Postprocessing... ", end="", flush=True)
    
    df = df_cleaned.copy()
    
    # Initialize report
    report = {
        'changes': []
    }
    
    for col in df.select_dtypes(include=[np.number]).columns:
        
        # Find matching original column (handles cleaned names)
        original_col = _match_column(col, df_original.columns)
        if original_col is None:
            continue
        
        original_data = df_original[original_col].dropna()
        if len(original_data) == 0:
            continue
        
        # Check if original was integer
        if _is_integer(original_data):
            df[col] = df[col].round(0).astype('Int64')
            report['changes'].append({'column': col, 'action': 'integer'})
        else:
            # Round to original decimal places
            decimals = _get_decimals(original_data)
            df[col] = df[col].round(decimals)
            report['changes'].append({'column': col, 'action': f'{decimals} decimals'})
    
    # Terminal output: end
    print("✓")
    
    return df, report


def _match_column(name: str, original_columns) -> str:
    """Match cleaned column name to original."""
    if name in original_columns:
        return name
    
    # Compare without spaces/underscores (handles clean_names conversion)
    clean = name.lower().replace('_', '').replace(' ', '')
    for orig in original_columns:
        if orig.lower().replace('_', '').replace(' ', '') == clean:
            return orig
    return None


def _is_integer(series: pd.Series) -> bool:
    """Check if series contains only integers."""
    try:
        return all(float(x) == int(float(x)) for x in series)
    except (ValueError, TypeError):
        return False


def _get_decimals(series: pd.Series) -> int:
    """Get maximum decimal places in series."""
    decimals = 0
    for val in series:
        try:
            s = str(float(val))
            if '.' in s:
                d = len(s.split('.')[1].rstrip('0') or '0')
                decimals = max(decimals, d)
        except:
            pass
    return decimals