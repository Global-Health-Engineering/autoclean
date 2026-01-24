# AutoClean Report

**Name of dataset:** Test Data (made up WHASH dataset)  
**Filepath of messy dataset:** Data/Test/Test.csv  
**Filepath of cleaned dataset:** Data/Test/Test_Cleaned.csv  
**Generated:** 24.01.2026, 00:58:38

---

## Summary

- **Original shape:** 52 rows × 13 columns
- **Final shape:** 50 rows × 11 columns
- **Total rows deleted:** 2
- **Total columns deleted:** 2
- **Total values imputed:** 0
- **Total outliers handled:** 0
- **Total semantic outliers detected:** 0
- **Total structural errors fixed:** 42

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
- **Total values changed:** 42
- **Total unique values before:** 29
- **Total unique values after:** 9

### Column: funding organization

- **Similarity method:** embeddings
- **Embedding model:** text-embedding-3-large
- **Clustering method:** connected_components
- **Threshold (connected components):** 0.6
- **Canonical selection:** llm
- **Values changed:** 40
- **Unique values before:** 24
- **Unique values after:** 5

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| Red Crss; RED CROSS; ICRC; International Red Cross; red cross; RedCross | International Red Cross |
| world health org; WHO; World Health Org; WH0; World Health Organization; W.H.O.; W.H.O; WHO. | World Health Organization |
| WorldBank; WORLD BANK; World Bank; Wrold Bank; world bank | World Bank |
| UNICEF; unicef; U.N.I.C.E.F.; United Nations Children's Fund | United Nations Children's Fund |
| WB | WB |

### Column: funding organization

- **Similarity method:** llm
- **LLM mode:** fast
- **LLM context provided:** Funding organizations
- **Clustering method:** hierarchical
- **Threshold (hierarchical):** 0.9
- **Canonical selection:** llm
- **Values changed:** 2
- **Unique values before:** 5
- **Unique values after:** 4

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| International Red Cross | International Red Cross |
| World Health Organization | World Health Organization |
| World Bank; WB | World Bank |
| United Nations Children's Fund | United Nations Children's Fund |

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
