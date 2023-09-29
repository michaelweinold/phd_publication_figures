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

df_initial = pd.read_csv(
    filepath_or_buffer = 'data/data_initial_construction.csv',
    sep = ',',
    skipinitialspace = True,
)

df_recurrent = pd.read_csv(
    filepath_or_buffer = 'data/data_recurring_emissions.csv',
    sep = ',',
    skipinitialspace = True,
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

ax.set_xlim(12, 150)
ax.set_ylim(0, 60)


# TICKS AND LABELS ###########

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Embodied Energy [TJ]")
ax.set_xlabel("Building Lifetime [years]")

# TITLE ######################

# PLOTTING ###################

ax.plot(
    df_initial['servicelife'],
    df_initial['energy'],
)
ax.plot(
    df_recurrent['servicelife'],
    df_recurrent['energy'],
)
ax.fill_between(df_recurrent['servicelife'], 0, df_recurrent['energy'], color='orange', alpha=0.3, label = 'Recurrent')
ax.fill_between(df_initial['servicelife'], 0, df_initial['energy'], color='lightblue', alpha=1, label = 'Initial')


# LEGEND ####################

ax.legend(
    loc = 'upper right',
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
