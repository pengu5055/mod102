"""
Now using a large scale model!
"""
import numpy as np
import matplotlib.pyplot as plt
from src import *
from pulp import *
import pandas as pd
import cmasher as cmr

food_data = food_data = pd.read_hdf("Data/FoodData_processed.h5")

# For DEBUG purposes take a subset of the data
food_data = food_data.iloc[:100, :]

# This is how you remember all these columns
# print(food_data.columns.tolist())

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Diet Problem", LpMinimize)

# Create a list of the food items
food_items = list(food_data.index)

# Create variables. These variables are the amounts of each food item to buy
food_vars = LpVariable.dicts("Food", food_items, lowBound=0, cat='Continuous')

# Define objective function and add it to the problem
prob += lpSum([food_data.loc[i, 'Energy'] * food_vars[i] for i in food_items]), "Total energy intake per person"

# And now we can add the constraints
prob += lpSum([food_data.loc[i, 'Fatty acids, total monounsaturated'] + \
               food_data.loc[i, 'Fatty acids, total polyunsaturated'] + \
               food_data.loc[i, 'Fatty acids, total saturated'] * \
               food_vars[i] for i in food_items]) >= 70, "FatRequirement"
prob += lpSum([food_data.loc[i, 'Carbohydrate, by difference'] +\
               food_data.loc[i, 'Carbohydrate, other'] *\
               food_vars[i] for i in food_items]) >= 310, "CarbohydrateRequirement"
prob += lpSum([food_data.loc[i, 'Protein'] * food_vars[i] for i in food_items]) >= 50, "ProteinRequirement"
prob += lpSum([food_data.loc[i, 'Calcium, Ca'] * food_vars[i] for i in food_items]) >= 1000, "CalciumRequirement"
prob += lpSum([food_data.loc[i, 'Iron, Fe'] * food_vars[i] for i in food_items]) >= 18, "IronRequirement"

# Mass limit where the table data is nutritional value per 100g
prob += lpSum([100 * food_vars[i] for i in food_items]) <= 2000, "MassLimit"

model_name = "diet-model_expanded"
prob.writeLP(f"Models/{model_name}.lp")

# Moving to cluster computing enabled solver will is practically
# a necessity. The default solver is too slow.
quit()

# Slove the problem
prob.solve()

# Print the status of the solution
# print("Status:", LpStatus[prob.status])

# Print the optimal solution
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total energy intake per person = ", value(prob.objective))

# Save the solution to a file with numpy
var_names = np.array([v.name for v in prob.variables()])
var_values = np.array([v.varValue for v in prob.variables()])
solution = np.column_stack((var_names, var_values))

np.savetxt(f"Solutions/{model_name}-sol.dat", solution, delimiter="\t", fmt="%s", header="Item,Value")
