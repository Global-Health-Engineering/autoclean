# Imported libraries
import pandas as pd
import numpy as np
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

"""
Data Profiling Function

Creates a comprehensive profile of a DataFrame for:
1. USER: Readable data quality report
2. LLM: Context for parameter selection in cleaning pipeline

Usage:
    profile = profile_dataframe(df)
    
    # For user
    profile.print_report()          # Print to console
    report_md = profile.to_markdown()   # Get markdown string
    
    # For LLM
    llm_context = profile.to_llm_prompt()  # Concise string for LLM

Based on: Bachelor Thesis Description (data profiling with pandas)
"""

# ============================================================================
# Pydantic Models for Structured Profile Output
# ============================================================================

class NumericStats(BaseModel):
    """Statistics for numeric columns."""
    min: float
    max: float
    mean: float
    median: float
    std: float
    q1: float  # 25th percentile
    q3: float  # 75th percentile
    skewness: float
    n_zeros: int
    n_negative: int
    n_outliers_iqr: int  # Outliers based on IQR method


class CategoricalStats(BaseModel):
    """Statistics for categorical columns."""
    n_unique: int
    unique_percent: float  # unique / total * 100
    top_values: list[dict]  # [{"value": "X", "count": 10, "percent": 5.0}, ...]
    is_constant: bool  # Only 1 unique value
    is_high_cardinality: bool  # >90% unique values


class DateTimeStats(BaseModel):
    """Statistics for datetime columns."""
    min_date: str
    max_date: str
    range_days: int
    n_unique: int


class ColumnProfile(BaseModel):
    """Complete profile for a single column."""
    name: str
    dtype: str
    dtype_category: str  # "numeric", "categorical", "datetime", "boolean", "other"
    
    # Missing values
    n_missing: int
    missing_percent: float
    
    # Unique values
    n_unique: int
    unique_percent: float
    
    # Sample values (first 5 non-null)
    sample_values: list[Any]
    
    # Type-specific stats (only one will be populated)
    numeric_stats: Optional[NumericStats] = None
    categorical_stats: Optional[CategoricalStats] = None
    datetime_stats: Optional[DateTimeStats] = None


class DataQualitySummary(BaseModel):
    """Summary of data quality issues."""
    total_missing_cells: int
    total_missing_percent: float
    n_duplicate_rows: int
    duplicate_rows_percent: float
    
    # Problem columns
    columns_with_missing: list[str]
    columns_high_missing: list[str]  # >50% missing
    columns_constant: list[str]  # Only 1 unique value
    columns_high_cardinality: list[str]  # >90% unique (potential IDs)
    columns_with_outliers: list[str]  # Has IQR outliers
    
    # Warnings
    warnings: list[str]


