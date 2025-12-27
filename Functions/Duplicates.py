# Imported libraries 
import pandas as pd

"""
Remove exact duplicate rows and columns
"""

# ============================================================================
# Main Function (Public)
# ============================================================================

def handle_duplicates(df: pd.DataFrame) -> tuple:
    """
    Returns:
        (df, report): Cleaned DataFrame and report dict
    """
    
    # Terminal output: start
    print("Handling duplicates... ", end="", flush=True)
    
    # Get # of rows & columns in the original file 
    n_original_rows = len(df)
    n_original_cols = len(df.columns)
    
    # Remove duplicate rows and reset index
    df = df.drop_duplicates().reset_index(drop=True)
    rows_removed = n_original_rows - len(df)
    
    # Remove duplicate columns and reset index 
    df = df.T.drop_duplicates().T
    # Note: .T transposes (rows become columns), drop_duplicates removes duplicate rows,
    #       .T transposes back (columns become rows again)
    cols_removed = n_original_cols - len(df.columns)
    
    # Build report
    report = {
        'rows_removed': rows_removed,
        'cols_removed': cols_removed
    }
    
    # Terminal output: end
    print("✓")
    
    return df, report