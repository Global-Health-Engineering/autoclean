"""
Script to evaluate & test Structural_Errors.py with real-world dataset Drilling.csv

Drilling.csv: Real-world wash data about borehole drilling and construction in Malawi 
(source: https://github.com/openwashdata/drillingdata)

Columns evaluated:
- funding_source
- drilling_contractor

Both columns contain typos, abbreviations and semantic variations that need standardization.
"""
# Imported library
import pandas as pd

# Import cleaning functions
from Functions.Pre_Processing import preprocess_data
from Functions.Structural_Errors import handle_structural_errors
from Functions.Post_Processing import postprocess_data
from Functions.Cleaning_Report import generate_cleaning_report

# =============================================================================
# SETTINGS
# =============================================================================

INPUT_FILEPATH = 'Data/Drilling/Drilling.csv'

# Optional:
DATASET_NAME = 'Malawi borehole drilling and construction data' # For header in Cleaning Report
OUTPUT_FILEPATH = 'Data/Drilling/Drilling_Cleaned.csv'
REPORT_FILEPATH = 'Data/Drilling/Drilling_Report.md'

# =============================================================================
# PRE-PROCESSING
# =============================================================================

df, df_original, report_pre = preprocess_data(INPUT_FILEPATH)

# Keep only the columns we want to evaluate
df = df[['funding_source', 'drilling_contractor']]
df_original = df_original[['funding_source', 'drilling_contractor']]

# =============================================================================
# STRUCTURAL ERRORS
# =============================================================================

# Define list to store all reports of handle_semantic_outliers()
report_str = []

df, report_str1 = handle_structural_errors(df,
                                           column = 'funding_source',
                                           similarity = 'rapidfuzz',
                                           clustering = 'connected_components',
                                           threshold_cc = 0.85,
                                           canonical = 'llm')
report_str.append(report_str1)
df, report_str2 = handle_structural_errors(df,
                                           column = 'funding_source',
                                           similarity = 'llm',
                                           llm_mode = 'fast',
                                           llm_context = 'Funding organizations and government bodies for water projects',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.75,
                                           canonical = 'most_frequent')
report_str.append(report_str2)
# -----------------------------------------------------------------------------
df, report_str3 = handle_structural_errors(df,
                                           column = 'drilling_contractor',
                                           similarity = 'rapidfuzz',
                                           clustering = 'connected_components',
                                           threshold_cc = 0.85,
                                           canonical = 'most_frequent')
report_str.append(report_str3)
df, report_str4 = handle_structural_errors(df,
                                           column = 'drilling_contractor',
                                           similarity = 'embeddings',
                                           embedding_model = 'text-embedding-3-large',
                                           clustering = 'connected_components',
                                           threshold_cc = 0.65,
                                           canonical = 'most_frequent')
report_str.append(report_str4)
df, report_str5 = handle_structural_errors(df,
                                           column = 'drilling_contractor',
                                           similarity = 'llm',
                                           llm_mode = 'fast',
                                           llm_context = 'Drilling contractor companies in East Africa',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.7,
                                           canonical = 'most_frequent')
report_str.append(report_str5)

# =============================================================================
# POST-PROCESSING
# =============================================================================

# Change names for better comparison of results
df = df.rename(columns={"funding_source": "funding_source_cleaned", 
                        "drilling_contractor": "drilling_contractor_cleaned",})

# Connect df & df_original for comparison of results & sort
df = pd.concat([df, df_original], axis = 1)
df = df[['funding_source','funding_source_cleaned','drilling_contractor','drilling_contractor_cleaned']]

report_post = postprocess_data(df, df_original, OUTPUT_FILEPATH)

# =============================================================================
# GENERATE REPORT
# =============================================================================

reports = {'preprocessing': report_pre,
           'structural_errors': report_str,
           'postprocessing': report_post}

generate_cleaning_report(reports, REPORT_FILEPATH, DATASET_NAME)

# =============================================================================
# EVALUATION
# =============================================================================
#
# RESULTS SUMMARY:
# - funding_source: 35 unique -> 11 unique 
# - drilling_contractor: 55 unique -> 13 unique 
#
# Based on my (Florin Seiler) domain knowledge, no mis-clusterings were identified.
#
# NOTE: most_frequent canonical selection was used more often because 
# company/organization names are not well-known to the LLM, and the most 
# frequent value in real data is likely correct.
#
# NOTE: Some clusters lost detailed information during standardization. 
# For example, "Scottish Government through the Climate Justice Fund" was 
# clustered with "Scottish Government". Assuming the core funding organization is
# the same, then this information loss is acceptable for standardization purposes.