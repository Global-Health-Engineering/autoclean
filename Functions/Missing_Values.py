"""
Missing Values: Impute missing values in a specific column

This function handles missing values for one column at a time. 
User specifies the column, method, and optionally which columns to use as features for KNN/MissForest.
Apply multiple times for different columns and append reports to a list.

Parameters:
    - df: DataFrame to clean
    - column: Name of column to apply handle_missing_values() (target column)
    - method: Imputation methods
        - 'mean': Fill with column average (only for numerical columns)
        - 'median': Fill with column median (only for numerical columns)
        - 'mode': Fill with most frequent value in the column (for numerical or categorical columns, default)
        - 'delete': Remove rows with missing values (for numerical or categorical columns)
        - 'knn': K-Nearest Neighbors imputation (for numerical or categorical columns)
        - 'missforest': Random Forest iterative imputation (for numerical or categorical columns)
    - features: Optional list of columns to use as features for KNN/MissForest
        - None: Use all columns (except the one specified for imputation) as features (default)
        - ['col1', 'col2', ...]: Use only specified columns as features 
    - n_neighbors: Number of neighbors for KNN imputation (default = 5)
    - max_iter: Maximum iterations for MissForest imputation (default = 10)
    - n_estimators: Number of decision trees in Random Forest for MissForest (default = 10)
    - max_depth: Maximum depth of each tree in Random Forest for MissForest (default = None, unlimited)
    - min_samples_leaf: Minimum samples required at each leaf node of the decision tree from Random Forest for MissForest (default = 1)

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
                          column: str,
                          method: str = 'mode',
                          features: list = None,
                          n_neighbors: int = 5,
                          max_iter: int = 10,
                          n_estimators: int = 10,
                          max_depth: int = None,
                          min_samples_leaf: int = 1) -> tuple:
    # Terminal output: start
    print(f"Handling missing values ({column})... ", end = "", flush = True)
    # Note: With flush = True, print is immediately

    # Work with copy, to not modify input df
    df_work = df.copy()

    # Validate if target column exists
    if column not in list(df_work.columns):
        # Note: list(df_work.columns) returns a list of all column names of df_work 
        raise ValueError(f"Column '{column}' not found in dataframe")

    # Initialize report
    report = {'column': column,
              'method': method,
              'n_missing_before': 0,
              'n_imputed': 0,
              'n_rows_deleted': 0,
              'imputations': []}

    # Add method-specific parameters to report
    if method == 'knn':
        report['features'] = features
        report['n_neighbors'] = n_neighbors

    elif method == 'missforest':
        report['features'] = features
        report['max_iter'] = max_iter
        report['n_estimators'] = n_estimators
        report['max_depth'] = max_depth
        report['min_samples_leaf'] = min_samples_leaf

    # Count missing values in target column before imputation and add it to report 
    n_missing_before = df_work[column].isna().sum()
    # Note: .isna() returns series of True / False, with True for missing values
    #       .sum() sums all True as 1 in the boolean series 
    report['n_missing_before'] = n_missing_before

    # End if no missing value in specified column 
    if n_missing_before == 0:
        print("✓")
        return df_work, report

    # Get boolean mask (True = missing value) as list for missing values before imputation (for report)
    mask_missing_before = list(df_work[column].isna())

    # Determine if target column is numerical (is_numerical = True) or categorical (is_numerical = False)
    is_numerical = np.issubdtype(df_work[column].dtype, np.number)
    # Note: .dtype returns the data type of a column
    #       np.issubdtype(x, y) returns True if x is equal to y (= specific type) or a subtype of y (= group of types, e.g. np.number)
    #       np.number includes all numerical types
    
    # Validate method compatibility (mean & median only work for numerical columns)
    if method in ['mean', 'median'] and not is_numerical:
        raise ValueError(f"Chosen method '{method}' only works with numerical columns. Specified column '{column}' is categorical.")

    # Get seperate df with only feature columns if method is KNN or MissForest
    if method in ['knn', 'missforest']:
        df_features = _prepare_features(df_work, column, features)
    
    # Execute specified imputation method
    if method == 'delete':
        # Get # of rows before removing rows with missing values in specified column (for report)
        n_rows_before = len(df_work)

        # Remove rows with missing values in specified column 
        df_work = df_work.dropna(subset = [column]).reset_index(drop = True)
        # Note: .dropna(subset = [column]) removes rows with missing values in column 
        #       .reset_index(drop = True) resets row indexes and doesnt keep old indexes as new column (drop = True)

        # Update report
        report['n_rows_deleted'] = n_rows_before - len(df_work)

        print("✓")
        return df_work, report

    elif method == 'mean':
        # Calculate mean of target column 
        fill_value = df_work[column].mean()

        # Fill missing value(s) in target column with mean
        df_work[column] = df_work[column].fillna(fill_value)

    elif method == 'median':
        # Calculate median of target target column
        fill_value = df_work[column].median()

        # Fill missing value(s) in target column with median
        df_work[column] = df_work[column].fillna(fill_value)

    elif method == 'mode':
        # Calculate the most frequent value in target column, which returns series (can be multiple values if tie) of which the first value is taken ([0])
        fill_value = df_work[column].mode()[0]

        # Fill missing value(s) in target column with most frequent value 
        df_work[column] = df_work[column].fillna(fill_value)

    elif method == 'knn':
        df_work = _impute_knn(df_work, column, df_features, n_neighbors, is_numerical)

    elif method == 'missforest':
        df_work = _impute_missforest(df_work, column, df_features, max_iter, n_estimators, max_depth, min_samples_leaf, is_numerical)

    else:
        raise ValueError(f"Invalid method: {method}. Must be 'mean', 'median', 'mode', 'delete', 'knn', or 'missforest'.")

    # Track imputations for report
    for idx in list(df_work.index): # list(df_work.index) gets list of row indexes
        # Check if value in target column, at row idx was missing value before imputation and is now imputed
        if mask_missing_before[idx] and pd.notna(df_work.at[idx, column]):
            # Note: pd.notna(x) returns True if x is not a missing value
            
            # Update report 
            report['imputations'].append({'row': idx, 'new_value': df_work.at[idx, column]})
            # Note: Value of key 'imputations' in dict report is a list, in which each value is a dictionary

    report['n_imputed'] = len(report['imputations'])

    # Terminal output: end
    print("✓")
    return df_work, report

# ============================================================================
# Helper Functions (Private)
# ============================================================================

def _prepare_features(df: pd.DataFrame, target_column: str, features: list) -> pd.DataFrame:
    """
    Return a dataframe with only feature columns for KNN/MissForest imputation
    """
    # If features == None, all columns except target_column (specified column for imputation) are features
    if features is None:
        feature_cols = [col for col in list(df.columns) if col != target_column]
    # If features are specified (features need to exist in df & can't be target column) 
    else:
        feature_cols = [col for col in features if col in list(df.columns) and col != target_column]
        if len(feature_cols) == 0:
            raise ValueError(f"No valid feature columns found. Provided: {features}")
    
    return df[feature_cols]

def _encode_categorical_columns(df: pd.DataFrame, categ_cols: list) -> tuple:
    """Encode (selected) categorical columns to numerical columns"""
    # Create encoder 
    encoder = OrdinalEncoder()

     # Fit encoder and transform (selected) categorical columns 
    df[categ_cols] = encoder.fit_transform(df[categ_cols])

    return df, encoder

def _decode_categorical_columns(df: pd.DataFrame, categ_cols: list, encoder: OrdinalEncoder) -> pd.DataFrame:
    """Decode (selected) categorical columns back to original numerical columns"""
    df[categ_cols] = df[categ_cols].round()
    # Note: KNN / MissForest may produce decimals, which need to be rounded to integers (resp. floats with .0 ending), to perform decoding 

    # Decode (selected) categorical columns back to original numerical columns
    df[categ_cols] = encoder.inverse_transform(df[categ_cols])

    return df

def _impute_knn(df: pd.DataFrame, column: str, df_features: pd.DataFrame, n_neighbors: int, is_numerical: bool) -> pd.DataFrame:
    """Impute missing values using KNN"""
    
    # Combine target column with features columns to one df (axis = 1 -> concatenate horizontally)
    df_work = pd.concat([df[[column]], df_features], axis = 1)
    
    # Get list of categorical column names 
    categ_cols = list(df_work.select_dtypes(include = ['object', 'category', 'bool']).columns)
    # Note: .select_dtypes(include = ['object', 'category', 'bool']) returns a dataframe with categorical columns
    #       .columns gets the names of the categorical columns (as pandas Index object)
    #       list() convert to list

    # Encode all categorical columns (if they exist), such that df_work is only numerical
    if len(categ_cols) > 0:
        df_work, encoder = _encode_categorical_columns(df_work, categ_cols)
    
    # Standardize all columns of df_work (mean = 0, standard deviation = 1) with StandardScaler()
    scaler = StandardScaler()
    df_scaled_array = scaler.fit_transform(df_work)

    # Convert back to DataFrame (scaler returns a np array)
    df_scaled = pd.DataFrame(df_scaled_array, columns = df_work.columns, index = df_work.index)
    
    # Apply KNN imputation (fills the missing values in all columns)
    imputer = KNNImputer(n_neighbors = n_neighbors)
    df_imputed_array = imputer.fit_transform(df_scaled)

    # Convert back to DataFrame (KNNImputer returns np array) & inverse standardization (.inverse_transform())
    df_imputed = pd.DataFrame(scaler.inverse_transform(df_imputed_array),
                              columns = df_work.columns,
                              index = df_work.index)
    
    # Decode target column back if its categorical
    if not is_numerical:
        df_imputed = _decode_categorical_columns(df_imputed, [column], encoder)
    
    # Update only target column
    df[column] = df_imputed[column]
    
    return df

def _impute_missforest(df: pd.DataFrame, 
                       column: str, 
                       df_features: pd.DataFrame, 
                       max_iter: int, 
                       n_estimators: int, 
                       max_depth: int, 
                       min_samples_leaf: int, 
                       is_numerical: bool) -> pd.DataFrame:
    """Impute missing values using MissForest"""
    # Combine target column with features columns to one df (axis = 1 -> concatenate horizontally)
    df_work = pd.concat([df[[column]], df_features], axis = 1)
    
    # Get list of categorical column names 
    categ_cols = list(df_work.select_dtypes(include = ['object', 'category', 'bool']).columns)
    # Note: .select_dtypes(include = ['object', 'category', 'bool']) returns a dataframe with categorical columns
    #       .columns gets the names of the categorical columns (as pandas Index object)
    #       list() convert to list

    # Encode all categorical columns (if they exist), such that df_work is only numerical
    if len(categ_cols) > 0:
        df_work, encoder = _encode_categorical_columns(df_work, categ_cols)
    
    # Apply MissForest (fills the missing values in all columns)
    imputer = IterativeImputer(estimator = RandomForestRegressor(n_estimators = n_estimators, 
                                                                 max_depth = max_depth, 
                                                                 min_samples_leaf = min_samples_leaf, 
                                                                 random_state = 0),
                               max_iter = max_iter, 
                               random_state = 0)
    # Note: random_state = 0 ensures reproducibility
    df_imputed_array = imputer.fit_transform(df_work.values) 
    # Note: df.values returns df without column and row indexes as np array 
    
    # Convert back to DataFrame (IterativeImputer returns np array)
    df_imputed = pd.DataFrame(df_imputed_array,
                              columns = df_work.columns,
                              index = df_work.index)
    
    # Decode target column back if its categorical
    if not is_numerical:
        df_imputed = _decode_categorical_columns(df_imputed, [column], encoder)
    
    # Update only target column
    df[column] = df_imputed[column]
    
    return df