class DataProfile(BaseModel):
    """Complete DataFrame profile."""
    
    # Metadata
    profile_created_at: str
    
    # Overview
    n_rows: int
    n_columns: int
    memory_usage_mb: float
    
    # Column type counts
    n_numeric_columns: int
    n_categorical_columns: int
    n_datetime_columns: int
    n_boolean_columns: int
    n_other_columns: int
    
    # Detailed column profiles
    columns: list[ColumnProfile]
    
    # Data quality summary
    quality_summary: DataQualitySummary
    
    # Sample rows
    sample_rows: list[dict]  # First 5 rows as dictionaries
    
    # ========================================================================
    # Output Methods
    # ========================================================================
    
    def print_report(self) -> None:
        """Print formatted report to console."""
        print(self.to_markdown())
    
    def to_markdown(self) -> str:
        """Convert profile to markdown string for user."""
        
        lines = []
        lines.append("# Data Profile Report")
        lines.append(f"\n*Generated: {self.profile_created_at}*\n")
        
        # Overview
        lines.append("## Overview")
        lines.append(f"- **Rows:** {self.n_rows:,}")
        lines.append(f"- **Columns:** {self.n_columns}")
        lines.append(f"- **Memory Usage:** {self.memory_usage_mb:.2f} MB")
        lines.append("")
        lines.append("**Column Types:**")
        lines.append(f"- Numeric: {self.n_numeric_columns}")
        lines.append(f"- Categorical: {self.n_categorical_columns}")
        lines.append(f"- DateTime: {self.n_datetime_columns}")
        lines.append(f"- Boolean: {self.n_boolean_columns}")
        lines.append(f"- Other: {self.n_other_columns}")
        lines.append("")
        
        # Data Quality Summary
        lines.append("## Data Quality Summary")
        qs = self.quality_summary
        lines.append(f"- **Total Missing Cells:** {qs.total_missing_cells:,} ({qs.total_missing_percent:.1f}%)")
        lines.append(f"- **Duplicate Rows:** {qs.n_duplicate_rows:,} ({qs.duplicate_rows_percent:.1f}%)")
        lines.append("")
        
        if qs.columns_high_missing:
            lines.append(f"- **Columns with >50% missing:** {', '.join(qs.columns_high_missing)}")
        if qs.columns_constant:
            lines.append(f"- **Constant columns (1 unique value):** {', '.join(qs.columns_constant)}")
        if qs.columns_high_cardinality:
            lines.append(f"- **High cardinality columns (>90% unique):** {', '.join(qs.columns_high_cardinality)}")
        if qs.columns_with_outliers:
            lines.append(f"- **Columns with outliers:** {', '.join(qs.columns_with_outliers)}")
        lines.append("")
        
        # Warnings
        if qs.warnings:
            lines.append("### ⚠️ Warnings")
            for warning in qs.warnings:
                lines.append(f"- {warning}")
            lines.append("")
        
        # Column Details
        lines.append("## Column Details")
        lines.append("")
        
        for col in self.columns:
            lines.append(f"### {col.name}")
            lines.append(f"- **Type:** {col.dtype} ({col.dtype_category})")
            lines.append(f"- **Missing:** {col.n_missing:,} ({col.missing_percent:.1f}%)")
            lines.append(f"- **Unique:** {col.n_unique:,} ({col.unique_percent:.1f}%)")
            lines.append(f"- **Sample:** {col.sample_values[:5]}")
            
            if col.numeric_stats:
                ns = col.numeric_stats
                lines.append(f"- **Range:** {ns.min:.2f} to {ns.max:.2f}")
                lines.append(f"- **Mean:** {ns.mean:.2f}, **Median:** {ns.median:.2f}, **Std:** {ns.std:.2f}")
                lines.append(f"- **Quartiles:** Q1={ns.q1:.2f}, Q3={ns.q3:.2f}")
                lines.append(f"- **Skewness:** {ns.skewness:.2f}")
                lines.append(f"- **Outliers (IQR):** {ns.n_outliers_iqr}")
                if ns.n_zeros > 0:
                    lines.append(f"- **Zeros:** {ns.n_zeros}")
                if ns.n_negative > 0:
                    lines.append(f"- **Negative values:** {ns.n_negative}")
            
            if col.categorical_stats:
                cs = col.categorical_stats
                lines.append(f"- **Top values:**")
                for tv in cs.top_values[:5]:
                    lines.append(f"  - {tv['value']}: {tv['count']} ({tv['percent']:.1f}%)")
            
            if col.datetime_stats:
                ds = col.datetime_stats
                lines.append(f"- **Date range:** {ds.min_date} to {ds.max_date} ({ds.range_days} days)")
            
            lines.append("")
        
        # Sample Rows
        lines.append("## Sample Rows (First 5)")
        lines.append("")
        if self.sample_rows:
            # Create markdown table
            headers = list(self.sample_rows[0].keys())
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for row in self.sample_rows[:5]:
                values = [str(row.get(h, ""))[:30] for h in headers]  # Truncate long values
                lines.append("| " + " | ".join(values) + " |")
        lines.append("")
        
        return "\n".join(lines)
    
    def to_llm_prompt(self) -> str:
        """Convert profile to concise string for LLM context."""
        
        lines = []
        lines.append("=== DATA PROFILE ===")
        lines.append(f"Rows: {self.n_rows:,}, Columns: {self.n_columns}")
        lines.append(f"Types: {self.n_numeric_columns} numeric, {self.n_categorical_columns} categorical, {self.n_datetime_columns} datetime")
        lines.append("")
        
        # Quality issues (most important for LLM)
        qs = self.quality_summary
        lines.append("QUALITY ISSUES:")
        lines.append(f"- Missing cells: {qs.total_missing_cells:,} ({qs.total_missing_percent:.1f}%)")
        lines.append(f"- Duplicate rows: {qs.n_duplicate_rows:,}")
        
        if qs.columns_high_missing:
            lines.append(f"- High missing (>50%): {', '.join(qs.columns_high_missing)}")
        if qs.columns_with_outliers:
            lines.append(f"- Columns with outliers: {', '.join(qs.columns_with_outliers)}")
        if qs.warnings:
            lines.append(f"- Warnings: {'; '.join(qs.warnings)}")
        lines.append("")
        
        # Column summary
        lines.append("COLUMNS:")
        for col in self.columns:
            col_info = f"- {col.name} ({col.dtype_category}): {col.missing_percent:.1f}% missing, {col.n_unique} unique"
            
            if col.numeric_stats:
                ns = col.numeric_stats
                col_info += f", range [{ns.min:.1f}, {ns.max:.1f}], {ns.n_outliers_iqr} outliers"
            
            if col.categorical_stats:
                cs = col.categorical_stats
                top_val = cs.top_values[0]['value'] if cs.top_values else "N/A"
                col_info += f", top: '{top_val}'"
            
            lines.append(col_info)
        
        lines.append("")
        lines.append("SAMPLE VALUES (first row):")
        if self.sample_rows:
            for key, val in self.sample_rows[0].items():
                lines.append(f"- {key}: {val}")
        
        return "\n".join(lines)
    
    def save_markdown(self, filepath: str) -> None:
        """Save markdown report to file."""
        with open(filepath, 'w') as f:
            f.write(self.to_markdown())
        print(f"Report saved to: {filepath}")


