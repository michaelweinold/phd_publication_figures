#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
# geographic plotting
import geopandas as gpd
from shapely.geometry import LineString
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
graticules = gpd.read_file('data/base_geodata/ne_50m_graticules_10')

def import_flightradar_csv(filepath: str) ->gpd.GeoDataFrame:
    df = pd.read_csv(
        filepath_or_buffer = filepath,
        sep = ',',
        header = 'infer',
        index_col = False,
    )
    df[['lat', 'lon']] = df['Position'].str.split(',', expand=True)
    df = df[['UTC', 'lat', 'lon']]

    geodf = gpd.GeoDataFrame(
        df,
        geometry = gpd.points_from_xy(
            x = df['lon'],
            y = df['lat'],
            crs = 'EPSG:4326' # World Geodetic System 1984 (standard for lat/lon)
        )
    )
    return geodf

geodf_finnair = import_flightradar_csv('data/AY99_2f2a9256.csv')
geodf_airfrance = import_flightradar_csv('data/3138ab42.csv')
geodf_easyjet = import_flightradar_csv('data/U27688_32c59827.csv')
geodf_aireuropa = import_flightradar_csv('data/UX51_32cb722b.csv')
geodf_airfrance2 = import_flightradar_csv('data/AF816_32c14da7.csv')

# GEOGRAPHY SETUP ###############################

# https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.set_crs.html
target_projection = "EPSG:3035" # seems to work well for Europe
# https://automating-gis-processes.github.io/CSC/notebooks/L2/projections.html

countries = countries.to_crs(target_projection)
popareas = popareas.to_crs(target_projection)
rivers = rivers.to_crs(target_projection)
lakes = lakes.to_crs(target_projection)
graticules = graticules.to_crs(target_projection)

# https://geopandas.org/en/stable/docs/reference/api/geopandas.points_from_xy.html#geopandas-points-from-xy
lower_left = gpd.points_from_xy(
    x = [-10], # longitude
    y = [33], # latitude
    crs='EPSG:4326' # = WGS 84
).to_crs(target_projection)

upper_right = gpd.points_from_xy(
    x = [70], # longitude
    y = [55], # latitude
    crs='EPSG:4326' # = WGS 84
).to_crs(target_projection)

# DATA MANIPULATION #############################

geodf_aireuropa = geodf_aireuropa.to_crs(target_projection)
geodf_airfrance = geodf_airfrance.to_crs(target_projection)
geodf_finnair = geodf_finnair.to_crs(target_projection)
geodf_airfrance2 = geodf_airfrance2.to_crs(target_projection)
geodf_easyjet = geodf_easyjet.to_crs(target_projection)

geoser_finnair = gpd.GeoSeries(LineString(geodf_finnair['geometry']))
geoser_airfrance = gpd.GeoSeries(LineString(geodf_airfrance['geometry']))
geoser_easyjet = gpd.GeoSeries(LineString(geodf_easyjet['geometry']))
geoser_aireuropa = gpd.GeoSeries(LineString(geodf_aireuropa['geometry']))
geoser_airfrance2 = gpd.GeoSeries(LineString(geodf_airfrance2['geometry']))

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 1,
    dpi = 300,
    figsize=(18*cm, 18*cm), # A4=(210x297)mm,
)

countries.plot(
    ax = ax,
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

ax.set_xticks([])
ax.set_yticks([])
ax.set_xticklabels([])
ax.set_yticklabels([])

# GRIDS ######################

graticules.plot(
    ax = ax,
    color = 'grey',
    linewidth = 0.5,
    linestyle = '--',
    alpha = 0.5,
)

# AXIS LABELS ################

# PLOTTING ###################

geoser_finnair.plot(
    ax = ax,
    color = 'red',
    linestyle = '-',
    linewidth = 2,
)
geoser_easyjet.plot(
    ax = ax,
    color = 'blue',
    linestyle = '-',
    linewidth = 2,
)
geoser_airfrance.plot(
    ax = ax,
    color = 'red',
    linestyle = '-',
    linewidth = 2,
)
geoser_airfrance2.plot(
    ax = ax,
    color = 'green',
    linestyle = '-',
    linewidth = 2,
)

# LEGEND ####################

# https://github.com/IndEcol/country_converter?tab=readme-ov-file#classification-schemes
import country_converter as coco
cc = coco.CountryConverter()

othercountries = ['CHE', 'NOR', 'LIE', 'ISL', 'GBR']

for index, country in countries.iterrows():
    if country['ADM0_A3'] in cc.convert(cc.EU27['name_short'], to='ISO3'):
        country = gpd.GeoSeries(country['geometry']) # otherwise 'country' is just a series (NOT a geoseries)
        country.plot(
            ax = ax,
            facecolor='lightblue',
            edgecolor='black',
            linewidth=1
        )
    elif country['ADM0_A3'] in othercountries:
        country = gpd.GeoSeries(country['geometry'])
        country.plot(
            ax = ax,
            facecolor='lightgreen',
            edgecolor='black',
            linewidth=1
        )
    else:
        pass

import matplotlib.patches as patches
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

legend_elements = [
    patches.Patch(
        facecolor = 'lightblue',
        edgecolor = 'black',
        label = 'EU Member States'
    ),
    patches.Patch(
        facecolor = 'lightgreen',
        edgecolor = 'black',
        label = 'Other ETS Countries'
    ),
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'red',
        linestyle = '-',
        label='ICAO CORSIA ETS'
    ),
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'blue',
        linestyle = '-',
        label='EU ETS',
    ),
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'green',
        linestyle = '-',
        label='No ETS',
    ),
]

ax.legend(
    handles=legend_elements,
    loc='upper right',
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
