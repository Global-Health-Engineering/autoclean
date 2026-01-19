# Imported libraries 
import pandas as pd
import numpy as np

"""
Handle outliers in numerical columns

If a numerical value is outside the range [q1 - multiplier * iqr, q3 + multiplier * iqr] = [lower bound, upper bound], 
it's considered as a outlier

The parameter 'multiplier' is set by default to 1.5 (standard in statistics)

Two methods: 
    1. method = 'winsorize' (default):
    Outlier is replaced by lower bound if it's smaller than lower bound else with upper bound

    2. method = 'delete'
    Rows containing an outlier are removed

Returns:
    Cleaned dataframe and report (as tuple)
"""

# ============================================================================
# Main Function (Public)
# ============================================================================

def handle_outliers(df: pd.DataFrame, method: str = 'winsorize', multiplier: float = 1.5) -> tuple:
    # Terminal output: start
    print("Handling outliers... ", end="", flush=True)
    # Note: With flush = True, print is immediately
    
    # Initialize report
    report = {'method': method,
              'multiplier': multiplier,
              'total_outliers': 0,
              'rows_deleted': 0,
              'column_bounds': [],
              'outliers': []}
    
    # Work with copy, to not modify input df 
    df_work = df.copy()

    # Get indexes of numerical columns
    i_num_cols = list(df_work.select_dtypes(include = np.number).columns)
    # Note: .select_dtypes(include = np.number) returns a dataframe with numerical columns 
    #       .columns gets the indexes of the numerical columns (as pandas Index object)
    #       list() convert to list
    
    # Get # of rows from original dataframe 
    n_original_row = len(df_work)
    
    for idx_col in i_num_cols:
        # Calculate 25th percentile q1, 75th percentile q3 & the interquartile range iqr (of column with index idx_col)
        q1 = df_work[idx_col].quantile(0.25)
        q3 = df_work[idx_col].quantile(0.75)
        iqr = q3 - q1

        # Calculate lower & upper bounds (of column with index idx_col) 
        lower_bound = q1 - (multiplier * iqr)
        upper_bound = q3 + (multiplier * iqr)
        
        # Get boolean mask (typ: Series), where for each element (of column with index idx_col) a bool tells if element is outlier 
        outliers = (df_work[idx_col] < lower_bound) | (df_work[idx_col] > upper_bound) 
        # Note: In pandas logical operators can be applied to rows, columns & dataframes and are executed element wise, 
        #       such that the output is a series or dataframe with booleans.
        #       The element wise operator of 'or' is |.  
        
        # Get # of outliers (of column with index idx_col) 
        n_outliers = outliers.sum()

        # Update report
        report['total_outliers'] += n_outliers
        report['column_bounds'].append({'column': idx_col,
                                        'lower_bound': lower_bound,
                                        'upper_bound': upper_bound})
        # Note: In the dict report the value of 'column_bounds' is a list of dict

        if n_outliers > 0:
            if method == 'winsorize':
                # Get boolean mask (typ: Series), for the two types of outliers (of column with index idx_col)
                lower_mask = (df_work[idx_col] < lower_bound)
                upper_mask = (df_work[idx_col] > upper_bound)
                
                # Track outliers (for report)
                for idx_row in list(df_work[lower_mask].index):
                    # Note: list(df_work[mask].index) gives row indexes, where mask is true (as list)

                    # Add outliers to report
                    report['outliers'].append({'row': idx_row,
                                               'column': idx_col,
                                               'original_value': df_work.at[idx_row, idx_col],
                                               'new_value': lower_bound,
                                               'bound': 'lower'})
                    # Note: In the dict report the value of 'outliers' is a list of dict

                for idx_row in list(df_work[upper_mask].index):
                    # Note: list(df_work[mask].index) gives row indexes, where mask is true (as list)

                    # Add outliers to report
                    report['outliers'].append({'row': idx_row,
                                               'column': idx_col,
                                               'original_value': df_work.at[idx_row, idx_col],
                                               'new_value': upper_bound,
                                               'bound': 'upper'})
                    # Note: In the dict report the value of 'outliers' is a list of dict

                # Replace outliers with bound values
                df_work.loc[lower_mask, idx_col] = lower_bound 
                df_work.loc[upper_mask, idx_col] = upper_bound
                # Note: df_work.loc[mask, col] creates a series (w.r.t the original dataframe df) of column col with mask applied
                #       The '=' is executed element wise 
 
            elif method == 'delete':
                # Track outliers (for report)
                for idx_row in list(df_work[outliers].index):
                    # Note: list(df_work[mask].index) gives row indexes, where mask is true (as list)

                    # Add outliers to report 
                    report['outliers'].append({
                        'row': idx_row,
                        'column': idx_col,
                        'original_value': df_work.at[idx_row, idx_col],
                        'new_value': 'None, deleted whole row',
                        'bound': 'lower' if df_work.at[idx_row, idx_col] < lower_bound else 'upper'}) # = Ternary Operator (One-Line If-Else), structure: ... = value_1 if condition else value_2
                    # Note: In the dict report the value of 'outliers' is a list of dict

                # Remove rows with outliers
                df_work = df_work[~outliers]
                # Note: '~' flips True & False
                #       df_work[mask] gets dataframe with rows for which mask is true
    
    if method == 'delete':
        # Reset index of rows & don't keep the old ones as a new column (drop = true)
        df_work = df_work.reset_index(drop = True)
        report['rows_deleted'] = n_original_row - len(df_work)
    
    # Terminal output: end
    print("✓")
    
    return df_work, report