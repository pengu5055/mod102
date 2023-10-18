import pandas as pd
import numpy as np

# Read in the data
df = pd.read_hdf("Data/FoodData_test.h5")

print(df.head())

print(df.shape)

