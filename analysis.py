import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

import geopandas as gpd
from shapely.geometry import Polygon, Point

# how many votes does the first party in every municipio get?
with open("data/europee_clean.csv", "r") as f:
    erp = pd.read_csv(f)


max_votes_per_comune = erp.groupby(["COMUNE"])["VOTI_LISTA"].transform(max) == erp["VOTI_LISTA"]
df = erp[max_votes_per_comune].copy()
df["perc_voto"] = df["VOTI_LISTA"] / df["VOTANTI"]
print(df.columns)
first_past_post = df[["COMUNE", "perc_voto", "ELETTORI"]].copy()
print(first_past_post.head)

first_sample = first_past_post.sample(frac=0.2, weights=first_past_post["ELETTORI"]/sum(first_past_post["ELETTORI"]))
ax = first_sample.plot(x="ELETTORI", y="perc_voto", kind="scatter", logx=True)
ax.figure.savefig("plots/first_past_post.png")

# correlation
corr = first_sample[["ELETTORI", "perc_voto"]].corr(method="pearson")
print(corr)


# best two parties?
n  = 2
'''n_past_post = first_past_post
for _ in range(n-1):
    more_parties = (df[~n_past_post.isin(df[["COMUNE", "perc_voto", "ELETTORI"]])]).groupby(["COMUNE"])["VOTI_LISTA"].transform(max) \
    == df[~n_past_post.isin(df[["COMUNE", "perc_voto", "ELETTORI"]])]
    
    n_past_post = n_past_post.aggregate(more_parties)'''

max_n = lambda x: x[:n]
n_past_post = df.groupby(["COMUNE"], group_keys=True, sort=True)[["VOTI_LISTA"]].apply(max_n)
n_past_post = df[n_past_post]
print(n_past_post.columns)

n_past_post = n_past_post.groupby("COMUNE")["VOTI_LISTA"].transform(sum).drop_duplicates()
ax = n_past_post.plot(x="ELETTORI", y="perc_voto", kind="scatter", logx=True)
ax.figure.savefig("plots/top_{n}_parties.png")


''' 
take the votes taken by each candidate in each town and 
compare it with how many votes were gotten in that town,
how different is that ratio compared to the circoscrizione?

a towny candidates takes 95% of the votes in a comune, but 90% of its votes come from these comuni.
'''


## indetify towny cnadidates
with open("data/candidates_clean.csv", "r") as f:
    cndts = pd.read_csv(f)

with open("data/istat_clean.csv", "r") as f:
    cmn = pd.read_csv(f)

