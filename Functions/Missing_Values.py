# Imported libraries 
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.experimental import enable_iterative_imputer 
# Note: from sklearn.experimental import enable_iterative_imputer needed to enable IterativeImputer (as its marked as experimental by sklearn) 
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestRegressor

"""
Handle missing values in the dataframe

To impute missing values with handle_missing_values, there are three important parameters. One is columns which can be used if imputation is needed only on certain columns and not all. The other two are method_num & method_categ which choose the methods for imputation of numerical / categorical columns. 

Column Selection (columns):
    - None: Process all columns (default)
    - ['col1', 'col2', ...]: Process only specified columns

Methods for numerical columns (method_num):
    - 'mean': Fill with column average (default)
    - 'median': Fill with column median  
    - 'mode': Fill with most frequent value
    - 'delete': Remove rows with numerical missing values
    - 'knn': K-Nearest Neighbors imputation
    - 'missforest': Random Forest iterative imputation
    - 'false': Skip all numerical columns
    
Methods for categorical columns (method_categ):
    - 'mode': Fill with most frequent value (default)
    - 'delete': Remove rows with categorical missing values
    - 'knn': K-Nearest Neighbors imputation
    - 'missforest': Random Forest iterative imputation
    - 'false': Skip all categorical columns
    
Note on remaining parameters for MissForest and KNN: 
    - n_neighbors : Number of neighbors for KNN imputation (default=5)
    - max_iter : Maximum iterations for MissForest imputation (default=10)
    - n_estimators : Number of trees in Random Forest for MissForest (default=10)

Returns: 
    Cleaned datafram and report (as tuple)

For further information about the algorithms KNN & MissForest, see in the folder Additional_Information
"""

# ============================================================================
# Main Function (Public)
# ============================================================================

