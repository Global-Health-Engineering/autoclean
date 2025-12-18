# Imported libraries
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field
from typing import Literal, Optional
from dotenv import load_dotenv
import instructor
from openai import OpenAI
import os

# Import data profiling function
from Data_Profiling import profile_dataframe

"""
LLM Parameter Selection for Data Cleaning

Uses LLM to automatically choose optimal parameters for cleaning functions
based on the data profile.

Pipeline (Nicolo's design):
    1. Input: DataFrame
    2. Data Profiling: Summarize/evaluate the dataframe for LLM context
    3. Pydantic Schemas: Constrain LLM output to valid parameter choices
    4. LLM Selection: LLM chooses parameters based on profile
    5. Apply Cleaning: Run cleaning function with chosen parameters
    6. Evaluation: Profile again, LLM evaluates if good or needs iteration

Public Functions:
    - select_missing_values_params(df, context) → MissingValuesParams
    - select_outlier_params(df, context) → OutlierParams
    - evaluate_cleaning_result(df_before, df_after, cleaning_type, params) → CleaningEvaluation

Usage:
    from LLM_Parameter_Selection import select_missing_values_params
    
    params = select_missing_values_params(df, context="WASH survey data")
    print(params.method)       # "knn"
    print(params.k_neighbors)  # 5
    print(params.reasoning)    # "Because..."
"""


# ============================================================================
# Pydantic Schemas (required for instructor to constrain LLM output)
# ============================================================================

class MissingValuesParams(BaseModel):
    """Parameters for missing value imputation - LLM must return this structure."""
    
    method: Literal["mean", "median", "mode", "knn", "missforest", "drop_rows", "drop_cols"] = Field(
        description="Imputation method to use"
    )
    k_neighbors: Optional[int] = Field(
        default=5, ge=1, le=20,
        description="Number of neighbors for KNN (only if method='knn')"
    )
    n_estimators: Optional[int] = Field(
        default=100, ge=10, le=500,
        description="Number of trees for MissForest (only if method='missforest')"
    )
    drop_threshold: Optional[float] = Field(
        default=0.5, ge=0.0, le=1.0,
        description="Drop columns with more than this % missing (only for drop methods)"
    )
    apply_to_numeric: bool = Field(default=True)
    apply_to_categorical: bool = Field(default=True)
    reasoning: str = Field(description="Why these parameters were chosen")


class OutlierParams(BaseModel):
    """Parameters for outlier detection - LLM must return this structure."""
    
    method: Literal["iqr", "zscore", "isolation_forest", "none"] = Field(
        description="Outlier detection method"
    )
    iqr_multiplier: Optional[float] = Field(
        default=1.5, ge=1.0, le=3.0,
        description="IQR multiplier (only if method='iqr')"
    )
    zscore_threshold: Optional[float] = Field(
        default=3.0, ge=2.0, le=5.0,
        description="Z-score threshold (only if method='zscore')"
    )
    action: Literal["remove", "cap", "flag"] = Field(
        default="remove",
        description="What to do with outliers"
    )
    reasoning: str = Field(description="Why these parameters were chosen")


class CleaningEvaluation(BaseModel):
    """LLM's evaluation of cleaning results."""
    
    is_satisfactory: bool = Field(description="True if cleaning was successful")
    quality_score: int = Field(ge=1, le=10, description="Score from 1-10")
    issues_found: list[str] = Field(default=[], description="Remaining issues")
    suggested_changes: list[str] = Field(default=[], description="What to try next")
    reasoning: str = Field(description="Explanation of evaluation")


# ============================================================================
# Public Functions
# ============================================================================

