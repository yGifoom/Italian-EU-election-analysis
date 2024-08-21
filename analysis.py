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


    # Assign colors to each party
party_colors = {
    'LEGA SALVINI PREMIER': '#27d93f', 
    'PARTITO DEMOCRATICO': '#e81e1e', 
    'MOVIMENTO 5 STELLE': '#facc00',  
    "FRATELLI D'ITALIA": '#a3a3a3', 
    'FORZA ITALIA': '#4557ff',  
}
for l in erp["LISTA"].unique(): 
    if l not in party_colors:
        party_colors[l] = "#000000"
        
# best m parties per circoscrizione?
m = 3
for n in range(1, m+1):


    # Map the colors to the dataframe
    erp['color'] = erp['LISTA'].map(party_colors)

    # Group by "COMUNE" and "LISTA", summing the "VOTI_LISTA"
    df_grouped = erp.groupby(["CIRCOSCRIZIONE", "PROVINCIA", 'COMUNE', 'LISTA'], as_index=False).agg({'VOTI_LISTA': 'sum', 'VOTANTI': 'first', 'color': 'first'})

    # Sort by "COMUNE" and "VOTI_LISTA" in descending order
    df_grouped = df_grouped.sort_values(['COMUNE', 'VOTI_LISTA'], ascending=[True, False])

    print(df_grouped)
    print(df_grouped.columns)
    
    # Select the top 2 parties for each comune
    df_topn = df_grouped.groupby(["CIRCOSCRIZIONE", "PROVINCIA", 'COMUNE'], as_index=False).head(n)

    print(df_topn)
    print(df_topn.columns)
    
    # Function to calculate weighted color
    def weighted_color(voti_list, colors):
        total_votes = voti_list.sum()
        weighted_rgb = [0, 0, 0]
        
        for voti, color in zip(voti_list, colors):
            color = color.lstrip('#')
            rgb = [int(color[i:i+2], 16) for i in (0, 2, 4)]
            weight = voti / total_votes
            weighted_rgb = [weighted_rgb[i] + rgb[i] * weight for i in range(3)]
        
        weighted_color_hex = '#{:02x}{:02x}{:02x}'.format(int(weighted_rgb[0]), int(weighted_rgb[1]), int(weighted_rgb[2]))
        return weighted_color_hex

    # Apply the weighted color calculation
    df_topn_grouped = df_topn.groupby(["CIRCOSCRIZIONE", "PROVINCIA", 'COMUNE'], as_index=False).agg({
        'VOTI_LISTA': 'sum', 
        'VOTANTI': 'first', 
        "color": lambda x: weighted_color(df_topn.loc[x.index, 'VOTI_LISTA'], x)})

    df_topn_grouped["perc_voti"] = df_topn_grouped["VOTI_LISTA"] / df_topn_grouped["VOTANTI"]
    
    # Get unique CIRCOSCRIZIONE values
    circoscrizioni = erp['CIRCOSCRIZIONE'].unique()

    # Determine the grid size for subplots
    n = len(circoscrizioni)
    cols = 2
    rows = (n + 1) // cols

    # Create subplots
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    axes = axes.flatten()  # Flatten in case we have more than one row

    # Plot each CIRCOSCRIZIONE
    for i, circoscrizione in enumerate(circoscrizioni):
        df_circoscrizione = df_topn_grouped[df_topn_grouped['CIRCOSCRIZIONE'] == circoscrizione]
        
        axes[i].scatter(y=df_circoscrizione['perc_voti'], x=df_circoscrizione['VOTANTI'], 
                        c=df_circoscrizione['color'], s=[10 for _ in range(len(df_circoscrizione["color"],
                        ))])
        axes[i].set_title(f'{circoscrizione}')
        axes[i].set_xscale('log')
        axes[i].set_xlabel('votanti')
        axes[i].set_ylabel('% lista maggiore')

    # Remove any empty subplots if the number of CIRCOSCRIZIONE is odd
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout(pad=5.0)
    plt.show()

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

