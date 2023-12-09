#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
# unit conversion
cm = 1/2.54 # for inches-cm conversion
# time manipulation
from datetime import datetime
# data science
import numpy as np
import pandas as pd

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 11
})

# DATA IMPORT ###################################

df_us = pd.read_excel(
    io = './data/data.xlsx',
    sheet_name = 'US',
    usecols = lambda column: column in [
        'Distance Bin, Upper Limit [km]',
        'Share of Emissions [%]',
    ],
    dtype={
        'Distance Bin, Upper Limit [km]': int,
        'Share of Emissions [%]': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_eu = pd.read_excel(
    io = './data/data.xlsx',
    sheet_name = 'EU',
    usecols = lambda column: column in [
        'Distance Bin, Upper Limit [km]',
        'Share of Emissions [%]',
    ],
    dtype={
        'Distance Bin, Upper Limit [km]': int,
        'Share of Emissions [%]': float,
    },
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

# distance bins Eurocontrol
distance_bins_eurocontrol = pd.IntervalIndex(
    data = [
        pd.Interval(left=0, right=500, closed='right'),
        pd.Interval(left=500, right=1500, closed='right'),
        pd.Interval(left=1500, right=2000, closed='right'),
        pd.Interval(left=2000, right=3000, closed='right'),
        pd.Interval(left=3000, right=13000, closed='right'),
    ],
)
df_us['Distance Bin (Eurocontrol) [km]'] = pd.cut(
    df_us['Distance Bin, Upper Limit [km]'],
    bins=distance_bins_eurocontrol
)
df_us_newbins = df_us.groupby('Distance Bin (Eurocontrol) [km]')['Share of Emissions [%]'].sum().reset_index()


# FIGURE ########################################

# SETUP ######################

fig, axes = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 3,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
)

# SECONDARY AXES ##############

# AXIS LIMITS ################

for ax in axes[0:2]:
    ax.set_ylim(0, 70)


# TICKS AND LABELS ###########

for ax in axes:
    ax.minorticks_on()
    ax.tick_params(axis='x', which='minor', bottom=True)

major_ticks = df_us_newbins.index
labels = [
    '$<$500',
    '501-1500',
    '1501-2000',
    '2001-3000',
    '$>$3001',
]

for ax in axes[0:2]:
    ax.set_xticks(major_ticks)
    ax.set_xticklabels(labels, rotation=90, va='top')
    ax.xaxis.tick_top()
    ax.tick_params(axis='x', which='both', pad=-10)

# GRIDS ######################

for ax in axes[0:2]:
    ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
    ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
    ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

axes[0].set_ylabel("Share of Emissions [%]")

axes[0].set_xlabel("Flight Distance [km]")
axes[1].set_xlabel("Flight Distance [km]")

# PLOTTING ###################

axes[0].bar(
    x = df_us_newbins.index,
    height = df_us_newbins['Share of Emissions [%]'],
    width = 0.75,
)

axes[1].bar(
    x = df_eu.index,
    height = df_eu['Share of Emissions [%]'],
    width = 0.75,
)

# LEGEND ####################

ax.legend(
    loc='lower right',
)

# EXPORT #########################################

from pathlib import Path
figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)