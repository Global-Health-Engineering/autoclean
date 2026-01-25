"""
Script to apply cleaning pipeline to dataset Drilling.csv

Drilling.csv: Real-world wash data about borehole drilling and construction in Malawi (source: https://github.com/openwashdata/drillingdata)
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

INPUT_FILEPATH = 'Data/Drilling/Drilling.csv'

# Optional:
DATASET_NAME = 'Malawi borehole drilling and construction data' # For header in Cleaning Report
OUTPUT_FILEPATH = 'Data/Drilling/Drilling_Cleaned.csv'
REPORT_FILEPATH = 'Data/Drilling/Drilling_Report.md'

# =============================================================================
# PRE-PROCESSING
# =============================================================================

df, df_original, report_pre = preprocess_data(INPUT_FILEPATH)

# =============================================================================
# DUPLICATES
# =============================================================================

df, report_dup = handle_duplicates(df)

# =============================================================================
# MISSING VALUES
# =============================================================================

# Remove rows with missing latitude / longitude 
df, report_miss = handle_missing_values(df,
                                        column = 'latitude',
                                        method = 'delete',)

# =============================================================================
# DATETIME STANDARDIZATION 
# =============================================================================

df, report_date = standardize_datetime(df,
                                       column = 'date_of_drilling',  
                                       american = True,
                                       handle_invalid = 'nat')

# =============================================================================
# STRUCTURAL ERRORS 
# =============================================================================

report_str = []

# -----------------------------------------------------------------------------
# DRILLING_CONTRACTOR (64 unique → ~13 companies)
# Issues: Typos (Copmany→Company), trailing spaces, newlines, case variations
# -----------------------------------------------------------------------------

# Pass 1: RapidFuzz for typos and minor variations
df, report_str1 = handle_structural_errors(df,
                                           column='drilling_contractor',
                                           similarity='rapidfuzz',
                                           clustering='hierarchical',
                                           threshold_h=0.85,
                                           canonical='llm')
report_str.append(report_str1)

# Pass 2: Embeddings for semantic similarity (OG Madzi ≈ OG Madzi Drilling Company)
df, report_str2 = handle_structural_errors(df,
                                           column='drilling_contractor',
                                           similarity='embeddings',
                                           embedding_model='text-embedding-3-large',
                                           clustering='hierarchical',
                                           threshold_h=0.6,
                                           canonical='llm')
report_str.append(report_str2)

# Pass 3: LLM to merge remaining company variations
df, report_str3 = handle_structural_errors(df,
                                           column='drilling_contractor',
                                           similarity='llm',
                                           llm_mode='fast',
                                           llm_context='Drilling contractor company names in Malawi',
                                           clustering='hierarchical',
                                           threshold_h=0.8,
                                           canonical='llm')
report_str.append(report_str3)

# -----------------------------------------------------------------------------
# FUNDING_SOURCE (42 unique → ~10 organizations)
# Issues: Trailing spaces, newlines, typos (foundaton→foundation), joint funders
# Note: "Habitat for Humanity and German Government" has 11 variations of word order
# -----------------------------------------------------------------------------

# Pass 1: RapidFuzz for typos (foundaton→foundation, trailing spaces)
df, report_str4 = handle_structural_errors(df,
                                           column='funding_source',
                                           similarity='rapidfuzz',
                                           clustering='hierarchical',
                                           threshold_h=0.85,
                                           canonical='llm')
report_str.append(report_str4)

# Pass 2: Embeddings for semantic grouping
df, report_str5 = handle_structural_errors(df,
                                           column='funding_source',
                                           similarity='embeddings',
                                           embedding_model='text-embedding-3-large',
                                           clustering='hierarchical',
                                           threshold_h=0.65,
                                           canonical='llm')
report_str.append(report_str5)

# Pass 3: LLM to merge remaining variations (Habitat + German Gov word orders)
df, report_str6 = handle_structural_errors(df,
                                           column='funding_source',
                                           similarity='llm',
                                           llm_mode='reliable',
                                           llm_context='Funding organizations and government bodies for water projects',
                                           clustering='hierarchical',
                                           threshold_h=0.85,
                                           canonical='llm')
report_str.append(report_str6)

# -----------------------------------------------------------------------------
# DRILLING_RIG_MODEL (91 unique → ~8 model families)
# Issues: Long specifications, overlapping terms (Ashokeleyland PRD contains both)
# Model families: PRD, KRD, Ashokeleyland, JCR DT-600, SC400, ELGI, PDI, LETO
# Note: This is complex - some entries are brand+model, some are just model
# -----------------------------------------------------------------------------

# Pass 1: RapidFuzz for obvious typos
df, report_str7 = handle_structural_errors(df,
                                           column='drilling_rig_model',
                                           similarity='rapidfuzz',
                                           clustering='hierarchical',
                                           threshold_h=0.8,
                                           canonical='llm')
report_str.append(report_str7)

# Pass 2: LLM to group by model family (handles long specs → model name)
df, report_str8 = handle_structural_errors(df,
                                           column='drilling_rig_model',
                                           similarity='llm',
                                           llm_mode='reliable',
                                           llm_context='Drilling rig models. Group by primary model type (PRD, KRD, JCR, Ashokeleyland, SC400, ELGI). Long specifications should match their model family.',
                                           clustering='hierarchical',
                                           threshold_h=0.7,
                                           canonical='llm')
report_str.append(report_str8)

# =============================================================================
# MISSING VALUES
# =============================================================================

# Remove rows with missing latitude / longitude 
df, report_miss = handle_missing_values(df,
                                         column = 'latitude',
                                         method = 'delete',)

# =============================================================================
# POST-PROCESSING
# =============================================================================

report_post = postprocess_data(df, df_original, OUTPUT_FILEPATH, clean_names=True, rounding=True)

# =============================================================================
# GENERATE REPORT
# =============================================================================

reports = {'preprocessing': report_pre,
           'duplicates': report_dup,
           'datetime': report_date,
           'structural_errors': report_str,
           'postprocessing': report_post}

generate_cleaning_report(reports, REPORT_FILEPATH, DATASET_NAME)
