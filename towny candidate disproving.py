import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import csv

with open("data/preferences_clean.csv", "r") as f:
    pref = pd.read_csv(f)
with open("data/europee_clean.csv", "r") as f:
    voti = pd.read_csv(f)
    
# gather not elected candidates and sum their preferences
pref_non_e = pref[pref["CODTIPOELETTO"] == "N"]
pool_pref = pref_non_e.groupby(["circoscrizione"], as_index=False)["PREFERENZE"].sum()

# calculate lower bound for votes (at most 3 preferences per vote)
low_votes = pref_non_e.groupby(["circoscrizione"], as_index=False)["PREFERENZE"].agg(
    {
        "PREFERENZE": lambda x: sum([y//3 for y in x]) # can find better model counting the party it comes from
    }
)

pool_pref = pd.DataFrame(pool_pref).merge(low_votes, on=["circoscrizione"])

# by party
dict_for_df = {
    "lista": pref["descrlista"].unique(),
    }

circoscrizioni = voti["CIRCOSCRIZIONE"].unique()
    
df = pd.DataFrame(dict_for_df)
for c in circoscrizioni:
    circ_preferenze = pref_non_e[pref_non_e["circoscrizione"] == c]
    res = pd.DataFrame(circ_preferenze.groupby("descrlista", as_index=False)["PREFERENZE"].sum())
    
    df[c] = res["PREFERENZE"]
    
print(df)
print(res.columns)

for i in df["lista"]:
    if i not in pref[pref["CODTIPOELETTO"] == "E"]["descrlista"].unique():
        df = df.drop(df[df['lista'] == i].index).reset_index(drop = True)


##########################################################
# votanti tot per comune
tot_voti = voti.groupby(["CIRCOSCRIZIONE", "PROVINCIA", "COMUNE", "VOTANTI"], as_index=False).agg({
    "CIRCOSCRIZIONE": "first",
    "PROVINCIA":"first", 
    "COMUNE": "first", 
    "VOTANTI": "first",
})
# votanti tot per circosctizione
tot_voti = tot_voti.groupby(["CIRCOSCRIZIONE"], as_index=False)["VOTANTI"].sum()

seggi = pd.DataFrame(
    {
    "circoscrizioni": list(voti["CIRCOSCRIZIONE"].unique()),
    "seggi": [20,15,15,18,8],
    }
)

# tot voti ha numero di votanti e votanti necessari per un seggio
seggi["voti per seggio"] = pd.to_numeric(tot_voti["VOTANTI"]).div(seggi["seggi"])
# QUANTI SEGGI PER CIRCOSCRIZIONE QUESTE MEZZE CALZETTE HANNO PROVIDED?
pool_pref["seggi dai minori max"] = pool_pref["PREFERENZE_x"].div(seggi["voti per seggio"])
pool_pref["seggi dai minori min"] = pool_pref["PREFERENZE_y"].div(seggi["voti per seggio"])

for col in df.columns:
    if col == "lista":
        continue

    df[col] = round(pd.to_numeric(df[col]) / seggi[seggi["circoscrizioni"] == col]["voti per seggio"].to_list()[0] , 3)

# Normalize the data between 0 and 1 for coloring purposes
norm = colors.Normalize(vmin=df.iloc[:, 1:].min().min(), vmax=df.iloc[:, 1:].max().max())

# Create a color map
cmap = plt.cm.plasma  # You can choose different colormaps like 'viridis', 'plasma', etc.

# Set up the plot
fig, ax = plt.subplots(figsize=(50, 10))  # Adjust the size as needed
ax.axis('tight')
ax.axis('off')

# Create the cell colors: apply white for 'lista' column, and apply colormap for other columns
cell_colors = []
for i in range(len(df)):
    row_colors = ['white']  # First column 'lista' will be white
    for j in range(1, df.shape[1]):
        value = df.iloc[i, j]
        if pd.isna(value):
            row_colors.append(cmap(0))  # Color NaNs with the darkest color in the colormap
        else:
            row_colors.append(cmap(norm(value)))  # Apply colormap based on normalized values
    cell_colors.append(row_colors)

# Create the table plot from the DataFrame with colors
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center',
                 cellColours=cell_colors)

# Adjust font size and layout
table.auto_set_font_size(False)
table.set_fontsize(12)

# Display the table
plt.show()

'''
# Set up the plot
fig, ax = plt.subplots(figsize=(50, 5))  # Adjust the size of the table if necessary
ax.axis('tight')
ax.axis('off')

# Create the table plot from the DataFrame
styled_df = df.style.background_gradient(cmap='YlGnBu', subset=[
    "lista",
    "i : italia nord occidentale", 
    "ii : italia nord orientale", 
    "iii : italia centrale", 
    "iv : italia meridionale", 
    "v : italia insulare"]).highlight_null(color='lightgrey')

table = ax.table(cellText=df.values, cellColours= styled_df.data, 
                colLabels=df.columns, cellLoc='center', loc='center')

# Adjust the font size of the table
table.auto_set_font_size(False)
table.set_fontsize(12)

# Display the table
plt.show()
'''