# Imported libraries
import pandas as pd

# Import cleaning functions
from Functions.Pre_Processing import preprocess_data
from Functions.Duplicates import handle_duplicates
from Functions.Missing_Values import handle_missing_values
from Functions.DateTime_Standardization import standardize_datetime
from Functions.Outliers import handle_outliers
from Functions.Structural_Errors_Simple import handle_structural_errors_simple
from Functions.Structural_Errors_LLM import handle_structural_errors_llm
from Functions.Post_Processing import postprocess_data
from Functions.Cleaning_Report import generate_cleaning_report


# ============================================================================
# Pipeline Function
# ============================================================================

def run_pipeline(
    # Required
    input_path: str,
    
    # Output settings
    output_path: str = None,
    report_path: str = 'cleaning_report.md',
    
    # Preprocessing (always runs)
    clean_names: bool = True,
    
    # Duplicates (always runs)
    
    # Missing Values
    run_missing_values: bool = False,
    missing_method_num: str = 'mean',
    missing_method_categ: str = 'mode',
    missing_columns: list = None,
    missing_n_neighbors: int = 5,
    missing_max_iter: int = 10,
    missing_n_estimators: int = 10,
    
    # DateTime
    run_datetime: bool = False,
    datetime_column: str = None,
    datetime_american: bool = False,
    datetime_handle_invalid: str = 'nat',
    
    # Outliers
    run_outliers: bool = False,
    outliers_method: str = 'winsorize',
    outliers_multiplier: float = 1.5,
    
    # Structural Errors Simple
    run_structural_simple: bool = False,
    structural_simple_column: str = None,
    structural_simple_threshold: float = 20.0,
    structural_simple_method: str = 'average',
    
    # Structural Errors LLM
    run_structural_llm: bool = False,
    structural_llm_column: str = None,
    structural_llm_preference: float = None,
    structural_llm_damping: float = 0.9,
    structural_llm_context: str = None,
    
    # Postprocessing
    run_postprocessing: bool = True,
):
    """
    Run the AutoClean pipeline with specified settings.
    
    Parameters:
        input_path: Path to input CSV/Excel file
        output_path: Path to save cleaned data (None = don't save)
        report_path: Path to save cleaning report
        
        ... (see parameter names for settings)
    
    Returns:
        (df_original, df_cleaned, reports): Original data, cleaned data, all reports
    """
    
    # Initialize reports dict
    reports = {}
    
    # ========== HEADER ==========
    print()
    print("=" * 40)
    print("AUTOCLEAN")
    print("=" * 40)
    print()
    
    # ========== PREPROCESSING (always runs) ==========
    df_original, df, reports['preprocessing'] = preprocess_data(
        input_path, 
        clean_names=clean_names
    )
    
    # ========== DUPLICATES (always runs) ==========
    df, reports['duplicates'] = handle_duplicates(df)
    
    # ========== MISSING VALUES ==========
    if run_missing_values:
        df, reports['missing_values'] = handle_missing_values(
            df,
            method_num=missing_method_num,
            method_categ=missing_method_categ,
            columns=missing_columns,
            n_neighbors=missing_n_neighbors,
            max_iter=missing_max_iter,
            n_estimators=missing_n_estimators
        )
    
    # ========== DATETIME ==========
    if run_datetime:
        if datetime_column is None:
            print("WARNING: run_datetime=True but datetime_column not specified")
        else:
            df, reports['datetime'] = standardize_datetime(
                df,
                column=datetime_column,
                american=datetime_american,
                handle_invalid=datetime_handle_invalid
            )
    
    # ========== OUTLIERS ==========
    if run_outliers:
        df, reports['outliers'] = handle_outliers(
            df,
            method=outliers_method,
            multiplier=outliers_multiplier
        )
    
    # ========== STRUCTURAL ERRORS SIMPLE ==========
    if run_structural_simple:
        if structural_simple_column is None:
            print("WARNING: run_structural_simple=True but column not specified")
        else:
            df, reports['structural_simple'] = handle_structural_errors_simple(
                df,
                column=structural_simple_column,
                threshold=structural_simple_threshold,
                method=structural_simple_method
            )
    
    # ========== STRUCTURAL ERRORS LLM ==========
    if run_structural_llm:
        if structural_llm_column is None:
            print("WARNING: run_structural_llm=True but column not specified")
        else:
            df, reports['structural_llm'] = handle_structural_errors_llm(
                df,
                column=structural_llm_column,
                preference=structural_llm_preference,
                damping=structural_llm_damping,
                context=structural_llm_context
            )
    
    # ========== POSTPROCESSING ==========
    if run_postprocessing:
        df, reports['postprocessing'] = postprocess_data(df, df_original)
    
    # ========== SAVE OUTPUT ==========
    if output_path:
        df.to_csv(output_path, index=False)
        print(f"Cleaned data saved: {output_path}")
    
    # ========== GENERATE REPORT ==========
    print()
    print("=" * 40)
    generate_cleaning_report(
        reports, 
        report_path, 
        dataset_name=input_path
    )
    print("=" * 40)
    print()
    
    return df_original, df, reports


# ============================================================================
# Test Functions
# ============================================================================

def test_basic():
    """Basic test - just preprocessing and duplicates"""
    run_pipeline(
        input_path='data/test.csv',
        output_path='output/test_cleaned.csv',
        report_path='output/test_report.md',
    )


def test_missing_values():
    """Test missing value imputation"""
    run_pipeline(
        input_path='data/test.csv',
        run_missing_values=True,
        missing_method_num='mean',
        missing_method_categ='mode',
    )


def test_full_pipeline():
    """Test full pipeline with all steps"""
    run_pipeline(
        input_path='data/test.csv',
        output_path='output/test_cleaned.csv',
        report_path='output/test_report.md',
        
        run_missing_values=True,
        missing_method_num='knn',
        
        run_datetime=True,
        datetime_column='date',
        datetime_american=False,
        
        run_outliers=True,
        outliers_method='winsorize',
        
        run_structural_simple=True,
        structural_simple_column='category',
        structural_simple_threshold=25.0,
    )


def test_wash_data():
    """Test with WASH dataset"""
    run_pipeline(
        input_path='data/wash_data.csv',
        output_path='output/wash_cleaned.csv',
        report_path='output/wash_report.md',
        
        run_missing_values=True,
        missing_method_num='missforest',
        missing_method_categ='mode',
        
        run_datetime=True,
        datetime_column='date_of_drilling',
        datetime_american=False,
        datetime_handle_invalid='nat',
        
        run_outliers=True,
        
        run_structural_simple=True,
        structural_simple_column='funding_source',
        structural_simple_threshold=20.0,
    )


def test_imdb_data():
    """Test with IMDB messy dataset"""
    run_pipeline(
        input_path='data/imdb_messy.csv',
        output_path='output/imdb_cleaned.csv',
        report_path='output/imdb_report.md',
        
        run_missing_values=True,
        missing_method_num='mean',
        
        run_structural_simple=True,
        structural_simple_column='genre',
        structural_simple_threshold=30.0,
    )


def test_structural_llm():
    """Test LLM-based structural error correction"""
    run_pipeline(
        input_path='data/test.csv',
        
        run_structural_llm=True,
        structural_llm_column='city',
        structural_llm_context='US cities',
    )


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == '__main__':
    
    # =============================================
    # CHANGE THIS TO RUN DIFFERENT TESTS
    # =============================================
    
    test_basic()
    
    # Other tests:
    # test_missing_values()
    # test_full_pipeline()
    # test_wash_data()
    # test_imdb_data()
    # test_structural_llm()