# ============================================================================
# Main Profiling Function
# ============================================================================

def profile_dataframe(df: pd.DataFrame) -> DataProfile:
    """
    Create a comprehensive profile of a DataFrame.
    
    Parameters:
        df: DataFrame to profile
    
    Returns:
        DataProfile object with all statistics and output methods
    
    Example:
        profile = profile_dataframe(df)
        profile.print_report()  # For user
        llm_context = profile.to_llm_prompt()  # For LLM
    """
    
    print("Profiling dataframe...")
    
    # ========================================================================
    # Basic Overview
    # ========================================================================
    
    n_rows, n_cols = df.shape
    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    
    # ========================================================================
    # Profile Each Column
    # ========================================================================
    
    column_profiles = []
    n_numeric = 0
    n_categorical = 0
    n_datetime = 0
    n_boolean = 0
    n_other = 0
    
    for col_name in df.columns:
        col = df[col_name]
        col_profile = _profile_column(col, col_name, n_rows)
        column_profiles.append(col_profile)
        
        # Count types
        if col_profile.dtype_category == "numeric":
            n_numeric += 1
        elif col_profile.dtype_category == "categorical":
            n_categorical += 1
        elif col_profile.dtype_category == "datetime":
            n_datetime += 1
        elif col_profile.dtype_category == "boolean":
            n_boolean += 1
        else:
            n_other += 1
    
    # ========================================================================
    # Data Quality Summary
    # ========================================================================
    
    quality_summary = _compute_quality_summary(df, column_profiles, n_rows)
    
    # ========================================================================
    # Sample Rows
    # ========================================================================
    
    sample_rows = df.head(5).to_dict(orient='records')
    # Convert any non-serializable values to strings
    for row in sample_rows:
        for key, val in row.items():
            if pd.isna(val):
                row[key] = None
            elif not isinstance(val, (str, int, float, bool, type(None))):
                row[key] = str(val)
    
    # ========================================================================
    # Create Profile Object
    # ========================================================================
    
    profile = DataProfile(
        profile_created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        n_rows=n_rows,
        n_columns=n_cols,
        memory_usage_mb=memory_mb,
        n_numeric_columns=n_numeric,
        n_categorical_columns=n_categorical,
        n_datetime_columns=n_datetime,
        n_boolean_columns=n_boolean,
        n_other_columns=n_other,
        columns=column_profiles,
        quality_summary=quality_summary,
        sample_rows=sample_rows
    )
    
    print(f"Profiling complete: {n_rows:,} rows, {n_cols} columns")
    
    return profile


