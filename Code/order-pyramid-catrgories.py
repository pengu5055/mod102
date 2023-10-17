"""
The aim here is to reduce the number of categories in the food database from 429
to a more manageable number of 12
"""
import numpy as np
import pandas as pd
import os
import openai
import json

# OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Read the data from the files
CATEGORIES = [
    "Grains",
    "Milk and milk products",
    "Fruit and frit products",
    "Eggs",
    "Meat and poultry",
    "Fish/shellfish",
    "Vegetables",
    "Fats/oils",
    "Legumes/nuts/seeds",
    "Sugar and sugar products",
    "Non-alcoholic beverages",
    "Alcoholic beverages",
]

# Load the data from the files
desired_cols = ["fdc_id", "brand_owner", "branded_food_category"]
branded_food = pd.read_table("Data/FoodData/branded_food.csv", sep=',', usecols=desired_cols, index_col=0)

# Now we need to somehow map the 429 categories to the 12 categories
unique_categories = branded_food["branded_food_category"].unique()

request = {
    "content": f"""
The following is a list of the 429 categories in the food database. 
The aim is to reduce the number of categories to a more manageable number of 12. 
The new categories should be as follows:

Grains
Milk and milk products
Fruit and fruit products
Eggs
Meat and poultry
Fish/shellfish
Vegetables
Fats/oils
Legumes/nuts/seeds
Sugar and sugar products (for example, chocolate, candy, cookies, desserts, etc.)
Non-alcoholic beverages
Alcoholic beverages
Miscellaneous (for example, spices, condiments, sauces, etc.)
Strange (backup category for items that do not fit into any of the above categories, try to avoid this category)
                  
Map the 429 categories to the 12 categories. You are NOT allowed to make up any more categories
than the ones I've given you. Make sure that each category is mapped to exactly one of the 12 
categories. The mapping should be a Python dictionary with the 429 categories as keys and the 12 
categories as values. For example anything related to Desserts should be mapped to the category
"Sugar and sugar products". 

Here is the list of 429 categories:

{unique_categories.tolist()}
                
""",
    "role": "system",
}

print("Sending request to OpenAI API...")
if True:
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k", messages=[request])
else:
    f = open("Data/FoodData/response.json", "r")
    completion = json.load(f)

print("Saving response to .json file...")
with open("Data/response.json", "w") as f:
    json.dump(completion, f) 

# Print the response
print(completion["choices"][0]["message"]["content"])

# Save the response to a file
print("Saving response text to file...")
with open("Data/categories-to-groups.map", "w") as f:
    f.write(completion["choices"][0]["message"]["content"])

print("Done.")

f.close()