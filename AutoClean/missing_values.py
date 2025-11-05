from timeit import default_timer as timer
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from loguru import logger
import warnings
warnings.filterwarnings('ignore')

'''
Module for handling missing values in the AutoClean pipeline.

This module provides comprehensive methods for dealing with missing data in both
numerical and categorical features using various imputation strategies including:
- KNN imputation
- Linear/Logistic regression imputation
- Statistical imputation (mean, median, mode)
- Deletion of missing values
'''

class MissingValues:

    def handle(self, df, _n_neighbors=3):
        """
        Main handler for processing missing values in a DataFrame.
        
        This method orchestrates the entire missing value handling process by:
        1. Detecting missing values in the dataset
        2. Removing completely empty rows
        3. Applying appropriate imputation strategies for numerical features
        4. Applying appropriate imputation strategies for categorical features
        
        Args:
            df (pd.DataFrame): The input DataFrame with potential missing values
            _n_neighbors (int): Number of neighbors for KNN imputation (default: 3)
            
        Returns:
            pd.DataFrame: DataFrame with missing values handled according to specified methods
            
        Note:
            - Requires self.missing_num and self.missing_categ to be set
            - Supported methods for numerical: 'auto', 'linreg', 'knn', 'mean', 'median', 'most_frequent', 'delete'
            - Supported methods for categorical: 'auto', 'logreg', 'knn', 'most_frequent', 'delete'
        """
        # Check if any missing value handling is requested
        if self.missing_num or self.missing_categ:
            logger.info('Started handling of missing values...', str(self.missing_num).upper())
            start = timer()
            
            # Count total number of missing values across all columns
            self.count_missing = df.isna().sum().sum()

            if self.count_missing != 0:
                logger.info('Found a total of {} missing value(s)', self.count_missing)
                
                # Remove rows where ALL values are missing (completely empty rows)
                df = df.dropna(how='all')
                df.reset_index(drop=True)
                
                # ===== HANDLE NUMERICAL MISSING VALUES =====
                if self.missing_num:
                    logger.info('Started handling of NUMERICAL missing values... Method: "{}"', str(self.missing_num).upper())
                    
                    # AUTO mode: Combines linear regression and KNN imputation
                    if self.missing_num == 'auto': 
                        # First attempt: Linear regression imputation
                        self.missing_num = 'linreg'
                        lr = LinearRegression()
                        df = MissingValues._lin_regression_impute(self, df, lr)
                        
                        # Second attempt: KNN imputation for any remaining missing values
                        self.missing_num = 'knn'
                        imputer = KNNImputer(n_neighbors=_n_neighbors)
                        df = MissingValues._impute(self, df, imputer, type='num')
                    
                    # Linear regression imputation: Predicts missing values using other features
                    elif self.missing_num == 'linreg':
                        lr = LinearRegression()
                        df = MissingValues._lin_regression_impute(self, df, lr)
                    
                    # KNN imputation: Uses K-nearest neighbors to estimate missing values
                    elif self.missing_num == 'knn':
                        imputer = KNNImputer(n_neighbors=_n_neighbors)
                        df = MissingValues._impute(self, df, imputer, type='num')
                    
                    # Statistical imputation: Fill with mean, median, or mode
                    elif self.missing_num in ['mean', 'median', 'most_frequent']:
                        imputer = SimpleImputer(strategy=self.missing_num)
                        df = MissingValues._impute(self, df, imputer, type='num')
                    
                    # Delete rows containing numerical missing values
                    elif self.missing_num == 'delete':
                        df = MissingValues._delete(self, df, type='num')
                        logger.debug('Deletion of {} NUMERIC missing value(s) succeeded', self.count_missing-df.isna().sum().sum())      

                # ===== HANDLE CATEGORICAL MISSING VALUES =====
                if self.missing_categ:
                    logger.info('Started handling of CATEGORICAL missing values... Method: "{}"', str(self.missing_categ).upper())
                    
                    # AUTO mode: Combines logistic regression and KNN imputation
                    if self.missing_categ == 'auto':
                        # First attempt: Logistic regression imputation
                        self.missing_categ = 'logreg'
                        lr = LogisticRegression()
                        df = MissingValues._log_regression_impute(self, df, lr)
                        
                        # Second attempt: KNN imputation for any remaining missing values
                        self.missing_categ = 'knn'
                        imputer = KNNImputer(n_neighbors=_n_neighbors)
                        df = MissingValues._impute(self, df, imputer, type='categ')
                    
                    # Logistic regression imputation: Predicts categorical values using classification
                    elif self.missing_categ == 'logreg':
                        lr = LogisticRegression()
                        df = MissingValues._log_regression_impute(self, df, lr)
                    
                    # KNN imputation: Uses K-nearest neighbors to estimate missing categories
                    elif self.missing_categ == 'knn':
                        imputer = KNNImputer(n_neighbors=_n_neighbors)
                        df = MissingValues._impute(self, df, imputer, type='categ')  
                    
                    # Mode imputation: Fill with most frequent category
                    elif self.missing_categ == 'most_frequent':
                        imputer = SimpleImputer(strategy=self.missing_categ)
                        df = MissingValues._impute(self, df, imputer, type='categ')
                    
                    # Delete rows containing categorical missing values
                    elif self.missing_categ == 'delete':
                        df = MissingValues._delete(self, df, type='categ')
                        logger.debug('Deletion of {} CATEGORICAL missing value(s) succeeded', self.count_missing-df.isna().sum().sum())
            else:
                logger.debug('{} missing values found', self.count_missing)
            
            # Log total execution time
            end = timer()
            logger.info('Completed handling of missing values in {} seconds', round(end-start, 6))  
        else:
            logger.info('Skipped handling of missing values')
        
        return df

    def _impute(self, df, imputer, type):
        """
        Applies scikit-learn imputers to fill missing values.
        
        This method handles both numerical and categorical features differently:
        - Numerical: Direct imputation with type preservation
        - Categorical: Converts to numeric codes, imputes, then converts back
        
        Args:
            df (pd.DataFrame): DataFrame with missing values
            imputer: Scikit-learn imputer object (KNNImputer or SimpleImputer)
            type (str): Either 'num' for numerical or 'categ' for categorical
            
        Returns:
            pd.DataFrame: DataFrame with imputed values
            
        Note:
            - Preserves integer type if original data were integers
            - For categorical data, maintains original category labels
        """
        # Identify all numerical columns in the DataFrame
        cols_num = df.select_dtypes(include=np.number).columns 

        if type == 'num':
            # ===== NUMERICAL FEATURES IMPUTATION =====
            for feature in df.columns: 
                # Only process numerical columns
                if feature in cols_num:
                    # Check if this column has any missing values
                    if df[feature].isna().sum().sum() != 0:
                        try:
                            # Reshape column to 2D array (required by sklearn)
                            df_imputed = pd.DataFrame(imputer.fit_transform(np.array(df[feature]).reshape(-1, 1)))
                            
                            # Count how many values were successfully imputed
                            counter = df[feature].isna().sum().sum() - df_imputed.isna().sum().sum()

                            # Check if original data were integers (using -9999 as placeholder for NaN)
                            if (df[feature].fillna(-9999) % 1  == 0).all():
                                df[feature] = df_imputed
                                # Convert back to integers to preserve original data type
                                df[feature] = df[feature].round()
                                df[feature] = df[feature].astype('Int64')                                        
                            else:
                                # Keep as float if original data were floats
                                df[feature] = df_imputed
                            
                            if counter != 0:
                                logger.debug('{} imputation of {} value(s) succeeded for feature "{}"', str(self.missing_num).upper(), counter, feature)
                        except:
                            logger.warning('{} imputation failed for feature "{}"', str(self.missing_num).upper(), feature)
        else:
            # ===== CATEGORICAL FEATURES IMPUTATION =====
            for feature in df.columns:
                # Only process categorical (non-numerical) columns
                if feature not in cols_num:
                    # Check if this column has any missing values
                    if df[feature].isna().sum()!= 0:
                        try:
                            # Create a mapping from category labels to integers
                            mapping = dict()
                            mappings = {k: i for i, k in enumerate(df[feature].dropna().unique(), 0)}
                            mapping[feature] = mappings
                            
                            # Convert categorical values to numeric codes
                            df[feature] = df[feature].map(mapping[feature])

                            # Apply imputation on numeric codes
                            df_imputed = pd.DataFrame(imputer.fit_transform(np.array(df[feature]).reshape(-1, 1)), columns=[feature])    
                            
                            # Count how many values were changed
                            counter = sum(1 for i, j in zip(list(df_imputed[feature]), list(df[feature])) if i != j)

                            # Round imputed values to integers (since they represent category codes)
                            df[feature] = df_imputed
                            df[feature] = df[feature].round()
                            df[feature] = df[feature].astype('Int64')  

                            # Map numeric codes back to original category labels
                            mappings_inv = {v: k for k, v in mapping[feature].items()}
                            df[feature] = df[feature].map(mappings_inv)
                            
                            if counter != 0:
                                logger.debug('{} imputation of {} value(s) succeeded for feature "{}"', self.missing_categ.upper(), counter, feature)
                        except:
                            logger.warning('{} imputation failed for feature "{}"', str(self.missing_categ).upper(), feature)
        
        return df

    def _lin_regression_impute(self, df, model):
        """
        Predicts missing numerical values using Linear Regression.
        
        This method uses other features as predictors to estimate missing values:
        1. Converts categorical features to numeric codes
        2. For each numerical column with missing values:
           - Splits data into train (non-missing) and test (missing)
           - Trains a linear regression model on complete cases
           - Predicts missing values
        3. Converts categorical features back to original labels
        
        Args:
            df (pd.DataFrame): DataFrame with missing values
            model: LinearRegression model instance
            
        Returns:
            pd.DataFrame: DataFrame with imputed numerical values
            
        Note:
            - Attempts log-transformation to handle skewed distributions
            - Falls back to non-transformed data if log-transform fails
            - Preserves integer type if original data were integers
        """
        # Identify numerical columns
        cols_num = df.select_dtypes(include=np.number).columns
        mapping = dict()
        
        # Convert categorical features to numeric codes for modeling
        for feature in df.columns:
            if feature not in cols_num:
                # Create a mapping dictionary: category -> integer
                mappings = {k: i for i, k in enumerate(df[feature])}
                mapping[feature] = mappings
                df[feature] = df[feature].map(mapping[feature])
        
        # Process each numerical column that has missing values
        for feature in cols_num: 
                try:
                    # Split data into:
                    # test_df: rows where THIS feature is missing (to be predicted)
                    # train_df: rows where THIS feature is NOT missing (to train on)
                    test_df = df[df[feature].isnull()==True].dropna(subset=[x for x in df.columns if x != feature])
                    train_df = df[df[feature].isnull()==False].dropna(subset=[x for x in df.columns if x != feature])
                    
                    # Only proceed if there are missing values to impute
                    if len(test_df.index) != 0:
                        # Create pipeline: StandardScaler -> LinearRegression
                        pipe = make_pipeline(StandardScaler(), model)

                        # Try log-transformation (helps with skewed distributions)
                        y = np.log(train_df[feature])
                        X_train = train_df.drop(feature, axis=1)
                        test_df.drop(feature, axis=1, inplace=True)
                        
                        try:
                            # Attempt to fit model with log-transformed target
                            model = pipe.fit(X_train, y)
                        except:
                            # If log-transform fails (e.g., negative values), use original data
                            y = train_df[feature]
                            model = pipe.fit(X_train, y)
                        
                        # Make predictions
                        if (y == train_df[feature]).all():
                            # If no log-transform was applied, predict directly
                            pred = model.predict(test_df)
                        else:
                            # If log-transform was applied, exponentiate predictions
                            pred = np.exp(model.predict(test_df))

                        test_df[feature]= pred

                        # Preserve integer type if original data were integers
                        if (df[feature].fillna(-9999) % 1  == 0).all():
                            test_df[feature] = test_df[feature].round()
                            test_df[feature] = test_df[feature].astype('Int64')
                            # Update original DataFrame with predictions
                            df[feature].update(test_df[feature])                          
                        else:
                            df[feature].update(test_df[feature])  
                        
                        logger.debug('LINREG imputation of {} value(s) succeeded for feature "{}"', len(pred), feature)
                except:
                    logger.warning('LINREG imputation failed for feature "{}"', feature)
        
        # Convert categorical features back to original labels
        for feature in df.columns: 
            try:   
                # Reverse the mapping: integer -> category
                mappings_inv = {v: k for k, v in mapping[feature].items()}
                df[feature] = df[feature].map(mappings_inv)
            except:
                pass
        
        return df

    def _log_regression_impute(self, df, model):
        """
        Predicts missing categorical values using Logistic Regression.
        
        This method treats missing categorical values as a classification problem:
        1. Converts all categorical features to numeric codes
        2. For each categorical column with missing values:
           - Splits data into train (non-missing) and test (missing)
           - Trains a logistic regression classifier
           - Predicts missing categories
        3. Converts all features back to original category labels
        
        Args:
            df (pd.DataFrame): DataFrame with missing values
            model: LogisticRegression model instance
            
        Returns:
            pd.DataFrame: DataFrame with imputed categorical values
            
        Note:
            - Uses StandardScaler to normalize features before classification
            - Preserves integer type if original data were integers
        """
        # Identify numerical columns
        cols_num = df.select_dtypes(include=np.number).columns
        mapping = dict()
        
        # Convert ALL categorical features to numeric codes
        for feature in df.columns:
            if feature not in cols_num:
                # Create mapping: category -> integer
                mappings = {k: i for i, k in enumerate(df[feature])}
                mapping[feature] = mappings
                df[feature] = df[feature].map(mapping[feature])

        # Identify which columns are categorical (target columns for imputation)
        target_cols = [x for x in df.columns if x not in cols_num]
            
        # Process each categorical column
        for feature in df.columns: 
            if feature in target_cols:
                try:
                    # Split data into:
                    # test_df: rows where THIS feature is missing (to be predicted)
                    # train_df: rows where THIS feature is NOT missing (to train on)
                    test_df = df[df[feature].isnull()==True].dropna(subset=[x for x in df.columns if x != feature])
                    train_df = df[df[feature].isnull()==False].dropna(subset=[x for x in df.columns if x != feature])
                    
                    # Only proceed if there are missing values to impute
                    if len(test_df.index) != 0:
                        # Create pipeline: StandardScaler -> LogisticRegression
                        pipe = make_pipeline(StandardScaler(), model)

                        # Prepare training data
                        y = train_df[feature]  # Target: the category to predict
                        train_df.drop(feature, axis=1, inplace=True)  # Features: all other columns
                        test_df.drop(feature, axis=1, inplace=True)

                        # Train the classifier
                        model = pipe.fit(train_df, y)
                        
                        # Predict missing categories
                        pred = model.predict(test_df)
                        test_df[feature]= pred

                        # Preserve integer type if needed
                        if (df[feature].fillna(-9999) % 1  == 0).all():
                            test_df[feature] = test_df[feature].round()
                            test_df[feature] = test_df[feature].astype('Int64')
                            # Update original DataFrame with predictions
                            df[feature].update(test_df[feature])                             
                        
                        logger.debug('LOGREG imputation of {} value(s) succeeded for feature "{}"', len(pred), feature)
                except:
                    logger.warning('LOGREG imputation failed for feature "{}"', feature)
        
        # Convert ALL features back to original category labels
        for feature in df.columns: 
            try:
                # Reverse the mapping: integer -> category
                mappings_inv = {v: k for k, v in mapping[feature].items()}
                df[feature] = df[feature].map(mappings_inv)
            except:
                pass     
        
        return df

    def _delete(self, df, type):
        """
        Removes rows containing missing values.
        
        This is the simplest approach to handling missing data - just delete rows
        that have missing values in the specified type of columns.
        
        Args:
            df (pd.DataFrame): DataFrame with missing values
            type (str): Either 'num' for numerical or 'categ' for categorical
            
        Returns:
            pd.DataFrame: DataFrame with rows containing missing values removed
            
        Note:
            - This method reduces dataset size
            - Useful when missing data is minimal and random
            - Can cause bias if missing data is not random
        """
        # Identify numerical columns
        cols_num = df.select_dtypes(include=np.number).columns 
        
        if type == 'num':
            # Delete rows with missing NUMERICAL values
            for feature in df.columns: 
                if feature in cols_num:
                    # Drop any row where this numerical column has a missing value
                    df = df.dropna(subset=[feature])
                    df.reset_index(drop=True)
        else:
            # Delete rows with missing CATEGORICAL values
            for feature in df.columns:
                if feature not in cols_num:
                    # Drop any row where this categorical column has a missing value
                    df = df.dropna(subset=[feature])
                    df.reset_index(drop=True)
        
        return df
