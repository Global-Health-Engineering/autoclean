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
    print("Handling duplicates... ", end="", flush = True)
    # Note: With flush = True, print is immediately

    # Work with copy, to not modify input df 
    df_work = df.copy()

    # Get # of rows & columns from original dataframe 
    n_original_rows = len(df_work)
    n_original_cols = len(df_work.columns)
    
    # Remove duplicate rows and reset index
    df_work = df_work.drop_duplicates().reset_index(drop = True)
    rows_removed = n_original_rows - len(df_work)

    # Remove duplicate columns 
    # Note: Store original dtypes of columns as a list because transpose converts all to object
    original_dtypes = df_work.dtypes
    # Note: df_work.dtypes returns a series, where each value is the type of the column and the indexes are the corresponding column name
    
    df_work = df_work.T.drop_duplicates().T
    # Note: First .T (columns become rows) → .drop_duplicates() (remove duplicate rows) → Second .T (rows become columns)
    
    # Restore original dtypes of columns for remaining columns
    for col in list(df_work.columns):
        df_work[col] = df_work[col].astype(original_dtypes[col])
    
    cols_removed = n_original_cols - len(df_work.columns)

    # Build report
    report = {'rows_removed': rows_removed,
              'cols_removed': cols_removed}
    
    # Terminal output: end
    print("✓")
    
    return df_work, report