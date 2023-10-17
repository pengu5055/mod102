"""
The point of this script is to read the data from the food database correctly since 
it is made up of multiple files that interlink with each other.
"""
import numpy as np
import pandas as pd

# Read the data from the files
desired_cols = ["fdc_id", "id", "nutrient_id", "amount"]
food_nutrient = pd.read_table("Data/FoodData/food_nutrient.csv", sep=',', usecols=desired_cols, index_col=1, )

desired_cols = ["fdc_id", "data_type", "description"]
food = pd.read_table("Data/FoodData/food.csv", sep=',', usecols=desired_cols, index_col=0)
# Only keep rows that are categorized as "Branded Food"
food = food[food["data_type"] == "branded_food"]
# Drop the "data_type" column
food = food.drop(columns=["data_type"])

desired_cols = ["fdc_id", "brand_owner", "branded_food_category"]
branded_food = pd.read_table("Data/FoodData/branded_food.csv", sep=',', usecols=desired_cols, index_col=0)

desired_cols = ["id", "name", "unit_name"]
nutrient = pd.read_table("Data/FoodData/nutrient.csv", sep=',', usecols=desired_cols, index_col=0)

# Load category to group mapping
with open("Data/categories-to-groups.map", "r") as f:
    raw = f.read()
    raw = raw.replace("{", "")
    raw = raw.replace("}", "")
    category_to_group = dict(raw)

print(category_to_group)
print(len(category_to_group.keys()))