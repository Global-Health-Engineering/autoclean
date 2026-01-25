# AutoClean Report

**Name of dataset:** Test Data (made up WHASH dataset)  
**Filepath of messy dataset:** Data/Test/Test.csv  
**Filepath of cleaned dataset:** Data/Test/Test_Cleaned.csv  
**Generated:** 25.01.2026, 18:11:25

---

## Summary

- **Original shape:** 52 rows × 18 columns
- **Final shape:** 50 rows × 16 columns
- **Total rows deleted:** 2
- **Total columns deleted:** 2
- **Total values imputed:** 13
- **Total outliers handled:** 0
- **Total semantic outliers detected:** 0
- **Total structural errors fixed:** 0

---

## Preprocessing

- **Completely empty rows removed:** 1
- **Completely empty columns removed:** 1

---

## Duplicates

- **Duplicate rows removed:** 1
- **Duplicate columns removed:** 1

---

## Missing Values

### Overview

- **Columns processed:** 3
- **Total values imputed:** 13
- **Total rows deleted:** 0

### Column: Water quality score

- **Method:** missforest
- **Features used:** well_depth_m; pump_age_years
- **n_estimators:** 10
- **max_iter:** 5
- **max_depth:** 3
- **min_samples_leaf:** 3
- **Missing values before imputation:** 5
- **Values imputed:** 5

#### Imputations

| Row | New imputed Value |
|-----|-------------------|
| 3 | 41.95842004662004 |
| 8 | 60.66916903958615 |
| 19 | 42.199022222222226 |
| 31 | 66.97927571208032 |
| 45 | 51.935611732711735 |

**Note:** Imputed values shown above are pre-rounding. Final values may be rounded in post-processing.
### Column: Annual maintenance cost

- **Method:** missforest
- **Features used:** well_depth_m; pump_age_years
- **n_estimators:** 10
- **max_iter:** 1
- **max_depth:** 3
- **min_samples_leaf:** 3
- **Missing values before imputation:** 5
- **Values imputed:** 5

#### Imputations

| Row | New imputed Value |
|-----|-------------------|
| 5 | 294.60238095238094 |
| 16 | 421.5731746031746 |
| 27 | 353.9897113997114 |
| 36 | 456.8509523809524 |
| 48 | 434.30095238095237 |

**Note:** Imputed values shown above are pre-rounding. Final values may be rounded in post-processing.
### Column: System condition

- **Method:** knn
- **Features used:** well_depth_m; pump_age_years; Water quality score
- **n_neighbors:** 3
- **Missing values before imputation:** 3
- **Values imputed:** 3

#### Imputations

| Row | New imputed Value |
|-----|-------------------|
| 12 | Fair |
| 25 | Fair |
| 42 | Fair |

**Note:** Imputed values shown above are pre-rounding. Final values may be rounded in post-processing.

---

## Postprocessing

### Precision Restoration (rounding)

| Column | Action |
|--------|--------|
| Flow Rate lps | Rounded to 2 decimals |
| well_depth_m | Restored to integer |
| pump_age_years | Restored to integer |
| Water quality score | Rounded to 2 decimals |
| Annual maintenance cost | Restored to integer |

### Renamed Columns

| Original Column Name | New Column Name |
|----------------------|-----------------|
| Village | village |
| Population served | population_served |
| Flow Rate lps | flow_rate_lps |
| funding organization | funding_organization |
| sample Volume | sample_volume |
| tank material | tank_material |
| Water quality score | water_quality_score |
| Annual maintenance cost | annual_maintenance_cost |
| System condition | system_condition |
