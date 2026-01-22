"""
Handle missing values in the dataframe

To impute missing values with handle_missing_values, there are four important parameters. One is columns which can be used if imputation is needed only on certain columns and not all. The other is exclude_features, which can be used if certain columns should not be used as features for KNN and MissForest. Note the list of columns and exclude_features should not have any intersection. Hence exclude_features can't have columns, for which one wants to apply data imputation. If there are columns which need data imputation and cannot be used as features for other columns which need data imputation, the function needs to be applied multiple times. The last two are method_num & method_categ which choose the methods for imputation of numerical / categorical columns. 

Column Selection (columns):
    - None: Process all columns (default)
    - ['col1', 'col2', ...]: Process only specified columns

Excluding columns as features (exclude_features):
    - None: Use all columns as potential features (default)
    - ['col1', 'col2', ...]: Dont use specified columns as potential features

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
    - n_estimators : Number of decision trees in Random Forest for MissForest (default=10)
    - max_depth : Maximum depth of each tree in Random Forest for MissForest (default=None, unlimited)
    - min_samples_leaf : Minimum samples required at each leaf node of the decision tree from Random Forest for MissForest (default=1)

Returns: 
    Cleaned datafram and report (as tuple)

For further information about the algorithms KNN & MissForest, see in the folder Additional_Information
"""

# Imported libraries 
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.experimental import enable_iterative_imputer 
# Note: from sklearn.experimental import enable_iterative_imputer needed to enable IterativeImputer (as its marked as experimental by sklearn) 
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

# ============================================================================
# Main Function (Public)
# ============================================================================

