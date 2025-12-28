# Imported libraries
import pandas as pd
import numpy as np
import janitor  # Python library PyJanitor

"""
Post-Processing: Polish data after cleaning pipeline

This function is the last step after all cleaning.
It rounds numeric columns to match original precision.

Steps applied:
    1. Round numeric columns to match original decimal places
    2. Restore integers (1.0 → 1), if the original column had integers 

Parameters:
    df_cleaned: Dataframe after cleaning pipeline
    df_original: Original dataframe (from Pre_Processing.py)
    clean_names: Must match the clean_names parameter used in Pre_Processing.py (default: True)

Returns:
    Final (polished) dataframe and final report (as tuple)
"""

# =============================================================================
# Main Function (Public)
# =============================================================================

def postprocess_data(df_cleaned: pd.DataFrame, 
                     df_original: pd.DataFrame,
                     clean_names: bool = True) -> tuple:
    # Terminal output: start
    print("Postprocessing... ", end="", flush=True)
    # Note: With flush = True, print is immediately

    # Work with copy of df_cleaned, s.t. df_cleaned stayes unchanged 
    df = df_cleaned.copy()
    
    # Clean column names in original dataframe (if clean_names = true in Pre_Processing.py)
    if clean_names:
        df_original = df_original.clean_names()
    # Note: clean_names() (from Pyjanitor) converts to lowercase, replaces spaces with underscores
    
    # Initialize report (as dictionary)
    report = {
        'changes': []
    }
    
    # Loop through numeric columns
    for col in list(df.select_dtypes(include = np.number).columns):
    # Note: .select_dtypes(include = np.number) returns a dataframe with numerical columns 
    #       .columns gets the indexes of the numerical columns (as pandas Index object)
    #       list() convert to list
        
        # Get column of original data (as pd.Series), without NaN values
        original_data = df_original[col].dropna()
        
        # Check if original_data contains only integer → restore to integer
        if _is_integer(original_data):
            df[col] = df[col].round(0).astype('Int64')
            # Note: .round(0) rounds all elements of the series to 0 decimal places (needed for imputed values)
            #.      .astype('Int64) converts all elements to integers or keeps NaN values 

            report['changes'].append({'column': col, 'action': 'restore to integer'})
            # Note: In the dict report the value of 'changes' is a list of dict

        # Otherwise → round to original decimal places
        else:
            decimals = _get_decimals(original_data)
            df[col] = df[col].round(decimals)
            report['changes'].append({'column': col, 'action': f'{decimals} decimals'})
    
    # Terminal output: end
    print("✓")
    
    return df, report

# =============================================================================
# Helper Functions (Private)
# =============================================================================

def _is_integer(series: pd.Series) -> bool:
    """Check if series contains only integers"""
    for x in series:
        if x % 1 != 0:
            return False
    return True

def _get_decimals(series: pd.Series) -> int:
    """Get maximum decimal places in series"""

    # Apply rounding up to 4 decimals until rounded values equal to original.
    # If there are values with more than 4 decimals, just use return 4. 
    for d in range(0, 4):
        if (series.round(d) == series).all():
            # Note: .all() converts bool Series to True if all values in Series == True otherwise False 
            return d
    return 4
