import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

import geopandas as gpd
from shapely.geometry import Polygon, Point

# how many votes does the first party in every municipio get?
with open("data/europee_clean.csv", "r") as f:
    erp = pd.read_csv(f)
with open("data/istat_clean.csv", "r") as f:
    cmn = pd.read_csv(f)


max_votes_per_comune = erp.groupby(["COMUNE"])["VOTI_LISTA"].transform(max) == erp["VOTI_LISTA"]
df = erp[max_votes_per_comune].copy()
df["perc_voto"] = df["VOTI_LISTA"] / df["VOTANTI"]
print(df.columns)

first_past_post = df[["COMUNE", "perc_voto", "ELETTORI"]].copy()
print(first_past_post.head)

first_sample = first_past_post.sample(frac=0.2, weights=first_past_post["ELETTORI"]/sum(first_past_post["ELETTORI"]))
ax = first_past_post.plot(x="ELETTORI", y="perc_voto", kind="scatter", logx=True)
ax.figure.savefig("plots/first_past_post.png")

# correlation
corr = first_sample[["ELETTORI", "perc_voto"]].corr(method="pearson")
print(corr)


# best n parties?
m = 10
for n in range(1, m):
    # Sort the dataframe by "comune" and "voti" in descending order
    df_grouped = erp.sort_values(by=['COMUNE', 'VOTI_LISTA'], ascending=[True, False])

    # Select the top 2 parties for each comune
    df_top2 = df_grouped.groupby(['COMUNE', "PROVINCIA"]).head(n)

    # Sum the votes of the top 2 parties for each comune
    df_result = df_top2.groupby(['COMUNE', "PROVINCIA"]).agg({'VOTI_LISTA': 'sum', 'VOTANTI': 'first'}).reset_index()
    df_result["perc_voto"] = df_result["VOTI_LISTA"] / df_result["VOTANTI"]
    print(df_result)

    df_final = pd.merge(df_result, cmn[["COMUNE", "SHAPE_AREA"]], on='COMUNE', how='left')
    
    res = df_final[df_final["SHAPE_AREA"] > 1]
    
    ax = res.plot(x="VOTANTI", y="perc_voto", kind="scatter", logx=True)
    ax.figure.savefig(f"plots/top_{n}_partiesV.png")
    
    
    ax = res.plot(x="SHAPE_AREA", y="perc_voto", kind="scatter", logx=True)
    ax.figure.savefig(f"plots/top_{n}_partiesA")
    
    res["DENSITY"] = res["VOTANTI"]/res["SHAPE_AREA"]
    ax = res.plot(x="DENSITY", y="perc_voto", kind="scatter", logx=True)
    ax.figure.savefig(f"plots/top_{n}_partiesD")

# how are the votes distributed in comuni with different area?

''' 
take the votes taken by each candidate in each town and 
compare it with how many votes were gotten in that town,
how different is that ratio compared to the circoscrizione?

a towny candidates takes 95% of the votes in a comune, but 90% of its votes come from these comuni.
'''


## indetify towny cnadidates
with open("data/candidates_clean.csv", "r") as f:
    cndts = pd.read_csv(f) 