def handle_missing_values(df: pd.DataFrame, 
                          method_num: str = 'mean', 
                          method_categ: str = 'mode',
                          columns: list = None,
                          exclude_features: list = None,
                          n_neighbors: int = 5, 
                          max_iter: int = 10,
                          n_estimators: int = 10, 
                          max_depth: int = None,
                          min_samples_leaf: int = 1) -> tuple:
    # Terminal output: start
    print("Handling missing values... ", end="", flush=True)
    # Note: With flush = True, print is immediately

    # Initialize report
    report = {'method_num': method_num,
              'method_categ': method_categ,
              'columns': columns,
              'exclude_features': exclude_features,
              'n_neighbors': n_neighbors, 
              'max_iter': max_iter,
              'n_estimators': n_estimators, 
              'max_depth': max_depth,
              'min_samples_leaf': min_samples_leaf,
              'num_missing_before': 0,
              'categ_missing_before': 0,
              'rows_deleted': 0,
              'imputations_num': [],
              'imputations_categ': []}
    
    # Work with copy, to not modify input df 
    df_work = df.copy()

    # Validation: columns and exclude_features should not intersect, if they do raise Value error
    if columns != None and exclude_features != None:
        intersection = [col for col in columns if col in exclude_features]
        if len(intersection) > 0:
            raise ValueError(f"List from columns and exclude_features do intersect with: {intersection}. This is invalid.")
        
    # Exclude specified columns as features (if provided) by removing them from df_work
    # Save excluded columns and column order, to add them at the end again in correct order  
    if exclude_features != None:
        original_column_order = list(df_work.columns)
        excluded_data = df_work[exclude_features].copy()
        df_work = df_work.drop(columns = exclude_features)

    # Get indexes of numerical & categorical columns
    i_num_cols = list(df_work.select_dtypes(include = np.number).columns)
    # Note: .select_dtypes(include = np.number) returns a dataframe with numerical columns 
    #       .columns gets the indexes of the numerical columns (as pandas Index object)
    #       list() convert to list
    i_categ_cols = list(df_work.select_dtypes(include = ['object', 'category', 'bool']).columns)
    # Note: .select_dtypes(include = ['object', 'category', 'bool']) returns a dataframe with categorical columns
    #       .columns gets the indexes of the numerical columns (as pandas Index object)
    #       list() convert to list

    # Adjust the i_num_cols / i_categ_cols if specific columns are selected to impute 
    if columns != None:
        # Keep only columns that are in the specified list (columns)
        i_num_cols = [col for col in i_num_cols if col in columns]
        i_categ_cols = [col for col in i_categ_cols if col in columns]

    # Count total missing values 
    n_num_missing = df_work[i_num_cols].isna().sum().sum() 
    # Note: df_work[i_num_cols] returns a dataframe with (selected) numerical columns 
    #       .isna() returns a dataframe of True / False, with True for missing values 
    #       First .sum() sums each column
    #       Second .sum() sums all the column totals
    #       if i_num_cols is empty, n_num_missing = 0
    n_categ_missing = df_work[i_categ_cols].isna().sum().sum() 
    # Note: df_work[i_categ_cols] returns a dataframe with (selected) categorical columns 
    #       .isna() returns a dataframe of True / False, with True for missing values 
    #       First .sum() sums each column
    #       Second .sum() sums all the column totals
    #       if i_categ_cols is empty, n_categ_missing = 0
    n_total_missing = n_categ_missing + n_num_missing

    # Update report
    report['num_missing_before'] = n_num_missing
    report['categ_missing_before'] = n_categ_missing

    # End if no missing value in total
    if n_total_missing == 0:
        # Add excluded columns in original order (if any were excluded)
        if exclude_features != None:
            # Add excluded columns to the right
            for col in exclude_features:
                df_work[col] = excluded_data[col]
            
            # Restore original column order    
            df_work = df_work[original_column_order]

        print("✓")
        return df_work, report
    
    # If no numerical missing values, then set method_num to false
    if n_num_missing == 0: 
        method_num = 'false'

    # Execute numerical methods (if methode_num == 'false', then execution is skipped)
    if method_num != 'false':
        # Get boolean mask for missing values before numerical imputation (for report)
        mask_missing_before_num = df_work[i_num_cols].isna().copy() 
        
        if method_num == 'delete':
            # Get # of rows before numerical delete is applied (for report) 
            n_rows_before = len(df_work)

            df_work = _handle_numerical_delete(df_work, i_num_cols)

            # Update report 
            report['rows_deleted'] = n_rows_before - len(df_work)

            # Possible that n_categ_missing has changed through deleting rows 
            n_categ_missing = df_work[i_categ_cols].isna().sum().sum()

        elif method_num in ['mean', 'median', 'mode']:
            df_work = _handle_numerical_statistical(df_work, i_num_cols, method_num)
            
        elif method_num == 'knn':
            df_work = _handle_numerical_knn(df_work, i_num_cols, n_neighbors)
        
        elif method_num == 'missforest':
            df_work = _handle_numerical_missforest(df_work, i_num_cols, max_iter, n_estimators, max_depth, min_samples_leaf)
    
    # Track for report data imputation (numerical) 
    if method_num not in ['false', 'delete']:
        for col in i_num_cols:
            for idx in df_work.index: # df_work.index gets row indexes 
                # Check if cell was missing before (mask_missing_before_num.at[idx, col]) and now has a value, i.e. was imputed (pd.notna(df_work.at[idx, col]))
                if mask_missing_before_num.at[idx, col] and pd.notna(df_work.at[idx, col]):
                    report['imputations_num'].append({'row': idx,
                                                      'column': col,
                                                      'new_value': df_work.at[idx, col],
                                                      'method': method_num})
                    # Note: Value of key 'imputations' in dict report is a list, in which each value is a dictionary 
    
    # If no categorical missing values, then set method_categ to false
    if n_categ_missing == 0: 
        method_categ = 'false'

    # Execute categorical methods (if methode_categ == 'false', then execution is skipped)
    if method_categ != 'false':
        # Get boolean mask for missing values before categorical imputation (for report)
        mask_missing_before_categ = df_work[i_categ_cols].isna().copy()

        if method_categ == 'delete':
            # Get # of rows before categorical delete is applied (for report) 
            n_rows_before = len(df_work)

            df_work = _handle_categorical_delete(df_work, i_categ_cols)
            
            # Update report 
            report['rows_deleted'] += n_rows_before - len(df_work)
            
        elif method_categ == 'mode':
            df_work = _handle_categorical_mode(df_work, i_categ_cols)
            
        elif method_categ == 'knn':
            df_work = _handle_categorical_knn(df_work, i_categ_cols, n_neighbors)
            
        elif method_categ == 'missforest':
            df_work = _handle_categorical_missforest(df_work, i_categ_cols, max_iter, n_estimators, max_depth, min_samples_leaf)
    
    # Track for report data imputation (categorical)
    if method_categ not in ['false', 'delete']:
        for col in i_categ_cols:
            for idx in df_work.index: # df_work.index gets row indexes 
                # Check if cell was missing before (mask_missing_before_categ.at[idx, col]) and now has a value, i.e. was imputed (pd.notna(df_work.at[idx, col]))
                if mask_missing_before_categ.at[idx, col] and pd.notna(df_work.at[idx, col]):
                    report['imputations_categ'].append({'row': idx,
                                                        'column': col,
                                                        'new_value': df_work.at[idx, col],
                                                        'method': method_categ})
                    # Note: Value of key 'imputations' in dict report is a list, in which each value is a dictionary

    # Add excluded columns in original order (if any were excluded)
    if exclude_features != None:
        # Add excluded columns to the right
        for col in exclude_features:
            df_work[col] = excluded_data[col]

        # Restore original column order    
        df_work = df_work[original_column_order]

    # Terminal output: end
    print("✓")
    return df_work, report

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
    
    # Standardize all columns of df_work (mean = 0, standard deviation = 1) with StandardScaler()
    scaler = StandardScaler()
    df_scaled_array = scaler.fit_transform(df_work)

    # Convert back to DataFrame (scaler returns a np array)
    df_scaled = pd.DataFrame(df_scaled_array, columns = df_work.columns, index = df_work.index)
    
    # Apply KNN imputation (fills all missing values, inlcuding orginially categorical columns)
    imputer = KNNImputer(n_neighbors = n_neighbors)
    df_imputed_array = imputer.fit_transform(df_scaled)
    
    # Convert back to DataFrame (KNNImputer returns np array) & inverse standardization (.inverse_transform())
    df_imputed = pd.DataFrame(scaler.inverse_transform(df_imputed_array),
                              columns = df_work.columns,
                              index = df_work.index)

    # Update only (selected) numerical columns in original dataframe
    for idx in i_num_cols:
        df[idx] = df_imputed[idx]
    
    return df

