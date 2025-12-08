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

Methods for numerical columns (method_num):
    - 'mean': Fill with column average (default)
    - 'median': Fill with column median  
    - 'mode': Fill with most frequent value
    - 'delete': Remove rows with numerical missing values
    - 'knn': K-Nearest Neighbors imputation
    - 'missforest': Random Forest iterative imputation
    - 'false': Skip numerical columns
    
Methods for categorical columns (method_categ):
    - 'mode': Fill with most frequent value (default)
    - 'delete': Remove rows with categorical missing values
    - 'knn': K-Nearest Neighbors imputation
    - 'missforest': Random Forest iterative imputation
    - 'false': Skip categorical columns

Column Selection (columns):
    - None: Process all columns (default)
    - ['col1', 'col2', ...]: Process only specified columns
    
Note on parameters for MissForest and KNN: 
    - n_neighbors : Number of neighbors for KNN imputation (default=5)
    - max_iter : Maximum iterations for MissForest imputation (default=10)
    - n_estimators : Number of trees in Random Forest for MissForest (default=10)
"""

# ============================================================================
# Main Function (Public)
# ============================================================================

def handle_missing_values(df: pd.DataFrame, 
                          method_num: str = 'mean', 
                          method_categ: str = 'mode',
                          columns: list = None,
                          n_neighbors: int = 5, 
                          max_iter: int = 10,
                          n_estimators: int = 10) -> pd.DataFrame:
    # Get indexes of numerical & categorical columns
    i_num_cols = list(df.select_dtypes(include = np.number).columns)
    # Note: .select_dtypes(include=np.number) returns a dataframe with numerical columns.
    #       .columns gets the indexes of the numerical columns.
    #       list() convert the indexes to a list.
    i_categ_cols = list(df.select_dtypes(exclude=np.number).columns)
    # Note: .select_dtypes(exclude=np.number) returns a dataframe with categorical columns.
    #       .columns gets the indexes of the categorical columns.
    #       list() convert the indexes to a list.

    # Filter columns if specific columns are requested
    if columns is not None:
        # Keep only columns that are in the specified list
        i_num_cols = [col for col in i_num_cols if col in columns]
        # Note: List comprehension - keeps only numerical columns that are in the columns list
        i_categ_cols = [col for col in i_categ_cols if col in columns]
        # Note: List comprehension - keeps only categorical columns that are in the columns list

    # Count total missing values 
    n_num_missing = df[i_num_cols].isna().sum().sum() if i_num_cols else 0
    # Note: df[i_num_cols] returns a dataframe with only numerical columns. 
    #       .isna() returns a dataframe of True / False, with True for missing values. 
    #       First .sum() sums each column.
    #       Second .sum() sums all the column totals.
    #       if i_num_cols else 0 handles case where i_num_cols is empty
    n_categ_missing = df[i_categ_cols].isna().sum().sum() if i_categ_cols else 0
    # Note: df[i_categ_cols] returns a dataframe with only categorical columns. 
    #       .isna() returns a dataframe of True / False, with True for missing values. 
    #       First .sum() sums each column.
    #       Second .sum() sums all the column totals.
    #       if i_categ_cols else 0 handles case where i_categ_cols is empty
    n_total_missing = n_categ_missing + n_num_missing

    if n_total_missing == 0: 
        print("No missing values found in selected columns" if columns else "No missing values found")
        return df
    
    print(f"{n_num_missing} numerical missing values & {n_categ_missing} categorical missing values found in selected columns")
    
    # If no numerical missing values, then set methode to false
    if n_num_missing == 0: 
        method_num = 'false'

    # Execute numerical methods (if methode_num == 'false', then execution is skipped)
    if method_num != 'false':
        if method_num == 'delete':
            df = _handle_numerical_delete(df, i_num_cols)
            # Possible that n_categ_missing has changed through deleting rows 
            n_categ_missing = df[i_categ_cols].isna().sum().sum() if i_categ_cols else 0

        elif method_num in ['mean', 'median', 'mode']:
            df = _handle_numerical_statistical(df, i_num_cols, method_num)
            
        elif method_num == 'knn':
            df = _handle_numerical_knn(df, i_num_cols, n_neighbors)
            
        elif method_num == 'missforest':
            df = _handle_numerical_missforest(df, i_num_cols, max_iter, n_estimators)
      
    # If no categorical missing values, then set methode to false
    if n_categ_missing == 0: 
        method_categ = 'false'

    # Execute categorical methods (if methode_categ == 'false', then execution is skipped)
    if method_categ != 'false':
        if method_categ == 'delete':
            df = _handle_categorical_delete(df, i_categ_cols)
            
        elif method_categ == 'mode':
            df = _handle_categorical_mode(df, i_categ_cols)
            
        elif method_categ == 'knn':
            df = _handle_categorical_knn(df, i_categ_cols, n_neighbors)
            
        elif method_categ == 'missforest':
            df = _handle_categorical_missforest(df, i_categ_cols, max_iter, n_estimators)
    
    print("Missing value imputation finished")
    return df

# ============================================================================
# Helper Functions (Private)
# ============================================================================

def _handle_numerical_delete(df: pd.DataFrame, i_num_cols: list) -> pd.DataFrame:
    """
    Delete rows that have missing values in numerical columns.
    """
    
    n_original_rows = len(df)
    
    # Get boolean mask (typ: Series), with True if row has missing values in numerical columns and otherwise False
    mask = df[i_num_cols].isna().any(axis = 1)
    # Note: df[i_num_cols] gets a dataframe with numerical columns.
    #       .isna() returns a dataframe of True / False, with True for missing values.
    #       .any(axis = 1) convert each row (axis = 1) into a single bool, if any True in row --> True and otherwise --> False. 

    # Remove rows, where mask is True (missing numerical value(s))
    df = df[~mask].reset_index(drop=True)
    # Note: '~' flips True & False.
    #       df[mask] gets dataframe with rows for which mask is true.
    #       .reset_index(drop=True) resets indexes of rows & don't keep the old ones as a new column (drop = true) 
    
    n_deleted = n_original_rows - len(df)
    print(f"  Deleted {n_deleted} rows with numerical missing values")
    return df

def _handle_numerical_statistical(df: pd.DataFrame, i_num_cols: list, method: str) -> pd.DataFrame:
    """
    Handle missing values in numerical columns with simple statistical methods (mean, median, mode).
    """

    for idx in i_num_cols:
        # Check if column idx has any missing number
        if df[idx].isna().any():
            if method == 'mean':
                # Calculate mean of column idx 
                fill_value = df[idx].mean() 
                
                # Fill missing values in column idx with mean
                df[idx] = df[idx].fillna(fill_value)

                print(f"Missing values in column {idx} filled with mean")

            elif method == 'median':
                # Calculate median of column idx 
                fill_value = df[idx].median()

                # Fill missing values in column idx with median
                df[idx] = df[idx].fillna(fill_value)

                print(f"Missing values in column {idx} filled with median")

            elif method == 'mode':
                # Calculate the most frequent value in column idx, which returns series (can be multiple values if tie of which first value is taken ([0]))
                fill_value = df[idx].mode()[0]

                # Fill missing values in column idx with most frequent value
                df[idx] = df[idx].fillna(fill_value)

                print(f"Missing values in column {idx} filled with mode")
    
    return df

def _encode_categorical_columns(df: pd.DataFrame, i_categ_cols: list) -> tuple:
    """
    Encode categorical columns to numerical values. 
    Returns: (df_encoded, encoders_dict)
    """
    # Create copy of original df 
    df_encoded = df.copy()
    encoders_dict = {}
    
    for idx in i_categ_cols:
        encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
        df_encoded[idx] = encoder.fit_transform(df_encoded[[idx]])
        encoders_dict[idx] = encoder
    
    return df_encoded, encoders_dict


def _decode_categorical_columns(df: pd.DataFrame, i_categ_cols: list, encoders_dict: dict) -> pd.DataFrame:
    """
    Decode categorical columns from numerical values back to original categories.
    """
    df_decoded = df.copy()
    
    for col in i_categ_cols:
        df_decoded[col] = df_decoded[col].round()
        encoder = encoders_dict[col]
        df_decoded[col] = encoder.inverse_transform(df_decoded[[col]]).flatten()
    
    return df_decoded

def _handle_numerical_knn(df: pd.DataFrame, i_num_cols: list, n_neighbors: int) -> pd.DataFrame:
    """
    Handle numerical columns with KNN imputation using ALL columns as features.
    Uses both numerical and categorical columns to find nearest neighbors for better accuracy.
    """
    print(f"  Using KNN imputation for numerical columns (n_neighbors={n_neighbors})")
    
    # Get categorical columns
    i_categ_cols = list(df.select_dtypes(exclude=np.number).columns)
    
    # Combine ALL columns (numerical + categorical) for finding neighbors
    all_cols = i_num_cols + i_categ_cols
    df_work = df[all_cols].copy()
    
    # Encode categorical columns if they exist
    if i_categ_cols:
        df_work, encoders = _encode_categorical_columns(df_work, i_categ_cols)
    
    # Apply KNN imputation on ALL columns
    imputer = KNNImputer(n_neighbors=n_neighbors)
    df_imputed_array = imputer.fit_transform(df_work)
    
    # Convert back to DataFrame
    df_imputed = pd.DataFrame(
        df_imputed_array,
        columns=all_cols,
        index=df.index
    )
    
    # Decode categorical columns back to original values
    if i_categ_cols:
        df_imputed = _decode_categorical_columns(df_imputed, i_categ_cols, encoders)
    
    # Update ONLY numerical columns in original dataframe
    for col in i_num_cols:
        df[col] = df_imputed[col]
    
    print(f"  KNN imputation complete for numerical columns")
    
    return df


def _handle_numerical_missforest(df: pd.DataFrame, i_num_cols: list, 
                                 max_iter: int, n_estimators: int) -> pd.DataFrame:
    """
    Handle numerical columns with MissForest imputation using ALL columns as features.
    Uses both numerical and categorical columns for better accuracy.
    """
    print(f"  Using MissForest for numerical columns (max_iter={max_iter}, n_estimators={n_estimators})")
    
    # Get categorical columns
    i_categ_cols = list(df.select_dtypes(exclude=np.number).columns)
    
    # Combine ALL columns (numerical + categorical) for imputation
    all_cols = i_num_cols + i_categ_cols
    df_work = df[all_cols].copy()
    
    # Encode categorical columns if they exist
    if i_categ_cols:
        df_work, encoders = _encode_categorical_columns(df_work, i_categ_cols)
    
    # Apply MissForest
    imputer = IterativeImputer(
        estimator=RandomForestRegressor(n_estimators=n_estimators, random_state=0),
        max_iter=max_iter,
        random_state=0,
        verbose=0
    )
    df_imputed_array = imputer.fit_transform(df_work.values)
    
    # Convert back to DataFrame
    df_imputed = pd.DataFrame(
        df_imputed_array,
        columns=all_cols,
        index=df.index
    )
    
    # Decode categorical columns back to original values
    if i_categ_cols:
        df_imputed = _decode_categorical_columns(df_imputed, i_categ_cols, encoders)
    
    # Update ONLY numerical columns in original dataframe
    for col in i_num_cols:
        df[col] = df_imputed[col]
    
    print(f"  MissForest imputation complete for numerical columns")
    
    return df

def _handle_categorical_delete(df: pd.DataFrame, i_categ_cols: list) -> pd.DataFrame:
    """
    Delete rows that have missing values in categorical columns only.
    """
    n_original_rows = len(df)
    
    # Create mask: True where ANY categorical column has missing value
    mask_missing = df[i_categ_cols].isna().any(axis=1)
    
    # Keep only rows where mask is False (no categorical missing)
    df = df[~mask_missing].reset_index(drop=True)
    
    n_deleted = n_original_rows - len(df)
    print(f"  Deleted {n_deleted} rows with categorical missing values")
    
    return df

def _handle_categorical_mode(df: pd.DataFrame, i_categ_cols: list) -> pd.DataFrame:
    """
    Handle categorical columns with mode (most frequent value).
    """
    for col in i_categ_cols:
        if df[col].isna().any():
            fill_value = df[col].mode()[0]
            df[col] = df[col].fillna(fill_value)
            print(f"  {col}: filled with mode ('{fill_value}')")
    
    return df

def _handle_categorical_knn(df: pd.DataFrame, i_categ_cols: list, n_neighbors: int) -> pd.DataFrame:
    """
    Handle categorical columns with KNN imputation using ALL columns as features.
    Uses both numerical and categorical columns to find nearest neighbors for better accuracy.
    """
    print(f"  Using KNN imputation for categorical columns (n_neighbors={n_neighbors})")
    
    # Get numerical columns
    i_num_cols = list(df.select_dtypes(include=np.number).columns)
    
    # Combine ALL columns (numerical + categorical) for finding neighbors
    all_cols = i_num_cols + i_categ_cols
    df_work = df[all_cols].copy()
    
    # Encode ALL categorical columns
    df_work, encoders = _encode_categorical_columns(df_work, i_categ_cols)
    
    # Apply KNN imputation on ALL columns
    imputer = KNNImputer(n_neighbors=n_neighbors)
    df_imputed_array = imputer.fit_transform(df_work)
    
    # Convert back to DataFrame
    df_imputed = pd.DataFrame(
        df_imputed_array,
        columns=all_cols,
        index=df.index
    )
    
    # Decode ALL categorical columns back to original values
    df_imputed = _decode_categorical_columns(df_imputed, i_categ_cols, encoders)
    
    # Update ONLY categorical columns in original dataframe
    for col in i_categ_cols:
        df[col] = df_imputed[col]
    
    print(f"  KNN imputation complete for categorical columns")
    
    return df

def _handle_categorical_missforest(df: pd.DataFrame, i_categ_cols: list,
                                   max_iter: int, n_estimators: int) -> pd.DataFrame:
    """
    Handle categorical columns with MissForest imputation using ALL columns as features.
    Uses both numerical and categorical columns for better accuracy.
    """
    print(f"  Using MissForest for categorical columns (max_iter={max_iter}, n_estimators={n_estimators})")
    
    # Get numerical columns
    i_num_cols = list(df.select_dtypes(include=np.number).columns)
    
    # Combine ALL columns (numerical + categorical) for imputation
    all_cols = i_num_cols + i_categ_cols
    df_work = df[all_cols].copy()
    
    # Encode ALL categorical columns
    df_work, encoders = _encode_categorical_columns(df_work, i_categ_cols)
    
    # Apply MissForest
    imputer = IterativeImputer(
        estimator=RandomForestRegressor(n_estimators=n_estimators, random_state=0),
        max_iter=max_iter,
        random_state=0,
        verbose=0
    )
    df_imputed_array = imputer.fit_transform(df_work.values)
    
    # Convert back to DataFrame
    df_imputed = pd.DataFrame(
        df_imputed_array,
        columns=all_cols,
        index=df.index
    )
    
    # Decode ALL categorical columns back to original values
    df_imputed = _decode_categorical_columns(df_imputed, i_categ_cols, encoders)
    
    # Update ONLY categorical columns in original dataframe
    for col in i_categ_cols:
        df[col] = df_imputed[col]
    
    print(f"  MissForest imputation complete for categorical columns")
    
    return df
