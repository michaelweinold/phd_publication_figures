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

df_fossil_price = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Fossil Price',
    usecols = lambda column: column in [
        'year',
        'jet fuel price ($(2020)/t)',
    ],
    dtype={
        'year': int,
        'jet fuel price ($(2020)/t)': float,
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
        figsize=(4*cm, 6*cm), # A4=(210x297)mm,
    )

# DATA #######################

# AXIS LIMITS ################

ax.set_xlim(1990, 2023)
ax.set_ylim(0, 1000)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

import matplotlib.ticker as ticker
def thousand_formatter(value, tick_number):
    """
    Formats the tick label with thousand separators: 1000 = 1'000.
    """
    return f"{int(value):,}".replace(",", "'")

ax.yaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Jet Fuel Price \n [\$(2020)/t(weight)]")

# PLOTTING ###################

ax.plot(
    df_fossil_price['year'],
    df_fossil_price['jet fuel price ($(2020)/t)'],
    color = 'black',
    label = 'Fossil'
)

# LEGEND ####################


# EXPORT #########################################

import os 
file_path = os.path.abspath(__file__)
file_name = os.path.splitext(os.path.basename(file_path))[0]
figure_name: str = str(file_name + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)