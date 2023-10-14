"""
This is the starting point for my project. I will try and use PuLP to solve a
linear programming problem. The example is to solve a diet problem.
"""
from pulp import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cmasher as cmr

df = pd.read_table('table.dat', sep=',', skiprows=2, index_col=0)
df.drop(df.columns[[-1, -2]], axis=1, inplace=True)
print(df)
