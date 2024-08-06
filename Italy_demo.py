import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

import geopandas as gpd
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

# Italian map
df_regions = gpd.read_file(filename="data/Limiti01012019_g/Reg01012019_g/Reg01012019_g_WGS84.shp").to_crs({'init': 'epsg:4326'})

## plot regional map of Italy
# ax = df_regions.plot(edgecolor='white', linewidth=1, figsize=(7,7))
# ax.figure.savefig('plots/italy_reg.png', bbox_inches='tight')

# get series of italy's comuni
df_comuni = gpd.read_file(filename="data/Limiti01012019_g/Com01012019_g/Com01012019_g_WGS84.shp").to_crs({'init': 'epsg:4326'})

## to plot all the comuni in Italy
# cities_pos = gpd.GeoSeries([p.representative_point() for p in df_comuni["geometry"]])

# ax = df_regions.plot(figsize=(7, 7), color='None', edgecolor='black', zorder=6, linewidth=0.6)

# cities_pos.plot(markersize= 0.5, ax=ax, color="red", zorder=4)
# ax.set_axis_off()
# ax.figure.savefig("plots/italy_cities.png", bbox_inches="tight")

## checking if comuni contains all the places people have voted in

def clean(s:str) -> str:
    return s.lower().strip()

def dumb_decode(s:str) -> str:
    s = clean(s).encode().replace(b"\xa3\xc2", b"").decode("utf8")
    
    s = s.replace("ã", "a'")
    s = s.replace("à", "a'")
    s = s.replace("â", "a")    
    s = s.replace("è", "e'")    
    s = s.replace("é", "e'")
    s = s.replace("ê", "e")    
    s = s.replace("ì", "i'")    
    s = s.replace("ò", "o'")
    s = s.replace("ô", "o")    
    s = s.replace("ù", "u'") 
    s = s.replace("ç", "c")
    
    #if s.find("'") + 1 < len(s):
    #    if s[s.find("'") + 1].isalpha():
    #        s = s[:s.find("'")] + s[s.find("'")+1:]
    
    while "-" in s:
        s = s.replace("-", " ")
    
    s = s.replace("   ", " ")
    return s

with open("data/PreferenzeEuropee_2019.csv", "r", encoding="utf8") as f:
    comuni_v = set()
    reader = csv.reader(f)
    for row in reader:
        # select comuni 
        n = dumb_decode(row[5])
        if n == "comune":
            continue # it's reading the index
        # eliminate double names
        if "/" in n:
            n = n[:n.find("/")]
            
        comuni_v.add(n)

# manual accounting for the last 26 communes which are in istat and not voting
def fuse(l: list, n: str, suppl: dict = dict()) -> dict:
    
    if len(l) == 1:
        res =  df_comuni_cut[df_comuni_cut["COMUNE"] == l[0]]["geometry"]
    res = unary_union(
    [df_comuni_cut[df_comuni_cut["COMUNE"] == c]["geometry"] for c in l]
    )
    
    df_comuni_cutted = df_comuni_cut.copy()
    for c in l:
        df_comuni_cutted = df_comuni_cutted.drop(df_comuni_cut[df_comuni_cut["COMUNE"] == c].index)
    if not suppl:
        suppl = {
            "COMUNE": list(),
            "SHAPE_AREA": list(),
            "geometry": list()
        }
        
    suppl["COMUNE"].append(n)
    suppl["SHAPE_AREA"].append(res.area)
    suppl["geometry"].append(res)

    return suppl, df_comuni_cutted

print(df_comuni.head)
print(df_comuni.columns)
df_comuni_cut = df_comuni[["COMUNE", "SHAPE_AREA", "geometry"]]

# decode awful encoding istat used
df_comuni_cut["COMUNE"] = pd.DataFrame(map(dumb_decode, df_comuni_cut["COMUNE"]))

# manual accounting
suppl, df_comuni_cut = fuse(["cuccaro monferrato", "lu"], "lu e cuccaro monferrato")

suppl, df_comuni_cut = fuse(["emare'se"], "emarese", suppl)

suppl, df_comuni_cut = fuse(["vermezzo", "zelo surrigone"], "vermezzo con zelo", suppl)

suppl, df_comuni_cut = fuse(["negrar"], "negrar di valpolicella", suppl)

suppl, df_comuni_cut = fuse(["ula' tirso"], "ula tirso", suppl)

suppl, df_comuni_cut = fuse(["cadrezzate", "osmate"], "cadrezzate con osmate", suppl)

suppl, df_comuni_cut = fuse(["san nazario", "campolongo sul brenta", "valstagna", "cismon del grappa"], "valbrenta", suppl)

suppl, df_comuni_cut = fuse(["san dorligo della valle"], "san dorligo della valle dolina", suppl)

suppl, df_comuni_cut = fuse(["paderno del grappa", "crespano del grappa"], "pieve del grappa", suppl)

suppl, df_comuni_cut = fuse(["fe'nis"], "fenis", suppl)

suppl, df_comuni_cut = fuse(["saint rhe'my en bosses"], "saint rhemy en bosses", suppl)

suppl, df_comuni_cut = fuse(["conco", "lusiana"], "lusiana conco", suppl)

suppl, df_comuni_cut = fuse(["mel", "lentiai", "trichiana"], "borgo valbelluna", suppl)

suppl, df_comuni_cut = fuse(["molvena", "mason vicentino"], "colceresa", suppl)

suppl, df_comuni_cut = fuse(["verre's"], "verres", suppl)


df_comuni_cut = pd.concat([df_comuni_cut, pd.DataFrame(suppl)])
comuni_i = set(df_comuni_cut["COMUNE"])

diff_vi = comuni_v.difference(comuni_i)
diff_iv = comuni_i.difference(comuni_v)

print(f"n of comuni in voting: {len(comuni_v)}, istat: {len(comuni_i)}")
print(f"diff in votes are {len(diff_vi)}: \n{diff_vi}")
print(f"diff in istat are {len(diff_iv)}: \n{diff_iv}")

df_comuni_cut.to_csv("data/istat_clean.csv")