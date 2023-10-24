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

df_co2 = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'CO2',
    usecols = lambda column: column in [
        'Authors (Label)',
        'ERF Average [mW/m2]',
        'ERF Lower Errorbar [mW/m2]',
        'ERF Upper Errorbar [mW/m2]',
    ],
    dtype={
        'Authors (Label)': str,
        'ERF Average [mW/m2]': float,
        'ERF Lower Errorbar [mW/m2]': float,
        'ERF Upper Errorbar [mW/m2]': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)

df_h2o = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Water Vapor',
    usecols = lambda column: column in [
        'Authors (Label)',
        'ERF Average [mW/m2]',
        'ERF Lower Errorbar [mW/m2]',
        'ERF Upper Errorbar [mW/m2]',
    ],
    dtype={
        'Authors (Label)': str,
        'ERF Average [mW/m2]': float,
        'ERF Lower Errorbar [mW/m2]': float,
        'ERF Upper Errorbar [mW/m2]': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)

df_aerosols_rad = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Aerosols-Radiation',
    usecols = lambda column: column in [
        'Authors (Label)',
        'ERF Average [mW/m2]',
        'ERF Lower Errorbar [mW/m2]',
        'ERF Upper Errorbar [mW/m2]',
        'Effect',
    ],
    dtype={
        'Authors (Label)': str,
        'ERF Average [mW/m2]': float,
        'ERF Lower Errorbar [mW/m2]': float,
        'ERF Upper Errorbar [mW/m2]': float,
        'Effect': str,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)

df_aerosols = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Aerosols',
    usecols = lambda column: column in [
        'Authors (Label)',
        'ERF Average [mW/m2]',
        'ERF Lower Errorbar [mW/m2]',
        'ERF Upper Errorbar [mW/m2]',
    ],
    dtype={
        'Authors (Label)': str,
        'ERF Average [mW/m2]': float,
        'ERF Lower Errorbar [mW/m2]': float,
        'ERF Upper Errorbar [mW/m2]': float,
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

for ax in axes:
    ax.set_xlim(-150,150)
    ax.set_ylim(-1,1)

# TICKS AND LABELS ###########

for ax in axes:
    ax.set_yticklabels([])
    ax.tick_params(axis='y', which='both', length=0)

# GRIDS ######################


# AXIS LABELS ################

plt.xlabel("Effective Radiative Forcing [mW/m$^2$]")

# PLOTTING ###################

# CO2

axes[0].barh(
    y = 0,
    width = df_co2['ERF Average [mW/m2]'],
    height = 1.5,
    align='center',
    color = 'red',
    edgecolor = 'black'
)

# https://stackoverflow.com/a/33857966
average = df_co2['ERF Average [mW/m2]']
lower = df_co2['ERF Lower Errorbar [mW/m2]']
upper = df_co2['ERF Upper Errorbar [mW/m2]']
axes[0].errorbar(
    x = average,
    y = 0,
    xerr = (
        abs(average - lower),
        pd.Series([0]),
    ),
    fmt = 'none',
    capsize = 2,
    ecolor = 'white',
    elinewidth = 1,
)
axes[0].errorbar(
    x = average,
    y = 0,
    xerr = (
        pd.Series([0]),
        abs(average - upper)
    ),
    fmt = 'none',
    capsize = 2,
    ecolor = 'black',
    elinewidth = 1,
)


axes[0].text(
    x=-140,
    y=0,
    s=r'\textbf{CO$_2$ Emissions} (' + df_co2['Authors (Label)'][0] + ')',
    ha='left',
    va='center',
    fontsize=8,
    color='black',
)

# Aerosols-Radiation

axes[1].barh(
    y = 0,
    width = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Soot']['ERF Average [mW/m2]'],
    height = 1.5,
    align='center',
    color = 'red',
    edgecolor = 'black'
)

average = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Soot']['ERF Average [mW/m2]']
lower = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Soot']['ERF Lower Errorbar [mW/m2]']
upper = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Soot']['ERF Upper Errorbar [mW/m2]']
axes[1].errorbar(
    x = average,
    y = 0,
    xerr = (
        abs(average - lower),
        pd.Series([0]),
    ),
    fmt = 'none',
    capsize = 2,
    ecolor = 'white',
    elinewidth = 1,
)
axes[1].errorbar(
    x = average,
    y = 0,
    xerr = (
        pd.Series([0]),
        abs(average - upper)
    ),
    fmt = 'none',
    capsize = 2,
    ecolor = 'black',
    elinewidth = 1,
)

axes[1].text(
    x=-140,
    y=0,
    s=r'\textbf{Soot/Radiation} (' + df_co2['Authors (Label)'][0] + ')',
    ha='left',
    va='center',
    fontsize=8,
    color='black',
)

axes[2].barh(
    y = 0,
    width = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Sulfur']['ERF Average [mW/m2]'],
    height = 1.5,
    align='center',
    color = 'blue',
    edgecolor = 'black'
)

average = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Sulfur']['ERF Average [mW/m2]']
lower = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Sulfur']['ERF Lower Errorbar [mW/m2]']
upper = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Sulfur']['ERF Upper Errorbar [mW/m2]']
axes[2].errorbar(
    x = average,
    y = 0,
    xerr = (
        pd.Series([0]),
        abs(average - upper),
    ),
    fmt = 'none',
    capsize = 2,
    ecolor = 'white',
    elinewidth = 1,
)
axes[2].errorbar(
    x = average,
    y = 0,
    xerr = (
        abs(average - lower),
        pd.Series([0])
    ),
    fmt = 'none',
    capsize = 2,
    ecolor = 'black',
    elinewidth = 1,
)

axes[2].text(
    x=-140,
    y=0,
    s=r'\textbf{Sulfur/Radiation} (' + df_co2['Authors (Label)'][0] + ')',
    ha='left',
    va='center',
    fontsize=8,
    color='black',
)

# Water Vapor (H2O)

axes[3].barh(
    y = 0,
    width = df_h2o['ERF Average [mW/m2]'],
    height = 1.5,
    align='center',
    color = 'red',
    edgecolor = 'black'
)

average = df_h2o['ERF Average [mW/m2]']
lower = df_h2o['ERF Lower Errorbar [mW/m2]']
upper = df_h2o['ERF Upper Errorbar [mW/m2]']
axes[3].errorbar(
    x = average,
    y = 0,
    xerr = (
        abs(average - lower),
        pd.Series([0]),
    ),
    fmt = 'none',
    capsize = 2,
    ecolor = 'white',
    elinewidth = 1,
)
axes[3].errorbar(
    x = average,
    y = 0,
    xerr = (
        pd.Series([0]),
        abs(average - upper)
    ),
    fmt = 'none',
    capsize = 2,
    ecolor = 'black',
    elinewidth = 1,
)

axes[3].text(
    x=-140,
    y=0,
    s=r'\textbf{Water Vapor} (' + df_co2['Authors (Label)'][0] + ')',
    ha='left',
    va='center',
    fontsize=8,
    color='black',
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
