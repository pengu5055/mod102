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
# category_to_group = pd.read_table("Data/categories-to-groups.map", sep=',', index_col=0).to_dict()

# print(category_to_group)
# print(len(category_to_group.keys()))

# Now replace the category names with the group names
# branded_food["branded_food_category"] = branded_food["branded_food_category"].map(category_to_group)

# food_nutrient codes to nutrient names
food_nutrient["nutrient_id"] = food_nutrient["nutrient_id"].map(nutrient["name"])

# Combine the dataframes into one master dataframe where all data is interpreted:
#   For each item in food we need to check for each nutrient in food_nutrient and add it as a column
#   to the food dataframe. We also add the category and brand owner to the food dataframe.

print(food_nutrient.head())