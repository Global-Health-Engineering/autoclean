# AutoClean Report

**Dataset:** Test Data
**Generated:** 17.01.2026, 00:28:58

---

## Summary

- **Original shape:** 75 rows × 14 columns
- **Shape after preprocessing:** 75 rows × 14 columns
- **Total rows deleted:** 2
- **Total values imputed:** 8
- **Total structural errors fixed:** 250

---

## Preprocessing

No completely empty rows or columns found resp. removed.

---

## Duplicates

- **Duplicate rows removed:** 2

---

## Missing Values

### Column Selection

**Selected columns**: 
- Water Quality_Score
- Population_served
- users_Count

**Note:** Only these columns were selected to handle missing values.

### Overview

- **Numerical missing values:** 8
- **Categorical missing values:** 0.0
- **Chosen method for numerical missing values:** missforest
- **Chosen method for categorical missing values:** false
- **Chosen parameters for MissForest:** n_estimators = 10; max_depth = None; max_iter = 10 & min_samples_leaf = 1

### Imputations

**Numerical:**
| Row | Column | New Value | Method |
|-----|--------|-----------|--------|
| 22 | Population_served | 2150.0 | missforest |
| 28 | Population_served | 1430.0 | missforest |
| 60 | Population_served | 1920.0 | missforest |
| 64 | Population_served | 1410.0 | missforest |
| 23 | users_Count | 2125.0 | missforest |
| 24 | Water Quality_Score | 76.6 | missforest |
| 27 | Water Quality_Score | 73.1 | missforest |
| 62 | Water Quality_Score | 73.6 | missforest |


---

## DateTime Standardization

- **Column:** date_Installed
- **Format:** European (DD/MM)
- **Invalid handling:** nat
- **Total values:** 73
- **Successfully converted / standardized:** 73
- **Invalid values:** 0

---

## Outliers

No numerical columns found in dataset.

---

## Structural Errors


## Overview

- **Columns processed:** 7
- **Total values changed:** 250
- **Total unique values before:** 116
- **Total unique values after:** 62
- **Total change in unique values:** 53.45%

### Column: city

- **Similarity method:** embeddings
- **Embedding model:** text-embedding-3-large
- **Clustering method:** affinity_propagation
- **Damping (affinity propagation):** 0.7
- **Canonical selection:** most_frequent
- **Values changed:** 48
- **Unique values before:** 21
- **Unique values after:** 6
- **Change in unique values:** 28.57%

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| New York; new york; NYC; NY; New York City | NYC |
| Boston; boston; BOSTON | boston |
| Los Angeles; LA; L.A.; los angeles | Los Angeles |
| Chicago; chicago; CHICAGO | Chicago |
| Seattle; seattle; SEATTLE | Seattle |
| Denver; denver; DENVER | Denver |

### Column: Facility Type

- **Similarity method:** rapidfuzz
- **Clustering method:** hierarchical
- **Threshold (hierarchical):** 0.75
- **Canonical selection:** most_frequent
- **Values changed:** 49
- **Unique values before:** 13
- **Unique values after:** 3
- **Change in unique values:** 23.08%

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| Hospital; hospital; HOSPITAL; Hosptial; hosptial | Hospital |
| Clinic; clinic; CLINIC; Clnic | Clinic |
| Health Center; health center; Health centre; Helth Center | Health Center |

### Column: Water source

- **Similarity method:** rapidfuzz
- **Clustering method:** hierarchical
- **Threshold (hierarchical):** 0.7
- **Canonical selection:** most_frequent
- **Values changed:** 49
- **Unique values before:** 13
- **Unique values after:** 3
- **Change in unique values:** 23.08%

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| Borehole; bore hole; Borehole well; borehole; BOREHOLE | bore hole |
| Hand pump; hand pump; Hand Pump; handpump | Hand pump |
| Piped water; Piped Water; piped water; Tap water | Piped water |

### Column: Funding_Organization

