"""
Main testing file
Test all cleaning functions on the Test_Data dataset.
"""

import pandas as pd
from Functions.Duplicates import handle_duplicates
from Functions.Missing_Values import handle_missing_values
from Functions.Outliers import handle_outliers
from Functions.Cluster_Categorical import cluster_categorical_values, preview_clusters

# ============================================================================
# Load Data
# ============================================================================

df = pd.read_csv("Data/Test_Data.csv")

print("=" * 70)
print("ORIGINAL DATA")
print("=" * 70)
print(df.to_string())
print(f"\nShape: {df.shape[0]} rows, {df.shape[1]} columns")
print()

# ============================================================================
# Step 1: Handle Duplicates
# ============================================================================

print("=" * 70)
print("STEP 1: DUPLICATES")
print("=" * 70)
df = handle_duplicates(df)
print(f"Shape after: {df.shape[0]} rows, {df.shape[1]} columns")
print()

# ============================================================================
# Step 2: Cluster Categorical Values (before missing values - cleaner data)
# ============================================================================

print("=" * 70)
print("STEP 2: CLUSTER CATEGORICAL VALUES")
print("=" * 70)
df = cluster_categorical_values(
    df,
    columns=['city', 'department', 'status'],
    threshold=0.75,
    method='levenshtein',
    canonical='most_frequent'
)
print()

# ============================================================================
# Step 3: Handle Missing Values
# ============================================================================

print("=" * 70)
print("STEP 3: MISSING VALUES")
print("=" * 70)
df = handle_missing_values(
    df,
    method_num='mean',
    method_categ='mode'
)
print(f"Shape after: {df.shape[0]} rows, {df.shape[1]} columns")
print()

# ============================================================================
# Step 4: Handle Outliers
# ============================================================================

print("=" * 70)
print("STEP 4: OUTLIERS")
print("=" * 70)
df = handle_outliers(
    df,
    method='clip'  # or 'delete', 'iqr'
)
print(f"Shape after: {df.shape[0]} rows, {df.shape[1]} columns")
print()

# ============================================================================
# Final Result
# ============================================================================

print("=" * 70)
print("FINAL CLEANED DATA")
print("=" * 70)
print(df.to_string())
print(f"\nFinal shape: {df.shape[0]} rows, {df.shape[1]} columns")

# ============================================================================
# Save to CSV
# ============================================================================

df.to_csv("Data/Test_Data_Cleaned.csv", index=False)
print("\nSaved to: Data/Test_Data_Cleaned.csv")