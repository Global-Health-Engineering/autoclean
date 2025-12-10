import pandas as pd
from Functions.Duplicates import handle_duplicates
from Functions.Outliers import handle_outliers
from Functions.Missing_Values import handle_missing_values
from Functions.Structural_Errors_Simple import handle_structural_errors_simple
from Functions.Structural_Errors_LLM import handle_structural_errors_llm

# Load data
df = pd.read_csv('Data/Test_Data.csv')
print("\n" + "=" * 200)
print("ORIGINAL DATA:")
print(df)
print("\n" + "=" * 200)


# Clean data
df = handle_duplicates(df)
df = handle_outliers(df, method='winsorize')
df = handle_missing_values(df, method_num='knn', method_categ='missforest')
df = handle_structural_errors_simple(df, 'facility_type', threshold=25)
df = handle_structural_errors_simple(df, 'water_source', threshold=25)
df = handle_structural_errors_simple(df, 'status', threshold=10)

# For semantic clustering (NYC = New York), use LLM version:
df = handle_structural_errors_llm(df, 'city', context="US city names")

print("\n" + "=" * 200)
print("CLEANED DATA:")
print(df)
print("\n" + "=" * 200)

# Save
df.to_csv('Data/Test_Data_cleaned.csv', index=False)
