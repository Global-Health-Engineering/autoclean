from timeit import default_timer as timer
import numpy as np
import pandas as pd
from math import isnan
from sklearn import preprocessing
from loguru import logger
import warnings
warnings.filterwarnings('ignore')

'''
Module for encoding categorical features in the AutoClean pipeline.

This module provides methods for converting categorical (text) features into
numerical representations that machine learning algorithms can process:

1. One-Hot Encoding: Creates binary columns for each category
   - Best for features with few unique values (≤10)
   - Example: Color ['red', 'blue'] → Color_red [1,0], Color_blue [0,1]

2. Label Encoding: Assigns integer codes to categories
   - Best for features with moderate unique values (≤20)
   - Example: Size ['S', 'M', 'L'] → Size_lab [0, 1, 2]

3. Auto Mode: Automatically chooses encoding method based on cardinality
'''

class EncodeCateg:

    def handle(self, df):
        """
        Main handler for encoding categorical features in the DataFrame.
        
        This method identifies categorical columns and applies the specified
        encoding strategy. It can encode all categorical columns or only
        specific ones.
        
        Args:
            df (pd.DataFrame): DataFrame with categorical features to encode
            
        Returns:
            pd.DataFrame: DataFrame with encoded categorical features
            
        Encoding methods (self.encode_categ):
            - 'auto': Chooses encoding based on number of unique values
              * ≤10 unique values: One-Hot encoding
              * 11-20 unique values: Label encoding
              * >20 unique values: Skip encoding
            - 'onehot': Force one-hot encoding for all specified columns
            - 'label': Force label encoding for all specified columns
            
        Note:
            - Skips datetime columns automatically
            - Can specify target columns as second element in self.encode_categ list
            - Original categorical columns are preserved (new columns added)
        """
        # Check if encoding is requested
        if self.encode_categ:
            # Ensure encode_categ is a list (wrap single value if needed)
            if not isinstance(self.encode_categ, list):
                self.encode_categ = ['auto']
            
            # Identify all categorical (non-numeric) columns
            cols_categ = set(df.columns) ^ set(df.select_dtypes(include=np.number).columns) 
            
            # Determine which columns to encode
            if len(self.encode_categ) == 1:
                # Only method specified, encode ALL categorical columns
                target_cols = cols_categ
            else:
                # Specific columns specified in second element
                target_cols = self.encode_categ[1]
            
            logger.info('Started encoding categorical features... Method: "{}"', str(self.encode_categ[0]).upper())
            start = timer()
            
            # Process each target column
            for feature in target_cols:
                # Handle both column names and column indices
                if feature in cols_categ:
                    # Feature is a column name
                    feature = feature
                else:
                    # Feature is a column index, get the name
                    feature = df.columns[feature]
                
                try:
                    # Skip datetime columns (shouldn't be encoded)
                    pd.to_datetime(df[feature])
                    logger.debug('Skipped encoding for DATETIME feature "{}"', feature)
                except:
                    # Not a datetime, proceed with encoding
                    try:
                        if self.encode_categ[0] == 'auto':
                            # AUTO MODE: Choose encoding based on cardinality
                            
                            # One-hot encoding for low cardinality (≤10 unique values)
                            if df[feature].nunique() <=10:
                                df = EncodeCateg._to_onehot(self, df, feature)
                                logger.debug('Encoding to ONEHOT succeeded for feature "{}"', feature)
                            
                            # Label encoding for medium cardinality (11-20 unique values)
                            elif df[feature].nunique() <=20:
                                df = EncodeCateg._to_label(self, df, feature)
                                logger.debug('Encoding to LABEL succeeded for feature "{}"', feature)
                            
                            # Skip encoding for high cardinality (>20 unique values)
                            else:
                                logger.debug('Encoding skipped for feature "{}"', feature)   

                        # ONEHOT MODE: Force one-hot encoding
                        elif self.encode_categ[0] == 'onehot':
                            df = EncodeCateg._to_onehot(df, feature)
                            logger.debug('Encoding to {} succeeded for feature "{}"', str(self.encode_categ[0]).upper(), feature)
                        
                        # LABEL MODE: Force label encoding
                        elif self.encode_categ[0] == 'label':
                            df = EncodeCateg._to_label(df, feature)
                            logger.debug('Encoding to {} succeeded for feature "{}"', str(self.encode_categ[0]).upper(), feature)      
                    except:
                        logger.warning('Encoding to {} failed for feature "{}"', str(self.encode_categ[0]).upper(), feature)    
            
            # Log execution time
            end = timer()
            logger.info('Completed encoding of categorical features in {} seconds', round(end-start, 6))
        else:
            logger.info('Skipped encoding of categorical features')
        
        return df

    def _to_onehot(self, df, feature, limit=10):
        """
        Applies One-Hot Encoding to a categorical feature.
        
        One-Hot Encoding creates a new binary column for each unique category.
        Each row has a 1 in the column corresponding to its category, and 0s elsewhere.
        
        Example:
            Original column 'Color' with values ['red', 'blue', 'red']
            Creates: Color_red [1, 0, 1], Color_blue [0, 1, 0]
        
        Args:
            df (pd.DataFrame): DataFrame containing the feature
            feature (str): Name of the categorical column to encode
            limit (int): Warning threshold for number of new columns (default: 10)
            
        Returns:
            pd.DataFrame: DataFrame with one-hot encoded columns added
            
        Note:
            - Original column is preserved
            - New columns are prefixed with original feature name
            - Warns if encoding creates too many columns (consider label encoding instead)
        """
        # Create binary columns for each unique category
        one_hot = pd.get_dummies(df[feature], prefix=feature)
        
        # Warn if too many new columns are created
        if one_hot.shape[1] > limit:
            logger.warning('ONEHOT encoding for feature "{}" creates {} new features. Consider LABEL encoding instead.', feature, one_hot.shape[1])
        
        # Add the new columns to the DataFrame
        df = df.join(one_hot)
        
        return df

    def _to_label(self, df, feature):
        """
        Applies Label Encoding to a categorical feature.
        
        Label Encoding assigns a unique integer to each category. This is more
        space-efficient than one-hot encoding but implies an ordinal relationship
        between categories (which may not exist).
        
        Example:
            Original column 'Size' with values ['S', 'M', 'L', 'S']
            Creates: Size_lab [0, 1, 2, 0]
        
        Args:
            df (pd.DataFrame): DataFrame containing the feature
            feature (str): Name of the categorical column to encode
            
        Returns:
            pd.DataFrame: DataFrame with label encoded column added
            
        Note:
            - Original column is preserved
            - New column has suffix '_lab'
            - Handles NaN values appropriately
            - Creates a mapping dictionary for reference
        """
        # Initialize the Label Encoder
        le = preprocessing.LabelEncoder()

        # Create new column with encoded values
        df[feature + '_lab'] = le.fit_transform(df[feature].values)
        
        # Create mapping dictionary: category -> integer code
        mapping = dict(zip(le.classes_, range(len(le.classes_))))
        
        # Handle NaN values if present in the mapping
        for key in mapping:
            try:
                if isnan(key):
                    # Replace the encoded NaN value back with actual NaN
                    replace = {mapping[key] : key }
                    df[feature].replace(replace, inplace=True)
            except:
                # Key is not NaN, skip
                pass
        
        return df