def handle_missing_values(df: pd.DataFrame, 
                          method_num: str = 'mean', 
                          method_categ: str = 'mode',
                          columns: list = None,
                          n_neighbors: int = 15, 
                          max_iter: int = 15,
                          n_estimators: int = 50) -> tuple:
    # Terminal output: start
    print("Handling missing values... ", end="", flush=True)
    # Note: With flush = True, print is immediately

    # Initialize report
    report = {'method_num': method_num,
              'method_categ': method_categ,
              'num_missing_before': 0,
              'categ_missing_before': 0,
              'rows_deleted': 0,
              'imputations_num': [],
              'imputations_categ': []}
    
    # If specific columns are chosen, add to report 
    if columns != None: 
        report['columns'] = columns

    # Get indexes of numerical & categorical columns
    i_num_cols = list(df.select_dtypes(include = np.number).columns)
    # Note: .select_dtypes(include = np.number) returns a dataframe with numerical columns 
    #       .columns gets the indexes of the numerical columns (as pandas Index object)
    #       list() convert to list
    i_categ_cols = list(df.select_dtypes(include = ['object', 'category', 'bool']).columns)
    # Note: .select_dtypes(include = ['object', 'category', 'bool']) returns a dataframe with categorical columns
    #       .columns gets the indexes of the numerical columns (as pandas Index object)
    #       list() convert to list

    # Adjust the i_num_cols / i_categ_cols if specific columns are selected to impute 
    if columns != None:
        # Keep only columns that are in the specified list (columns)
        i_num_cols = [col for col in i_num_cols if col in columns]
        i_categ_cols = [col for col in i_categ_cols if col in columns]

    # Count total missing values 
    n_num_missing = df[i_num_cols].isna().sum().sum() 
    # Note: df[i_num_cols] returns a dataframe with (selected) numerical columns 
    #       .isna() returns a dataframe of True / False, with True for missing values 
    #       First .sum() sums each column
    #       Second .sum() sums all the column totals
    #       if i_num_cols is empty, n_num_missing = 0
    n_categ_missing = df[i_categ_cols].isna().sum().sum() 
    # Note: df[i_categ_cols] returns a dataframe with (selected) categorical columns 
    #       .isna() returns a dataframe of True / False, with True for missing values 
    #       First .sum() sums each column
    #       Second .sum() sums all the column totals
    #       if i_categ_cols is empty, n_categ_missing = 0
    n_total_missing = n_categ_missing + n_num_missing

    # Update report
    report['num_missing_before'] = n_num_missing
    report['categ_missing_before'] = n_categ_missing

    if n_total_missing == 0:
        print("✓")
        return df, report
    
    # If no numerical missing values, then set method_num to false
    if n_num_missing == 0: 
        method_num = 'false'

    # Execute numerical methods (if methode_num == 'false', then execution is skipped)
    if method_num != 'false':
        # Get boolean mask for missing values before numerical imputation (for report)
        mask_missing_before_num = df[i_num_cols].isna().copy() 
        
        if method_num == 'delete':
            # Get # of rows before numerical delete is applied (for report) 
            n_rows_before = len(df)

            df = _handle_numerical_delete(df, i_num_cols)

            # Update report 
            report['rows_deleted'] = n_rows_before - len(df)

            # Possible that n_categ_missing has changed through deleting rows 
            n_categ_missing = df[i_categ_cols].isna().sum().sum()

        elif method_num in ['mean', 'median', 'mode']:
            df = _handle_numerical_statistical(df, i_num_cols, method_num)
            
        elif method_num == 'knn':
            df = _handle_numerical_knn(df, i_num_cols, n_neighbors)
            
        elif method_num == 'missforest':
            df = _handle_numerical_missforest(df, i_num_cols, max_iter, n_estimators)
    
    # Track for report data imputation (numerical) 
    if method_num not in ['false', 'delete']:
        for col in i_num_cols:
            for idx in df.index: # df.index gets row indexes 
                # Check if cell was missing before (mask_missing_before_num.at[idx, col]) and now has a value, i.e. was imputed (pd.notna(df.at[idx, col]))
                if mask_missing_before_num.at[idx, col] and pd.notna(df.at[idx, col]):
                    report['imputations_num'].append({'row': idx,
                                                      'column': col,
                                                      'new_value': df.at[idx, col],
                                                      'method': method_num})
                    # Note: Value of key 'imputations' in dict report is a list, in which each value is a dictionary 
    
    # If no categorical missing values, then set method_categ to false
    if n_categ_missing == 0: 
        method_categ = 'false'

    # Execute categorical methods (if methode_categ == 'false', then execution is skipped)
    if method_categ != 'false':
        # Get boolean mask for missing values before categorical imputation (for report)
        mask_missing_before_categ = df[i_categ_cols].isna().copy()

        if method_categ == 'delete':
            # Get # of rows before categorical delete is applied (for report) 
            n_rows_before = len(df)

            df = _handle_categorical_delete(df, i_categ_cols)
            
            # Update report 
            report['rows_deleted'] += n_rows_before - len(df)
            
        elif method_categ == 'mode':
            df = _handle_categorical_mode(df, i_categ_cols)
            
        elif method_categ == 'knn':
            df = _handle_categorical_knn(df, i_categ_cols, n_neighbors)
            
        elif method_categ == 'missforest':
            df = _handle_categorical_missforest(df, i_categ_cols, max_iter, n_estimators)
    
    # Track for report data imputation (categorical)
    if method_categ not in ['false', 'delete']:
        for col in i_categ_cols:
            for idx in df.index: # df.index gets row indexes 
                # Check if cell was missing before (mask_missing_before_categ.at[idx, col]) and now has a value, i.e. was imputed (pd.notna(df.at[idx, col]))
                if mask_missing_before_categ.at[idx, col] and pd.notna(df.at[idx, col]):
                    report['imputations_categ'].append({'row': idx,
                                                        'column': col,
                                                        'new_value': df.at[idx, col],
                                                        'method': method_categ})
                    # Note: Value of key 'imputations' in dict report is a list, in which each value is a dictionary

    # Terminal output: end
    print("✓")
    return df, report

# ============================================================================
# Helper Functions (Private)
# ============================================================================

def _handle_numerical_delete(df: pd.DataFrame, i_num_cols: list) -> pd.DataFrame:
    """
    Delete rows that have missing values in (selected) numerical columns 
    """
    
    # Get boolean mask (type: Series) with True if row has missing values in (selected) numerical columns & otherwise False
    mask = df[i_num_cols].isna().any(axis = 1)
    # Note: df[i_num_cols] gets a dataframe with (selected) numerical columns
    #       .isna() returns a dataframe of True / False, with True for missing values
    #       .any(axis = 1) convert each row (axis = 1) into a single bool (if any True in row --> True, otherwise --> False) 

    # Remove rows, where mask is True (missing numerical value(s))
    df = df[~mask].reset_index(drop=True)
    # Note: '~' flips True & False
    #       df[mask] gets dataframe with rows for which mask is true
    #       .reset_index(drop=True) resets indexes of rows & don't keep the old ones as a new column (drop = true) 
    
    return df

