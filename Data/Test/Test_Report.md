# AutoClean Report

**Dataset:** Test Data  
**Generated:** 23.01.2026, 00:00:45

---

## Summary

- **Original shape:** 52 rows × 13 columns
- **Final shape:** 50 rows × 11 columns
- **Total rows deleted:** 2
- **Total columns deleted:** 2
- **Total values imputed:** 0
- **Total outliers handled:** 0
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
| 1234.56 | 0.2 | 1 |
| 999.99 | 0.2 | 1 |
| not so many | 0.0 | 1 |

---

## Postprocessing

### Precision Restoration (rounding)

No precision restoration (rounding) was applied in post-processing.

### Renamed Columns

| Original Column Name | New Column Name |
|----------------------|-----------------|
| Village | village |
| Population served | population_served |
| Flow Rate lps | flow_rate_lps |
| funding organization | funding_organization |
| sample Volume | sample_volume |
| tank material | tank_material |
