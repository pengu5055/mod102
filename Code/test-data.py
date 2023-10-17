import pandas as pd
import numpy as np

# Read in the data
food_data = pd.read_hdf("Data/FoodData_processed.h5")

print(food_data.head())