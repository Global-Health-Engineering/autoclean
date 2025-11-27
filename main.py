# Imported libraries & functions
import pandas as pd
from Functions.Duplicates import handle_duplicates
from Functions.Outliers import handle_outliers
#from Functions.Missing_Values import handle_missing_values

# Load the data
test_data_unclean = pd.read_csv("Data/Test_Data.csv")

# Test duplicates function
#test_data_clean = handle_outliers(test_data_unclean)
