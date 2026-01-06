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

DATASET_NAME = 'Test Data' # Used for report title
INPUT_FILE = 'Data/Test/Test.csv'
OUTPUT_FILE = 'Data/Test/Test_Cleaned.csv'
REPORT_FILE = 'Data/Test/Test_Report.md'

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

df, report_date = standardize_datetime(df,
                                       column='date_installed',  
                                       american=False,
                                       handle_invalid='nat')


# =============================================================================
# OUTLIERS
# =============================================================================

df, report_out = handle_outliers(df,
                                 method='winsorize',
                                 multiplier=1.5)

# =============================================================================
# STRUCTURAL ERRORS 
# =============================================================================

# List to collect all structural error reports
structural_reports = []

# city: NYC, NY, New York, etc. → semantic variations, use embeddings + affinity propagation
df, report = handle_structural_errors(df,
                                      column='city',  
                                      similarity='embeddings',
                                      clustering='affinity_propagation',
                                      canonical='llm',
                                      embedding_model='text-embedding-3-small')
structural_reports.append(report)

# facility_type: Hospital, hospital, HOSPITAL, Hosptial (typos) → use rapidfuzz + low threshold
df, report = handle_structural_errors(df,
                                      column='facility_type',  
                                      similarity='rapidfuzz',
                                      clustering='connected_components',
                                      canonical='most_frequent',
                                      threshold_h=0.75)
structural_reports.append(report)

# water_source: Borehole, bore hole, Borehole well, Hand pump → rapidfuzz + low threshold
df, report = handle_structural_errors(df,
                                      column='water_source',  
                                      similarity='rapidfuzz',
                                      clustering='connected_components',
                                      canonical='most_frequent',
                                      threshold_h=0.75)
structural_reports.append(report)

# funding_organization: WHO, W.H.O., World Health Organization → semantic, needs embeddings + low threshold
df, report = handle_structural_errors(df,
                                      column='funding_organization',  
                                      similarity='embeddings',
                                      clustering='hierarchical',
                                      canonical='llm',
                                      threshold_h=0.60,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report)

# daily_usage: 500L, 480 liters, 520000ml → very different strings but same concept
# Using embeddings with very low threshold to try grouping similar units
df, report = handle_structural_errors(df,
                                      column='daily_usage',  
                                      similarity='embeddings',
                                      clustering='affinity_propagation',
                                      canonical='llm',
                                      threshold_h=0.70,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report)

# is_functional: Yes, Y, 1, true, TRUE → semantic similarity with low threshold
df, report = handle_structural_errors(df,
                                      column='is_functional',  
                                      similarity='embeddings',
                                      clustering='hierarchical',
                                      canonical='llm',
                                      threshold_h=0.70,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report)

# maintenance_frequency: Monthly, monthly, MONTHLY, Mothly (typos) → rapidfuzz for typos
df, report = handle_structural_errors(df,
                                      column='maintenance_frequency',  
                                      similarity='rapidfuzz',
                                      clustering='hierarchical',
                                      canonical='most_frequent',
                                      threshold_h=0.70)
structural_reports.append(report)

# number_of_staff: 25, twenty-six, twelve → very different (numbers vs words)
# Using embeddings with low threshold to try semantic grouping
df, report = handle_structural_errors(df,
                                      column='number_of_staff',  
                                      similarity='embeddings',
                                      clustering='affinity_propagation',
                                      canonical='llm',
                                      threshold_h=0.50,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report)

# =============================================================================
# MISSING VALUES
# =============================================================================

df['water_quality_score'] = pd.to_numeric(df['water_quality_score'], errors='coerce')

df, report_miss = handle_missing_values(df,
                                        method_num='missforest',
                                        method_categ='false',
                                        columns=['water_quality_score'],
                                        n_neighbors=5,
                                        max_iter=10,
                                        n_estimators=10)

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
           'missing_values': report_miss,
           'datetime': report_date,          
           'outliers': report_out,
           'structural_errors': structural_reports,  # Now a LIST of reports
           'postprocessing': report_post}

generate_cleaning_report(reports, REPORT_FILE, dataset_name=DATASET_NAME)