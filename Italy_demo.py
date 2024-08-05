import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

import geopandas as gpd
from shapely.geometry import Polygon, Point

# plot regional map of Italy
df_regions = gpd.read_file(filename="data/Limiti01012019_g/Reg01012019_g/Reg01012019_g_WGS84.shp").to_crs({'init': 'epsg:4326'})
# ax = df_regions.plot(edgecolor='white', linewidth=1, figsize=(7,7))
# ax.figure.savefig('plots/italy_reg.png', bbox_inches='tight')

# get series of italy's comuni
df_comuni = gpd.read_file(filename="data/Limiti01012019_g/Com01012019_g/Com01012019_g_WGS84.shp").to_crs({'init': 'epsg:4326'})

cities_pos = gpd.GeoSeries([p.representative_point() for p in df_comuni["geometry"]])

ax = df_regions.plot(figsize=(7, 7), color='None', edgecolor='black', zorder=6, linewidth=0.6)

cities_pos.plot(markersize= 0.5, ax=ax, color="red", zorder=4)
ax.set_axis_off()
ax.figure.savefig("plots/italy_cities.png", bbox_inches="tight")
