# %%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
cm = 1/2.54 # for inches-cm conversion

# data science
import numpy as np
import pandas as pd

# i/o
from pathlib import PurePath, Path

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": "Computer Modern",
    'font.size': 8
})

# DATA IMPORT ###################################

df_aerosols = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Aerosols',
    usecols = lambda column: column in [
        'Authors (Label)',
        'RF Average [mW/m2]',
        'RF Lower Errorbar [mW/m2]',
        'RF Upper Errorbar [mW/m2]',
    ],
    dtype={
        'Authors (Label)': str,
        'RF Average [mW/m2]': float,
        'RF Lower Errorbar [mW/m2]': float,
        'RF Upper Errorbar [mW/m2]': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)

# DATA MANIPULATION #############################

# FIGURE ########################################

# SETUP ######################

fig, axes = plt.subplots(
        num = 'main',
        nrows = 5,
        ncols = 1,
        sharex=True,
        dpi = 300,
        figsize=(16.5*cm, 5*cm), # A4=(210x297)mm
    )

# AXIS LIMITS ################

axes[0].set_xlim(-400,150)
axes[0].set_ylim(-1,1)

# TICKS AND LABELS ###########

for ax in axes:
    ax.set_yticklabels([])
    ax.tick_params(axis='y', which='both', length=0)

# GRIDS ######################


# AXIS LABELS ################

plt.xlabel("Effective Radiative Forcing [mW/m$^2$]")

# PLOTTING ###################

axes[0].scatter(
    x = df_aerosols['RF Average [mW/m2]'],
    y = 0,
    s = 5,
    marker = 'o',
    color = 'black',
    label = df_aerosols['Authors (Label)'],
)
axes[0].errorbar(
    x = df_aerosols['RF Average [mW/m2]'],
    y = 0,
    xerr = (df_aerosols['RF Lower Errorbar [mW/m2]'], df_aerosols['RF Upper Errorbar [mW/m2]']),
    fmt = 'none',
    capsize = 2,
    ecolor = 'black',
    elinewidth = 1,
)

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