- **Similarity method:** embeddings
- **Embedding model:** text-embedding-3-large
- **Clustering method:** hierarchical
- **Threshold (hierarchical):** 0.65
- **Canonical selection:** most_frequent
- **Values changed:** 40
- **Unique values before:** 9
- **Unique values after:** 3
- **Change in unique values:** 33.33%

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| WHO; World Health Organization; W.H.O. | WHO |
| UNICEF; United Nations Children's Fund; United Nations Childrens Fund | UNICEF |
| Scottish Government; The Scottish Government; Scottish Gov | Scottish Government |

### Column: Is Functional

- **Similarity method:** embeddings
- **Embedding model:** text-embedding-3-large
- **Clustering method:** affinity_propagation
- **Damping (affinity propagation):** 0.7
- **Canonical selection:** most_frequent
- **Values changed:** 15
- **Unique values before:** 9
- **Unique values after:** 4
- **Change in unique values:** 44.44%

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| Yes; No | Yes |
| Y; N | Y |
| 1; 0 | 1 |
| true; TRUE; false | true |

### Column: Number of Staff

- **Similarity method:** embeddings
- **Embedding model:** text-embedding-3-large
- **Clustering method:** hierarchical
- **Threshold (hierarchical):** 0.8
- **Canonical selection:** most_frequent
- **Values changed:** 1
- **Unique values before:** 42
- **Unique values after:** 41
- **Change in unique values:** 97.62%

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| 25 | 25 |
| 24 | 24 |
| twenty-six | twenty-six |
| 26 | 26 |
| 12 | 12 |
| 11 | 11 |
| twelve | twelve |
| 32 | 32 |
| 31 | 31 |
| thirty-three | thirty-three |
| 18 | 18 |
| 17 | 17 |
| eighteen | eighteen |
| 10 | 10 |
| 9 | 9 |
| ten | ten |
| 28 | 28 |
| twenty-nine | twenty-nine |
| 21 | 21 |
| 22 | 22 |
| twenty; 20 | twenty |
| 15 | 15 |
| 14 | 14 |
| 29 | 29 |
| thirty | thirty |
| twenty-two | twenty-two |
| eleven | eleven |
| twenty-seven | twenty-seven |
| 27 | 27 |
| twenty-eight | twenty-eight |
| 13 | 13 |
| thirteen | thirteen |
| 35 | 35 |
| thirty-six | thirty-six |
| 19 | 19 |
| nineteen | nineteen |
| twenty-one | twenty-one |
| fourteen | fourteen |
| 250 | 250 |
| 30 | 30 |
| -5 | -5 |

### Column: Maintenance_Frequency

- **Similarity method:** rapidfuzz
- **Clustering method:** hierarchical
- **Threshold (hierarchical):** 0.75
- **Canonical selection:** most_frequent
- **Values changed:** 48
- **Unique values before:** 9
- **Unique values after:** 2
- **Change in unique values:** 22.22%

#### Clustering Results

| Original Values | Clustered to Canonical |
|-----------------|------------------------|
| Monthly; monthly; MONTHLY; Mothly; Montly | monthly |
| Quarterly; quarterly; QUARTERLY; Quartely | Quarterly |

---

## Postprocessing

### Precision Restoration (rounding)

| Column | Action |
|--------|--------|
| Population_served | Restored to integer |
| users_Count | Restored to integer |
| Water Quality_Score | Restored to integer |

### Renamed Columns

| Original Column Name | New Column Name |
|----------------------|-----------------|
| Facility Type | facility_type |
| Water source | water_source |
| Funding_Organization | funding_organization |
| date_Installed | date_installed |
| Population_served | population_served |
| users_Count | users_count |
| Water Quality_Score | water_quality_score |
| Distance_km | distance_km |
| Daily_Usage | daily_usage |
| Is Functional | is_functional |
| Maintenance_Frequency | maintenance_frequency |
| Number of Staff | number_of_staff |
