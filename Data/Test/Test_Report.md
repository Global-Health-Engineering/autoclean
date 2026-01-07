# AutoClean Report

**Dataset:** Test Data
**Generated:** 2026-01-07 01:48:21

---

## Summary

- **Original shape:** 75 rows × 14 columns
- **After preprocessing:** 75 rows × 14 columns
- **Total rows deleted:** 2
- **Total values imputed:** 8
- **Total structural errors fixed:** 249

---

## Preprocessing

- **Columns renamed:** 12

| Original | New |
|----------|-----|
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
| ... | (2 more) |

---

## Duplicates

- **Duplicate rows removed:** 2

---

## Missing Values

- **Numerical missing:** 8
- **Categorical missing:** 0.0
- **Method (numerical):** missforest
- **Method (categorical):** false

### Imputations

| Row | Column | New Value | Method |
|-----|--------|-----------|--------|
| 22 | population_served | 2170 | missforest |
| 28 | population_served | 1425 | missforest |
| 60 | population_served | 1920 | missforest |
| 64 | population_served | 1410 | missforest |
| 23 | users_count | 2095 | missforest |
| 24 | water_quality_score | 76.7 | missforest |
| 27 | water_quality_score | 73.3 | missforest |
| 62 | water_quality_score | 73.7 | missforest |

---

## DateTime Standardization

- **Column:** date_installed
- **Format:** European (DD/MM)
- **Invalid handling:** nat
- **Total values:** 73
- **Successfully converted:** 73
- **Invalid:** 0

---

## Outliers

No outliers found.

---

## Structural Errors

- **Columns processed:** 6
- **Total values changed:** 249

### city

- **Similarity method:** embeddings
- **Clustering method:** affinity_propagation
- **Canonical selection:** most_frequent
- **Embedding model:** text-embedding-3-large
- **Unique values before:** 21
- **Unique values after:** 6
- **Values changed:** 48

#### Clustering Results

| Original Values | Canonical |
|-----------------|-----------|
| New York; new york; NYC; NY; New York City | NYC |
| Boston; boston; BOSTON | boston |
| Los Angeles; LA; L.A.; los angeles | Los Angeles |
| Chicago; chicago; CHICAGO | Chicago |
| Seattle; seattle; SEATTLE | Seattle |
| Denver; denver; DENVER | Denver |

### facility_type

- **Similarity method:** rapidfuzz
- **Clustering method:** hierarchical
- **Canonical selection:** most_frequent
- **Threshold:** 0.75
- **Unique values before:** 13
- **Unique values after:** 3
- **Values changed:** 49

#### Clustering Results

| Original Values | Canonical |
|-----------------|-----------|
| Clinic; clinic; CLINIC; Clnic | Clinic |
| Hospital; hospital; HOSPITAL; Hosptial; hosptial | Hospital |
| Health Center; health center; Health centre; Helth Center | Health Center |

### water_source

- **Similarity method:** rapidfuzz
- **Clustering method:** hierarchical
- **Canonical selection:** most_frequent
- **Threshold:** 0.7
- **Unique values before:** 13
- **Unique values after:** 3
- **Values changed:** 49

#### Clustering Results

| Original Values | Canonical |
|-----------------|-----------|
| Borehole; bore hole; Borehole well; borehole; BOREHOLE | bore hole |
| Hand pump; hand pump; Hand Pump; handpump | Hand pump |
| Piped water; Piped Water; piped water; Tap water | Piped water |

### funding_organization

- **Similarity method:** embeddings
- **Clustering method:** hierarchical
- **Canonical selection:** most_frequent
- **Threshold:** 0.65
- **Embedding model:** text-embedding-3-large
- **Unique values before:** 9
- **Unique values after:** 3
- **Values changed:** 40

#### Clustering Results

| Original Values | Canonical |
|-----------------|-----------|
| WHO; World Health Organization; W.H.O. | WHO |
| UNICEF; United Nations Children's Fund; United Nations Childrens Fund | UNICEF |
| Scottish Government; The Scottish Government; Scottish Gov | Scottish Government |

### is_functional

- **Similarity method:** embeddings
- **Clustering method:** affinity_propagation
- **Canonical selection:** most_frequent
- **Embedding model:** text-embedding-3-large
- **Unique values before:** 9
- **Unique values after:** 4
- **Values changed:** 15

#### Clustering Results

| Original Values | Canonical |
|-----------------|-----------|
| Yes; No | Yes |
| Y; N | Y |
| 1; 0 | 1 |
| true; TRUE; false | true |

### maintenance_frequency

- **Similarity method:** rapidfuzz
- **Clustering method:** hierarchical
- **Canonical selection:** most_frequent
- **Threshold:** 0.75
- **Unique values before:** 9
- **Unique values after:** 2
- **Values changed:** 48

#### Clustering Results

| Original Values | Canonical |
|-----------------|-----------|
| Monthly; monthly; MONTHLY; Mothly; Montly | monthly |
| Quarterly; quarterly; QUARTERLY; Quartely | Quarterly |

---

## Postprocessing

| Column | Action |
|--------|--------|
| population_served | Restored to integer |
| users_count | Restored to integer |
| water_quality_score | Restored to integer |
