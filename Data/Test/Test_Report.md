# AutoClean Report

**Name of dataset:** Test Data (made up WHASH dataset)  
**Filepath of messy dataset:** Data/Test/Test.csv  
**Filepath of cleaned dataset:** Data/Test/Test_Cleaned.csv  
**Generated:** 24.01.2026, 00:51:24

---

## Summary

- **Original shape:** 52 rows × 13 columns
- **Final shape:** 50 rows × 11 columns
- **Total rows deleted:** 2
- **Total columns deleted:** 2
- **Total values imputed:** 0
- **Total outliers handled:** 3
- **Total semantic outliers detected:** 8
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

## Semantic Outliers

### Overview

- **Columns processed:** 2
- **Total outliers detected:** 8
- **Total number of affected rows:** 8

### Column: Village

- **Given context:** Location name in Africa
- **Threshold:** 0.5
- **Action:** nan
- **Unique values checked:** 14
- **Outliers detected:** 4

#### Detected Outliers

| Value | Confidence | Number of affected rows |
|-------|------------|-------------------------|
| sdflkajsdf | 0.0 | 1 |
| I love studying at ETH! | 0.0 | 1 |
| 1.8 | 0.0 | 1 |
| unknown | 0.0 | 1 |

### Column: Population served

- **Given context:** Number of people
- **Threshold:** 0.5
- **Action:** nan
- **Unique values checked:** 50
- **Outliers detected:** 4

#### Detected Outliers

| Value | Confidence | Number of affected rows |
|-------|------------|-------------------------|
| -250 | 0.0 | 1 |
| 1234.89 | 0.2 | 1 |
| 999.99 | 0.0 | 1 |
| not so many | 0.0 | 1 |

---

## Outliers

### Lower & Upper Bounds

| Column | Lower Bound | Upper Bound |
|--------|-------------|-------------|
| Flow Rate lps | -1.6987 | 6.7512 |

### Overview

- **Multiplier:** 1.5
- **Total outliers:** 3
- **Method:** winsorize

### Outliers Handled

| Column | Original | New Value | Bound |
|--------|----------|-----------|-------|
| Flow Rate lps | 48.7 | 6.75125 | upper |
| Flow Rate lps | 9.2 | 6.75125 | upper |
| Flow Rate lps | 12.8 | 6.75125 | upper |

**Note:** New values shown above are pre-rounding. Final values may be rounded in post-processing to match original column precision.

---

## DateTime Standardization

- **Column:** install_date
- **Format:** European (DD/MM)
- **Invalid handling:** nat
- **Total values:** 50
- **Successfully converted / standardized:** 40
- **Invalid values:** 10

### Invalid values handled

| Original | Action |
|----------|--------|
| 15/2020 | set to NaT |
| January 2020 | set to NaT |
| 15/25/2020 | set to NaT |
| 31/04/2020 | set to NaT |
| 29/02/2023 | set to NaT |
| 15/05/2200 | set to NaT |
| 15/2020/05 | set to NaT |
| 01/25/2024 | set to NaT |
| 2024/25/01 | set to NaT |
| unknown | set to NaT |

---

## Postprocessing

### Precision Restoration (rounding)

| Column | Action |
|--------|--------|
| Flow Rate lps | Rounded to 2 decimals |

### Renamed Columns

| Original Column Name | New Column Name |
|----------------------|-----------------|
| Village | village |
| Population served | population_served |
| Flow Rate lps | flow_rate_lps |
| funding organization | funding_organization |
| sample Volume | sample_volume |
| tank material | tank_material |
