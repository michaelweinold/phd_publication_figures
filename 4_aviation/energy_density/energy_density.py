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

df_fossil = pd.read_csv(
    filepath_or_buffer = 'data/fossil.csv',
    sep = ',',
    header = 'infer',
    index_col = False,
    skipinitialspace=True
)
df_avition_requirements = pd.read_csv(
    filepath_or_buffer = 'data/aviation_requirements.csv',
    sep = ',',
    header = 'infer',
    index_col = False,
    skipinitialspace=True
)

# DATA MANIPULATION #############################

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm
    )

# DATA #######################

x_fossil = df_fossil['MJ/kg']
y_fossil = df_fossil['MJ/l']

# AXIS LIMITS ################

ax.set_xlim(0,150)
ax.set_ylim(0,80)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

ax.set_xlabel("Gravimetric Energy Density [MJ/kg]")
ax.set_ylabel("Volumetric Energy Density [MJ/l]")

# PLOTTING ###################

ax.scatter(
    x_fossil,
    y_fossil,
    color = 'black',
)
ax.axvline(x=df_avition_requirements.iloc[0]['MJ/kg'], color='r', linestyle='--')

# LEGEND ####################

# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%
