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

df_eu = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'ReFuelEU',
    usecols = lambda column: column in [
        'year',
        'SAF share [%]',
        'of which synth-fuel share [%]'
    ],
    dtype={
        'year': int,
        'SAF share [%]': float,
        'of which synth-fuel share [%]': float
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)

# DATA MANIPULATION #############################

df_eu['of which synth-fuel share [%]'] = ((df_eu['SAF share [%]']/100)*(df_eu['of which synth-fuel share [%]']/100))*100

# FIGURE ########################################

# SETUP ######################

fig, axes = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 2,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
    sharex=True
)
plt.subplots_adjust(wspace=0.2)

# SECONDARY AXES ##############


# AXIS LIMITS ################

axes[0].set_xlim(2023, 2053)
axes[0].set_ylim(0,100)

# TICKS AND LABELS ###########

# GRIDS ######################

axes[0].grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
axes[0].grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

axes[0].set_ylabel("Share of Aviation Fuel [\%]")

axes[1].set_ylabel("Share of Aviation Fuel [\%]")


# PLOTTING ###################

axes[0].bar(
    x = df_eu['year'],
    height = df_eu['SAF share [%]'],
    color = 'green',
    width = 2,
    label = 'Non-Fossil Fuels',
    edgecolor = 'black'
)
axes[0].bar(
    x = df_eu['year'],
    height = df_eu['of which synth-fuel share [%]'],
    color = 'green',
    hatch = '///',
    width = 2,
    label = 'of which Synth-Fuel',
    edgecolor = 'white',
)
axes[0].bar(
    x = df_eu['year'],
    height = df_eu['of which synth-fuel share [%]'],
    color = 'none',
    width = 2,
    edgecolor = 'black',
)

axes[0].text(
    x=0.03,
    y=0.93,
    s=r'\textbf{Min. Requirements}',
    ha='left',
    va='center',
    fontsize=12,
    color='black',
    transform = axes[0].transAxes  # Use relative axes coordinates
)

# LEGEND ####################

axes[0].legend(
    loc='upper right',
    frameon = False
)

# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)