def _handle_numerical_missforest(df: pd.DataFrame, i_num_cols: list, max_iter: int, n_estimators: int, max_depth: int, min_samples_leaf: int) -> pd.DataFrame:
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
    imputer = IterativeImputer(estimator = RandomForestRegressor(n_estimators = n_estimators, max_depth = max_depth, min_samples_leaf = min_samples_leaf, random_state = 0),
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
    
    # Standardize all columns of df_work (mean = 0, standard deviation = 1) with StandardScaler()
    scaler = StandardScaler()
    df_scaled_array = scaler.fit_transform(df_work)

    # Convert back to DataFrame (scaler returns a np array)
    df_scaled = pd.DataFrame(df_scaled_array, columns = df_work.columns, index = df_work.index)

    # Apply KNN imputation (fills all missing values, including numerical columns)
    imputer = KNNImputer(n_neighbors = n_neighbors)
    df_imputed_array = imputer.fit_transform(df_scaled)
    
    # Convert back to DataFrame (KNNImputer returns np array) & inverse standardization (.inverse_transform())
    df_imputed = pd.DataFrame(scaler.inverse_transform(df_imputed_array),
                              columns = df_work.columns,
                              index = df_work.index)
    
    # Decode all categorical columns back to original values
    df_imputed = _decode_categorical_columns(df_imputed, i_all_categ_cols, encoder)
    
    # Update only (selected) categorical columns in original dataframe
    for idx in i_categ_cols:
        df[idx] = df_imputed[idx]
    
    return df

def _handle_categorical_missforest(df: pd.DataFrame, i_categ_cols: list, max_iter: int, n_estimators: int, max_depth: int, min_samples_leaf: int) -> pd.DataFrame:
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
    imputer = IterativeImputer(estimator = RandomForestRegressor(n_estimators = n_estimators, max_depth = max_depth, min_samples_leaf = min_samples_leaf, random_state = 0),
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