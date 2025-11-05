from timeit import default_timer as timer
from loguru import logger
import warnings
warnings.filterwarnings('ignore')

'''
Module for handling duplicate rows in the AutoClean pipeline.

This module provides functionality for detecting and removing duplicate rows
from a DataFrame. Duplicate rows are rows where all column values are identical
to another row in the dataset.

Removing duplicates is important for:
- Reducing dataset size and memory usage
- Preventing bias in statistical analysis and machine learning models
- Ensuring data quality and integrity
'''

class Duplicates:

    def handle(self, df):
        """
        Identifies and removes duplicate rows from the DataFrame.
        
        A duplicate row is defined as a row where ALL column values match
        another row exactly. The first occurrence of each unique row is kept,
        and subsequent duplicates are removed.
        
        Args:
            df (pd.DataFrame): DataFrame potentially containing duplicate rows
            
        Returns:
            pd.DataFrame: DataFrame with duplicate rows removed
            
        Process:
            1. Records original DataFrame shape
            2. Removes duplicate rows using pandas drop_duplicates()
            3. Resets the index to avoid gaps in row numbers
            4. Calculates and logs the number of duplicates removed
            5. Logs execution time
            
        Note:
            - Only runs if self.duplicates is set to True
            - Preserves the first occurrence of each unique row
            - Maintains column order and data types
        """
        # Check if duplicate handling is requested
        if self.duplicates:
            logger.info('Started handling of duplicates... Method: "{}"', str(self.duplicates).upper())
            start = timer()
            
            # Store original shape to calculate how many duplicates were removed
            original = df.shape
            
            try:
                # Remove duplicate rows (keeps first occurrence)
                df.drop_duplicates(inplace=True, ignore_index=False)
                
                # Reset index to avoid gaps in row numbers
                df = df.reset_index(drop=True)
                
                # Calculate how many rows were removed
                new = df.shape
                count = original[0] - new[0]  # Difference in number of rows
                
                # Log results
                if count != 0:
                    logger.debug('Deletion of {} duplicate(s) succeeded', count)
                else:
                    logger.debug('{} missing values found', count)
                
                # Log execution time
                end = timer()
                logger.info('Completed handling of duplicates in {} seconds', round(end-start, 6))

            except:
                logger.warning('Handling of duplicates failed')        
        else:
            logger.info('Skipped handling of duplicates')
        
        return df
