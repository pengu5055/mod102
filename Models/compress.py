import numpy as np
from pulp import *
import tables
from contextlib import closing

with open("Models/diet-model_expanded.lp", "r") as f:
    data = np.array(f.readlines())

# This would load the model from a file
# prob = LpProblem.from_dict(data)

FILTERS = tables.Filters(complib='zlib', complevel=9)

# Compress it for storage in HDF5
with closing(tables.open_file("Models/diet-model_expanded.h5", mode="w", filters=FILTERS)) as hdf:
    hdf.create_array("/", "model", data)


# NOTE: DO NOT USE THIS SCRIPT: IT PRODUCES A 1GB FILE FROM 100MB OF DATA