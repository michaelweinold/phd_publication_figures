#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
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

df_share = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'modal share',
    usecols = lambda column: column in [
        'trip distance (km)',
        'share rail (%)',
        'share air (%)',
    ],
    dtype={
        'trip distance (km)': str,
        'share rail (%)': float,
        'share air (%)': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_traveltime = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'city pairs',
    usecols = lambda column: column in [
        'distance (km)',
        'air travel time (min)',
        'rail travel time (min)'
    ],
    dtype={
        'distance (km)': float,
        'air travel time (min)': float,
        'rail travel time (min)': float
    },
    header = 0,
    engine = 'openpyxl'
)
		
# DATA MANIPULATION #############################

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 2,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm,
    )

# AXIS SCALING ###############

# AXIS LIMITS ################

ax[0].set_ylim(0, 100)
#ax[0].set_xlim(0, 4)

ax[1].set_xlim(0, 1000)
#ax[1].set_ylim(0, 80000)

# TICKS AND LABELS ###########

labels = df_share['trip distance (km)']
ax[0].set_xticklabels(labels, rotation=45, ha='right')

ax[1].minorticks_on()
ax[1].tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

ax[1].grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax[1].grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

ax[0].grid(which='both', axis='y', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

ax[0].set_xlabel("Trip Distance [km]")
ax[0].set_ylabel("Modal Share (Mass Transport) [\%]")

ax[1].set_xlabel("Travel Distance (City Pairs) [km]")
ax[1].set_ylabel("Travel Time (City Centers) [min]")

# PLOTTING ###################

width = 0.4
x = np.arange(len(df_share['trip distance (km)']))
ax[0].set_xticks(x, df_share['trip distance (km)'])

ax[0].bar(
    x = x,
    height = df_share['share rail (%)'],
    width = width,
    label = 'Rail',
    color = 'darkorange',
)
ax[0].bar(
    x = x,
    bottom = df_share['share rail (%)'],
    height = df_share['share air (%)'],
    width = width,
    label = 'Air',
    color = 'royalblue',
)

ax[1].scatter(
    x = df_traveltime['distance (km)'],
    y = df_traveltime['air travel time (min)'],
    s = 7,
    label = 'Air',
    color = 'royalblue',
)
ax[1].scatter(
    x = df_traveltime['distance (km)'],
    y = df_traveltime['rail travel time (min)'],
    s = 7,
    label = 'Rail',
    color = 'darkorange',
)


# LEGEND ####################

from matplotlib.patches import Patch

ax[0].legend(
    loc = 'lower left',
)
ax[1].legend(
    loc = 'best',
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
