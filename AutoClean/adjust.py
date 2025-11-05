from timeit import default_timer as timer
import pandas as pd
from loguru import logger
import warnings
warnings.filterwarnings('ignore')

'''
Module for adjusting data types and converting datetime features in the AutoClean pipeline.

This module provides functionality for:
1. Extracting datetime components (day, month, year, hour, minute, second) from datetime strings
2. Converting feature types and adjusting decimal precision to match original data
'''

class Adjust:

    def convert_datetime(self, df):
        """
        Extracts datetime components from string-formatted datetime columns.
        
        This method identifies datetime columns and extracts individual components
        based on the specified granularity level. It creates new columns for each
        component (Day, Month, Year, Hour, Minute, Sec) and removes components
        that are all zeros.
        
        Args:
            df (pd.DataFrame): DataFrame potentially containing datetime strings
            
        Returns:
            pd.DataFrame: DataFrame with datetime components extracted into separate columns
            
        Granularity options (self.extract_datetime):
            - 'auto' or 's': Extract all components (Day through Second)
            - 'm': Extract Day through Minute
            - 'h': Extract Day through Hour
            - 'Y': Extract Day through Year
            - 'M': Extract Day through Month
            - 'D': Extract Day only
            
        Note:
            - Only processes non-numeric columns
            - Skips columns that cannot be converted to datetime
            - Removes time components if all zeros (date-only data)
            - Removes date components if all zeros (time-only data)
        """
        # Check if datetime extraction is requested
        if self.extract_datetime:
            logger.info('Started conversion of DATETIME features... Granularity: {}', self.extract_datetime)
            start = timer()
            
            # Get all non-numeric columns (potential datetime strings)
            cols = set(df.columns) ^ set(df.select_dtypes(include='number').columns) 
            
            for feature in cols: 
                try:
                    # Attempt to convert string to datetime format
                    df[feature] = pd.to_datetime(df[feature], infer_datetime_format=True)
                    
                    try:
                        # Extract Day component (always extracted)
                        df['Day'] = pd.to_datetime(df[feature]).dt.day

                        # Extract Month (if granularity >= 'M')
                        if self.extract_datetime in ['auto', 'M','Y','h','m','s']:
                            df['Month'] = pd.to_datetime(df[feature]).dt.month

                            # Extract Year (if granularity >= 'Y')
                            if self.extract_datetime in ['auto', 'Y','h','m','s']:
                                df['Year'] = pd.to_datetime(df[feature]).dt.year

                                # Extract Hour (if granularity >= 'h')
                                if self.extract_datetime in ['auto', 'h','m','s']:
                                    df['Hour'] = pd.to_datetime(df[feature]).dt.hour

                                    # Extract Minute (if granularity >= 'm')
                                    if self.extract_datetime in ['auto', 'm','s']:
                                        df['Minute'] = pd.to_datetime(df[feature]).dt.minute

                                        # Extract Second (if granularity == 's' or 'auto')
                                        if self.extract_datetime in ['auto', 's']:
                                            df['Sec'] = pd.to_datetime(df[feature]).dt.second
                        
                        logger.debug('Conversion to DATETIME succeeded for feature "{}"', feature)

                        try: 
                            # Clean up: Remove time components if they're all zeros (date-only data)
                            if (df['Hour'] == 0).all() and (df['Minute'] == 0).all() and (df['Sec'] == 0).all():
                                df.drop('Hour', inplace = True, axis =1 )
                                df.drop('Minute', inplace = True, axis =1 )
                                df.drop('Sec', inplace = True, axis =1 )
                            # Clean up: Remove date components if they're all zeros (time-only data)
                            elif (df['Day'] == 0).all() and (df['Month'] == 0).all() and (df['Year'] == 0).all():
                                df.drop('Day', inplace = True, axis =1 )
                                df.drop('Month', inplace = True, axis =1 )
                                df.drop('Year', inplace = True, axis =1 )   
                        except:
                            # Columns may not exist depending on granularity setting
                            pass          
                    except:
                        # Feature could not be converted to datetime
                        logger.warning('Conversion to DATETIME failed for "{}"', feature)
                except:
                    # Not a datetime column, skip it
                    pass
            
            # Log execution time
            end = timer()
            logger.info('Completed conversion of DATETIME features in {} seconds', round(end-start, 4))
        else:
            logger.info('Skipped datetime feature conversion')
        
        return df

    def round_values(self, df, input_data):
        """
        Adjusts numerical data types and decimal precision to match original data.
        
        This method ensures that after all data transformations:
        1. Integer columns remain as integers (not converted to floats)
        2. Float columns maintain their original decimal precision
        
        This is important because many data processing steps (imputation, outlier
        handling, etc.) can inadvertently change data types or add unnecessary
        decimal places.
        
        Args:
            df (pd.DataFrame): The processed DataFrame (after transformations)
            input_data (pd.DataFrame): The original input DataFrame (for reference)
            
        Returns:
            pd.DataFrame: DataFrame with corrected data types and precision
            
        Note:
            - Only runs if at least one transformation was applied
            - Checks each numerical column individually
            - Uses original data to determine appropriate decimal places
        """
        # Only perform type conversion if some transformation was applied
        if self.duplicates or self.missing_num or self.missing_categ or self.outliers or self.encode_categ or self.extract_datetime:
            logger.info('Started feature type conversion...')
            start = timer()
            counter = 0  # Track number of features converted
            
            # Get all numerical columns
            cols_num = df.select_dtypes(include='number').columns
            
            for feature in cols_num:
                    # Check if all values are integers (no decimal parts)
                    # Using -9999 as placeholder for NaN when checking modulo
                    if (df[feature].fillna(-9999) % 1  == 0).all():
                        try:
                            # Convert to integer type (Int64 supports NaN values)
                            df[feature] = df[feature].astype('Int64')
                            counter += 1
                            logger.debug('Conversion to type INT succeeded for feature "{}"', feature)
                        except:
                            logger.warning('Conversion to type INT failed for feature "{}"', feature)
                    else:
                        # Feature contains decimal values, handle as float
                        try:
                            df[feature] = df[feature].astype(float)
                            
                            # Determine original decimal precision from input data
                            dec = None  # Number of decimal places
                            for value in input_data[feature]:
                                try:
                                    # Find the decimal point position by reversing the string
                                    # e.g., "123.45" -> "54.321", find('.') = 2 decimal places
                                    if dec == None:
                                        dec = str(value)[::-1].find('.')
                                    else:
                                        # Keep the maximum decimal places found
                                        if str(value)[::-1].find('.') > dec:
                                            dec = str(value)[::-1].find('.')
                                except:
                                    # Skip values that can't be converted to string (e.g., NaN)
                                    pass
                            
                            # Round to the original number of decimal places
                            df[feature] = df[feature].round(decimals = dec)
                            counter += 1
                            logger.debug('Conversion to type FLOAT succeeded for feature "{}"', feature)
                        except:
                            logger.warning('Conversion to type FLOAT failed for feature "{}"', feature)
            
            # Log execution time
            end = timer()
            logger.info('Completed feature type conversion for {} feature(s) in {} seconds', counter, round(end-start, 6))
        else:
            logger.info('Skipped feature type conversion')
        
        return df
