# MissForest Imputation

## Overview

MissForest is an iterative imputation method that uses Random Forest as the prediction model. Unlike simple methods (mean, median) or distance-based methods (KNN), MissForest trains a machine learning model for each feature to predict missing values based on other features. The algorithm iterates multiple times, refining predictions with each iteration.

**Note:** MissForest only works with numerical data. Categorical columns must be encoded to numerical values first (using OrdinalEncoder), then decoded back after imputation.

## Algorithm Steps

### 1. Initialization

Fill all missing values with mean.

### 2. Iteration Loop

**For each feature with missing values:**
1. Use all other features as predictors (X)
2. Use the current feature as the target (y)
3. Train a Random Forest model with X & y
4. Predict missing values in the target feature
5. Update the dataset with new predictions

### 3. Convergence

Repeat iterations until maximum iterations (`max_iter`) reached or convergence criterion is met.

**Convergence Criterion:**

```
    max(|X_{t} - X_{t-1}|)     
    ────────────────────  < tol
    max(|X[known_vals]|)     
```

Where:
- `X_t` = Complete dataframe at current iteration
- `X_{t-1}` = Complete dataframe at previous iteration  
- `X[known_vals]` = Original dataframe with all non-missing values
- `tol` = tolerance (default: 0.001 = 0.1%)

**What this means:**
- **Numerator**: Maximum absolute change in any value between iterations
- **Denominator**: Maximum absolute value from original dataframe with all non-missing values
- **Result**: Relative change normalized by data scale

---

## Example

### Dataset

```
     pH  turbidity  temperature
0   7.2       15.0         25.0   ✓ Complete
1   6.8       20.0         28.0   ✓ Complete
2   NaN       18.0         26.0   ← Missing pH
3   7.5        NaN         27.0   ← Missing turbidity
4   6.9       22.0          NaN   ← Missing temperature
```

**Note:** This dataset has only numerical features. If categorical features existed, they would be encoded first.

---

### INITIALIZATION

Fill all NaN with column means:

```
     pH  turbidity  temperature
0   7.2       15.0         25.0
1   6.8       20.0         28.0
2   7.1       18.0         26.0   ← Mean: (7.2+6.8+7.5+6.9)/4 = 7.1
3   7.5       18.75        27.0   ← Mean: (15+20+18+22)/4 = 18.75
4   6.9       22.0         26.5   ← Mean: (25+28+26+27)/4 = 26.5
```

---

### ITERATION 1

#### Step 1: Impute pH column

**Training data** (rows where pH was originally present):
```
Features:                          Target:
[turbidity, temp]             →    [pH]
[15.0, 25.0]                  →    7.2
[20.0, 28.0]                  →    6.8
[18.75, 27.0]                 →    7.5
[22.0, 26.5]                  →    6.9
```

**Train Random Forest:** Learn relationship `pH = f(turbidity, temperature)`

**Predict** for Row 2 (originally missing pH):
```
Input: [turbidity=18, temperature=26]
Random Forest prediction: pH ≈ 7.2
```

**Update** Row 2: pH = 7.2 (improved from initial 7.1)

---

#### Step 2: Impute turbidity column

**Training data** (rows where turbidity was originally present):
```
Features:                          Target:
[pH, temp]                    →    [turbidity]
[7.2, 25.0]                   →    15.0
[6.8, 28.0]                   →    20.0
[7.2, 26.0]                   →    18.0  ← Uses updated pH from Step 1!
[6.9, 26.5]                   →    22.0
```

**Train Random Forest:** Learn relationship `turbidity = f(pH, temperature)`

**Predict** for Row 3 (originally missing turbidity):
```
Input: [pH=7.5, temperature=27]
Random Forest prediction: turbidity ≈ 20.0
```

**Update** Row 3: turbidity = 20.0 (improved from initial 18.75)

---

#### Step 3: Impute temperature column

**Training data** (rows where temperature was originally present):
```
Features:                          Target:
[pH, turbidity]               →    [temperature]
[7.2, 15.0]                   →    25.0
[6.8, 20.0]                   →    28.0
[7.2, 18.0]                   →    26.0  ← Uses updated pH from Step 1!
[7.5, 20.0]                   →    27.0  ← Uses updated turbidity from Step 2!
```

**Train Random Forest:** Learn relationship `temperature = f(pH, turbidity)`

**Predict** for Row 4 (originally missing temperature):
```
Input: [pH=6.9, turbidity=22]
Random Forest prediction: temperature ≈ 27.5
```

**Update** Row 4: temperature = 27.5 (improved from initial 26.5)

---

**End of Iteration 1:**
```
     pH  turbidity  temperature
0   7.2       15.0         25.0
1   6.8       20.0         28.0
2   7.2       18.0         26.0   ← Updated pH from 7.1
3   7.5       20.0         27.0   ← Updated turbidity from 18.75
4   6.9       22.0         27.5   ← Updated temperature from 26.5
```

---

### ITERATION 2

Repeat the same process with improved values from Iteration 1.

Values refine slightly: pH 7.2 → 7.18, etc.

---

### ITERATION 3+

Continue iterating until:
- Maximum iterations reached (`max_iter`) 

- Changes become very small (convergence criterion is met)

---

### Final Result

```
     pH  turbidity  temperature
0   7.2       15.0         25.0
1   6.8       20.0         28.0
2   7.2       18.0         26.0   ← Imputed with ML!
3   7.5       20.0         27.0   ← Imputed with ML!
4   6.9       22.0         27.5   ← Imputed with ML!
```

**Note:** If MissForest is used for missing values of (selected) categorical columns, those (selected) categorical columns would be decoded back to text after imputation. 

---

