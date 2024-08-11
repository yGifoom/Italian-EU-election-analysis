import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

import geopandas as gpd
from shapely.geometry import Polygon, Point

    
''' 
take the votes taken by each candidate in each town and 
compare it with how many votes were gotten in that town,
how different is that ratio compared to the circoscrizione?

a towny candidates takes 95% of the votes in a comune, but 90% of its votes come from these comuni.
'''


## indetify towny cnadidates
with open("data/candidates_clean.csv", "r") as f:
    cndts = pd.read_csv(f)
with open("data/europee_clean.csv", "r") as f:
    erp = pd.read_csv(f)
with open("data/istat_clean.csv", "r") as f:
    cmn = pd.read_csv(f)
print(cndts.head)

# TODO: find towny candidates