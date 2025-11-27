# Imported libraries 
import pandas as pd

'''
Remove exact duplicate rows 
''' 

# ============================================================================
# Main Function (Public)
# ============================================================================

def handle_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    # Get # of rows in the original file 
    n_original_rows = len(df)
    
    # Remove duplicates and reset index
    df = df.drop_duplicates().reset_index(drop=True)
    
    duplicates_removed = n_original_rows - len(df)
    
    print(f"Removed {duplicates_removed} duplicate rows")
    
    return df
