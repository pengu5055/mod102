"""
After 6 hours of waiting for data to preprocess, I think it's time to
parallelize the code. This is essentially a rewrite of preprocess-food-data.py

In basic principle all nodes can load the helper data but only one instance of 
food_nutrient should be loaded. This should then be split into chunks and 
distributed to the nodes. 

"""
import numpy as np
import pandas as pd
from mpi4py import MPI
import socket

# Helper functions
def most_frequent(List):
    """
    Finds the most frequent element in a list.
    """
    return max(set(List), key = List.count)


# Setup MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
status = MPI.Status()
name = MPI.Get_processor_name()
hostname = socket.gethostname()

print(f"Hi! This is rank {rank} on {hostname}. Ready to go to work...")


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

# NOTE: THIS IS HERE FOR DEBUGGING PURPOSES
# food_nutrient = food_nutrient.iloc[:100, :]

# ---- Split and distribute the data ----
# Split the data into chunks
full_size = len(food_nutrient.index)
chunk_size = full_size // size
remainder = full_size % size

# Reserve memory for the chunk indices
chunk_indices = np.empty(size * 100, dtype=tuple)

if rank == 0:
    # Create a list of the chunk sizes
    chunk_sizes = [chunk_size] * size
    
    # This will never go out of range, since the
    # extra rows cannot be more than the number of nodes.
    for i in range(remainder):
        chunk_sizes[i] += 1
    
    # Then create a list of the pairs of indices that define the chunks
    chunk_indices = []
    start = 0
    for i in range(size):
        end = start + chunk_sizes[i]
        chunk_indices.append((start, end))
        start = end

chunk_indices = comm.bcast(chunk_indices, root=0)

print(f"Rank {rank} has indices {chunk_indices[rank]}")

quit()

# food_nutrient codes to nutrient names
food_nutrient["nutrient_id"] = food_nutrient["nutrient_id"].map(nutrient["name"])

# Add column with brand owner
food_nutrient["brand_owner"] = food_nutrient.index.map(branded_food["brand_owner"])

# food_nutrient codes to food names
food_nutrient.index = food_nutrient.index.map(food["description"])

# Also do the same for the branded_food DataFrame
branded_food.index = branded_food.index.map(food["description"])

# Now gather all duplications of the id column and append the nutrient_id and amount columns
food_nutrient = food_nutrient.groupby(food_nutrient.index).agg({"nutrient_id": lambda x: list(x), "amount": lambda x: list(x), "brand_owner": lambda x: list(x)})

# Now for each row create columns for each nutrient_id and amount
# First we need to find all unique nutrient_ids
unique_nutrient_ids = np.unique(np.array([item for sublist in food_nutrient["nutrient_id"].tolist() for item in sublist]))

# It is necessary to use DataFrame operations since the data is so massive
# First create a DataFrame of zeros
food_nutrient_expanded = pd.DataFrame(0.0, index=food_nutrient.index, columns=[*unique_nutrient_ids, "group"])

# Now fill the DataFrame with the values from the food_nutrient DataFrame
for i, row in food_nutrient.iterrows():
    for nutrient_id, amount in zip(row["nutrient_id"], row["amount"]):
        food_nutrient_expanded.loc[i, nutrient_id] = amount
    
    # Since we're already iterating, swap category with group

    # Since database input is stupid values are NOT UNIQUE check if there
    # are multiple categories and if so take the most frequent one
    try:
        group = branded_food.loc[i, "branded_food_category"].tolist()
        if len(group) > 1:
            group = most_frequent(group)
    
    except AttributeError:
        pass
    
    # It is possible that the category is not in the category_to_group.map file
    # which is strange but would mean that OpenAI did not correctly categorize 
    try: 
        # Explicitly cast to string so DataFrame switches to object type
        food_nutrient_expanded.loc[i, "group"] = str(group)
    
    except NameError:
        food_nutrient_expanded.loc[i, "group"] = str("Unknown")

# Now add the brand_owner column but only keep the first value
food_nutrient_expanded["brand_owner"] = food_nutrient["brand_owner"].apply(lambda x: x[0])

# Set the index name to "Item"
food_nutrient_expanded.index.name = "Item"

# Now we can save the DataFrame to a file
food_nutrient_expanded.to_hdf("Data/FoodData_test.h5", index=True, complevel=9, 
                              key="food_nutrient_expanded", mode="w")