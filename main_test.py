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

df_original, df, report_pre = preprocess_data(INPUT_FILE)

# =============================================================================
# DUPLICATES
# =============================================================================

df, report_dup = handle_duplicates(df)

# =============================================================================
# DATETIME STANDARDIZATION 
# =============================================================================

df, report_date = standardize_datetime(df,
                                       column='date_Installed',  
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
df, report1 = handle_structural_errors(df,
                                      column='city',  
                                      similarity='embeddings',
                                      clustering='affinity_propagation',
                                      canonical='most_frequent',
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report1)

# facility_type: Hospital, HOSPITAL, Hosptial → case + typos, embeddings for semantic match
df, report2 = handle_structural_errors(df,
                                      column='Facility Type',  
                                      similarity='rapidfuzz',
                                      clustering='hierarchical',
                                      canonical='most_frequent',
                                      threshold_h=0.75,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report2)

# water_source: Borehole, BOREHOLE, bore hole → case + spacing, embeddings for semantic match
df, report3 = handle_structural_errors(df,
                                      column='Water source',  
                                      similarity='rapidfuzz',
                                      clustering='hierarchical',
                                      canonical='most_frequent',
                                      threshold_h=0.70,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report3)

# funding_organization: WHO, W.H.O., World Health Organization → abbreviations
df, report4 = handle_structural_errors(df,
                                      column='Funding_Organization',  
                                      similarity='embeddings',
                                      clustering='hierarchical',
                                      canonical='most_frequent',
                                      threshold_h=0.65,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report4)

# is_functional: Yes, Y, 1, true → need auto-clustering to find Yes-group and No-group
df, report5 = handle_structural_errors(df,
                                      column='Is Functional',  
                                      similarity='embeddings',
                                      clustering='affinity_propagation',
                                      canonical='most_frequent',
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report5)

df, report6 = handle_structural_errors(df,
                                      column='Number of Staff',  
                                      similarity='embeddings',
                                      clustering='hierarchical',
                                      canonical='most_frequent',
                                      threshold_h = 0.8,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report6)

# maintenance_frequency: Monthly, monthly, MONTHLY, Quartely → case + typos
df, report7 = handle_structural_errors(df,
                                      column='Maintenance_Frequency',  
                                      similarity='rapidfuzz',
                                      clustering='hierarchical',
                                      canonical='most_frequent',
                                      threshold_h=0.75,
                                      embedding_model='text-embedding-3-large')
structural_reports.append(report7)

# =============================================================================
# MISSING VALUES
# =============================================================================

#df['Water Quality_Score'] = pd.to_numeric(df['Water Quality_Score'], errors='coerce')
#df['Population_served'] = pd.to_numeric(df['Population_served'], errors='coerce')
#df['users_Count'] = pd.to_numeric(df['users_Count'], errors='coerce')

df, report_miss = handle_missing_values(df,
                                        method_num='missforest',
                                        method_categ='false',
                                        columns=['Water Quality_Score', 'Population_served', 'users_Count'],
                                        n_neighbors=5,
                                        max_iter=10,
                                        n_estimators=10)

# =============================================================================
# POST-PROCESSING
# =============================================================================

df, report_post = postprocess_data(df, df_original, clean_names=True)

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
