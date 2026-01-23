# AutoClean Report

**Name of dataset:** Test Data (made up WHASH dataset)  
**Filepath of messy dataset:** Data/Test/Test.csv  
**Filepath of cleaned dataset:** Data/Test/Test_Cleaned.csv  
**Generated:** 24.01.2026, 00:28:56

---

## Summary

- **Original shape:** 52 rows × 13 columns
- **Final shape:** 50 rows × 11 columns
- **Total rows deleted:** 2
- **Total columns deleted:** 2
- **Total values imputed:** 0
- **Total outliers handled:** 0
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
