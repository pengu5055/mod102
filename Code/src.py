"""
The goal of this script is to provide helper functions for the project.
Among other things, this script will contain functions for loading the model
solution and the database of food items and visualizing the results.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cmasher as cmr
from floweaver import *
import tomllib as toml


def load_model(path):
    """
    Load model solution from a file.
    Essentially this is just an alias for the pd.read_table() function.
    """
    df = pd.read_table(path, sep=',', index_col=0)
    if "Food_" in df.index.name:
        new_index = df.index.str.replace("Food_", "")
        df.index = new_index

    return df

def load_database(path):
    """
    Load the database of food items.
    Again just an alias for the pd.read_table() function.
    """
    df = pd.read_table(path, sep=',', skiprows=2, index_col=0)
    return df

def load_constraints(path):
    """
    Load the constraints from a file.
    """
    with open(path, "rb") as f:
        constraints = toml.load(f)
    return constraints

def plot_category_sankey(model_data, food_database, constraints):
    """
    
    """
    nodes = {
        "item": ProcessGroup(food_database.index),
        "full": ProcessGroup([np.sum([100 * point for point in model_data["Values"]])])
    }

    partition_data = []

    for category in food_database["Category"].unique():
        partition_data.append(Partition.Simple(category, 
                     food_database[food_database["Category"] == category].index))
        
    nodes["item"].partition = Partition.MultiLevel(*partition_data)

    ordering = [
        ["item"],
        ["category"],
        ["full"],
    ]
    
    bundles = [
        Bundle("item", "category"),
        Bundle("category", "full"),
    ]

    sdd = SankeyDefinition(nodes, bundles, ordering)
    weave(sdd, model_data).to_widget()

