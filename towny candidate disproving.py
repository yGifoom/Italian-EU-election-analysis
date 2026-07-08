import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
import csv
import seaborn as sns

with open("data/preferences_clean.csv", "r") as f:
    pref = pd.read_csv(f)
with open("data/europee_clean.csv", "r") as f:
    voti = pd.read_csv(f)
europarlamentari = { x[1] for x in [
("ALDO", "PATRICIELLO"),
("ALESSANDRA", "BASSO"),
("ALESSANDRA", "MORETTI"),
("ALESSANDRO", "PANZA"),
("ANDREA", "CAROPPO"),
("ANDREA", "COZZOLINO"),
("ANGELO", "CIOCCA"),
("ANNA", "BONFRISCO"),
("ANNALISA", "TARDINO"),
("ANTONIO MARIA", "RINALDI"),
("ANTONIO", "TAJANI"),
("BRANDO MARIA", "BENIFEI"),
("CARLO", "CALENDA"),
("CARLO", "FIDANZA"),
("CATERINA", "CHINNICI"),
("CHIARA MARIA", "GEMMA"),
("DANIELA", "RONDINELLI"),
("DANILO OSCAR", "LANCINI"),
("DAVID MARIA", "SASSOLI"),
("DINO RICCARDO MARIA", "GIARRUSSO"),
("ELENA", "LIZZI"),
("ELEONORA", "EVI"),
("ELISABETTA", "GUALMINI"),
("FABIO MASSIMO", "CASTALDO"),
("FRANCESCA", "DONATO"),
("FRANCO", "ROBERTI"),
("FULVIO", "MARTUSCIELLO"),
("GIANANTONIO", "DA RE"),
("GIANNA", "GANCIA"),
("GIULIANO", "PISAPIA"),
("GIUSEPPE", "FERRANDINO"),
("GIUSEPPE", "MILAZZO"),
("GIUSEPPINA", "PICIERNO"),
("HERBERT", "DORFMANN"),
("IGNAZIO", "CORRAO"),
("IRENE", "TINAGLI"),
("ISABELLA", "ADINOLFI"),
("ISABELLA", "TOVAGLIERI"),
("LAURA", "FERRARA"),
("LUCIA", "VUOLO"),
("LUISA", "REGIMENTI"),
("MARA", "BIZZOTTO"),
("MARCO", "CAMPOMENOSI"),
("MARCO", "DREOSTO"),
("MARCO", "ZANNI"),
("MARCO", "ZULLO"),
("MARIO", "FURORE"),
("MASSIMILIANO", "SALINI"),
("MASSIMILIANO", "SMERIGLIO"),
("MASSIMO", "CASANOVA"),
("MATTEO", "ADINOLFI"),
("NICOLA", "PROCACCINI"),
("PAOLO", "BORCHIA"),
("PAOLO", "DE CASTRO"),
("PATRIZIA FERMA FRANCESCA", "TOIA"),
("PIERFRANCESCO", "MAJORINO"),
("PIERNICOLA", "PEDICINI"),
("PIETRO", "BARTOLO"),
("PIETRO", "FIOCCHI"),
("RAFFAELE", "FITTO"),
("RAFFAELE", "STANCANELLI"),
("ROBERTO", "GUALTIERI"),
("ROSA", "D'AMATO"),
("ROSANNA", "CONTE"),
("SABRINA", "PIGNEDOLI"),
("SALVATORE", "DE MEO"),
("SERGIO ANTONIO", "BERLATO"),
("SILVIA SERAFINA", "SARDONE"),
("SILVIO", "BERLUSCONI"),
("SIMONA", "BONAFE'"),
("SIMONA RENATA", "BALDASSARRE"),
("STEFANIA", "ZAMBELLI"),
("SUSANNA", "CECCARDI"),
("TIZIANA", "BEGHIN"),
("VALENTINO", "GRANT"),
("VINCENZO", "SOFO")]

}


# gather not elected candidates and sum their preferences
pref_non_e = pref[pref["CODTIPOELETTO"] == "N"]
for cogn in europarlamentari:
    pref_non_e = pref_non_e[pref_non_e["cognome"] != cogn]


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

    df[col] = round(pd.to_numeric(df[col]) / seggi[seggi["circoscrizioni"] == col]["voti per seggio"].to_list()[0] , 2)

df = df.fillna(0)
'''
df_q = pd.DataFrame()
for col in df:
    if col != "lista":
        df_q[col] = pd.to_numeric(pd.qcut(df[col], 2, labels=list(range(2))))

sns.heatmap(df_q)
plt.show()
'''
df["lista"] = ["pd", "lega", "M5S", "FI", "FDI", "SVP"]
print(df.columns)
df.columns= ["lista", "i" ,"ii", "iii","iv","v"]
df.set_index("lista", inplace=True)
plt.figure(figsize=(10,6))

sns.heatmap(df, annot=True, cmap="flare", vmin=0.0, vmax=1.064, cbar=True)

plt.title("seats gotten by votes to non elected candidates")
plt.savefig('plots/towny candidates ruined 2.png')

print(seggi)
'''
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


