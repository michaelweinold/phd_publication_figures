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

df_nox = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'NOx',
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

# see also:
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subfigures.html

fig = plt.figure(
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm
)

# AXIS LIMITS ################



# PLOTTING ###################

# CO2

ax0 = fig.add_axes(
    rect = (0,0,1,0.15),
    label = 'CO2'
)

ax0.set_xlim(-150,150)
ax0.set_ylim(-1,1)

ax0.barh(
    y = 0,
    width = df_co2['ERF Average [mW/m2]'],
    height = 1,
    align='center',
    color = 'red',
    edgecolor = 'black'
)

ax1 = fig.add_axes(
    rect = (0,0.25,1,0.15),
    label = 'CO3'
)

ax1.set_xlim(-150,150)
ax1.set_ylim(-1,1)

ax1.barh(
    y = 0,
    width = df_co2['ERF Average [mW/m2]'],
    height = 1,
    align='center',
    color = 'red',
    edgecolor = 'black'
)

ax2 = fig.add_axes(
    rect = (0,0.45,1,0.3),
    label = 'CO2'
)

ax2.set_xlim(-150,150)
ax2.set_ylim(-1,1)

ax2.barh(
    y = 0,
    width = df_co2['ERF Average [mW/m2]'],
    height = 0.5,
    align='center',
    color = 'red',
    edgecolor = 'black'
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
