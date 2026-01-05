# Imported libraries 
import pandas as pd

"""
Remove exact duplicate rows and columns

Note: Regarding exact duplicate columns, only the values in the column need to match, the column name can be different. 

Returns:
    Cleaned dataframe and report (as tuple)
"""

# ============================================================================
# Main Function (Public)
# ============================================================================

def handle_duplicates(df: pd.DataFrame) -> tuple:
    # Terminal output: start
    print("Handling duplicates... ", end="", flush=True)
    # Note: With flush = True, print is immediately

    # Get # of rows & columns from original dataframe 
    n_original_rows = len(df)
    n_original_cols = len(df.columns)
    
    # Remove duplicate rows and reset index
    df = df.drop_duplicates().reset_index(drop=True)
    rows_removed = n_original_rows - len(df)
    
    # Remove duplicate columns 
    df = df.T.drop_duplicates().T
    # Note: First .T (columns become rows) → .drop_duplicates() (remove duplicate rows) → Second .T (rows become columns)
    cols_removed = n_original_cols - len(df.columns)
    
    # Build report
    report = {'rows_removed': rows_removed,
              'cols_removed': cols_removed}
    
    # Terminal output: end
    print("✓")
    
    return df, report