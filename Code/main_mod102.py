"""
This is the main script for the project (for now). Here I will try and use PuLP to solve a
linear programming problem, with some modifications to the basic.py script.
"""
from pulp import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cmasher as cmr
from src import *

# Parameters
OptFat = False
OptCost = True
Posh = False

df = pd.read_table('Data/table.dat', sep=',', skiprows=2, index_col=0)

print(df.columns.tolist())   

# Create the 'prob' variable to contain the problem data
prob = LpProblem("Diet Problem", LpMinimize)

# Create a list of the food items
food_items = list(df.index)

# Create variables. These variables are the amounts of each food item to buy
food_vars = LpVariable.dicts("Food", food_items, lowBound=0, cat='Continuous')

# Define objective function and add it to the problem
if OptFat:
    prob += lpSum([df.loc[i, 'Mascobe[g]'] * food_vars[i] for i in food_items]), "Total fat intake per person"
elif OptCost:
    prob += lpSum([df.loc[i, 'Cena[EUR]'] * food_vars[i] for i in food_items]), "Total cost of food"
else:
    prob += lpSum([df.loc[i, 'Energija[kcal]'] * food_vars[i] for i in food_items]), "Total energy intake per person"

# And now we can add the constraints
if OptFat:
    prob += lpSum([df.loc[i, 'Energija[kcal]'] * food_vars[i] for i in food_items]) >= 2000, "EnergyRequirement"
else:
    prob += lpSum([df.loc[i, 'Mascobe[g]'] * food_vars[i] for i in food_items]) >= 70, "FatRequirement"

if Posh:
    prob += lpSum([df.loc[i, 'Cena[EUR]'] * food_vars[i] for i in food_items]) >= 15, "CostRequirement"

prob += lpSum([df.loc[i, 'Ogljikovi_Hidrati[g]'] * food_vars[i] for i in food_items]) >= 310, "CarbohydrateRequirement"
prob += lpSum([df.loc[i, 'Proteini[g]'] * food_vars[i] for i in food_items]) >= 50, "ProteinRequirement"
prob += lpSum([df.loc[i, 'Ca[mg]'] * food_vars[i] for i in food_items]) >= 1000, "CalciumRequirement"
prob += lpSum([df.loc[i, 'Fe[mg]'] * food_vars[i] for i in food_items]) >= 18, "IronRequirement"

# Add additional constraints
if True:
    prob += lpSum([df.loc[i, 'Vitamin_C[mg]'] * food_vars[i] for i in food_items]) >= 60, "VitCRequirement"
    prob += lpSum([df.loc[i, 'Kalij[mg]'] * food_vars[i] for i in food_items]) >= 3500, "PotassiumRequirement"
    prob += lpSum([df.loc[i, 'Natrij[mg]'] * food_vars[i] for i in food_items]) >= 500, "SodiumLowerBound"
    prob += lpSum([df.loc[i, 'Natrij[mg]'] * food_vars[i] for i in food_items]) <= 2400, "SodiumUpperBound"

# Add mass limit
if False:
    prob += lpSum([100 * food_vars[i] for i in food_items]) <= 2000, "MassLimit"

if False:
    prob += prob.objective >= 15

model_name = "diet-model_min-eur-add"
title = "Kalorično prekomerna prehrana"
subtext = "Cost [EUR] optimization, as low as possible with additional constraints"
unit="EUR" # Of the objective function
prob.writeLP(f"Models/{model_name}.lp")

# Slove the problem
prob.solve()

# Print the status of the solution
print("Status:", LpStatus[prob.status])

# Calculate calories
if OptCost or OptFat:
    calories = 0
    for v in prob.variables():
        calories += df.loc[v.name.replace("Food_", ""), "Energija[kcal]"] * v.varValue
    print("Total calories = ", calories)
else:
    for v in prob.variables():
        print(v.name, "=", v.varValue)
    print("Total energy intake per person = ", value(prob.objective))
    calories = prob.objective

# Check if mass limit is satisfied
print("Total mass of food = ", lpSum([100 * v.varValue for v in prob.variables()]))

# Save the solution to a file with numpy
var_names = np.array([v.name for v in prob.variables()])
var_values = np.array([v.varValue for v in prob.variables()])
solution = np.column_stack((var_names, var_values))

np.savetxt(f"Solutions/{model_name}-sol.dat", solution, delimiter=",", fmt="%s", header="Item,Value")

# Visualize the model solution


# Load the model solution
model_data = load_model(f"Solutions/{model_name}-sol.dat")

# Load the database of food items
food_data = load_database("Data/table.dat")

plot_category_sankey(f"{model_name}-visual", model_data, food_data,
                     title=title, subtext=subtext, opt=prob.objective.value(),
                     unit=unit, energy=calories)

