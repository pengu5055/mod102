import pandas as pd
import numpy as np

# Read in the data
df = pd.read_hdf("Data/FoodData_processed.h5")

# Reduce each list of brand_owner to a single string 
df['brand_owner'] = df['brand_owner'].apply(lambda x: x[0])

df.to_hdf("Data/FoodData_processed.h5", index=True, complevel=9, 
                              key="FoodData_processed", mode="w")