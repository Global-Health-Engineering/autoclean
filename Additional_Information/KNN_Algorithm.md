# K-Nearest Neighbors (KNN) Imputation

## Overview

K-Nearest Neighbors (KNN) imputation is a method for filling missing values based on the similarity between data samples. For each missing value, KNN finds the K most similar samples (neighbors) and imputes the missing value using the average of the neighbors values.

**Note:** KNN only works with numerical data. Categorical columns must be encoded to numerical values first (using OrdinalEncoder), then decoded back after imputation. Further to improve KNN, the numerical columns are standardized (mean = 0, standard deviation = 1) before applying KNN and obviosly after imputation restored again. 

## Algorithm Steps

### 1. Distance Calculation

For each sample with a missing value, calculate the distance to all other samples using only the **features where both samples have values**, i.e. ≠ NaN. 

**Distance metric**: `nan_euclidean` (Euclidean distance that handles NaN)

```
distance = √(Σ(xi - yi)²)
```

where the sum is only over features where both x and y are not NaN.

### 2. Find K Nearest Neighbors

Identify the K samples with the smallest distances.

### 3. Impute Missing Value

Replace the missing value with the **mean** of the K neighbors values for that feature.

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

### Task 1: Fill pH in Row 2 (K=2)

**Row 2 has**: turbidity=18, temperature=26

#### Step 1: Calculate distances to all rows

**Row 2 vs Row 0:**
- Common features: turbidity, temperature
- Distance = √[(18-15)² + (26-25)²] = √[9+1] = **√10 = 3.16**

**Row 2 vs Row 1:**
- Common features: turbidity, temperature
- Distance = √[(18-20)² + (26-28)²] = √[4+4] = **√8 = 2.83**

**Row 2 vs Row 3:**
- Common features: temperature only (Row 3 missing turbidity!)
- Distance = √[(26-27)²] = **1.0**

**Row 2 vs Row 4:**
- Common features: turbidity only (Row 4 missing temperature!)
- Distance = √[(18-22)²] = **4.0**

#### Step 2: Find 2 nearest neighbors

Sorted distances:
1. Row 3: distance = 1.0 ✓ (nearest)
2. Row 1: distance = 2.83 ✓ (second nearest)
3. Row 0: distance = 3.16
4. Row 4: distance = 4.0

**K=2 nearest neighbors**: Row 3 and Row 1

#### Step 3: Impute missing pH

```
Imputed pH = (pH of Row 3 + pH of Row 1) / 2
           = (7.5 + 6.8) / 2
           = 7.15
```

---

### Task 2: Fill temperature in Row 4 (K=2)

**Row 4 has**: pH=6.9, turbidity=22

#### Step 1: Calculate distances to all rows

**Row 4 vs Row 0:**
- Common features: pH, turbidity
- Distance = √[(6.9-7.2)² + (22-15)²] = √[0.09+49] = **√49.09 = 7.01**

**Row 4 vs Row 1:**
- Common features: pH, turbidity
- Distance = √[(6.9-6.8)² + (22-20)²] = √[0.01+4] = **√4.01 = 2.00**

**Row 4 vs Row 2:**
- Common features: turbidity only (Row 2 missing pH!)
- Distance = √[(22-18)²] = **4.0**

**Row 4 vs Row 3:**
- Common features: pH only (Row 3 missing turbidity!)
- Distance = √[(6.9-7.5)²] = **0.6**

#### Step 2: Find 2 nearest neighbors

Sorted distances:
1. Row 3: distance = 0.6 ✓ (nearest)
2. Row 1: distance = 2.00 ✓ (second nearest)
3. Row 2: distance = 4.0
4. Row 0: distance = 7.01

**K=2 nearest neighbors**: Row 3 and Row 1

#### Step 3: Impute missing temperature

```
Imputed temperature = (temperature of Row 3 + temperature of Row 1) / 2
                    = (27 + 28) / 2
                    = 27.5
```
---

### Task 3: Fill turbidity in Row 3 (K=2)

Analog steps as in Task 1 & 2 are being taken, which yields to an imputed turbidity of 21.0. 

---

### Final Result

```
     pH  turbidity  temperature
0   7.2       15.0         25.0
1   6.8       20.0         28.0
2   7.15      18.0         26.0   ← pH filled!
3   7.5       21.0         27.0   ← turbidity filled!
4   6.9       22.0         27.5   ← temperature filled!
```

**Note:** As it can be seen in the example, all missing values are filled simultaneously. This means that for example in task 2 the imputed pH value of task 1 is not used as a known feature and still treated as NaN. 

---

