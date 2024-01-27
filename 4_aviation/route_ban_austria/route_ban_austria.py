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
popareas = gpd.read_file('data/base_geodata/ne_10m_urban_areas/ne_10m_urban_areas.shp')
rivers = gpd.read_file('data/base_geodata/ne_10m_rivers_lake_centerlines/ne_10m_rivers_lake_centerlines.shp')
lakes = gpd.read_file('data/base_geodata/ne_10m_lakes/ne_10m_lakes.shp')

track_vienna_villach = gpd.read_file('data/vienna_villach.geojson')
track_graz_bruck = gpd.read_file('data/graz_bruck.geojson')

airport_vie = gpd.points_from_xy(
    x = [16.570833], # longitude
    y = [48.110833], # latitude
    crs='EPSG:4326' # = WGS 84
).to_crs('EPSG:3035')

airport_grz = gpd.points_from_xy(
    x = [15.439167], # longitude
    y = [46.993056], # latitude
    crs='EPSG:4326' # = WGS 84
).to_crs('EPSG:3035')

airport_klu = gpd.points_from_xy(
    x = [14.337222], # longitude
    y = [46.642778], # latitude
    crs='EPSG:4326' # = WGS 84
).to_crs('EPSG:3035')


# DATA MANIPULATION #############################

# https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.set_crs.html
target_projection = "EPSG:3035" # seems to work well for Europe
# https://automating-gis-processes.github.io/CSC/notebooks/L2/projections.html

countries = countries.to_crs(target_projection)
popareas = popareas.to_crs(target_projection)
rivers = rivers.to_crs(target_projection)
lakes = lakes.to_crs(target_projection)

track_vienna_villach = track_vienna_villach.to_crs(target_projection)
track_graz_bruck = track_graz_bruck.to_crs(target_projection)

# https://geopandas.org/en/stable/docs/reference/api/geopandas.points_from_xy.html#geopandas-points-from-xy
lower_left = gpd.points_from_xy(
    x = [9], # longitude
    y = [46], # latitude
    crs='EPSG:4326' # = WGS 84
).to_crs(target_projection)

upper_right = gpd.points_from_xy(
    x = [18], # longitude
    y = [50], # latitude
    crs='EPSG:4326' # = WGS 84
).to_crs(target_projection)

# FIGURE ########################################

# SETUP ######################

ax = countries.plot(
    figsize = (20*cm, 20*cm),
    color = 'white',
    edgecolor = 'black',
    linewidth = 0.75,
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

# TICKS AND LABELS ###########

ax.set_xticks([])
ax.set_yticks([])
ax.set_xticklabels([])
ax.set_yticklabels([])

# GRIDS ######################

# AXIS LABELS ################

# PLOTTING ###################

popareas.plot(
    ax = ax,
    color = 'orange',
    alpha = 0.5
)
rivers.plot(
    ax = ax,
    color = 'lightblue',
    alpha = 0.5
)
lakes.plot(
    ax = ax,
    color = 'blue',
    alpha = 0.5
)

track_vienna_villach.plot(
    ax = ax,
    color = 'red',
)
track_graz_bruck.plot(
    ax = ax,
    color = 'red',
)

flight_vie_klu = ax.plot(
    [airport_vie.x[0], airport_klu.x[0]],
    [airport_vie.y[0], airport_klu.y[0]],
    color = 'blue',
    linestyle = '-',
)

flight_vie_grz = ax.plot(
    [airport_vie.x[0], airport_grz.x[0]],
    [airport_vie.y[0], airport_grz.y[0]],
    color = 'blue',
    linestyle = '-',
)

# LEGEND ####################

import matplotlib.patches as patches
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

legend_elements = [
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'blue',
        linestyle = '-',
        label='Flight Track',
    ),
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'red',
        linestyle = '-',
        label='Train Track',
    ),
]

ax.legend(
    handles=legend_elements,
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
