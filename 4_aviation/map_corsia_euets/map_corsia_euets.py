#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
# geographic plotting
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import shapely.geometry as sgeom
import cartopy.io.shapereader as shpreader
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

df_finnair = pd.read_csv(
    filepath_or_buffer = 'data/AY99_2f2a9256.csv',
    sep = ',',
    header = 'infer',
    index_col = False,
)
df_british = pd.read_csv(
    filepath_or_buffer = 'data/BA57_301ab0b0.csv',
    sep = ',',
    header = 'infer',
    index_col = False,
)
df_airfrance = pd.read_csv(
    filepath_or_buffer = 'data/3138ab42.csv',
    sep = ',',
    header = 'infer',
    index_col = False,
)
df_easyjet = pd.read_csv(
    filepath_or_buffer = 'data/U27688_32c59827.csv',
    sep = ',',
    header = 'infer',
    index_col = False,
)
df_aireuropa = pd.read_csv(
    filepath_or_buffer = 'data/UX51_32cb722b.csv',
    sep = ',',
    header = 'infer',
    index_col = False,
)

# DATA MANIPULATION #############################

def extract_coordinates_from_csv(
        df: pd.DataFrame,
        column_name: str = 'Position'
) -> pd.DataFrame:
    df_coords: pd.DataFrame = df[column_name].str.split(',', expand=True).astype(float)
    df_coords.columns = ['lat', 'lon']
    ls_coords = sgeom.LineString(
        zip(
            df_coords['lon'],
            df_coords['lat']
        )
    )
    lat_cities: list = [df_coords['lat'].iloc[0], df_coords['lat'].iloc[-1]]
    lon_cities: list = [df_coords['lon'].iloc[0], df_coords['lon'].iloc[-1]]
    return ls_coords, lat_cities, lon_cities

finnair_track, lat_finnair, lon_finnair = extract_coordinates_from_csv(
    df = df_finnair,
    column_name = 'Position'
)
british_track, lat_british, lon_british = extract_coordinates_from_csv(
    df = df_british,
    column_name = 'Position'
)
airfrance_track, lat_airfrance, lon_airfrance = extract_coordinates_from_csv(
    df = df_airfrance,
    column_name = 'Position'
)
easyjet_track, lat_easyjet, lon_easyjet = extract_coordinates_from_csv(
    df = df_easyjet,
    column_name = 'Position'
)
aireuropa_track, lat_aireuropa, lon_aireuropa = extract_coordinates_from_csv(
    df = df_aireuropa,
    column_name = 'Position'
)


list_of_tracks = [finnair_track, british_track, airfrance_track]

# FIGURE ########################################

# SETUP ######################

# https://stackoverflow.com/a/60724892/
plateCr = ccrs.PlateCarree()
plateCr._threshold = plateCr._threshold/10.

fig = plt.figure(
    num = 'main',
    dpi = 300,
    figsize=(30*cm, 15*cm), # A4=(210x297)mm
)
ax = plt.axes(
    projection=ccrs.PlateCarree(),
)
ax.add_feature(cfeature.BORDERS, linestyle='-', alpha=1)
ax.add_feature(cfeature.COASTLINE, linestyle='-', alpha=1)


# DATA #######################

# AXIS LIMITS ################

ax.set_extent ((-45, 50, 30, 65), None) # (x0, x1, y0, y1)

# TICKS AND LABELS ###########

# GRIDS ######################

ax.gridlines()

# AXIS LABELS ################

# PLOTTING ###################

# https://github.com/IndEcol/country_converter?tab=readme-ov-file#classification-schemes
import country_converter as coco
cc = coco.CountryConverter()

shpfilename = shpreader.natural_earth(
    resolution='50m',
    category='cultural',
    name='admin_0_countries'
)
reader = shpreader.Reader(shpfilename)

lines_list = []

countries = reader.records()
for country in countries:
    if country.attributes['ADM0_A3'] in cc.convert(cc.EU27['name_short'], to='ISO3'):
        for track in list_of_tracks:
            lines_list.append(country.geometry.intersection(track))
        ax.add_geometries(
            country.geometry,
            ccrs.PlateCarree(),
            facecolor='blue',
            edgecolor='black',
            linewidth=1
        )

countries = reader.records()
for country in countries:
    if country.attributes['ADM0_A3'] in ['POL']:
        ax.add_geometries(
            country.geometry,
            ccrs.PlateCarree(),
            facecolor='blue',
            edgecolor='black',
            linewidth=1
        )

countries = reader.records()
for country in countries:
    if country.attributes['ADM0_A3'] in ['CHE', 'NOR', 'LIE', 'ISL']:
        ax.add_geometries(
            country.geometry,
            ccrs.PlateCarree(),
            facecolor='green',
            edgecolor='black',
            linewidth=1
        )


ax.add_geometries(
    geoms = finnair_track,
    crs = ccrs.PlateCarree(),
    facecolor = 'none',
    edgecolor = 'red',
    linewidth = 2
)
ax.add_geometries(
    geoms = british_track,
    crs = ccrs.PlateCarree(),
    facecolor = 'none',
    edgecolor = 'red',
    linewidth = 2
)
ax.add_geometries(
    geoms = airfrance_track,
    crs = ccrs.PlateCarree(),
    facecolor = 'none',
    edgecolor = 'red',
    linewidth = 2
)
ax.add_geometries(
    geoms = easyjet_track,
    crs = ccrs.PlateCarree(),
    facecolor = 'none',
    edgecolor = 'lightblue',
    linewidth = 2
)
ax.add_geometries(
    geoms = aireuropa_track,
    crs = ccrs.PlateCarree(),
    facecolor = 'none',
    edgecolor = 'lightblue',
    linewidth = 2
)

for line_segment in lines_list:
    ax.add_geometries(
        geoms = line_segment,
        crs = ccrs.PlateCarree(),
        facecolor = 'none',
        edgecolor = 'yellow',
        linewidth = 2
    )

# LEGEND ####################

import matplotlib.patches as patches
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe

legend_elements = [
    patches.Patch(
        facecolor = 'blue',
        edgecolor = 'black',
        label = 'EU(27)'
    ),
    patches.Patch(
        facecolor = 'green',
        edgecolor = 'black',
        label = 'Other ETS Countries'
    ),
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'red',
        linestyle = '-',
        label='ICAO CORSIA'
    ),
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'yellow',
        linestyle = '-',
        label='EU ETS',
        path_effects=[pe.Stroke(linewidth=5, foreground='black'), pe.Normal()]
    ),
]

ax.legend(
    handles=legend_elements,
    loc='lower left',
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