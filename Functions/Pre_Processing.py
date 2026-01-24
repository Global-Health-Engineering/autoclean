"""
Pre-Processing: Prepare data before cleaning 

This function is the first step before any cleaning.
It returns three items (as tuple):
    - df_original: Untouched dataframe for reference (used in post-processing)
    - df: Preprocessed dataframe ready for cleaning
    - report: Dict with preprocessing details

Parameters:
    input_filepath: Filepath to inptu CSV file (dataset to clean)
    
Steps applied:
    1. Load data from file & Standardize missing values ("NA", "", "-", "null", etc. → NaN)
    2. Strip whitespace from string columns
    3. Remove completely empty rows
    4. Remove completely empty columns
"""

# Imported libraries
import pandas as pd
import numpy as np
import janitor  # Python library PyJanitor 

# =============================================================================
# Main Function (Public)
# =============================================================================

def preprocess_data(input_filepath: str) -> tuple:
    # Terminal output: start
    print("Preprocessing... ", end = "", flush = True)
    # Note: With flush = True, print is immediately

    # Load data (only CSV file otherwise error)
    if input_filepath.endswith('.csv'):
        df = pd.read_csv(input_filepath, na_values = [' ', '  ', '   ', '    ', '     ', 'none', '-', '--', '.', 'na'])
    # Note: pd.read_csv converts values like: ““, “#N/A”, “#N/A N/A”, “#NA”, “-1.#IND”, “-1.#QNAN”, “-NaN”, “-nan”, “1.#IND”, “1.#QNAN”, “<NA>”, “N/A”, “NA”, “NULL”, “NaN”, “None”, “n/a”, “nan”, “null“ by default to np.nan.
    # Additionally also the values from the list na_values. 

    else:
        raise ValueError(f"{input_filepath} = unsupported file type (only CSV)")

    # Store original dataframe
    df_original = df.copy()

    # Initialize report (as dictionary)
    report = {'original_shape': df_original.shape,
              'input_filepath': input_filepath,
              'rows_removed': 0,
              'cols_removed': 0}
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
        
    # Update report
    report['rows_removed'] = len(df_original) - len(df)
    report['cols_removed'] = len(df_original.columns) - len(df.columns)
    
    # Terminal output: end
    print("✓")
    
    return df, df_original, report