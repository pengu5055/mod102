"""
The purpose of this script is to visualize the results of the model.
"""
import numpy as np
import matplotlib.pyplot as plt
from src import *

# Load the model solution
model_data = load_model("Solutions/diet-model_basic.lp-sol.dat")

# Load the database of food items
food_database = load_database("Data/table.dat")

# Load the constraints
constraints = load_constraints("Data/basic_con.toml")

# Plot the results
plot_category_sankey(model_data, food_database, constraints)
