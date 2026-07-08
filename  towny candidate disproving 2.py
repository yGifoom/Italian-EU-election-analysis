import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import csv
import seaborn as sns

with open("data/provinces_votes.csv", "r") as f:
    pref = pd.read_csv(f)
    
appetibili = pref[pref["0"] < 0.4]

print(appetibili)
print(len(appetibili["0"]))