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

df_priceindex = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Air Travel Price Index',
    usecols = lambda column: column in [
        'year',
        'figure price index',
        'cpi'
    ],
    dtype={
        'year': datetime,
        'figure price index': float,
        'cpi': float
    },
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

df_priceindex['figure price index'] = df_priceindex['figure price index'] / 100
df_priceindex['cpi'] = df_priceindex['cpi'] / 100

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm,
        sharex=True
    )

# SECONDARY AXES ##############

ax_delta = ax.twinx()

# AXIS LIMITS ################

ax.set_xlim(1950, 2023)
ax.set_ylim(0,15)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Price Indices [1950=1]")
ax_delta.set_ylabel("$\Delta$ Price Indices")

# PLOTTING ###################

ax.plot(
    df_priceindex['year'],
    df_priceindex['figure price index'],
    color = 'black',
    linewidth = 1,
    label = 'Price Index (Air Travel, U.S. Domestic Routes)'
)
ax.plot(
    df_priceindex['year'],
    df_priceindex['cpi'],
    color = 'black',
    linewidth = 1,
    label = 'Consumer Price Index (U.S. Urban Consumers)',
    linestyle = '--'
)

ax_delta.plot(
    df_priceindex['year'],
    df_priceindex['cpi'] - df_priceindex['figure price index'],
    color = 'blue',
    linewidth = 1,
    label = 'Consumer Price Index (U.S. Urban Consumers)'
)

ax_delta.axhline(y=0, color='black')


# LEGEND ####################

from matplotlib.lines import Line2D
legend_elements = [
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'black',
        linestyle = '-',
        label='Price Index (Air Travel, U.S. Domestic Routes)'
    ),
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'black',
        linestyle = '--',
        label='Consumer Price Index (U.S. Urban Consumers)'
    ),
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'blue',
        linestyle = '-',
        label='$\Delta$ Price Indices'
    ),
]


ax.legend(
    handles=legend_elements,
    loc='upper left',
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
