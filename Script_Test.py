"""
Script to apply cleaning pipeline to dataset Test.csv

Test.csv: made up WASH dataset (monitoring rural water points in East African villages), to demonstrate the cleaning functions & pipeline
"""

# Import cleaning functions
from Functions.Pre_Processing import preprocess_data
from Functions.Duplicates import handle_duplicates
from Functions.Semantic_Outliers import handle_semantic_outliers
from Functions.Outliers import handle_outliers
from Functions.DateTime_Standardization import standardize_datetime
from Functions.Structural_Errors import handle_structural_errors
from Functions.Missing_Values import handle_missing_values
from Functions.Post_Processing import postprocess_data
from Functions.Cleaning_Report import generate_cleaning_report

# =============================================================================
# SETTINGS
# =============================================================================

INPUT_FILEPATH = 'Data/Test/Test.csv'

# Optional:
DATASET_NAME = 'Test Data (made up WHASH dataset)' # For header in Cleaning Report
OUTPUT_FILEPATH = 'Data/Test/Test_Cleaned.csv'
REPORT_FILEPATH = 'Data/Test/Test_Report.md'

# =============================================================================
# PRE-PROCESSING
# =============================================================================

df, df_original, report_pre = preprocess_data(INPUT_FILEPATH)

# =============================================================================
# DUPLICATES
# =============================================================================

df, report_dup = handle_duplicates(df)

# =============================================================================
# SEMANTIC OUTLIERS
# =============================================================================
'''
# Define list to store all reports of handle_semantic_outliers()
report_sem = []

df, report_sem1 = handle_semantic_outliers(df,
                                           column = 'Village',
                                           context = 'Location names in Africa',
                                           threshold = 0.5,
                                           action = 'nan')
report_sem.append(report_sem1)

df, report_sem2 = handle_semantic_outliers(df,
                                           column = 'Population served',
                                           context = 'Number of people',
                                           threshold = 0.5,
                                           action = 'nan')
report_sem.append(report_sem2)
'''
# =============================================================================
# OUTLIERS
# =============================================================================
'''
df, report_out = handle_outliers(df,
                                 method = 'winsorize',
                                 multiplier = 1.5)
'''
# =============================================================================
# DATETIME STANDARDIZATION 
# =============================================================================
'''
df, report_date = standardize_datetime(df,
                                       column = 'install_date',  
                                       american = False,
                                       handle_invalid = 'nat')
'''
# =============================================================================
# STRUCTURAL ERRORS 
# =============================================================================

# Define list to store all reports of handle_structural_errors()
report_str = []

df, report_str1 = handle_structural_errors(df,
                                           column = 'funding organization',
                                           similarity = 'embeddings',
                                           embedding_model = 'text-embedding-3-large',
                                           clustering = 'connected_components',
                                           threshold_cc = 0.6,
                                           canonical = 'llm')
report_str.append(report_str1)
df, report_str2 = handle_structural_errors(df,
                                           column = 'funding organization',
                                           similarity = 'llm',
                                           llm_mode = 'fast',
                                           llm_context = 'Funding organizations',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.9,
                                           canonical = 'llm')
report_str.append(report_str2)


'''
df, report_str3 = handle_structural_errors(df,
                                          column = 'water_source',
                                          similarity = 'rapidfuzz',
                                          clustering = 'hierarchical',
                                          threshold_h = 0.85,
                                          canonical = 'llm')
report_str.append(report_str3) 
'''
'''
df, report_str4 = handle_structural_errors(df,
                                           column = 'is_functional',
                                           similarity = 'rapidfuzz',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.8,
                                           canonical = 'most_frequent')
report_str.append(report_str4)# 0.85


df, report_str5 = handle_structural_errors(df,
                                           column = 'is_functional',
                                           similarity = 'llm',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.7,
                                           llm_context = 'Wether water point is working or not',
                                           canonical = 'llm')
report_str.append(report_str5)
'''
'''
df, report_str1 = handle_structural_errors(df,
                                           column = 'sample Volume',
                                           similarity = 'rapidfuzz',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.6,
                                           canonical = 'llm')
report_str.append(report_str1)# 0.9

df, report_str1 = handle_structural_errors(df,
                                           column = 'sample Volume',
                                           similarity = 'llm',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.9,
                                           units = True,
                                           llm_context = 'Volume measurements',
                                           canonical = 'llm')
report_str.append(report_str1)
'''
'''
df, report_str6 = handle_structural_errors(df,
                                           column = 'staff_count',
                                           similarity = 'llm',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.7,
                                           llm_context = 'Number of staff working',
                                           canonical = 'llm')
report_str.append(report_str6)
'''
# =============================================================================
# POST-PROCESSING
# =============================================================================

report_post = postprocess_data(df, df_original, OUTPUT_FILEPATH, clean_names = True, rounding = True)

# =============================================================================
# GENERATE REPORT
# =============================================================================

reports = {'preprocessing': report_pre,
           'duplicates': report_dup,
           #'semantic_outliers': report_sem,
           #'outliers': report_out,
           #'datetime': report_date,
           'structural_errors': report_str,
           #'missing_values': report_miss,
           'postprocessing': report_post}

generate_cleaning_report(reports, REPORT_FILEPATH, DATASET_NAME)