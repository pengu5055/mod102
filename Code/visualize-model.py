"""
The purpose of this script is to visualize the results of the model.
"""
import numpy as np
import matplotlib.pyplot as plt
from src import *

# Load the model solution
model_data = pd.read_table(f"Solutions/diet-model_expanded-sol.dat", sep='\t', names=["Item", "Value"], skiprows=1, index_col=0)

new_index = model_data.index.tolist()
new_index = [item.replace("Food_", "") for item in new_index]
model_data.index = new_index

# Load the database of food items
food_data = food_data = pd.read_hdf("Data/FoodData_processed.h5")
food_data = food_data.iloc[:100, :]

print(food_data["category"])

# Plot the results
# plot_expanded("expanded-model", model_data, food_data)
