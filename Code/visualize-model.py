"""
The purpose of this script is to visualize the results of the model.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src import *


model_name = "diet-model_expanded"
food_data = pd.read_hdf("Data/FoodData_test.h5")
# For DEBUG purposes take a subset of the data
food_data = food_data.iloc[:100, :]

model_data = pd.read_table(f"Solutions/{model_name}-sol.dat", sep='\t', names=["Item", "Value"], skiprows=1, index_col=0)

new_index = model_data.index.tolist()
new_index = [item.replace("Food_", "") for item in new_index]
model_data.index = new_index

# PuLP also changes all spaces to underscores so we need to change them back
new_index = model_data.index.tolist()
new_index = [item.replace("_", " ") for item in new_index]
model_data.index = new_index

print(food_data["group"])

# Plot the results
# plot_expanded(f"{model_name}_visual.png", model_data, food_data)

