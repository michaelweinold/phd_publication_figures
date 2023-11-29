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
    "text.usetex": False,
    "font.family": "Arial",
    'font.size': 10
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
df_pal = pd.read_csv(
    filepath_or_buffer = 'data/PR102_3056874f.csv',
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
df_quantas = pd.read_csv(
    filepath_or_buffer = 'data/QF63_3025161d.csv',
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
pal_track, lat_pal, lon_pal = extract_coordinates_from_csv(
    df = df_pal,
    column_name = 'Position'
)
airfrance_track, lat_airfrance, lon_airfrance = extract_coordinates_from_csv(
    df = df_airfrance,
    column_name = 'Position'
)
quantas_track, lat_quantas, lon_quantas = extract_coordinates_from_csv(
    df = df_quantas,
    column_name = 'Position'
)

# FIGURE ########################################

# SETUP ######################

# https://stackoverflow.com/a/60724892/
plateCr = ccrs.PlateCarree()
plateCr._threshold = plateCr._threshold/10.

fig = plt.figure(
    num = 'main',
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm
)
ax = plt.subplot(
    projection=plateCr,
)

# https://scitools.org.uk/cartopy/docs/latest/gallery/lines_and_polygons/features.html#features
ax.add_feature(cfeature.BORDERS, alpha=0.25, linewidth=0.5)
ax.add_feature(cfeature.LAKES, alpha=0.5, linewidth=0.5)
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.set_global()

# DATA #######################

# AXIS LIMITS ################

ax.set_ylim(-70,70)

# TICKS AND LABELS ###########

# GRIDS ######################

# AXIS LABELS ################

# PLOTTING ###################

ax.add_geometries(
    geoms = finnair_track,
    crs = ccrs.PlateCarree(),
    facecolor = 'none',
    edgecolor = 'red',
    linewidth = 1
)
ax.add_geometries(
    geoms = british_track,
    crs = ccrs.PlateCarree(),
    facecolor = 'none',
    edgecolor = 'red',
    linewidth = 1
)
ax.add_geometries(
    geoms = pal_track,
    crs = ccrs.Geodetic(), # https://stackoverflow.com/a/67730772
    facecolor = 'none',
    edgecolor = 'red',
    linewidth = 1
)
ax.add_geometries(
    geoms = airfrance_track,
    crs = ccrs.PlateCarree(),
    facecolor = 'none',
    edgecolor = 'red',
    linewidth = 1
)

ax.plot(
    lon_finnair,
    lat_finnair,
    color='blue',
    transform=ccrs.Geodetic(),
    linewidth = 1,
)
ax.plot(
    lon_british,
    lat_british,
    color='blue',
    transform=ccrs.Geodetic(),
    linewidth = 1
)
ax.plot(
    lon_pal,
    lat_pal,
    color='blue',
    transform=ccrs.Geodetic(),
    linewidth = 1
)
ax.plot(
    lon_airfrance,
    lat_airfrance,
    color='blue',
    transform=ccrs.Geodetic(),
    linewidth = 1
)

# LEGEND ####################

from matplotlib.lines import Line2D

legend_elements = [
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'blue',
        linestyle = '-',
        label='Great Circle'
    ),
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'red',
        linestyle = '-',
        label='Aircraft Track'
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
# %%