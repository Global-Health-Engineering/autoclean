from timeit import default_timer as timer
import numpy as np
from loguru import logger
import warnings
warnings.filterwarnings('ignore')

'''
Module for handling outliers in the AutoClean pipeline.

This module provides methods for detecting and handling outliers in numerical data using:
- IQR (Interquartile Range) method for outlier detection
- Winsorization: Capping outliers at computed bounds
- Deletion: Removing rows containing outliers

The IQR method identifies outliers as values that fall outside the range:
    [Q1 - k*IQR, Q3 + k*IQR]
where Q1 and Q3 are the 25th and 75th percentiles, IQR = Q3 - Q1,
and k is a multiplier parameter (typically 1.5).
'''

class Outliers:

    def handle(self, df):
        """
        Main handler for processing outliers in numerical features.
        
        This method detects and handles outliers using one of two strategies:
        1. Winsorization (default/auto): Caps outliers at the computed bounds
        2. Deletion: Removes rows containing outliers
        
        Args:
            df (pd.DataFrame): The input DataFrame potentially containing outliers
            
        Returns:
            pd.DataFrame: DataFrame with outliers handled according to specified method
            
        Note:
            - Only processes numerical columns
            - Requires self.outliers to be set ('auto', 'winz', or 'delete')
            - Uses self.outlier_param for IQR multiplier (typically 1.5)
        """
        # Check if outlier handling is requested
        if self.outliers:
            logger.info('Started handling of outliers... Method: "{}"', str(self.outliers).upper())
            start = timer()  

            # Apply winsorization (capping) for 'auto' or 'winz' methods
            if self.outliers in ['auto', 'winz']:  
                df = Outliers._winsorization(self, df)
            # Delete rows containing outliers
            elif self.outliers == 'delete':
                df = Outliers._delete(self, df)
            
            # Log execution time
            end = timer()
            logger.info('Completed handling of outliers in {} seconds', round(end-start, 6))
        else:
            logger.info('Skipped handling of outliers')
        
        return df     

    def _winsorization(self, df):
        """
        Caps outliers at computed lower and upper bounds (Winsorization).
        
        Winsorization is a technique that replaces extreme values with less extreme ones:
        - Values below the lower bound are set to the lower bound
        - Values above the upper bound are set to the upper bound
        
        This preserves the row (unlike deletion) but reduces the impact of extreme values.
        
        Args:
            df (pd.DataFrame): DataFrame containing potential outliers
            
        Returns:
            pd.DataFrame: DataFrame with outliers capped at bounds
            
        Note:
            - Only processes numerical columns
            - Preserves integer type if original data were integers
            - Uses IQR method to compute bounds
        """
        # Get all numerical columns
        cols_num = df.select_dtypes(include=np.number).columns    
        
        for feature in cols_num:           
            counter = 0  # Track number of outliers handled
            
            # Compute the lower and upper bounds for this feature
            lower_bound, upper_bound = Outliers._compute_bounds(self, df, feature)    
            
            # Check each value in the column
            for row_index, row_val in enumerate(df[feature]):
                # If value is outside bounds, cap it
                if row_val < lower_bound or row_val > upper_bound:
                    if row_val < lower_bound:
                        # Cap at lower bound
                        if (df[feature].fillna(-9999) % 1  == 0).all():
                            # Preserve integer type
                            df.loc[row_index, feature] = lower_bound
                            df[feature] = df[feature].astype(int) 
                        else:    
                            df.loc[row_index, feature] = lower_bound
                        counter += 1
                    else:
                        # Cap at upper bound
                        if (df[feature].fillna(-9999) % 1  == 0).all():
                            # Preserve integer type
                            df.loc[row_index, feature] = upper_bound
                            df[feature] = df[feature].astype(int) 
                        else:
                            df.loc[row_index, feature] = upper_bound
                        counter += 1
            
            # Log results for this feature
            if counter != 0:
                logger.debug('Outlier imputation of {} value(s) succeeded for feature "{}"', counter, feature)        
        
        return df

    def _delete(self, df):
        """
        Removes rows containing outliers from the DataFrame.
        
        This method completely removes any row where at least one numerical
        feature contains an outlier value (based on IQR bounds).
        
        Args:
            df (pd.DataFrame): DataFrame containing potential outliers
            
        Returns:
            pd.DataFrame: DataFrame with outlier rows removed
            
        Warning:
            - This reduces dataset size
            - Can lead to significant data loss if many outliers exist
            - May introduce bias if outliers contain important information
        """
        # Get all numerical columns
        cols_num = df.select_dtypes(include=np.number).columns    
        
        for feature in cols_num:
            counter = 0  # Track number of outliers deleted
            
            # Compute the lower and upper bounds for this feature
            lower_bound, upper_bound = Outliers._compute_bounds(self, df, feature)    
            
            # Identify and delete rows with outliers
            for row_index, row_val in enumerate(df[feature]):
                if row_val < lower_bound or row_val > upper_bound:
                    df = df.drop(row_index)
                    counter +=1
            
            # Reset index after deletion to avoid gaps
            df = df.reset_index(drop=True)
            
            # Log results for this feature
            if counter != 0:
                logger.debug('Deletion of {} outliers succeeded for feature "{}"', counter, feature)
        
        return df

    def _compute_bounds(self, df, feature):
        """
        Computes lower and upper bounds for outlier detection using IQR method.
        
        The Interquartile Range (IQR) method defines outliers as values that fall outside:
            Lower Bound = Q1 - (k × IQR)
            Upper Bound = Q3 + (k × IQR)
        
        where:
            - Q1 = 25th percentile (first quartile)
            - Q3 = 75th percentile (third quartile)
            - IQR = Q3 - Q1 (interquartile range)
            - k = self.outlier_param (typically 1.5)
        
        Args:
            df (pd.DataFrame): DataFrame containing the feature
            feature (str): Name of the column to compute bounds for
            
        Returns:
            tuple: (lower_bound, upper_bound) for outlier detection
            
        Note:
            - Standard k=1.5 identifies "moderate" outliers
            - k=3.0 identifies "extreme" outliers
            - Smaller k values are more aggressive in detecting outliers
        """
        # Sort the feature values
        featureSorted = sorted(df[feature])
        
        # Calculate Q1 (25th percentile) and Q3 (75th percentile)
        q1, q3 = np.percentile(featureSorted, [25, 75])
        
        # Calculate the Interquartile Range
        iqr = q3 - q1

        # Compute bounds using the IQR method
        lb = q1 - (self.outlier_param * iqr)  # Lower bound
        ub = q3 + (self.outlier_param * iqr)  # Upper bound

        return lb, ub
