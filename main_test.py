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

DATASET_NAME = 'Test Data'
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

structural_reports = []

# city: NYC, NY, New York → semantic variations, needs embeddings
df, report = handle_structural_errors(df,
                                      column='city',  
                                      similarity='embeddings',
                                      clustering='affinity_propagation',
                                      canonical='most_frequent',
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report)

# facility_type: Hospital, HOSPITAL, Hosptial → case + typos, embeddings for semantic match
df, report = handle_structural_errors(df,
                                      column='facility_type',  
                                      similarity='rapidfuzz',
                                      clustering='hierarchical',
                                      canonical='most_frequent',
                                      threshold_h=0.75,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report)

# water_source: Borehole, BOREHOLE, bore hole → case + spacing, embeddings for semantic match
df, report = handle_structural_errors(df,
                                      column='water_source',  
                                      similarity='rapidfuzz',
                                      clustering='hierarchical',
                                      canonical='most_frequent',
                                      threshold_h=0.70,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report)

# funding_organization: WHO, W.H.O., World Health Organization → abbreviations
df, report = handle_structural_errors(df,
                                      column='funding_organization',  
                                      similarity='embeddings',
                                      clustering='hierarchical',
                                      canonical='most_frequent',
                                      threshold_h=0.65,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report)

# is_functional: Yes, Y, 1, true → need auto-clustering to find Yes-group and No-group
df, report = handle_structural_errors(df,
                                      column='is_functional',  
                                      similarity='embeddings',
                                      clustering='affinity_propagation',
                                      canonical='most_frequent',
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report)

# maintenance_frequency: Monthly, monthly, MONTHLY, Quartely → case + typos
df, report = handle_structural_errors(df,
                                      column='maintenance_frequency',  
                                      similarity='rapidfuzz',
                                      clustering='hierarchical',
                                      canonical='most_frequent',
                                      threshold_h=0.75,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report)

# =============================================================================
# MISSING VALUES
# =============================================================================

df['water_quality_score'] = pd.to_numeric(df['water_quality_score'], errors='coerce')
df['population_served'] = pd.to_numeric(df['population_served'], errors='coerce')
df['users_count'] = pd.to_numeric(df['users_count'], errors='coerce')

df, report_miss = handle_missing_values(df,
                                        method_num='missforest',
                                        method_categ='false',
                                        columns=['water_quality_score', 'population_served', 'users_count'],
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

df.to_csv(OUTPUT_FILE, index=False)

# =============================================================================
# GENERATE REPORT
# =============================================================================

reports = {
    'preprocessing': report_pre,
    'duplicates': report_dup,
    'missing_values': report_miss,
    'datetime': report_date,          
    'outliers': report_out,
    'structural_errors': structural_reports,
    'postprocessing': report_post
}

generate_cleaning_report(reports, REPORT_FILE, dataset_name=DATASET_NAME)
