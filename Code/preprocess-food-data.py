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
desired_cols = ["category", "group"]
category_to_group = pd.read_table("Data/categories-to-groups.map", sep='\t\t', names=["category", "group"], index_col=0)

# Pair the category names with the group names
category_to_group_map = category_to_group.to_dict()["group"]

# Now replace the category names with the group names
branded_food["branded_food_category"] = branded_food["branded_food_category"].replace(category_to_group_map)

# food_nutrient codes to nutrient names
food_nutrient["nutrient_id"] = food_nutrient["nutrient_id"].map(nutrient["name"])

# Add column with brand owner
food_nutrient["brand_owner"] = food_nutrient.index.map(branded_food["brand_owner"])

# food_nutrient codes to food names
food_nutrient.index = food_nutrient.index.map(food["description"])

# Now gather all duplications of the id column and append the nutrient_id and amount columns
food_nutrient = food_nutrient.groupby(food_nutrient.index).agg({"nutrient_id": lambda x: list(x), "amount": lambda x: list(x), "brand_owner": lambda x: list(x)})

print(food_nutrient.head())