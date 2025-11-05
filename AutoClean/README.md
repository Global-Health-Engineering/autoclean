# AutoClean - Modular Structure

This is a refactored version of AutoClean with the code organized into separate, well-documented modules for better maintainability and understanding.

## File Structure

```
autoclean/
├── autoclean.py          # Main AutoClean class and pipeline orchestration
├── missing_values.py     # Missing value imputation methods
├── outliers.py           # Outlier detection and handling
├── adjust.py             # Data type adjustment and datetime extraction
├── encode_categ.py       # Categorical feature encoding
├── duplicates.py         # Duplicate row handling
└── README.md            # This file
```

## Module Descriptions

### 1. **autoclean.py** - Main Pipeline Controller
The main AutoClean class that:
- Accepts user parameters for data cleaning
- Validates all input parameters
- Orchestrates the cleaning pipeline in optimal order
- Manages logging and timing

**Key Components:**
- `AutoClean.__init__()`: Main entry point with all parameters
- `_validate_params()`: Comprehensive parameter validation
- `_clean_data()`: Executes the cleaning pipeline
- `_initialize_logger()`: Sets up logging system

### 2. **missing_values.py** - Missing Value Handling
Handles missing data in both numerical and categorical features.

**Available Methods:**
- **Linear Regression** (`linreg`): Predicts numerical missing values
- **Logistic Regression** (`logreg`): Predicts categorical missing values
- **K-Nearest Neighbors** (`knn`): Imputation based on similar samples
- **Statistical** (`mean`, `median`, `most_frequent`): Simple statistical imputation
- **Deletion** (`delete`): Removes rows with missing values
- **Auto** (`auto`): Combines regression and KNN methods

**Key Functions:**
- `handle()`: Main handler for missing values
- `_impute()`: Generic imputation using sklearn
- `_lin_regression_impute()`: Linear regression imputation
- `_log_regression_impute()`: Logistic regression imputation
- `_delete()`: Deletion of missing values

### 3. **outliers.py** - Outlier Detection & Handling
Detects and handles outliers using the IQR (Interquartile Range) method.

**Methods:**
- **Winsorization** (`winz`): Caps outliers at computed bounds
- **Deletion** (`delete`): Removes rows containing outliers

**Outlier Detection:**
Uses IQR method: `[Q1 - k*IQR, Q3 + k*IQR]`
- Q1 = 25th percentile
- Q3 = 75th percentile
- IQR = Q3 - Q1
- k = outlier_param (default: 1.5)

**Key Functions:**
- `handle()`: Main outlier handler
- `_winsorization()`: Caps outliers at bounds
- `_delete()`: Removes outlier rows
- `_compute_bounds()`: Calculates IQR-based bounds

### 4. **adjust.py** - Data Type & Datetime Adjustment
Handles data type conversions and datetime feature extraction.

**Features:**
- Extracts datetime components (Day, Month, Year, Hour, Minute, Second)
- Converts data types to match original precision
- Maintains integer types where appropriate
- Rounds floats to original decimal places

**Key Functions:**
- `convert_datetime()`: Extracts datetime components
- `round_values()`: Adjusts types and precision

### 5. **encode_categ.py** - Categorical Encoding
Converts categorical features to numerical representations.

**Encoding Methods:**
- **One-Hot Encoding**: Creates binary columns for each category
  - Best for low cardinality (≤10 unique values)
  - Example: Color ['red', 'blue'] → Color_red [1,0], Color_blue [0,1]
  
- **Label Encoding**: Assigns integer codes to categories
  - Best for medium cardinality (11-20 unique values)
  - Example: Size ['S', 'M', 'L'] → Size_lab [0, 1, 2]

- **Auto Mode**: Automatically selects encoding based on cardinality

**Key Functions:**
- `handle()`: Main encoding handler
- `_to_onehot()`: One-hot encoding
- `_to_label()`: Label encoding

### 6. **duplicates.py** - Duplicate Row Removal
Identifies and removes duplicate rows from the DataFrame.

**Behavior:**
- Detects rows where ALL columns have identical values
- Keeps the first occurrence
- Removes subsequent duplicates
- Resets index after removal

**Key Functions:**
- `handle()`: Detects and removes duplicates

## Usage Example

```python
import pandas as pd
from autoclean import AutoClean

# Load your data
df = pd.read_csv('data.csv')

# Automatic mode (recommended for quick cleaning)
cleaner = AutoClean(df, mode='auto')
cleaned_df = cleaner.output

# Manual mode with custom parameters
cleaner = AutoClean(
    df, 
    mode='manual',
    duplicates='auto',           # Remove duplicates
    missing_num='knn',            # KNN imputation for numbers
    missing_categ='most_frequent', # Mode imputation for categories
    outliers='winz',              # Winsorize outliers
    encode_categ=['onehot'],      # One-hot encode all categories
    extract_datetime='Y',         # Extract up to year
    outlier_param=1.5,            # Standard IQR multiplier
    logfile=True,                 # Create log file
    verbose=False                 # Don't print to console
)
cleaned_df = cleaner.output
```

## Pipeline Execution Order

The cleaning pipeline executes in the following order for optimal results:

1. **Duplicates** → Reduce data size first
2. **Missing Values** → Handle before other operations
3. **Outliers** → Detect in clean data
4. **Datetime Extraction** → Create new features
5. **Categorical Encoding** → Convert to numerical
6. **Type Adjustment** → Finalize types and precision

## Parameter Guide

### Mode Options
- `'auto'`: Uses optimal defaults for all parameters
- `'manual'`: Allows custom configuration

### Missing Value Methods
**Numerical:**
- `'auto'`: Linear regression + KNN
- `'linreg'`: Linear regression prediction
- `'knn'`: K-nearest neighbors
- `'mean'`: Mean imputation
- `'median'`: Median imputation
- `'most_frequent'`: Mode imputation
- `'delete'`: Remove rows
- `False`: Skip

**Categorical:**
- `'auto'`: Logistic regression + KNN
- `'logreg'`: Logistic regression prediction
- `'knn'`: K-nearest neighbors
- `'most_frequent'`: Mode imputation
- `'delete'`: Remove rows
- `False`: Skip

### Outlier Methods
- `'auto'` or `'winz'`: Winsorization (capping)
- `'delete'`: Remove rows
- `False`: Skip

### Encoding Options
- `['auto']`: Smart encoding based on cardinality
- `['onehot']`: One-hot encode all
- `['label']`: Label encode all
- `['onehot', ['col1', 'col2']]`: Encode specific columns
- `False`: Skip

### Datetime Granularity
- `'s'`: Second-level (all components)
- `'m'`: Minute-level
- `'h'`: Hour-level
- `'Y'`: Year-level
- `'M'`: Month-level
- `'D'`: Day-level
- `False`: Skip

## Benefits of Modular Structure

1. **Readability**: Each module focuses on one specific task
2. **Maintainability**: Easy to update individual components
3. **Testability**: Can test each module independently
4. **Extensibility**: Easy to add new cleaning methods
5. **Documentation**: Each module is thoroughly commented
6. **Reusability**: Modules can be imported separately if needed

## Requirements

```
pandas
numpy
scikit-learn
loguru
```

## Notes

- All modules preserve data types (integers stay integers, floats maintain precision)
- Original columns are preserved when encoding (new columns are added)
- Logging captures all operations for transparency
- Each module handles errors gracefully with informative messages

## License

This is a refactored version of AutoClean by Elise Mercury.
Original repository: https://github.com/elisemercury/AutoClean
