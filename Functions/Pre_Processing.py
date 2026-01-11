# Imported libraries
import pandas as pd
import numpy as np
import janitor  # Python library PyJanitor 

"""
Pre-Processing: Prepare data before cleaning 

This function is the first step before any cleaning.
It returns three items (as tuple):
    - df_original: Untouched dataframe for reference (used in post-processing)
    - df: Preprocessed dataframe ready for cleaning
    - report: Dict with preprocessing details

Parameters:
    filepath: Path to CSV file
    clean_names: If True, standardize column names (default: True)
    
Steps applied:
    1. Load data from file
    2. Strip whitespace from string columns
    3. Standardize missing values ("NA", "", "-", "null", etc. → NaN)
    4. Remove completely empty rows
    5. Remove completely empty columns
    6. Clean column names (lowercase, underscores)
"""
# =============================================================================
# Main Function (Public)
# =============================================================================

def preprocess_data(filepath: str, clean_names: bool = True) -> tuple:
    # Terminal output: start
    print("Preprocessing... ", end = "", flush = True)
    # Note: With flush = True, print is immediately

    # Load data (only CSV file otherwise error)
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath, na_values = [' ', '  ', '   ', '    ', '     ', 'none', '-', '--', '.', 'na'])
    # Note: pd.read_csv converts by default values like: ““, “#N/A”, “#N/A N/A”, “#NA”, “-1.#IND”, “-1.#QNAN”, “-NaN”, “-nan”, “1.#IND”, “1.#QNAN”, “<NA>”, “N/A”, “NA”, “NULL”, “NaN”, “None”, “n/a”, “nan”, “null“ 
    # by default to np.nan. Additionally also the values from the list na_values. 

    else:
        raise ValueError(f"{filepath} = unsupported file type (only CSV)")

    # Store original dataframe
    df_original = df.copy()
    
    # Initialize report (as dictionary)
    report = {'original_shape': df_original.shape,
              'final_shape': None,
              'rows_removed': 0,
              'cols_removed': 0,
              'columns_renamed': []}
    # Note: .shape = (#rows, #columns)

    # Strip whitespace from string columns
    for col in list(df.select_dtypes(include = 'object').columns):
        df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)
    # Note: select_dtypes(include = 'object') returns string columns or mixed type columns 
    #       .columns returns the column names (as pandas Index)
    #       list() convert to list 
    #       .map(func) runs function on every cell in column
    #       Lambda function: strips whitespace if value is string, otherwise returns input 
    #       x.strip() removes leading/trailing whitespace
    #       isinstance(x, str) checks if x is a string

    # Remove empty rows and columns (using remove_empty() from PyJanitor)
    df = df.remove_empty()
    
    # Get original column names 
    original_col_names = df.columns
    
    # Clean column names (if clean_names = true) 
    if clean_names:
        df = df.clean_names()
        # Note: clean_names() (from Pyjanitor) converts to lowercase, replaces spaces with underscores
        
        # Get cleaned column names
        cleaned_col_names = df.columns 

        # Track renamed columns for report 
        for old, new in zip(original_col_names, cleaned_col_names):
            if old != new:
                report['columns_renamed'].append({'old': old, 'new': new})
        # Note: In the dict report the value of 'columns_renamed' is a list of dict
        
    # Update report
    report['final_shape'] = df.shape
    report['rows_removed'] = len(df_original) - len(df)
    report['cols_removed'] = len(df_original.columns) - len(df.columns)
    
    # Terminal output: end
    print("✓")
    
    return df_original, df, report