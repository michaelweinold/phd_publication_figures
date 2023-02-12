#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from mpl_toolkits.basemap import Basemap
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

# DATA MANIPULATION #############################

finnair_coords = df_finnair['Position'].str.split(',', expand=True)
finnair_lats = finnair_coords[0].astype(float).values
finnair_lons = finnair_coords[1].astype(float).values

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 15*cm), # A4=(210x297)mm
    )

m = Basemap(
    projection='mill',
    llcrnrlat=-70,
    urcrnrlat=75,
    llcrnrlon=-180,
    urcrnrlon=180,
    resolution='c'
)

m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='0.8', lake_color=None, ax=None, zorder=None, alpha=None)

# DATA #######################

finnair_x, finnair_y = m(finnair_lons, finnair_lats)

# AXIS LIMITS ################

# TICKS AND LABELS ###########

# GRIDS ######################

# AXIS LABELS ################

# PLOTTING ###################

m.plot(finnair_x, finnair_y, 'r-', linewidth=2, markersize=5, label='Actual Track')
m.drawgreatcircle(finnair_lons[0], finnair_lats[0], finnair_lons[-1], finnair_lats[-1], del_s=300, color='blue', linewidth = 2, label='Great Circle Distance')

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
