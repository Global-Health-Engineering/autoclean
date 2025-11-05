"""
AutoClean - Automated Data Cleaning Pipeline
=============================================

AutoClean is a comprehensive data cleaning and preprocessing tool that automates
common data preparation tasks for machine learning and data analysis.

Main Features:
- Duplicate row detection and removal
- Missing value imputation (numerical and categorical)
- Outlier detection and handling
- Datetime feature extraction
- Categorical feature encoding
- Data type adjustment and precision preservation

For detailed documentation and usage guide, please visit:
https://github.com/elisemercury/AutoClean

Author: Elise Mercury
Year: 2022
"""

import os
import sys
from timeit import default_timer as timer
import pandas as pd
from loguru import logger

# Import all cleaning modules
from missing_values import MissingValues
from outliers import Outliers
from adjust import Adjust
from encode_categ import EncodeCateg
from duplicates import Duplicates


class AutoClean:
    """
    Main AutoClean class for automated data cleaning and preprocessing.
    
    AutoClean provides a unified interface for performing various data cleaning
    operations on pandas DataFrames. It can run in automatic mode (with sensible
    defaults) or manual mode (with custom parameters).
    
    The cleaning pipeline executes steps in the following order:
    1. Duplicate removal
    2. Missing value handling
    3. Outlier handling
    4. Datetime extraction
    5. Categorical encoding
    6. Data type adjustment
    
    Example:
        >>> import pandas as pd
        >>> from autoclean import AutoClean
        >>> df = pd.read_csv('data.csv')
        >>> cleaner = AutoClean(df, mode='auto')
        >>> cleaned_df = cleaner.output
    """

    def __init__(self, input_data, mode='auto', duplicates=False, missing_num=False, 
                 missing_categ=False, encode_categ=False, extract_datetime=False, 
                 outliers=False, outlier_param=1.5, logfile=True, verbose=False):
        """
        Initialize AutoClean with data and cleaning parameters.
        
        Parameters:
        -----------
        input_data : pd.DataFrame
            The input pandas DataFrame to be cleaned
            
        mode : str, default='auto'
            Cleaning mode selection:
            - 'auto': Automatically applies all cleaning steps with optimal defaults
            - 'manual': Allows custom parameter configuration for each step
            
        duplicates : str or False, default=False
            How to handle duplicate rows (rows where all features are identical):
            - 'auto': Delete all duplicate copies, keeping first occurrence
            - False: Skip duplicate handling
            
        missing_num : str or False, default=False
            How to handle missing values in NUMERICAL features:
            - 'auto': Combines linear regression and KNN imputation
            - 'linreg': Use Linear Regression to predict missing values
            - 'knn': Use K-Nearest Neighbors algorithm for imputation
            - 'mean': Fill with column mean
            - 'median': Fill with column median
            - 'most_frequent': Fill with column mode
            - 'delete': Remove rows with missing numerical values
            - False: Skip numerical missing value handling
            
        missing_categ : str or False, default=False
            How to handle missing values in CATEGORICAL features:
            - 'auto': Combines logistic regression and KNN imputation
            - 'logreg': Use Logistic Regression to predict missing values
            - 'knn': Use K-Nearest Neighbors algorithm for imputation
            - 'most_frequent': Fill with column mode
            - 'delete': Remove rows with missing categorical values
            - False: Skip categorical missing value handling
            
        encode_categ : list or False, default=False
            How to encode CATEGORICAL features:
            - ['auto']: Automatically choose encoding based on cardinality
              (one-hot for ≤10 unique values, label for 11-20, skip if >20)
            - ['onehot']: One-hot encode all categorical features
            - ['label']: Label encode all categorical features
            - ['onehot', ['col1', 'col2']]: Encode only specific columns
            - False: Skip categorical encoding
            
        extract_datetime : str or False, default=False
            Whether to extract components from DATETIME features:
            - 'auto' or 's': Extract all components (Day, Month, Year, Hour, Minute, Second)
            - 'm': Extract Day through Minute
            - 'h': Extract Day through Hour
            - 'Y': Extract Day through Year
            - 'M': Extract Day through Month
            - 'D': Extract Day only
            - False: Skip datetime extraction
            
        outliers : str or False, default=False
            How to handle outliers in numerical features:
            - 'auto' or 'winz': Winsorization (cap outliers at computed bounds)
            - 'delete': Remove rows containing outliers
            - False: Skip outlier handling
            Note: Outliers are detected using IQR method:
            [Q1 - outlier_param*IQR, Q3 + outlier_param*IQR]
            
        outlier_param : int or float, default=1.5
            Multiplier for IQR in outlier detection bounds.
            Standard values:
            - 1.5: Identifies "moderate" outliers (standard)
            - 3.0: Identifies "extreme" outliers (conservative)
            
        logfile : bool, default=True
            Whether to create a log file during cleaning process.
            Log file is saved as "autoclean.log" in working directory.
            
        verbose : bool, default=False
            Whether to print AutoClean logs to console during execution.
            
        Attributes:
        -----------
        output : pd.DataFrame
            The cleaned DataFrame, accessible after initialization
            
        Examples:
        ---------
        Automatic mode (recommended for quick cleaning):
        >>> cleaner = AutoClean(df, mode='auto')
        >>> cleaned_df = cleaner.output
        
        Manual mode with custom parameters:
        >>> cleaner = AutoClean(
        ...     df, 
        ...     mode='manual',
        ...     duplicates='auto',
        ...     missing_num='knn',
        ...     missing_categ='most_frequent',
        ...     outliers='winz',
        ...     encode_categ=['onehot']
        ... )
        >>> cleaned_df = cleaner.output
        """
        # Start timing the cleaning process
        start = timer()
        
        # Initialize logging system
        self._initialize_logger(verbose, logfile)
        
        # Create a copy to avoid modifying original data
        output_data = input_data.copy()

        # Set automatic parameters if mode is 'auto'
        if mode == 'auto':
            duplicates = 'auto'
            missing_num = 'auto'
            missing_categ = 'auto'
            outliers = 'winz'
            encode_categ = ['auto']
            extract_datetime = 's'

        # Store all parameters as instance variables
        self.mode = mode
        self.duplicates = duplicates
        self.missing_num = missing_num
        self.missing_categ = missing_categ
        self.outliers = outliers
        self.encode_categ = encode_categ
        self.extract_datetime = extract_datetime
        self.outlier_param = outlier_param
        
        # Validate all input parameters before processing
        self._validate_params(output_data, verbose, logfile)
        
        # Execute the cleaning pipeline and store result
        self.output = self._clean_data(output_data, input_data)  

        # Calculate and log total execution time
        end = timer()
        logger.info('AutoClean process completed in {} seconds', round(end-start, 6))

        # Print completion message to console
        if not verbose:
            print('AutoClean process completed in', round(end-start, 6), 'seconds')
        if logfile:
            print('Logfile saved to:', os.path.join(os.getcwd(), 'autoclean.log'))

    def _initialize_logger(self, verbose, logfile):
        """
        Initialize the logging system for AutoClean.
        
        Sets up loguru logger to output to console and/or file based on parameters.
        The logger tracks all operations, warnings, and errors during the cleaning process.
        
        Parameters:
        -----------
        verbose : bool
            If True, log messages are printed to console (stderr)
        logfile : bool
            If True, log messages are saved to 'autoclean.log' in working directory
            
        Log Format:
        -----------
        Each log entry includes:
        - Timestamp (DD-MM-YYYY HH:mm:ss.SS)
        - Log level (INFO, DEBUG, WARNING, ERROR)
        - Message describing the operation
        
        Note:
        -----
        Removes any existing logger handlers before adding new ones to avoid duplication.
        """
        # Remove any existing logger handlers
        logger.remove()
        
        # Add console handler if verbose mode is enabled
        if verbose == True:
            logger.add(sys.stderr, format='{time:DD-MM-YYYY HH:mm:ss.SS} - {level} - {message}')
        
        # Add file handler if logfile is enabled
        if logfile == True:    
            logger.add('autoclean.log', mode='w', format='{time:DD-MM-YYYY HH:mm:ss.SS} - {level} - {message}')
        
        return

    def _validate_params(self, df, verbose, logfile):
        """
        Validate all input parameters to ensure they have acceptable values.
        
        This method performs comprehensive validation of all AutoClean parameters
        before the cleaning process begins. It raises ValueError with descriptive
        messages if any parameter has an invalid value.
        
        Parameters:
        -----------
        df : pd.DataFrame
            The input DataFrame to validate
        verbose : bool
            Verbose mode flag to validate
        logfile : bool
            Logfile mode flag to validate
            
        Raises:
        -------
        ValueError
            If any parameter has an invalid value, with a descriptive error message
            
        Validation Checks:
        ------------------
        - df must be a pandas DataFrame
        - mode must be 'manual' or 'auto'
        - duplicates must be False or 'auto'
        - missing_num must be one of the supported methods
        - missing_categ must be one of the supported methods
        - outliers must be one of the supported methods
        - encode_categ must follow the correct format (list or False)
        - outlier_param must be numeric (int or float)
        - extract_datetime must be one of the supported granularities
        - verbose and logfile must be boolean
        """
        logger.info('Started validation of input parameters...')
        
        # Validate input data type
        if type(df) != pd.core.frame.DataFrame:
            raise ValueError('Invalid value for "df" parameter. Must be a pandas DataFrame.')
        
        # Validate mode parameter
        if self.mode not in ['manual', 'auto']:
            raise ValueError('Invalid value for "mode" parameter. Must be "manual" or "auto".')
        
        # Validate duplicates parameter
        if self.duplicates not in [False, 'auto']:
            raise ValueError('Invalid value for "duplicates" parameter. Must be False or "auto".')
        
        # Validate missing_num parameter
        if self.missing_num not in [False, 'auto', 'linreg', 'knn', 'mean', 'median', 'most_frequent', 'delete']:
            raise ValueError('Invalid value for "missing_num" parameter. Must be False, "auto", "linreg", "knn", "mean", "median", "most_frequent", or "delete".')
        
        # Validate missing_categ parameter
        if self.missing_categ not in [False, 'auto', 'logreg', 'knn', 'most_frequent', 'delete']:
            raise ValueError('Invalid value for "missing_categ" parameter. Must be False, "auto", "logreg", "knn", "most_frequent", or "delete".')
        
        # Validate outliers parameter
        if self.outliers not in [False, 'auto', 'winz', 'delete']:
            raise ValueError('Invalid value for "outliers" parameter. Must be False, "auto", "winz", or "delete".')
        
        # Validate encode_categ parameter (more complex due to list format)
        if isinstance(self.encode_categ, list):
            # Check if encoding method is valid
            if len(self.encode_categ) > 2 or (len(self.encode_categ) >= 1 and self.encode_categ[0] not in ['auto', 'onehot', 'label']):
                raise ValueError('Invalid value for "encode_categ" parameter. First element must be "auto", "onehot", or "label".')
            # Check if column specification is valid
            if len(self.encode_categ) == 2:
                if not isinstance(self.encode_categ[1], list):
                    raise ValueError('Invalid value for "encode_categ" parameter. Second element must be a list of column names or indices.')
        else:
            # If not a list, must be False
            if self.encode_categ not in [False]:
                raise ValueError('Invalid value for "encode_categ" parameter. Must be a list (e.g., ["auto"]) or False.')
        
        # Validate outlier_param parameter
        if not isinstance(self.outlier_param, int) and not isinstance(self.outlier_param, float):
            raise ValueError('Invalid value for "outlier_param" parameter. Must be a number (int or float).')
        
        # Validate extract_datetime parameter
        if self.extract_datetime not in [False, 'auto', 'D', 'M', 'Y', 'h', 'm', 's']:
            raise ValueError('Invalid value for "extract_datetime" parameter. Must be False, "auto", "D", "M", "Y", "h", "m", or "s".')
        
        # Validate verbose parameter
        if not isinstance(verbose, bool):
            raise ValueError('Invalid value for "verbose" parameter. Must be True or False.')
        
        # Validate logfile parameter
        if not isinstance(logfile, bool):
            raise ValueError('Invalid value for "logfile" parameter. Must be True or False.')

        logger.info('Completed validation of input parameters')
        return
            
    def _clean_data(self, df, input_data):
        """
        Execute the complete data cleaning pipeline.
        
        This method orchestrates all cleaning steps in the optimal order to ensure
        best results. Each step uses the appropriate module class and passes the
        necessary parameters.
        
        Pipeline Execution Order:
        -------------------------
        1. Duplicates: Remove duplicate rows first to reduce data size
        2. Missing Values: Handle missing data before other operations
        3. Outliers: Detect and handle outliers in clean data
        4. Datetime Extraction: Create new features from datetime columns
        5. Categorical Encoding: Convert categories to numerical format
        6. Type Adjustment: Finalize data types and precision
        
        Parameters:
        -----------
        df : pd.DataFrame
            The DataFrame to clean (already copied from input)
        input_data : pd.DataFrame
            The original input DataFrame (used for type/precision reference)
            
        Returns:
        --------
        pd.DataFrame
            The fully cleaned DataFrame with all specified operations applied
            
        Note:
        -----
        - Each step is independent and can be skipped if not enabled
        - The order matters: e.g., outliers should be handled after missing values
        - Type adjustment is done last to preserve data types from all operations
        """
        # Reset index to ensure continuous numbering from 0
        df = df.reset_index(drop=True)
        
        # Step 1: Handle duplicate rows
        df = Duplicates.handle(self, df)
        
        # Step 2: Handle missing values (numerical and categorical)
        df = MissingValues.handle(self, df)
        
        # Step 3: Handle outliers in numerical features
        df = Outliers.handle(self, df)
        
        # Step 4: Extract datetime components into separate features
        df = Adjust.convert_datetime(self, df)
        
        # Step 5: Encode categorical features
        df = EncodeCateg.handle(self, df)
        
        # Step 6: Adjust data types and round values to match original precision
        df = Adjust.round_values(self, df, input_data)
        
        return df