def select_missing_values_params(df: pd.DataFrame,
                                  context: str = None,
                                  verbose: bool = True) -> MissingValuesParams:
    """
    Use LLM to select optimal parameters for missing value imputation.
    
    Parameters:
        df: DataFrame with missing values
        context: Optional context about the data (e.g., "WASH survey data")
        verbose: Print progress
    
    Returns:
        MissingValuesParams with LLM-chosen parameters
    
    Example:
        params = select_missing_values_params(df, context="Survey data")
        print(params.method)       # "knn"
        print(params.k_neighbors)  # 5
    """
    
    # Load API key
    client = _get_instructor_client()
    
    if verbose:
        print("Selecting missing values parameters with LLM...")
    
    # Profile the data
    profile = profile_dataframe(df)
    llm_context = profile.to_llm_prompt()
    
    # Build prompt
    context_str = f"\nData Context: {context}" if context else ""
    
    prompt = f"""You are a data cleaning expert. Based on the data profile, 
choose optimal parameters for handling missing values.

{llm_context}
{context_str}

Guidelines:
- If missing < 5%: mean/median/mode usually sufficient
- If missing 5-20%: KNN often works well for numeric data
- If missing > 20%: MissForest or consider dropping columns
- For small datasets (<1000 rows): simpler methods are better
- For categorical data: mode is usually best
- If columns have >50% missing: consider drop_cols"""

    # Get LLM response
    params = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data cleaning expert."},
            {"role": "user", "content": prompt}
        ],
        response_model=MissingValuesParams
    )
    
    if verbose:
        print(f"  Method: {params.method}")
        if params.method == "knn":
            print(f"  K neighbors: {params.k_neighbors}")
        print(f"  Reasoning: {params.reasoning}")
    
    return params


def select_outlier_params(df: pd.DataFrame,
                           context: str = None,
                           verbose: bool = True) -> OutlierParams:
    """
    Use LLM to select optimal parameters for outlier detection.
    
    Parameters:
        df: DataFrame to check for outliers
        context: Optional context about the data
        verbose: Print progress
    
    Returns:
        OutlierParams with LLM-chosen parameters
    """
    
    client = _get_instructor_client()
    
    if verbose:
        print("Selecting outlier parameters with LLM...")
    
    # Profile the data
    profile = profile_dataframe(df)
    llm_context = profile.to_llm_prompt()
    
    context_str = f"\nData Context: {context}" if context else ""
    
    prompt = f"""You are a data cleaning expert. Based on the data profile,
choose optimal parameters for outlier detection.

{llm_context}
{context_str}

Guidelines:
- IQR 1.5: standard, catches moderate outliers
- IQR 3.0: only extreme outliers
- Z-score: assumes normal distribution
- If few outliers (<1%): might be valid, use 'flag'
- If many outliers (>5%): use higher threshold"""

    params = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data cleaning expert."},
            {"role": "user", "content": prompt}
        ],
        response_model=OutlierParams
    )
    
    if verbose:
        print(f"  Method: {params.method}")
        print(f"  Action: {params.action}")
        print(f"  Reasoning: {params.reasoning}")
    
    return params


def evaluate_cleaning_result(df_before: pd.DataFrame,
                              df_after: pd.DataFrame,
                              cleaning_type: str,
                              params_used: dict,
                              verbose: bool = True) -> CleaningEvaluation:
    """
    Use LLM to evaluate if cleaning was successful.
    
    Parameters:
        df_before: DataFrame before cleaning
        df_after: DataFrame after cleaning
        cleaning_type: What was cleaned (e.g., "missing_values")
        params_used: Parameters that were used
        verbose: Print progress
    
    Returns:
        CleaningEvaluation with LLM assessment
    """
    
    client = _get_instructor_client()
    
    if verbose:
        print("Evaluating cleaning result with LLM...")
    
    # Profile before and after
    profile_before = profile_dataframe(df_before)
    profile_after = profile_dataframe(df_after)
    
    prompt = f"""Evaluate if the data cleaning was successful.

CLEANING TYPE: {cleaning_type}
PARAMETERS USED: {params_used}

BEFORE:
{profile_before.to_llm_prompt()}

AFTER:
{profile_after.to_llm_prompt()}

Score from 1-10:
- 1-3: Poor, issues remain or cleaning caused problems
- 4-6: Acceptable, could improve
- 7-9: Good, effective
- 10: Excellent"""

    evaluation = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data cleaning expert."},
            {"role": "user", "content": prompt}
        ],
        response_model=CleaningEvaluation
    )
    
    if verbose:
        print(f"  Satisfactory: {evaluation.is_satisfactory}")
        print(f"  Score: {evaluation.quality_score}/10")
        print(f"  Reasoning: {evaluation.reasoning}")
    
    return evaluation


# ============================================================================
# Helper Functions (Private)
# ============================================================================

def _get_instructor_client():
    """Load API key and return instructor client."""
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")
    
    return instructor.from_openai(OpenAI(api_key=api_key))
