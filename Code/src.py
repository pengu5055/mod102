"""
The goal of this script is to provide helper functions for the project.
Among other things, this script will contain functions for loading the model
solution and the database of food items and visualizing the results.
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cmasher as cmr
import holoviews as hv
from holoviews import dim, opts
import tomllib as toml

hv.extension('matplotlib')
hv.output(fig='png')


def most_frequent(List):
    """
    Finds the most frequent element in a list.
    """
    return max(set(List), key = List.count)


def load_model(path):
    """
    Load model solution from a file.
    Essentially this is just an alias for the pd.read_table() function.
    """
    df = pd.read_table(path, sep=',', names=["Item", "Value"], skiprows=1, index_col=0)

    new_index = df.index.tolist()
    new_index = [item.replace("Food_", "") for item in new_index]
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


def plot_category_sankey(output_filename, model_data, food_database, title="",
                         subtext="", opt=0, unit="g", energy=0):
    """
    
    """ 
    # Add nodes where value is non-zero
    model_data_select = model_data[model_data["Value"] > 0]

    # For given item name find category in food database
    categories = np.unique(np.array([food_database.loc[item, "Category"] for item in model_data_select.index.tolist()]))

    categories_mass = np.zeros(len(categories))
    # Calculate the total mass of each category
    for i, category in enumerate(categories):
        # Get all items in the category
        items = [item for item in model_data_select.index.tolist() if food_database.loc[item, "Category"] == category]
        
        # Calculate the total mass that each item contributes to the category
        mass = np.sum(np.array([100 * model_data_select.loc[item, "Value"] for item in items]))

        categories_mass[i] = mass

    food_items = model_data_select.index.tolist()
    nodes_in = np.array(["Full diet", *categories, *food_items])
    nodes = hv.Dataset(enumerate(nodes_in), 'index', 'label')

    edges_lyr1 = [
        (0, i + 1, categories_mass[i]) for i in range(len(categories))
    ]

    edges_lye2 = []
    for i, category in enumerate(categories):
        items = [item for item in model_data_select.index.tolist() if food_database.loc[item, "Category"] == category]
        for item in items:
            edges_lye2.append((i + 1, list(nodes_in).index(item) , 100 * model_data_select.loc[item, "Value"]))

    edges = [*edges_lyr1, *edges_lye2]

    value_dim = hv.Dimension('Weight', label='Weight', unit='g')

    fig = hv.Sankey((edges, nodes), ['From', 'To'], vdims=value_dim).opts(
        opts.Sankey(cmap="kgy", labels="label", label_position='right',
                     edge_color=dim('To').str(), fig_size=700, label_text_font_size='22',
                     node_color=dim('index').str(), )
    ) * hv.Text(550, -70, subtext, color="gray", fontsize=28) * \
        hv.Text(550, -100, f"Minimized quantity: {round(opt, 3)} {unit}", color="gray", fontsize=26) * \
        hv.Text(550, -130, f"Total calories: {round(energy ,3)} kcal", color="gray", fontsize=26)
    

    fig.opts(opts.Overlay(title=title, fontsize=36))

    hv.save(fig, f"Images/{output_filename}.png", dpi=700)


def plot_expanded(output_filename, model_data, food_database):
    """
    
    """ 
    # Add nodes where value is non-zero
    model_data_select = model_data[model_data["Value"] > 0]

    # For given item name find group in food database
    categories = np.unique(np.array([food_database.loc[item, "group"] for item in model_data_select.index.tolist()]))

    categories_mass = np.zeros(len(categories))
    # Calculate the total mass of each group
    for i, group in enumerate(categories):
        # Get all items in the group
        items = [item for item in model_data_select.index.tolist() if food_database.loc[item, "group"] == group]
        
        # Calculate the total mass that each item contributes to the group
        mass = np.sum(np.array([100 * model_data_select.loc[item, "Value"] for item in items]))

        categories_mass[i] = mass

    food_items = model_data_select.index.tolist()
    nodes_in = np.array(["Full diet", *categories, *food_items])
    nodes = hv.Dataset(enumerate(nodes_in), 'index', 'label')

    edges_lyr1 = [
        (0, i + 1, categories_mass[i]) for i in range(len(categories))
    ]

    edges_lye2 = []
    for i, group in enumerate(categories):
        items = [item for item in model_data_select.index.tolist() if food_database.loc[item, "group"] == group]
        for item in items:
            edges_lye2.append((i + 1, list(nodes_in).index(item) , 100 * model_data_select.loc[item, "Value"]))

    edges = [*edges_lyr1, *edges_lye2]

    print(edges)
    #+ [
    #    (len(model_data.index) + i, len(model_data.index) + len(categories)) for i in range(len(model_data.index))
    #]

    value_dim = hv.Dimension('Weight', label='Weight', unit='g')

    fig = hv.Sankey((edges, nodes), ['From', 'To'], vdims=value_dim).opts(
        opts.Sankey(cmap="bmy", labels="label", label_position='right',
                     edge_color=dim('To').str(), fig_size=700, label_text_font_size='22',
                     node_color=dim('index').str(), )
    )


    hv.save(fig, f"Images/{output_filename}.png", dpi=700)