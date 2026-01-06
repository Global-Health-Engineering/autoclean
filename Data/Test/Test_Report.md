# AutoClean Report

**Dataset:** Test Data
**Generated:** 2026-01-06 14:18:05

---

## Summary

- **Original shape:** 75 rows × 14 columns
- **After preprocessing:** 75 rows × 14 columns
- **Total rows deleted:** 2
- **Total values imputed:** 3
- **Total structural errors fixed:** 306

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

- **Numerical missing:** 3
- **Categorical missing:** 0.0
- **Method (numerical):** missforest
- **Method (categorical):** false

### Imputations

| Row | Column | New Value | Method |
|-----|--------|-----------|--------|
| 24 | water_quality_score | 81.9 | missforest |
| 27 | water_quality_score | 73.1 | missforest |
| 62 | water_quality_score | 73.4 | missforest |

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

- **Columns processed:** 8
- **Total values changed:** 306

### city

- **Similarity method:** embeddings
- **Clustering method:** affinity_propagation
- **Canonical selection:** llm
- **Embedding model:** text-embedding-3-small
- **Unique values before:** 21
- **Unique values after:** 6
- **Values changed:** 50

| Original Values | Canonical |
|-----------------|-----------|
| New York, new york, NYC, NY, New York City | New York City |
| Boston, boston, BOSTON | Boston |
| Los Angeles, LA, L.A., los angeles | Los Angeles |
| Chicago, chicago, CHICAGO | Chicago |
| Seattle, seattle, SEATTLE | Seattle |
| Denver, denver, DENVER | Denver |

### facility_type

- **Similarity method:** rapidfuzz
- **Clustering method:** connected_components
- **Canonical selection:** most_frequent
- **Threshold:** 0.85
- **Unique values before:** 13
- **Unique values after:** 8
- **Values changed:** 12

| Original Values | Canonical |
|-----------------|-----------|
| Hospital, hospital, Hosptial, hosptial | Hospital |
| Clinic, Clnic | Clinic |
| Health Center, Helth Center | Health Center |

### water_source

- **Similarity method:** rapidfuzz
- **Clustering method:** connected_components
- **Canonical selection:** most_frequent
- **Threshold:** 0.85
- **Unique values before:** 13
- **Unique values after:** 6
- **Values changed:** 40

| Original Values | Canonical |
|-----------------|-----------|
| Borehole, bore hole, borehole | bore hole |
| Hand pump, hand pump, Hand Pump, handpump | Hand pump |
| Piped water, Piped Water, piped water | Piped water |

### funding_organization

- **Similarity method:** embeddings
- **Clustering method:** hierarchical
- **Canonical selection:** llm
- **Threshold:** 0.6
- **Embedding model:** text-embedding-3-large
- **Unique values before:** 9
- **Unique values after:** 3
- **Values changed:** 49

| Original Values | Canonical |
|-----------------|-----------|
| WHO, World Health Organization, W.H.O. | World Health Organization |
| UNICEF, United Nations Children's Fund, United Nations Childrens Fund | United Nations Children's Fund |
| Scottish Government, The Scottish Government, Scottish Gov | The Scottish Government |

### daily_usage

- **Similarity method:** embeddings
- **Clustering method:** affinity_propagation
- **Canonical selection:** llm
- **Embedding model:** text-embedding-3-large
- **Unique values before:** 64
- **Unique values after:** 5
- **Values changed:** 67

| Original Values | Canonical |
|-----------------|-----------|
| 500L, 490L, 640L, 560L, 580L, 520L, 540L, 700L, 5000L | 540L |
| 480 liters, 510 liters, 230 liters, 620 liters, 350 liters, 184 liters, 550 liters, 420 liters, 290 liters, 570 liters, 430 liters, 210 liters, 530 liters, 250 liters, 690 liters, 370 liters, 190 liters, 390 liters, 270 liters, 600 liters, 360 liters, 196 liters | 480 liters |
| 520000ml, 250000ml, 660000ml, 370000ml, 196000ml, 570000ml, 430000ml, 280000ml, 590000ml, 450000ml, 230000ml, 530000ml, 550000ml, 270000ml, 710000ml, 390000ml, 210000ml, 420000ml, 620000ml | 530000ml |
| 240L, 236L, 190L, 220L, 260L, 200L, 280L | 240L |
| 630L, 360L, 420L, 410L, 440L, 380L, 430L | 630L |

### is_functional

- **Similarity method:** embeddings
- **Clustering method:** hierarchical
- **Canonical selection:** llm
- **Threshold:** 0.7
- **Embedding model:** text-embedding-3-large
- **Unique values before:** 9
- **Unique values after:** 7
- **Values changed:** 4

| Original Values | Canonical |
|-----------------|-----------|
| true, TRUE, false | TRUE |

### maintenance_frequency

- **Similarity method:** rapidfuzz
- **Clustering method:** hierarchical
- **Canonical selection:** most_frequent
- **Threshold:** 0.7
- **Unique values before:** 9
- **Unique values after:** 4
- **Values changed:** 27

| Original Values | Canonical |
|-----------------|-----------|
| Monthly, monthly, Mothly, Montly | monthly |
| Quarterly, quarterly, Quartely | Quarterly |

### number_of_staff

- **Similarity method:** embeddings
- **Clustering method:** affinity_propagation
- **Canonical selection:** llm
- **Embedding model:** text-embedding-3-large
- **Unique values before:** 42
- **Unique values after:** 10
- **Values changed:** 57

| Original Values | Canonical |
|-----------------|-----------|
| 25, 24, 26, 21, 22, twenty-two | 22 |
| twenty-six, twelve, eighteen, twenty-nine, twenty-seven, twenty-eight, thirteen, twenty-one | twenty-one |
| 12, 11, 10, 9, eleven | 12 |
| 32, 31, 28, 29, 27, 35, 30 | 30 |
| thirty-three, thirty, thirty-six | thirty |
| 18, 17, 19, nineteen | 19 |
| ten, twenty, 20 | 20 |
| 15, 14, 13, fourteen | 15 |

---

## Postprocessing

| Column | Action |
|--------|--------|
| water_quality_score | Restored to integer |
