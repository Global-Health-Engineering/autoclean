# AutoClean Report

**Dataset:** Diabetes Data
**Generated:** 2026-01-06 14:30:29

---

## Summary

- **Original shape:** 773 rows × 9 columns
- **After preprocessing:** 773 rows × 9 columns
- **Total rows deleted:** 5
- **Total values imputed:** 176

---

## Preprocessing

- **Columns renamed:** 9

| Original | New |
|----------|-----|
| Pregnancies | pregnancies |
| Glucose | glucose |
| BloodPressure | bloodpressure |
| SkinThickness | skinthickness |
| Insulin | insulin |
| BMI | bmi |
| DiabetesPedigreeFunction | diabetespedigreefunction |
| Age | age |
| Outcome | outcome |

---

## Duplicates

- **Duplicate rows removed:** 5

---

## Missing Values

- **Numerical missing:** 176
- **Categorical missing:** 0.0
- **Method (numerical):** knn
- **Method (categorical):** false

### Imputations

| Row | Column | New Value | Method |
|-----|--------|-----------|--------|
| 2 | pregnancies | 2.4 | knn |
| 12 | pregnancies | 2.8 | knn |
| 49 | pregnancies | 4.8 | knn |
| 69 | pregnancies | 4.6 | knn |
| 108 | pregnancies | 4.4 | knn |
| 139 | pregnancies | 3 | knn |
| 176 | pregnancies | 4.4 | knn |
| 194 | pregnancies | 2.6 | knn |
| 222 | pregnancies | 2.2 | knn |
| 223 | pregnancies | 3.6 | knn |
| 235 | pregnancies | 2.4 | knn |
| 369 | pregnancies | 3.4 | knn |
| 375 | pregnancies | 1 | knn |
| 416 | pregnancies | 4.4 | knn |
| 420 | pregnancies | 2 | knn |
| 477 | pregnancies | 6 | knn |
| 503 | pregnancies | 5 | knn |
| 635 | pregnancies | 1.8 | knn |
| 651 | pregnancies | 2 | knn |
| 673 | pregnancies | 5.8 | knn |
| ... | ... | ... | (156 more) |

---

## Postprocessing

| Column | Action |
|--------|--------|
| pregnancies | Restored to integer |
| glucose | Restored to integer |
| bloodpressure | Restored to integer |
| skinthickness | Restored to integer |
| insulin | Restored to integer |
| bmi | Rounded to 1 decimals |
| diabetespedigreefunction | Rounded to 3 decimals |
| age | Restored to integer |
| outcome | Restored to integer |
