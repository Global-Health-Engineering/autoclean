"""
Script to evaluate & test Semantic_Outliers.py and Structural_Errors.py with dataset Salary.csv

Salary.csv: Real-world salary survey data from Ask A Manager blog
(source: https://www.askamanager.org/2021/04/how-much-money-do-you-make-4.html)

Column evaluated:
- What country do you work in? 

This column contains semantic outliers (gibberish, sentences, cities instead of countries) 
and structural errors (typos, casing, abbreviations) that need to be detected and standardized.

Sampling: As the survey includes over 28'000 rows, sampling is needed for precise evaluation. 
Therefore Semantic_Outliers.py and Structural_Errors.py was tested only on a sample of 190 rows. 
The sample includes only unique values and tries to cover a good spectrum of variations and outliers.
"""

# Imported library
import pandas as pd

# Import cleaning functions
from Functions.Pre_Processing import preprocess_data
from Functions.Semantic_Outliers import handle_semantic_outliers
from Functions.Structural_Errors import handle_structural_errors
from Functions.Post_Processing import postprocess_data
from Functions.Cleaning_Report import generate_cleaning_report

# =============================================================================
# SETTINGS
# =============================================================================

INPUT_FILEPATH = 'Data/Salary/Salary.csv'

# Optional:
DATASET_NAME = 'Ask A Manager Salary Survey 2021 (Sample)'
OUTPUT_FILEPATH = 'Data/Salary/Salary_Cleaned.csv'
REPORT_FILEPATH = 'Data/Salary/Salary_Report.md'

# =============================================================================
# PRE-PROCESSING
# =============================================================================

df, df_original, report_pre = preprocess_data(INPUT_FILEPATH)

# Keep only the column we want to evaluate
df = df[['What country do you work in?']]
df_original = df_original[['What country do you work in?']]

# =============================================================================
# SAMPLING
# =============================================================================

# Remove duplicates (keep only unique values)
df = df.drop_duplicates()
# Sort the values in descending alphabetic order and take the first 190 as our sample 
df = df.sort_values(by = 'What country do you work in?', ascending = False).head(190)
df_original = df.copy()

# =============================================================================
# SEMANTIC OUTLIERS (1)
# =============================================================================

df, report_sem = handle_semantic_outliers(df,
                                          column = 'What country do you work in?',
                                          context = 'Answers to question: What country do you work in? (abbreviations and possible typos are acceptable)',
                                          threshold = 0.1,
                                          action = 'nan')

# =============================================================================
# STRUCTURAL ERRORS
# =============================================================================

# Define list to store all reports of handle_semantic_outliers()
report_str = []

df, report_str1 = handle_structural_errors(df,
                                           column = 'What country do you work in?',
                                           similarity = 'rapidfuzz',
                                           clustering = 'connected_components',
                                           threshold_cc = 0.81,
                                           canonical = 'most_frequent')
report_str.append(report_str1)
df, report_str2 = handle_structural_errors(df,
                                           column = 'What country do you work in?',
                                           similarity = 'embeddings',
                                           embedding_model = 'text-embedding-3-large',
                                           clustering = 'connected_components',
                                           threshold_cc = 0.66,
                                           canonical = 'most_frequent')
report_str.append(report_str2)


df, report_str3 = handle_structural_errors(df,
                                           column = 'What country do you work in?',
                                           similarity = 'llm',
                                           llm_mode = 'reliable',
                                           llm_context = 'Answers to question: What country do you work in? (abbreviations and typos are possible)',
                                           clustering = 'hierarchical',
                                           threshold_h = 0.7,
                                           canonical = 'most_frequent')
report_str.append(report_str3)

# =============================================================================
# SEMANTIC OUTLIERS (2)
# =============================================================================

df, report_sem = handle_semantic_outliers(df,
                                          column = 'What country do you work in?',
                                          context = 'Answers to question: What country do you work in? (abbreviations and possible typos are acceptable)',
                                          threshold = 1.1,
                                          action = 'nan')

# =============================================================================
# POST-PROCESSING
# =============================================================================

# Change name for better comparison of results
df = df.rename(columns={"What country do you work in?": "What country do you work in? (cleaned)"})

# Connect df & df_original for better comparison of the results 
df = pd.concat([df, df_original], axis = 1)

report_post = postprocess_data(df, df_original, OUTPUT_FILEPATH)

# =============================================================================
# GENERATE REPORT
# =============================================================================

reports = {'preprocessing': report_pre,
           'semantic_outliers': report_sem,
           'structural_errors': report_str,
           'postprocessing': report_post}

generate_cleaning_report(reports, REPORT_FILEPATH, DATASET_NAME)

# =============================================================================
# EVALUATION
# =============================================================================
