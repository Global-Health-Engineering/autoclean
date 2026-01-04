# Imported libraries
import pandas as pd

# Import cleaning functions
from Functions.Pre_Processing import preprocess_data
from Functions.Duplicates import handle_duplicates
from Functions.Missing_Values import handle_missing_values
from Functions.DateTime_Standardization import standardize_datetime
from Functions.Outliers import handle_outliers
from Functions.Structural_Errors import fix_structural_errors
from Functions.Post_Processing import postprocess_data
from Functions.Cleaning_Report import generate_cleaning_report


# =============================================================================
# SETTINGS
# =============================================================================

INPUT_FILE = 'Data/Test/Test.csv'
OUTPUT_FILE = 'Data/Test/Test_Cleaned.csv'
REPORT_FILE = 'Data/Test/Test_Report.md'


# =============================================================================
# LOAD DATA
# =============================================================================

df_original, df, report_pre = preprocess_data(INPUT_FILE,
                                              clean_names = True)


# =============================================================================
# DUPLICATES
# =============================================================================

df, report_dup = handle_duplicates(df)


# =============================================================================
# MISSING VALUES
# =============================================================================
"""
df, report_miss = handle_missing_values(df,
                                        method_num = 'mean',
                                        method_categ = 'mode',
                                        columns = None,
                                        n_neighbors = 5,
                                        max_iter = 10,
                                        n_estimators = 10)
"""


# =============================================================================
# DATETIME STANDARDIZATION
# =============================================================================
"""
df, report_date = standardize_datetime(df,
                                       column = 'date',
                                       american = False,
                                       handle_invalid = 'nat')
"""


# =============================================================================
# OUTLIERS
# =============================================================================
"""
df, report_out = handle_outliers(df,
                                 method = 'winsorize',
                                 multiplier = 1.5)
"""


# =============================================================================
# STRUCTURAL ERRORS
# =============================================================================
"""
df, report_struct = fix_structural_errors(df,
                                          column = 'city',
                                          similarity = 'rapidfuzz',
                                          clustering = 'hierarchical',
                                          canonical = 'most_frequent',
                                          threshold = 0.85,
                                          embedding_model = 'text-embedding-3-small')
"""


# =============================================================================
# POST-PROCESSING
# =============================================================================

df, report_post = postprocess_data(df, df_original)


# =============================================================================
# SAVE OUTPUT
# =============================================================================

df.to_csv(OUTPUT_FILE, index=False)


# =============================================================================
# GENERATE REPORT
# =============================================================================

reports = {
    'preprocessing': report_pre,
    'duplicates': report_dup,
    # 'missing_values': report_miss,
    # 'datetime': report_date,
    # 'outliers': report_out,
    # 'structural_errors': report_struct,
    'postprocessing': report_post
}
generate_cleaning_report(reports, REPORT_FILE, dataset_name=INPUT_FILE)