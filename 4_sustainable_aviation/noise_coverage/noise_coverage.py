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
    'font.size': 12
})

# DATA IMPORT ###################################

df_baseline = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'baseline',
    usecols = lambda column: column in [
        'year',
        'area [km2]',
    ],
    dtype={
        'year': float,
        'area [km2]': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_lowtech = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'low_tech',
    usecols = lambda column: column in [
        'year',
        'area [km2]',
    ],
    dtype={
        'year': float,
        'area [km2]': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_modtech = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'mod_tech',
    usecols = lambda column: column in [
        'year',
        'area [km2]',
    ],
    dtype={
        'year': float,
        'area [km2]': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_advtech = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'adv_tech',
    usecols = lambda column: column in [
        'year',
        'area [km2]',
    ],
    dtype={
        'year': float,
        'area [km2]': float,
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
    figsize=(10*cm, 10*cm), # A4=(210x297)mm,
)

# AXIS LIMITS ################

ax.set_xlim(2010, 2050)
#ax.set_ylim(0, 9)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)

import matplotlib.ticker as ticker
def thousand_formatter(value, tick_number):
    """
    Formats the tick label with thousand separators: 1000 = 1'000.
    """
    return f"{int(value):,}".replace(",", "'")

ax.yaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))


# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# axes[0]IS LABELS ################

ax.set_ylabel("Area where DNL$>$55dB(A) [km$^2$] \n (DNL = Day-Night Average Sound Level)")

# PLOTTING ###################

ax.plot(
    df_baseline['year'],
    df_baseline['area [km2]'],
    label = 'Baseline Forecast',
    color = 'black',
    linestyle = '-',
    linewidth = 1,
)
ax.plot(
    df_lowtech['year'],
    df_lowtech['area [km2]'],
    label = 'Low Tech Scenario',
    color = 'red',
    linestyle = '--',
    linewidth = 1,
)
ax.plot(
    df_modtech['year'],
    df_modtech['area [km2]'],
    label = 'Moderate Tech Scenario',
    color = 'green',
    linestyle = '--',
    linewidth = 1,
)
ax.plot(
    df_advtech['year'],
    df_advtech['area [km2]'],
    label = 'Advanced Tech Scenario',
    color = 'blue',
    linestyle = '--',
    linewidth = 1,
)

# LEGEND ####################

ax.legend(loc = 'upper left')

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