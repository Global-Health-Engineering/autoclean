# Imported libraries
import pandas as pd
import janitor  # PyJanitor - extends pandas with cleaning methods

"""
Pre-Processing: Prepare data before cleaning pipeline

This function is the FIRST step before any cleaning.
It returns three items:
    - df_original: Untouched copy for reference (used in post-processing)
    - df: Preprocessed copy ready for cleaning
    - report: Dict with preprocessing details

Steps applied:
    1. Load data from file
    2. Strip whitespace from string columns
    3. Standardize missing values ("NA", "", "-", "null", etc. → NaN)
    4. Remove completely empty rows
    5. Remove completely empty columns
    6. Clean column names (lowercase, underscores)
"""


def preprocess_data(filepath: str, clean_names: bool = True) -> tuple:
    """
    Load and preprocess data for cleaning pipeline.
    
    Parameters:
        filepath: Path to CSV or Excel file
        clean_names: If True, standardize column names (default: True)
    
    Returns:
        (df_original, df, report): Original DataFrame, preprocessed DataFrame, and report dict
    """
    
    # Terminal output: start
    print("Preprocessing... ", end="", flush=True)
    
    # Step 1: Load data
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    elif filepath.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(filepath)
    else:
        print("ERROR")
        raise ValueError(f"Unsupported file type: {filepath}")
    
    # Store original (untouched copy)
    df_original = df.copy()
    
    # Initialize report
    report = {
        'original_shape': df_original.shape,
        'final_shape': None,
        'rows_removed': 0,
        'cols_removed': 0,
        'columns_renamed': []
    }
    
    # Step 2: Strip whitespace from string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Step 3: Standardize missing values
    # Common representations of missing data → NaN
    missing_values = ['', ' ', 'NA', 'N/A', 'na', 'n/a', 'NaN', 'nan', 
                      'NULL', 'null', 'None', 'none', '-', '--', '.']
    df = df.replace(missing_values, pd.NA)
    
    # Step 4 & 5: Remove empty rows and columns (PyJanitor)
    df = df.remove_empty()
    # Note: remove_empty() removes rows AND columns that are completely empty
    
    # Step 6: Clean column names (PyJanitor)
    original_col_names = df.columns.tolist()
    if clean_names:
        df = df.clean_names()
        # Note: clean_names() converts to lowercase, replaces spaces with underscores
        # Example: "First Name" → "first_name", "Date of Birth" → "date_of_birth"
        
        # Track renamed columns
        for old, new in zip(original_col_names, df.columns):
            if old != new:
                report['columns_renamed'].append({'old': old, 'new': new})
    
    # Update report
    report['final_shape'] = df.shape
    report['rows_removed'] = len(df_original) - len(df)
    report['cols_removed'] = len(df_original.columns) - len(df.columns)
    
    # Terminal output: end
    print("✓")
    
    return df_original, df, report