# ============================================================================
# Helper Functions
# ============================================================================

def _profile_column(col: pd.Series, col_name: str, n_rows: int) -> ColumnProfile:
    """Profile a single column."""
    
    # Basic info
    dtype_str = str(col.dtype)
    n_missing = col.isna().sum()
    missing_pct = (n_missing / n_rows) * 100 if n_rows > 0 else 0
    n_unique = col.nunique()
    unique_pct = (n_unique / n_rows) * 100 if n_rows > 0 else 0
    
    # Sample values (non-null)
    sample_vals = col.dropna().head(5).tolist()
    # Convert to serializable types
    sample_vals = [str(v) if not isinstance(v, (str, int, float, bool, type(None))) else v for v in sample_vals]
    
    # Determine dtype category
    dtype_category = _get_dtype_category(col)
    
    # Type-specific stats
    numeric_stats = None
    categorical_stats = None
    datetime_stats = None
    
    if dtype_category == "numeric":
        numeric_stats = _compute_numeric_stats(col)
    elif dtype_category == "categorical":
        categorical_stats = _compute_categorical_stats(col, n_rows)
    elif dtype_category == "datetime":
        datetime_stats = _compute_datetime_stats(col)
    
    return ColumnProfile(
        name=col_name,
        dtype=dtype_str,
        dtype_category=dtype_category,
        n_missing=int(n_missing),
        missing_percent=round(missing_pct, 2),
        n_unique=int(n_unique),
        unique_percent=round(unique_pct, 2),
        sample_values=sample_vals,
        numeric_stats=numeric_stats,
        categorical_stats=categorical_stats,
        datetime_stats=datetime_stats
    )


def _get_dtype_category(col: pd.Series) -> str:
    """Determine the category of a column's dtype."""
    
    if pd.api.types.is_bool_dtype(col):
        return "boolean"
    elif pd.api.types.is_numeric_dtype(col):
        return "numeric"
    elif pd.api.types.is_datetime64_any_dtype(col):
        return "datetime"
    elif isinstance(col.dtype, pd.CategoricalDtype) or pd.api.types.is_object_dtype(col):
        return "categorical"
    else:
        return "other"


def _compute_numeric_stats(col: pd.Series) -> NumericStats:
    """Compute statistics for numeric columns."""
    
    col_clean = col.dropna()
    
    if len(col_clean) == 0:
        return NumericStats(
            min=0, max=0, mean=0, median=0, std=0,
            q1=0, q3=0, skewness=0,
            n_zeros=0, n_negative=0, n_outliers_iqr=0
        )
    
    q1 = float(col_clean.quantile(0.25))
    q3 = float(col_clean.quantile(0.75))
    iqr = q3 - q1
    
    # Count outliers using IQR method
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    n_outliers = int(((col_clean < lower_bound) | (col_clean > upper_bound)).sum())
    
    # Skewness (handle constant columns)
    try:
        skewness = float(col_clean.skew())
    except:
        skewness = 0.0
    
    return NumericStats(
        min=float(col_clean.min()),
        max=float(col_clean.max()),
        mean=float(col_clean.mean()),
        median=float(col_clean.median()),
        std=float(col_clean.std()) if len(col_clean) > 1 else 0,
        q1=q1,
        q3=q3,
        skewness=skewness,
        n_zeros=int((col_clean == 0).sum()),
        n_negative=int((col_clean < 0).sum()),
        n_outliers_iqr=n_outliers
    )


