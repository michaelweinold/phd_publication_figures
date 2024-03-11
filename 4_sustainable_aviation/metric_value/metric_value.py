#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# sys
import os
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

df_trendline = pd.read_excel(
    io = 'data/data.xlsx', 
    sheet_name = 'trendline',
    usecols = lambda column: column in [
        'year',
        'metric value [kg/km]',
    ],
    dtype={
        'year': float,
        'metric value [kg/km]': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)
df_sa_acft = pd.read_excel(
    io = 'data/data.xlsx', 
    sheet_name = 'sa_acft',
    usecols = lambda column: column in [
        'year',
        'metric value [kg/km]',
    ],
    dtype={
        'year': int,
        'metric value [kg/km]': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)
df_sta_acft = pd.read_excel(
    io = 'data/data.xlsx', 
    sheet_name = 'sta_acft',
    usecols = lambda column: column in [
        'year',
        'metric value [kg/km]',
    ],
    dtype={
        'year': int,
        'metric value [kg/km]': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)
df_my_acft = pd.read_excel(
    io = 'data/data.xlsx', 
    sheet_name = 'my_acft',
    usecols = lambda column: column in [
        'year',
        'metric value [kg/km]',
    ],
    dtype={
        'year': int,
        'metric value [kg/km]': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
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

# SECONDARY AXES ##############

# AXIS LIMITS ################

ax.set_xlim(1960,2040)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("\"CO$_2$ Emissions Evaluation Metric\" [kg/km]")

# PLOTTING ###################

ax.plot(
    df_trendline['year'],
    df_trendline['metric value [kg/km]'],
    label = 'All Size Average (Delivery Year)',
    color = 'black',
    linestyle = '-',
    linewidth = 2,
)
ax.scatter(
    df_sa_acft['year'],
    df_sa_acft['metric value [kg/km]'],
    label = 'Single-Isle',
    color = 'blue',
    marker = 'o',
)
ax.scatter(
    df_sta_acft['year'],
    df_sta_acft['metric value [kg/km]'],
    label = 'Small Twin-Aisle',
    color = 'red',
    marker = 'o',
)
"""
ax.scatter(
    df_my_acft['year'],
    df_my_acft['metric value [kg/km]'],
    label = 'Large Twin-Aisle',
    color = 'green',
    marker = 'o',
)
"""

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