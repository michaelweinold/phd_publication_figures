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
    'font.size': 11
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

# DATA MANIPULATION #############################

def extract_coordinates_from_csv(
        df: pd.DataFrame,
        column_name: str = 'Position'
) -> pd.DataFrame:
    df_coords: pd.DataFrame = df[column_name].str.split(',', expand=True)
    df_coords.columns = ['lat', 'lon']
    ls_coords = sgeom.LineString(
        zip(
            df_coords['lon'].astype(float),
            df_coords['lat'].astype(float)
        )
    )
    return ls_coords

finnair_coords = extract_coordinates_from_csv(
    df = df_finnair,
    column_name = 'Position'
)
british_coords = extract_coordinates_from_csv(
    df = df_british,
    column_name = 'Position'
)

# FIGURE ########################################

# SETUP ######################

fig = plt.figure(
    num = 'main',
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm
)
ax = plt.subplot(
    projection=ccrs.PlateCarree(),
)

# https://scitools.org.uk/cartopy/docs/latest/gallery/lines_and_polygons/features.html#features
ax.add_feature(cfeature.BORDERS, alpha=0.25)
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.COASTLINE)

# DATA #######################

# AXIS LIMITS ################

# TICKS AND LABELS ###########

# GRIDS ######################

# AXIS LABELS ################

# PLOTTING ###################

ax.add_geometries(
    geoms = finnair_coords,
    crs = ccrs.PlateCarree(),
    facecolor = 'none',
    edgecolor = 'red',
    linewidth = 1
)
ax.add_geometries(
    geoms = british_coords,
    crs = ccrs.PlateCarree(),
    facecolor = 'none',
    edgecolor = 'red',
    linewidth = 1
)

# LEGEND ####################

plt.legend(
    loc = 'lower left',
    frameon = False,
    fontsize = 14)

# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%
