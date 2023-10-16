"""
This is the main script for the project (for now). Here I will try and use PuLP to solve a
linear programming problem, with some modifications to the basic.py script.
"""
from pulp import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cmasher as cmr

df = pd.read_table('table.dat', sep=',', skiprows=2, index_col=0)

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Diet Problem", LpMinimize)

# Create a list of the food items
food_items = list(df.index)

# Create variables. These variables are the amounts of each food item to buy
food_vars = LpVariable.dicts("Food", food_items, lowBound=0, cat='Continuous')

# Define objective function and add it to the problem
prob += lpSum([df.loc[i, 'Energija[kcal]'] * food_vars[i] for i in food_items]), "Total energy intake per person"

# And now we can add the constraints
prob += lpSum([df.loc[i, 'Mascobe[g]'] * food_vars[i] for i in food_items]) >= 70, "FatRequirement"
prob += lpSum([df.loc[i, 'Ogljikovi_Hidrati[g]'] * food_vars[i] for i in food_items]) >= 310, "CarbohydrateRequirement"
prob += lpSum([df.loc[i, 'Proteini[g]'] * food_vars[i] for i in food_items]) >= 50, "ProteinRequirement"
prob += lpSum([df.loc[i, 'Ca[mg]'] * food_vars[i] for i in food_items]) >= 1000, "CalciumRequirement"
prob += lpSum([df.loc[i, 'Fe[mg]'] * food_vars[i] for i in food_items]) >= 18, "IronRequirement"
# Mass limit where the table data is nutritional value per 100g
prob += lpSum([100 * food_vars[i] for i in food_items]) <= 2000, "MassLimit"

model_name = "diet-model_basic.lp"
prob.writeLP(f"Models/{model_name}")

# Slove the problem
prob.solve()

# Print the status of the solution
print("Status:", LpStatus[prob.status])

# Print the optimal solution
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total energy intake per person = ", value(prob.objective))

# Check if mass limit is satisfied
print("Total mass of food = ", lpSum([100 * v.varValue for v in prob.variables()]))

# Save the solution to a file with numpy
var_names = np.array([v.name for v in prob.variables()])
var_values = np.array([v.varValue for v in prob.variables()])
solution = np.column_stack((var_names, var_values))

np.savetxt(f"Solutions/{model_name}-sol.dat", solution, delimiter=",", fmt="%s", header="Variable,Value")

