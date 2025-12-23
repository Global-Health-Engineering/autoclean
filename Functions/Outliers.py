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
"""
# ============================================================================
# Main Function (Public)
# ============================================================================

def handle_outliers(df: pd.DataFrame, method: str = 'winsorize', multiplier: float = 1.5) -> pd.DataFrame:
    # Get indexes of numerical columns
    i_num_cols = list(df.select_dtypes(include = np.number).columns)
    # Note: .select_dtypes(include = np.number) returns a dataframe with numerical columns 
    #       .columns gets the indexes of the numerical columns (as pandas Index object)
    #       list() convert to list
    total_outliers = 0
    
    for idx in i_num_cols:
        # Calculate 25th percentile q1, 75th percentile q3 & the interquartile range iqr (of column with index i)
        q1 = df[idx].quantile(0.25)
        q3 = df[idx].quantile(0.75)
        iqr = q3 - q1

        # Calculate lower & upper bounds (of column with index i) 
        lower_bound = q1 - (multiplier * iqr)
        upper_bound = q3 + (multiplier * iqr)
        
        # Get boolean mask (typ: Series), where for each element (of column with index i) a bool tells if element is outlier 
        outliers = (df[idx] < lower_bound) | (df[idx] > upper_bound) 
        # Note: In pandas logical operators can be applied to rows, columns & dataframes and are executed element wise, 
        #       such that the output is a series or dataframe with booleans.
        #       The element wise operator of 'or' is |.  
        
        # Get # of outliers (of the column with index i) & add to total outliers
        n_outliers = outliers.sum()
        total_outliers += n_outliers

        if n_outliers > 0:
            print(f"Column {idx} (with lower bound = {lower_bound:.2f} & upper bound = {upper_bound:.2f}) has {n_outliers} outliers")
            
            if method == 'winsorize':
                # Get boolean mask (typ: Series), for the two types of outliers (of column with index i)
                lower_mask = (df[idx] < lower_bound)
                upper_mask = (df[idx] > upper_bound)
                
                # Replace outliers with bound values
                df.loc[lower_mask, idx] = lower_bound 
                df.loc[upper_mask, idx] = upper_bound
                # Note: df.loc[mask, col] creates a series (w.r.t the original dataframe df) of column col with mask applied
                #       The '=' is executed element wise 
 
            elif method == 'delete':
                # Remove rows with outliers
                df = df[~outliers]
                # Note: '~' flips True & False
                #       df[mask] gets dataframe with rows for which mask is true
    
    if method == 'delete':
        # Reset index of rows & don't keep the old ones as a new column (drop = true)
        df = df.reset_index(drop = True)
        
    print(f"{total_outliers} outliers handled")
    return df
