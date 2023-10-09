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
    'font.size': 11
})

# DATA IMPORT ###################################

df_BE = pd.read_csv(
    filepath_or_buffer = 'data/Belgium.csv',
    sep = ',',
    skipinitialspace = True,
    header=None,
    names=['x', 'y'],
)
df_BR = pd.read_csv(
    filepath_or_buffer = 'data/Brazil.csv',
    sep = ',',
    skipinitialspace = True,
    header=None,
    names=['x', 'y'],
)
df_IE = pd.read_csv(
    filepath_or_buffer = 'data/Ireland.csv',
    sep = ',',
    skipinitialspace = True,
    header=None,
    names=['x', 'y'],
)
df_SW = pd.read_csv(
    filepath_or_buffer = 'data/Sweden.csv',
    sep = ',',
    skipinitialspace = True,
    header=None,
    names=['x', 'y'],
)
df_EN = pd.read_csv(
    filepath_or_buffer = 'data/UK.csv',
    sep = ',',
    skipinitialspace = True,
    header=None,
    names=['x', 'y'],
)
df_US = pd.read_csv(
    filepath_or_buffer = 'data/US.csv',
    sep = ',',
    skipinitialspace = True,
    header=None,
    names=['x', 'y'],
)
		
# DATA MANIPULATION #############################

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
    num = 'main',
    sharey = True,
    sharex = True,
    nrows = 1,
    ncols = 1,
    dpi = 300,
    figsize=(20*cm, 5*cm), # A4=(210x297)mm,
)

# AXIS SCALING ###############

# AXIS LIMITS ################

ax.set_xlim(1600, 2020)
ax.set_ylim(0, 8)


# TICKS AND LABELS ###########

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Persons per Household")

# TITLE ######################

# PLOTTING ###################

ax.plot(
    df_BE['x'],
    df_BE['y'],
    marker = 'o',
    label = 'Belgium',
)
ax.plot(
    df_BR['x'],
    df_BR['y'],
    marker = 'x',
    label = 'Brazil',
)
ax.plot(
    df_IE['x'],
    df_IE['y'],
    marker = 's',
    label = 'Ireland',
)
ax.plot(
    df_SW['x'],
    df_SW['y'],
    marker = 'v',
    label = 'Sweden',
)
ax.plot(
    df_EN['x'],
    df_EN['y'],
    marker = '^',
    label = 'England',
)
ax.plot(
    df_US['x'],
    df_US['y'],
    marker = '>',
    label = 'US',
)


# LEGEND ####################

ax.legend(
    loc = 'upper left',
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

# %%