def _handle_numerical_statistical(df: pd.DataFrame, i_num_cols: list, method: str) -> pd.DataFrame:
    """
    Handle missing values in (selected) numerical columns with simple statistical methods (mean, median, mode)
    """

    for idx in i_num_cols:
        # Check if column idx has any missing number
        if df[idx].isna().any():
            if method == 'mean':
                # Calculate mean of column idx 
                fill_value = df[idx].mean() 
                
                # Fill missing value(s) in column idx with mean
                df[idx] = df[idx].fillna(fill_value)

            elif method == 'median':
                # Calculate median of column idx 
                fill_value = df[idx].median()

                # Fill missing value(s) in column idx with median
                df[idx] = df[idx].fillna(fill_value)

            elif method == 'mode':
                # Calculate the most frequent value in column idx, which returns series (can be multiple values if tie) of which the first value is taken ([0])
                fill_value = df[idx].mode()[0]

                # Fill missing value(s) in column idx with most frequent value
                df[idx] = df[idx].fillna(fill_value)
    
    return df

def _encode_categorical_columns(df: pd.DataFrame, i_categ_cols: list) -> tuple:
    """
    Encode (selected) categorical columns to numerical values
    """
    
    # Create encoder for (selected) categorical columns
    encoder = OrdinalEncoder()
    
    # Fit encoder and transform (selected) categorical columns 
    df[i_categ_cols] = encoder.fit_transform(df[i_categ_cols])
    
    return df, encoder

def _decode_categorical_columns(df: pd.DataFrame, i_categ_cols: list, encoder: OrdinalEncoder) -> pd.DataFrame:
    """
    Decode (selected) categorical columns from numerical values back to original categories
    """
    
    df[i_categ_cols] = df[i_categ_cols].round()
    # Note: KNN / MissForest may produce decimals, which need to be rounded to integers, to perform decoding 
    
    # Decode (selected) categorical columns back to original values
    df[i_categ_cols] = encoder.inverse_transform(df[i_categ_cols])
    
    return df

def _handle_numerical_knn(df: pd.DataFrame, i_num_cols: list, n_neighbors: int) -> pd.DataFrame:
    """
    Handle (selected) numerical columns with KNN imputation using all columns as features
    """
    
    # Work with copy of df to impute only (selected) numerical columns  
    df_work = df.copy()
    
    # Get indexes of all categorical columns 
    i_categ_cols = list(df_work.select_dtypes(include = ['object', 'category', 'bool']).columns)
    
    # Encode all categorical columns (if they exist), such that df_work is only numerical
    if len(i_categ_cols) > 0:
        df_work, encoder = _encode_categorical_columns(df_work, i_categ_cols)
    
    # Apply KNN imputation (fills all missing values, inlcuding orginially categorical columns)
    imputer = KNNImputer(n_neighbors = n_neighbors)
    df_imputed_array = imputer.fit_transform(df_work)
    
    # Convert back to DataFrame (KNNImputer returns np array)
    df_imputed = pd.DataFrame(df_imputed_array,
                              columns = df_work.columns,
                              index = df_work.index)
    
    # Update only (selected) numerical columns in original dataframe
    for idx in i_num_cols:
        df[idx] = df_imputed[idx]
    
    return df

def _handle_numerical_missforest(df: pd.DataFrame, i_num_cols: list, max_iter: int, n_estimators: int) -> pd.DataFrame:
    """
    Handle (selected) numerical columns with MissForest imputation using all columns as features
    """
    
    # Work with copy of df to impute only (selected) numerical columns
    df_work = df.copy()
    
    # Get indexes of all categorical columns
    i_categ_cols = list(df_work.select_dtypes(include = ['object', 'category', 'bool']).columns)
    
    # Encode categorical columns (if they exist), such that df_work is only numerical
    if len(i_categ_cols) > 0:
        df_work, encoder = _encode_categorical_columns(df_work, i_categ_cols)
    
    # Apply MissForest (fills all missing values, inlcuding orginially categorical columns)
    imputer = IterativeImputer(estimator = RandomForestRegressor(n_estimators = n_estimators, max_depth = 5, min_samples_leaf = 2, random_state = 0),
                               max_iter = max_iter, 
                               random_state = 0)
    # Note: random_state = 0 ensures reproducibility
    df_imputed_array = imputer.fit_transform(df_work.values)
    
    # Convert back to DataFrame (IterativeImputer returns np array)
    df_imputed = pd.DataFrame(df_imputed_array,
                              columns = df_work.columns,
                              index = df_work.index)
    
    # Update only (selected) numerical columns in original dataframe
    for idx in i_num_cols:
        df[idx] = df_imputed[idx]
    
    return df

