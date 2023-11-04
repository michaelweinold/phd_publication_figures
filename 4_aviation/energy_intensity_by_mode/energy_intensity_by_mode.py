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

df_air = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Aircraft',
    usecols = lambda column: column in [
        'year',
        'energy intensity [kJ/pax-km]'
    ],
    dtype={
        'year': int,
        'energy intensity [kJ/pax-km]': float
    },
    header = 0,
    engine = 'openpyxl'
)

df_car = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Cars',
    usecols = lambda column: column in [
        'year',
        'energy intensity [kJ/pax-km]'
    ],
    dtype={
        'year': int,
        'energy intensity [kJ/pax-km]': float
    },
    header = 0,
    engine = 'openpyxl'
)

df_train = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Trains',
    usecols = lambda column: column in [
        'year',
        'energy intensity [kJ/pax-km]'
    ],
    dtype={
        'year': int,
        'energy intensity [kJ/pax-km]': float
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
    ncols = 1,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
)

# AXIS SCALING ###############

# AXIS LIMITS ################

ax.set_xlim(1950, 2023)

# TICKS AND LABELS ###########

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Energy Intensity [kJ/pax-km]")
ax.set_xlabel("Year")

# PLOTTING ###################


ax.plot(
    df_air['year'],
    df_air['energy intensity [kJ/pax-km]'],
    color = 'black',
    label = 'Air (U.S., Domestic Routes)',
    linestyle = '-',
)

ax.plot(
    df_car['year'],
    df_car['energy intensity [kJ/pax-km]'],
    color = 'black',
    label = 'Cars (U.S., \"Light-Duty\")',
    linestyle = '--',
)

ax.plot(
    df_train['year'],
    df_train['energy intensity [kJ/pax-km]'],
    color = 'black',
    label = 'Rail (U.S., Inter-City Routes)',
    linestyle = '-.',
)

 
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