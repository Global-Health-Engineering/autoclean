# Imported libraries
import pandas as pd

# Import cleaning functions
from Functions.Pre_Processing import preprocess_data
from Functions.Duplicates import handle_duplicates
from Functions.Missing_Values import handle_missing_values
from Functions.DateTime_Standardization import standardize_datetime
from Functions.Outliers import handle_outliers
from Functions.Structural_Errors import handle_structural_errors
from Functions.Post_Processing import postprocess_data
from Functions.Cleaning_Report import generate_cleaning_report


# =============================================================================
# SETTINGS
# =============================================================================

DATASET_NAME = 'Manager Data' # Used for report title
INPUT_FILE = 'Data/Manager/Manager.csv'
OUTPUT_FILE = 'Data/Manager/Manager_Cleaned.csv'
REPORT_FILE = 'Data/Manager/Manager_Report.md'

# =============================================================================
# PRE-PROCESSING
# =============================================================================

df_original, df, report_pre = preprocess_data(INPUT_FILE, clean_names=True)

# =============================================================================
# DUPLICATES
# =============================================================================

df, report_dup = handle_duplicates(df)

# =============================================================================
# DATETIME STANDARDIZATION 
# =============================================================================
"""
df, report_date = standardize_datetime(df,
                                       column='',  
                                       american=False,
                                       handle_invalid='nat')
"""

# =============================================================================
# OUTLIERS
# =============================================================================

"""
df, report_out = handle_outliers(df,
                                 method='winsorize',
                                 multiplier=1.5)
"""

# =============================================================================
# STRUCTURAL ERRORS 
# =============================================================================
# List to collect all structural error reports
structural_reports = []

# Pass 1: 
df, report1 = handle_structural_errors(df,
                                       column='what_country_do_you_work_in_',
                                       similarity='rapidfuzz',
                                       clustering='hierarchical',
                                       canonical='most_frequent',
                                       threshold_cc=0.88, 
                                       threshold_h=0.82)
structural_reports.append(report1)

# Pass 2: 
df, report2 = handle_structural_errors(df,
                                       column='what_country_do_you_work_in_',
                                       similarity='embeddings',
                                       clustering='hierarchical',
                                       canonical='most_frequent',
                                       threshold_cc=0.73,
                                       threshold_h=0.65,
                                       embedding_model='text-embedding-3-large')
structural_reports.append(report2)


# =============================================================================
# MISSING VALUES
# =============================================================================

"""
df, report_miss = handle_missing_values(df,
                                        method_num='mean',
                                        method_categ='mode',
                                        columns=None,
                                        n_neighbors=5,
                                        max_iter=10,
                                        n_estimators=10)
"""

# =============================================================================
# POST-PROCESSING
# =============================================================================

df, report_post = postprocess_data(df, df_original)

# =============================================================================
# SAVE OUTPUT
# =============================================================================

df.to_csv(OUTPUT_FILE, index=False) # index = false removes column with row numbers

# =============================================================================
# GENERATE REPORT
# =============================================================================

reports = {'preprocessing': report_pre,
           'duplicates': report_dup,
          #'missing_values': report_miss,
          #'datetime': report_date,          
          #'outliers': report_out,
           'structural_errors': structural_reports,  
           'postprocessing': report_post}

generate_cleaning_report(reports, REPORT_FILE, dataset_name = DATASET_NAME)