def _handle_categorical_delete(df: pd.DataFrame, i_categ_cols: list) -> pd.DataFrame:
    """
    Delete rows that have missing values in (selected) categorical columns 
    """
    
    # Get boolean mask (type: Series) with True if row has missing values in (selected) categorical columns & otherwise False
    mask = df[i_categ_cols].isna().any(axis=1)
    
    # Remove rows, where mask is True (missing categorical value(s))
    df = df[~mask].reset_index(drop=True)
    
    return df

def _handle_categorical_mode(df: pd.DataFrame, i_categ_cols: list) -> pd.DataFrame:
    """
    Handle missing values in (selected) categorical columns with mode
    """
    
    for idx in i_categ_cols:
        # Check if column idx has any missing value
        if df[idx].isna().any():
            # Calculate the most frequent value in column idx
            fill_value = df[idx].mode()[0]

            # Fill missing value(s) in column idx with most frequent value
            df[idx] = df[idx].fillna(fill_value)
    
    return df

def _handle_categorical_knn(df: pd.DataFrame, i_categ_cols: list, n_neighbors: int) -> pd.DataFrame:
    """
    Handle (selected) categorical columns with KNN imputation using all columns as features
    """
    
    # Work with copy of df to impute only (selected) categorical columns
    df_work = df.copy()
    
    # Get indexes of all categorical columns 
    i_all_categ_cols = list(df_work.select_dtypes(include = ['object', 'category', 'bool']).columns)
    
    # Encode all categorical columns, such that df_work is only numerical
    df_work, encoder = _encode_categorical_columns(df_work, i_all_categ_cols)
    
    # Apply KNN imputation (fills all missing values, including numerical columns)
    imputer = KNNImputer(n_neighbors = n_neighbors)
    df_imputed_array = imputer.fit_transform(df_work)
    
    # Convert back to DataFrame (KNNImputer returns np array)
    df_imputed = pd.DataFrame(df_imputed_array,
                              columns = df_work.columns,
                              index = df_work.index)
    
    # Decode all categorical columns back to original values
    df_imputed = _decode_categorical_columns(df_imputed, i_all_categ_cols, encoder)
    
    # Update only (selected) categorical columns in original dataframe
    for idx in i_categ_cols:
        df[idx] = df_imputed[idx]
    
    return df

def _handle_categorical_missforest(df: pd.DataFrame, i_categ_cols: list, max_iter: int, n_estimators: int) -> pd.DataFrame:
    """
    Handle (selected) categorical columns with MissForest imputation using all columns as features
    """
    
    # Work with copy of df to impute only (selected) categorical columns
    df_work = df.copy()
    
    # Get indexes of all categorical columns
    i_all_categ_cols = list(df_work.select_dtypes(include = ['object', 'category', 'bool']).columns)
    
    # Encode all categorical columns, such that df_work is only numerical
    df_work, encoder = _encode_categorical_columns(df_work, i_all_categ_cols)
    
    # Apply MissForest (fills all missing values, including numerical columns)
    imputer = IterativeImputer(estimator = RandomForestRegressor(n_estimators = n_estimators, random_state = 0),
                               max_iter = max_iter, 
                               random_state = 0)
    # Note: random_state = 0 ensures reproducibility
    df_imputed_array = imputer.fit_transform(df_work.values)
    
    # Convert back to DataFrame (IterativeImputer returns np array)
    df_imputed = pd.DataFrame(df_imputed_array,
                              columns = df_work.columns,
                              index = df_work.index)
    
    # Decode all categorical columns back to original values
    df_imputed = _decode_categorical_columns(df_imputed, i_all_categ_cols, encoder)
    
    # Update only (selected) categorical columns in original dataframe
    for idx in i_categ_cols:
        df[idx] = df_imputed[idx]
    
    return df