"""
The goal of this script is to provide helper functions for the project.
Among other things, this script will contain functions for loading the model
solution and the database of food items and visualizing the results.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cmasher as cmr
import plotly.graph_objects as go

def load_model(path):
    """
    Load model solution from a file.
    Essentially this is just an alias for the pd.read_table() function.
    """
    df = pd.read_table(path, sep=',', skiprows=1, index_col=0)
    if "Food_" in df.index.name:
        new_index = df.index.str.replace('Food_', '')
        df.index = new_index

    return df

def load_database(path):
    """
    Load the database of food items.
    Again just an alias for the pd.read_table() function.
    """
    df = pd.read_table(path, sep=',', skiprows=2, index_col=0)
    return df

def plot_category_sankey(model_data, food_database):
    """
    
    """
    fig = go.Figure(data=[go.Sankey(
        node = dict(
            pad = 15,
            thickness = 20,
            line = dict(color = "black", width = 0.5),
            label = model_data.index,
            color = "blue"
        ),

        link = dict(
            source = model_data.index,
            target = food_database['Category'],
            value = model_data['Value']
        ))])

    fig.update_layout(title_text="Basic diet plan", font_size=12)
    fig.show()

