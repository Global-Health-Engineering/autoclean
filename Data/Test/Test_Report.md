# AutoClean Report

**Name of dataset:** Test Data (made up WHASH dataset)  
**Filepath of messy dataset:** Data/Test/Test.csv  
**Filepath of cleaned dataset:** Data/Test/Test_Cleaned.csv  
**Generated:** 24.01.2026, 02:11:51

---

## Summary

- **Original shape:** 52 rows × 13 columns
- **Final shape:** 50 rows × 11 columns
- **Total rows deleted:** 2
- **Total columns deleted:** 2
- **Total values imputed:** 0
- **Total outliers handled:** 0
- **Total semantic outliers detected:** 0
- **Total structural errors fixed:** 59

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
- **Total values changed:** 59
- **Total unique values before:** 42
- **Total unique values after:** 19

### Column: sample Volume

- **Similarity method:** rapidfuzz
- **Clustering method:** hierarchical
- **Threshold (hierarchical):** 0.9
- **Canonical selection:** llm
- **Values changed:** 19
- **Unique values before:** 26
- **Unique values after:** 16

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| 500l; 500L | 500L |
| 1000 l; 1000L; 1000 L | 1000 L |
| 250l; 250L | 250L |
| 1 kL | 1 kL |
| five hundred liters | five hundred liters |
| 1m³ | 1m³ |
| 250 litres; 250 Liters; 250 liters | 250 liters |
| 500 litres; 500 Liters; 500 liters | 500 liters |
| 1000000 ml | 1000000 ml |
| 1000 Liters; 1000 liters | 1000 liters |
| 250 L | 250 L |
| 0.25 m³ | 0.25 m³ |
| 1 cubic meter | 1 cubic meter |
| 250000ml; 250000 ml | 250000 ml |
| 0.5 kL | 0.5 kL |
| 500 L | 500 L |

### Column: sample Volume

- **Similarity method:** llm
- **LLM mode:** strict
- **LLM context provided:** Volume measurements
- **Clustering method:** connected_components
- **Threshold (connected components):** 1.0
- **Canonical selection:** llm
- **Values changed:** 40
- **Unique values before:** 16
- **Unique values after:** 3

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| 500L; five hundred liters; 500 liters; 0.5 kL; 500 L | 500 L |
| 1000 L; 1 kL; 1m³; 1000000 ml; 1000 liters; 1 cubic meter | 1000 liters |
| 250L; 250 liters; 250 L; 0.25 m³; 250000 ml | 250 liters |

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
