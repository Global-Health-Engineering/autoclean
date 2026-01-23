# AutoClean Report

**Name of dataset:** Test Data (made up WHASH dataset)  
**Filepath of messy dataset:** Data/Test/Test.csv  
**Filepath of cleaned dataset:** Data/Test/Test_Cleaned.csv  
**Generated:** 23.01.2026, 19:16:10

---

## Summary

- **Original shape:** 52 rows × 13 columns
- **Final shape:** 50 rows × 11 columns
- **Total rows deleted:** 2
- **Total columns deleted:** 2
- **Total values imputed:** 0
- **Total outliers handled:** 0
- **Total semantic outliers detected:** 0
- **Total structural errors fixed:** 47

---

## Preprocessing

- **Completely empty rows removed:** 1
- **Completely empty columns removed:** 1

---

## Duplicates

- **Duplicate rows removed:** 1
- **Duplicate columns removed:** 1

---

## Structural Errors

## Overview

- **Columns processed:** 2
- **Total values changed:** 47
- **Total unique values before:** 34
- **Total unique values after:** 15

### Column: is_functional

- **Similarity method:** rapidfuzz
- **Clustering method:** hierarchical
- **Threshold (hierarchical):** 0.8
- **Canonical selection:** most_frequent
- **Values changed:** 14
- **Unique values before:** 21
- **Unique values after:** 13

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| No; NO; no | No |
| TRUE; True; true | True |
| FALSE; false | FALSE |
| broken | broken |
| 0 | 0 |
| not functional | not functional |
| working | working |
| yes; YES | yes |
| N; n | N |
| y; Y | y |
| not working | not working |
| operational | operational |
| 1 | 1 |

### Column: is_functional

- **Similarity method:** llm
- **LLM model:** gpt-4.1-mini
- **LLM context:** Wether water point is working or not
- **Clustering method:** hierarchical
- **Threshold (hierarchical):** 0.7
- **Canonical selection:** llm
- **Values changed:** 33
- **Unique values before:** 13
- **Unique values after:** 2

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| No; FALSE; broken; 0; not functional; N; not working | No |
| True; working; yes; y; operational; 1 | True |

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