def _compute_categorical_stats(col: pd.Series, n_rows: int) -> CategoricalStats:
    """Compute statistics for categorical columns."""
    
    col_clean = col.dropna()
    value_counts = col_clean.value_counts()
    n_unique = len(value_counts)
    
    # Top values
    top_values = []
    for val, count in value_counts.head(10).items():
        top_values.append({
            "value": str(val),
            "count": int(count),
            "percent": round((count / n_rows) * 100, 2) if n_rows > 0 else 0
        })
    
    unique_pct = (n_unique / n_rows) * 100 if n_rows > 0 else 0
    
    return CategoricalStats(
        n_unique=n_unique,
        unique_percent=round(unique_pct, 2),
        top_values=top_values,
        is_constant=(n_unique <= 1),
        is_high_cardinality=(unique_pct > 90)
    )


def _compute_datetime_stats(col: pd.Series) -> DateTimeStats:
    """Compute statistics for datetime columns."""
    
    col_clean = col.dropna()
    
    if len(col_clean) == 0:
        return DateTimeStats(
            min_date="N/A",
            max_date="N/A",
            range_days=0,
            n_unique=0
        )
    
    min_date = col_clean.min()
    max_date = col_clean.max()
    
    try:
        range_days = (max_date - min_date).days
    except:
        range_days = 0
    
    return DateTimeStats(
        min_date=str(min_date),
        max_date=str(max_date),
        range_days=int(range_days),
        n_unique=int(col_clean.nunique())
    )


def _compute_quality_summary(df: pd.DataFrame, 
                              column_profiles: list[ColumnProfile], 
                              n_rows: int) -> DataQualitySummary:
    """Compute overall data quality summary."""
    
    # Total missing
    total_cells = n_rows * len(column_profiles)
    total_missing = sum(cp.n_missing for cp in column_profiles)
    total_missing_pct = (total_missing / total_cells) * 100 if total_cells > 0 else 0
    
    # Duplicate rows
    n_duplicates = df.duplicated().sum()
    dup_pct = (n_duplicates / n_rows) * 100 if n_rows > 0 else 0
    
    # Problem columns
    cols_with_missing = [cp.name for cp in column_profiles if cp.n_missing > 0]
    cols_high_missing = [cp.name for cp in column_profiles if cp.missing_percent > 50]
    cols_constant = [cp.name for cp in column_profiles 
                     if cp.categorical_stats and cp.categorical_stats.is_constant]
    cols_high_card = [cp.name for cp in column_profiles 
                      if cp.categorical_stats and cp.categorical_stats.is_high_cardinality]
    cols_with_outliers = [cp.name for cp in column_profiles 
                          if cp.numeric_stats and cp.numeric_stats.n_outliers_iqr > 0]
    
    # Generate warnings
    warnings = []
    if total_missing_pct > 10:
        warnings.append(f"High overall missing rate: {total_missing_pct:.1f}%")
    if dup_pct > 5:
        warnings.append(f"Significant duplicate rows: {dup_pct:.1f}%")
    if cols_high_missing:
        warnings.append(f"{len(cols_high_missing)} column(s) have >50% missing values")
    if cols_constant:
        warnings.append(f"{len(cols_constant)} constant column(s) may be useless")
    if cols_high_card:
        warnings.append(f"{len(cols_high_card)} column(s) may be ID columns (>90% unique)")
    
    return DataQualitySummary(
        total_missing_cells=int(total_missing),
        total_missing_percent=round(total_missing_pct, 2),
        n_duplicate_rows=int(n_duplicates),
        duplicate_rows_percent=round(dup_pct, 2),
        columns_with_missing=cols_with_missing,
        columns_high_missing=cols_high_missing,
        columns_constant=cols_constant,
        columns_high_cardinality=cols_high_card,
        columns_with_outliers=cols_with_outliers,
        warnings=warnings
    )



