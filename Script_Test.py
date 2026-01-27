"""
Script to apply full cleaning pipeline to dataset Test.csv

Test.csv: Made up WASH dataset, which simulates the monitoring of rural water points in African villages. Columns well_depth_m, pump_age_years, Water quality score, Annual maintenance cost & System condition were generated with Generate_Correlated_Columns.py (see in folder Test). They are correlated and used to test the handle_missing_values() function appropriately. The rest was generated with the help of AI.

Context of each column: 
    - Village: Names of rural villages in Africa, in which water is supplied by development organisations (has semantic outliers)
    - Population served: Number of people in the village using the water point (has semantic outliers)
    - Flow Rate lps: Rate by which water is supplied at the water point (has statistical outliers)
    - install_date: Date when the water point was installed in the village (has mixed date formats & invalid dates)
    - funding organization: International organizations funding water projects (has variations, abbreviations & typos)
    - water_source: Type of water source at the water point (has typos, casing & spacing issues)
    - is_functional: Whether water point is working or not (has boolean variations)
    - tank material: Material of water tank (has categorical variations)
    - sample Volume: Sample volume of water used for testing the water quality (has different units)
    - country: African country where water point is located (has variations, abbreviations & demonyms)
    - staff_count: Number of people maintaining the water point (has digits & words)
    - well_depth_m: Depth (in meters) of the water borehole (feature for imputation)
    - pump_age_years: Age of pump system (in years) (feature for imputation)
    - Water quality score: Quality of the water sample (0 - 100) (has missing values & feature for imputation)
    - Annual maintenance cost: Yearly cost to maintain the water point (has missing values)
    - System condition: Overall condition of the water point (poor, fair, good) (has missing values)
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
DATASET_NAME = 'Test Data (made up WASH dataset)' # For header in Cleaning Report
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

# Define list to store all reports of handle_semantic_outliers()
report_sem = []

df, report_sem1 = handle_semantic_outliers(df,
                                           column = 'Village',
                                           context = 'Location names in Africa',
                                           threshold = 0.5,
                                           action = 'nan')
report_sem.append(report_sem1)
# -----------------------------------------------------------------------------
df, report_sem2 = handle_semantic_outliers(df,
                                           column = 'Population served',
                                           context = 'Number of people',
                                           threshold = 0.5,
                                           action = 'nan')
report_sem.append(report_sem2)

# =============================================================================
# OUTLIERS
# =============================================================================

df, report_out = handle_outliers(df,
                                 method = 'winsorize',
                                 multiplier = 1.5)

# =============================================================================
# DATETIME STANDARDIZATION 
# =============================================================================

df, report_date = standardize_datetime(df,
                                       column = 'install_date',  
                                       american = False,
                                       handle_invalid = 'nat')

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
# -----------------------------------------------------------------------------
df, report_str3 = handle_structural_errors(df,
                                           column = 'water_source',
                                           similarity = 'rapidfuzz',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.85,
                                           canonical = 'llm')
report_str.append(report_str3) 
# -----------------------------------------------------------------------------
df, report_str4 = handle_structural_errors(df,
                                           column = 'is_functional',
                                           similarity = 'rapidfuzz',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.85,
                                           canonical = 'llm')
report_str.append(report_str4)
df, report_str5 = handle_structural_errors(df,
                                           column = 'is_functional',
                                           similarity = 'llm',
                                           llm_mode = 'reliable',
                                           llm_context = 'Wether water point is working or not',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.85,
                                           canonical = 'llm')
report_str.append(report_str5)
# -----------------------------------------------------------------------------
df, report_str6 = handle_structural_errors(df,
                                           column = 'tank material',
                                           similarity = 'rapidfuzz',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.7,
                                           canonical = 'llm')
report_str.append(report_str6)
df, report_str7 = handle_structural_errors(df,
                                           column = 'tank material',
                                           similarity = 'llm',
                                           llm_mode = 'fast',
                                           llm_context = 'Material of tank',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.5,
                                           canonical = 'llm')
report_str.append(report_str7)
# -----------------------------------------------------------------------------
df, report_str8 = handle_structural_errors(df,
                                           column = 'sample Volume',
                                           similarity = 'rapidfuzz',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.9,
                                           canonical = 'llm')
report_str.append(report_str8)
df, report_str9 = handle_structural_errors(df,
                                           column = 'sample Volume',
                                           similarity = 'llm',
                                           llm_mode = 'strict',
                                           llm_context = 'Volume measurements',
                                           clustering = 'connected_components',
                                           threshold_cc = 1.0,
                                           canonical = 'llm')
report_str.append(report_str9)
# -----------------------------------------------------------------------------
df, report_str10 = handle_structural_errors(df,
                                            column = 'country',
                                            similarity = 'embeddings',
                                            embedding_model = 'text-embedding-3-large',
                                            clustering = 'hierarchical',
                                            threshold_h = 0.6,
                                            canonical = 'llm')
report_str.append(report_str10)
df, report_str11 = handle_structural_errors(df,
                                            column = 'country',
                                            similarity = 'llm',
                                            llm_mode = 'fast',
                                            llm_context = 'African countries',
                                            clustering = 'hierarchical',
                                            threshold_h = 0.8,
                                            canonical = 'llm')
report_str.append(report_str11)
# -----------------------------------------------------------------------------
df, report_str12 = handle_structural_errors(df,
                                            column = 'staff_count',
                                            similarity = 'llm',
                                            llm_mode = 'fast',
                                            llm_context = 'Number of staff',
                                            clustering = 'hierarchical',
                                            threshold_h = 0.8,
                                            canonical = 'llm')
report_str.append(report_str12)

# =============================================================================
# MISSING VALUES
# =============================================================================

# Define list to store all reports of handle_missing_values()
report_miss = []

df, report_miss1 = handle_missing_values(df,
                                         column = 'Water quality score',
                                         method = 'missforest',
                                         features = ['well_depth_m', 'pump_age_years'],
                                         max_iter = 5,
                                         n_estimators = 10,
                                         max_depth = 3,
                                         min_samples_leaf = 3)
report_miss.append(report_miss1)
# -----------------------------------------------------------------------------
df, report_miss2 = handle_missing_values(df,
                                         column = 'Annual maintenance cost',
                                         method = 'missforest',
                                         features = ['well_depth_m', 'pump_age_years'],
                                         max_iter = 1,
                                         n_estimators = 10,
                                         max_depth = 3,
                                         min_samples_leaf = 3)
report_miss.append(report_miss2)
# -----------------------------------------------------------------------------
df, report_miss3 = handle_missing_values(df,
                                        column = 'System condition',
                                        method = 'knn',
                                        features=  ['well_depth_m', 'pump_age_years', 'Water quality score'],
                                        n_neighbors = 3)
report_miss.append(report_miss3)

# Ground truth values:
# Water quality score:     Row 3: 47.9, Row 8: 56.56, Row 19: 42.04, Row 32: 60.57, Row 47: 35.59
# Annual maintenance cost: Row 5: 272, Row 16: 421, Row 28: 353, Row 38: 452, Row 50: 431
# System condition:        Row 12: Fair, Row 25: Fair, Row 44: Fair

# =============================================================================
# POST-PROCESSING
# =============================================================================

report_post = postprocess_data(df, df_original, OUTPUT_FILEPATH, clean_names = True, rounding = True)

# =============================================================================
# GENERATE REPORT
# =============================================================================

reports = {'preprocessing': report_pre,
           'duplicates': report_dup,
           'semantic_outliers': report_sem,
           'outliers': report_out,
           'datetime': report_date,
           'structural_errors': report_str,
           'missing_values': report_miss,
           'postprocessing': report_post}

generate_cleaning_report(reports, REPORT_FILEPATH, DATASET_NAME)

# =============================================================================
# Evaluation
# =============================================================================
#
# RESULTS SUMMARY:
# - Preprocessing: Loaded data, removed empty row/column 
# - Duplicates: Found and removed duplicate row 
# - Semantic Outliers: Detected all 8 outliers correctly 
# - Statistical Outliers: Found 3 statistical outliers correctly 
# - DateTime: Standardized 40 dates, identified 10 invalid dates 
# - Structural Errors: Clustered 7 columns, reduced 210 to 79 unique values 
# - Missing Values: Imputed with MAE = 6.59 (in Water quality score), 6.60 (in Annual maintenance cost), 100% accuracy (in System condition) 
# - Postprocessing: Cleaned column names, applied appropriate rounding, saved CSV 
# - Report: Generated full cleaning report 
#
# NOTE: Check the generated report (in folder Test), to get more insights about the results 
#
# GROUND TRUTH VALUES FOR MISSING VALUE IMPUTATION:
# - Water quality score:     Row 3: 47.9, Row 8: 56.56, Row 19: 42.04, Row 32: 60.57, Row 47: 35.59
# - Annual maintenance cost: Row 5: 272, Row 16: 421, Row 28: 353, Row 38: 452, Row 50: 431
# - System condition:        Row 12: Fair, Row 25: Fair, Row 44: Fair
#
# NOTE ON MISSING VALUE IMPUTATION:
# Results depend heavily on correlation strength and noise in the data. MAE increases
# when ground truth values are outliers (deviate from the pattern). For example, row 5
# Annual maintenance cost = 272 had prediction error of ~ 23 (vs ~ 5 for others), which
# significantly impacts MAE. This is expected, as no algorithm can predict random noise.
# The goal was to demonstrate that handle_missing_values() achieves accurate predictions
# when correlations exist between features and target columns.