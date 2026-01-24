"""
Generate correlated columns for Missing Values Imputation

This script creates 5 new columns with controlled correlations for testing 
the handle_missing_values() function. The columns are appended to Test.csv.

Columns generated:
    - well_depth_m (Feature, Integer): Random values 20-120
    - pump_age_years (Feature, Integer): Random values 1-15
    - Water quality score (Target, Float): Correlated with features
    - Annual maintenance cost (Target, Integer): Correlated with features  
    - System condition (Target, Categorical): Based on Water quality score

Correlation Logic:
    - Water quality score = 50 + (well_depth * 0.3) - (pump_age * 2) + noise
        -> Deeper well = better quality (positive correlation)
        -> Older pump = worse quality (negative correlation)
    
    - Annual maintenance cost = 100 + (well_depth * 2) + (pump_age * 15) + noise
        -> Deeper well = higher cost (positive correlation)
        -> Older pump = higher cost (positive correlation)
    
    - System condition = "Poor" / "Fair" / "Good"
        if Water quality score < 45: "Poor"
        elif Water quality score ≥ 45 & Water quality score < 65: "Fair"  
        elif Water quality score ≥ 65: "Good"

Special rows handled:
    - Row 25 (0-indexing): Empty row
    - Row 10 & 35 (0-indexing): Duplicate rows 
"""

# Imported libraries
import pandas as pd
import numpy as np

# =============================================================================
# Settings
# =============================================================================

INPUT_FILEPATH = 'Data/Test/Test.csv'
OUTPUT_FILEPATH = 'Data/Test/Test.csv'  # Overwrite with new columns

RANDOM_SEED = 42  # For reproducibility

# Rows for special handling (0-indexing)
EMPTY_ROW_INDEX = 25
DUPLICATE_ROW_INDICES = (10, 35)

# =============================================================================
# Load Data
# =============================================================================

df = pd.read_csv(INPUT_FILEPATH)
n_rows = len(df)

# =============================================================================
# Set Random Seed
# =============================================================================

np.random.seed(RANDOM_SEED) # Ensures reproducibility (same results each run)

# =============================================================================
# Step 1: Generate Feature Columns (Random Values)
# =============================================================================

# Feature 1: well_depth_m (Integer, range: 20-120 meters)
well_depth_m = np.random.randint(20, 121, n_rows) # numpy array with n_rows random values in range [20, 120]

# Feature 2: pump_age_years (Integer, range: 1-15 years)
pump_age_years = np.random.randint(1, 16, n_rows) # numpy array with n_rows random values in range [1, 15]

# =============================================================================
# Step 2: Generate Target Columns (Correlated with Features)
# =============================================================================

# Target 1: Water quality score (Float)
noise_quality = np.random.normal(0, 5, n_rows)  # Gaussian noise (n_rows random sample drawn from gauss distribution (mean = 0, standard deviation = 5), each sample is drawn with the probability appearing in the distribution)
water_quality_score = 50 + (well_depth_m * 0.3) - (pump_age_years * 2) + noise_quality
water_quality_score = np.clip(water_quality_score, 0, 100)  # Set all values smaler than 0 to 0 and values larger than 100 to 100
water_quality_score = np.round(water_quality_score, 2)  # Round to 2 decimals

# Target 2: Annual maintenance cost (Integer)
noise_cost = np.random.normal(0, 20, n_rows)  # Gaussian noise (n_rows random sample drawn from gauss distribution (mean = 0, standard deviation = 20), each sample is drawn with the probability appearing in the distribution)
annual_maintenance_cost = 100 + (well_depth_m * 2) + (pump_age_years * 15) + noise_cost
annual_maintenance_cost = np.clip(annual_maintenance_cost, 50, 500).astype(int)  # Set all values smaler than 50 to 50 and values larger than 500 to 500 and cut off decimals to convert to int 

# Target 3: System condition (Categorical)
def get_system_condition(water_quality_score):
    if water_quality_score < 45:
        return "Poor"
    elif water_quality_score < 65:
        return "Fair"
    else:
        return "Good"

system_condition = [get_system_condition(score) for score in water_quality_score]

# =============================================================================
# Step 3: Handle Special Rows
# =============================================================================

# Convert to object type to allow empty strings (= missing values)
well_depth_m = well_depth_m.astype(object)
pump_age_years = pump_age_years.astype(object)
water_quality_score = water_quality_score.astype(object)
annual_maintenance_cost = annual_maintenance_cost.astype(object)

# Handle empty row 
well_depth_m[EMPTY_ROW_INDEX] = ""
pump_age_years[EMPTY_ROW_INDEX] = ""
water_quality_score[EMPTY_ROW_INDEX] = ""
annual_maintenance_cost[EMPTY_ROW_INDEX] = ""
system_condition[EMPTY_ROW_INDEX] = ""

# Handle duplicate rows
idx_original, idx_duplicate = DUPLICATE_ROW_INDICES
well_depth_m[idx_duplicate] = well_depth_m[idx_original]
pump_age_years[idx_duplicate] = pump_age_years[idx_original]
water_quality_score[idx_duplicate] = water_quality_score[idx_original]
annual_maintenance_cost[idx_duplicate] = annual_maintenance_cost[idx_original]
system_condition[idx_duplicate] = system_condition[idx_original]

# =============================================================================
# Step 4: Add Columns to DataFrame
# =============================================================================

df['well_depth_m'] = well_depth_m
df['pump_age_years'] = pump_age_years
df['Water quality score'] = water_quality_score
df['Annual maintenance cost'] = annual_maintenance_cost
df['System condition'] = system_condition

# =============================================================================
# Step 5: Export DataFrame as CSV
# =============================================================================

df.to_csv(OUTPUT_FILEPATH, index=False)
# Note: index = False leads to no row index in final csv 

# =============================================================================
# Verification: Correlation Matrix
# =============================================================================

print("\n")
print("Correlation Matrix")
print("-" * 100)

# Convert columns back to numerical columns ("" -> NaN) to calculate correlation matrix
df['well_depth_m'] = pd.to_numeric(df['well_depth_m'])
df['pump_age_years'] = pd.to_numeric(df['pump_age_years'])
df['Water quality score'] = pd.to_numeric(df['Water quality score'])
df['Annual maintenance cost'] = pd.to_numeric(df['Annual maintenance cost'])

print(df[['well_depth_m', 'pump_age_years', 'Water quality score', 'Annual maintenance cost']].corr().round(3))
print("\n")