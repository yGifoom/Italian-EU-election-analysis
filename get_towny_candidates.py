import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

import geopandas as gpd
from shapely.geometry import Polygon, Point

def clean(s:str) -> str:
    return s.lower().strip()

def b_clean(s:str) -> str:
    s = clean(s)
    while "-" in s:
        s = s.replace("-", " ")
    
    s = s.replace("   ", " ")
    return s

# to create a useful datastruct with all the candidates info
def congregate(congregated: list, i: int)-> None:
    for el in congregated:
        if data["nome e cognome"][i] == el["nome e cognome"]:
            if int(data["PREFERENZE"][i]) > 0:
                el["preferenze"][data["comune"][i]] = data["PREFERENZE"][i]
                return
    if int(data["PREFERENZE"][i]) > 0:
        el = {
            "nome e cognome": data["nome e cognome"][i],
            "partito": data["descrlista"][i],
            "datanascita": data["datanascita"][i],
            "luogonascita": data["luogonascita"][i],
            "sesso": data["sesso"][i],
            "eletto": data["CODTIPOELETTO"][i],
            "preferenze": {data["comune"][i] : data["PREFERENZE"][i]},
        }
        congregated.append(el)

cndts = list() # should hold candidate name, birth, party, {town1: nvotes, town2: nvotes....}

## create a list of dict of candidates and all the votes they got
with open("data/preferences_clean.csv", "r") as f:
    prfcs = pd.read_csv(f, low_memory = False)

data = prfcs.to_dict()

for i in range(len(data["nome e cognome"])):
    congregate(cndts, i)

## decomment for csv
pd.DataFrame(cndts).to_csv("data/candidates_clean.csv")

## cleaning european general data
with open("data/europee-20190526.csv", "r") as f:
    prfz = pd.read_csv(f, sep=";")

print(prfz.columns)
prfz = prfz.drop(["DATA_ELEZIONE", "TIPO_ELEZIONE"], axis=1)
for c in ["CIRCOSCRIZIONE", "REGIONE", "PROVINCIA", "COMUNE"]:
    prfz[c] = prfz[c].apply(b_clean)

# they fucked up the spelling
# TODO: right now this rewrites the whole row to the new string when i would like it to chane only COMUNE
filter = {
    "reggio calabria": "reggio di calabria", 
    "cassano allo ionio": "cassano all'ionio", 
    "staletti": "staletti'",
    "negrar": "negrar di valpolicella",
    "barcellona p.g.": "barcellona pozzo di gotto",
    "valsaviore": "cevo" # valsaviore does not exist, cevo is one of the comuni that it became
    } 

prfz.replace(filter, regex=True, inplace=True)

## decomment for csv
prfz.to_csv("data/europee_clean.csv")
