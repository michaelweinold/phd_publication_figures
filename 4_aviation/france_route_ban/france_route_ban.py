#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
# geographic plotting
import geopandas as gpd
# unit conversion
cm = 1/2.54 # for inches-cm conversion
# time manipulation
from datetime import datetime
# data science
import numpy as np
import pandas as pd

# i/o
from pathlib import PurePath, Path

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 12
})

# DATA IMPORT ###################################

countries = gpd.read_file('data/base_geodata/ne_10m_admin_0_countries/ne_10m_admin_0_countries.shp')
popareas = gpd.read_file('data/base_geodata/ne_50m_urban_areas/ne_50m_urban_areas.shp')
rivers = gpd.read_file('data/base_geodata/ne_10m_rivers_lake_centerlines/ne_10m_rivers_lake_centerlines.shp')
lakes = gpd.read_file('data/base_geodata/ne_10m_lakes/ne_10m_lakes.shp')

track_paris_lyon = gpd.read_file('data/paris_lyon.geojson')
track_paris_bordeaux = gpd.read_file('data/paris_bordeaux.geojson')


# DATA MANIPULATION #############################

# https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.set_crs.html
target_projection = "EPSG:3035" # seems to work well for Europe
# https://automating-gis-processes.github.io/CSC/notebooks/L2/projections.html

countries = countries.to_crs(target_projection)
urban = urban.to_crs(target_projection)
rivers = rivers.to_crs(target_projection)
lakes = lakes.to_crs(target_projection)

track_paris_lyon = track_paris_lyon.to_crs(target_projection)
track_paris_bordeaux = track_paris_bordeaux.to_crs(target_projection)

# https://geopandas.org/en/stable/docs/reference/api/geopandas.points_from_xy.html#geopandas-points-from-xy
lower_left = gpd.points_from_xy(
    x = [-10], # longitude
    y = [40], # latitude
    crs='EPSG:4326' # = WGS 84
).to_crs(target_projection)

upper_right = gpd.points_from_xy(
    x = [10], # longitude
    y = [52], # latitude
    crs='EPSG:4326' # = WGS 84
).to_crs(target_projection)

# FIGURE ########################################

# SETUP ######################

ax = countries.plot(
    figsize = (20*cm, 20*cm),
    color = 'white',
    edgecolor = 'black',
    linewidth = 0.5,
    alpha = 1,
)

# DATA #######################

# AXIS LIMITS ################

ax.set_xlim(
    lower_left.x[0],
    upper_right.x[0]
)

ax.set_ylim(
    lower_left.y[0],
    upper_right.y[0]
)

# TICKS AND LABELS ###########

# GRIDS ######################

# AXIS LABELS ################

# PLOTTING ###################

urban.plot(
    ax = ax,
    color = 'orange',
    label = 'Urban Areas',
    alpha = 0.5
)
rivers.plot(
    ax = ax,
    color = 'lightblue',
    label = 'Rivers',
    alpha = 0.5
)
lakes.plot(
    ax = ax,
    color = 'blue',
    alpha = 0.5
)

track_paris_lyon.plot(
    ax = ax,
    color = 'red',
    label = 'Paris-Lyon Track'
)
track_paris_bordeaux.plot(
    ax = ax,
    color = 'red',
    label = 'Paris-Bordeaux Track'
)


# LEGEND ####################

ax.legend(
    loc='upper left',
)

# EXPORT #########################################

file_path = os.path.abspath(__file__)
file_name = os.path.splitext(os.path.basename(file_path))[0]
figure_name: str = str(file_name + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%
