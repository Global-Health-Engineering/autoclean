"""
Post-Processing: Polish data after cleaning pipeline

This function is the last step after all cleaning.
It rounds numeric columns to match original precision (if rounding = True), cleans column names (if clean_names = True) and export the final df as CSV.

Steps applied:
    1. Round numeric columns to match original decimal places (if rounding = True)
    2. Restore integers (1.0 → 1), if the original column had integers (if rounding = True)
    3. Clean column names (lowercase with underscores) (if clean_names = True)
    4. Export df as CSV to specified location (output_filepath)

Parameters:
    df_cleaned: Dataframe after cleaning pipeline
    df_original: Original dataframe (from Pre_Processing.py)
    rounding: If True, rounding is applied (default: False)
    clean_names: If True, standardize column names (default: False)
    output_filepath: Filepath where df as CSV is saved

Notes: If Outliers.py and or Missing_Values.py was applied, recommended to set rounding = True. 

Returns:
    report (as dictionary)
"""

# Imported libraries
import pandas as pd
import numpy as np
import janitor  # Python library PyJanitor

# =============================================================================
# Main Function (Public)
# =============================================================================

def postprocess_data(df_cleaned: pd.DataFrame, 
                     df_original: pd.DataFrame,
                     output_filepath: str,
                     clean_names: bool = False,
                     rounding: bool = False) -> dict:
    # Terminal output: start
    print("Postprocessing... ", end="", flush=True)
    # Note: With flush = True, print is immediately

    # Work with copy of df_cleaned, s.t. df_cleaned stayes unchanged 
    df = df_cleaned.copy()
 
    # Initialize report (as dictionary)
    report = {'changes': [],
              'columns_renamed': [], 
              'final_shape': None}
    
    if rounding:
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

                report['changes'].append({'column': col, 'action': 'Restored to integer'})
                # Note: In the dict report the value of 'changes' is a list of dict

            # Otherwise → round to original decimal places
            else:
                decimals = _get_decimals(original_data)
                df[col] = df[col].round(decimals)
                report['changes'].append({'column': col, 'action': f'Rounded to {decimals} decimals'})
    
    # Clean column names (if clean_names = True)
    if clean_names:
        # Get original column names
        original_col_names = df.columns
        
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
    
    # Export final df as csv to specified location (output_filepath)
    df.to_csv(output_filepath, index = False)
    # Note: index = False leads to no row index in final csv 

    # Terminal output: end
    print("✓")
    
    return report

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
