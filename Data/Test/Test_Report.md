# AutoClean Report

**Dataset:** Test Data  
**Generated:** 23.01.2026, 01:10:00

---

## Summary

- **Original shape:** 52 rows × 13 columns
- **Final shape:** 47 rows × 11 columns
- **Total rows deleted:** 5
- **Total columns deleted:** 2
- **Total values imputed:** 0
- **Total outliers handled:** 3
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

## Outliers

### Lower & Upper Bounds

| Column | Lower Bound | Upper Bound |
|--------|-------------|-------------|
| Flow Rate lps | -1.6987 | 6.7512 |

### Overview

- **Multiplier:** 1.5
- **Total outliers:** 3
- **Method:** delete
- **Rows deleted:** 3

### Outliers Handled

| Column | Original | New Value | Bound |
|--------|----------|-----------|-------|
| Flow Rate lps | 48.7 | None, deleted whole row | upper |
| Flow Rate lps | 9.2 | None, deleted whole row | upper |
| Flow Rate lps | 12.8 | None, deleted whole row | upper |

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
