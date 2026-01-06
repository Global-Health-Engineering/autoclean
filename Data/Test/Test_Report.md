# AutoClean Report

**Dataset:** Test Data
**Generated:** 2026-01-06 13:16:12

---

## Summary

- **Original shape:** 75 rows × 14 columns
- **After preprocessing:** 75 rows × 14 columns
- **Total rows deleted:** 2
- **Total structural errors fixed:** 50

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

- **Numerical missing:** 0.0
- **Categorical missing:** 3
- **Method (numerical):** false
- **Method (categorical):** false

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

- **Column:** city
- **Similarity method:** embeddings
- **Clustering method:** affinity_propagation
- **Canonical selection:** llm
- **Embedding model:** text-embedding-3-small
- **Unique values before:** 21
- **Unique values after:** 6
- **Values changed:** 50

### Mappings

| Original Values | Canonical |
|-----------------|-----------|
| New York, new york, NYC, NY, New York City | New York City |
| Boston, boston, BOSTON | Boston |
| Los Angeles, LA, L.A., los angeles | Los Angeles |
| Chicago, chicago, CHICAGO | Chicago |
| Seattle, seattle, SEATTLE | Seattle |
| Denver, denver, DENVER | Denver |

---

## Postprocessing

No postprocessing changes applied.
