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

df_fuels = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Energy Density Fuels',
    usecols = lambda column: column in [
        'substance',
        'MJ/kg',
        'MJ/l'
    ],
    dtype={
        'substance': str,
        'MJ/kg': float,
        'MJ/l': float
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
        gridspec_kw = dict(
            width_ratios=[9, 1],
        ),
        sharey=True
    )
plt.subplots_adjust(wspace=0.075)


# AXIS LIMITS ################

ax[0].set_xlim(0,60)
ax[0].set_ylim(0,60)

ax[1].set_xlim(140,150)
ax[1].set_ylim(0,60)

# TICKS AND LABELS ###########

ax[0].minorticks_on()
ax[0].tick_params(axis='x', which='both', bottom=False)
ax[0].tick_params(axis='y', which='both', bottom=False)

ax[1].minorticks_on()
ax[1].tick_params(axis='x', which='both', bottom=False)
ax[1].tick_params(axis='y', which='both', bottom=False)

# GRIDS ######################

ax[0].grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax[0].grid(which='both', axis='x', linestyle='-', linewidth = 0.5)

ax[1].grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax[1].grid(which='both', axis='x', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

ax[0].set_xlabel("Gravimetric Energy Density [MJ/kg]")
ax[0].set_ylabel("Volumetric Energy Density [MJ/l]")

# PLOTTING ###################

ax[0].scatter(
    df_fuels['MJ/kg'],
    df_fuels['MJ/l'],
    color = 'black',
)
ax[1].scatter(
    df_fuels['MJ/kg'],
    df_fuels['MJ/l'],
    color = 'black',
)

# LEGEND ####################

# ANNOTATION ################

for idx, row in df_fuels.iterrows():
    ax[0].annotate(
        row['substance'],
        (row['MJ/kg'], row['MJ/l']),
        ha='right',
        va='bottom',
        fontsize=9
    )
    ax[1].annotate(
        row['substance'],
        (row['MJ/kg'], row['MJ/l']),
        ha='right',
        va='bottom',
        fontsize=9
    )

# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%

# %%
