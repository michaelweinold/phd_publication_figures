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

df_main = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'data',
    usecols = lambda column: column in [
        'year',
        'category',
        'country_iso',
        'country_name',
        'country_region',
        'sum(countAc)',
    ],
    dtype={
        'year': int,
        'category': str,
        'country_iso': str,
        'country_name': str,
        'country_region': str,
        'sum(countAc)': int,
    },
    header = 0,
    engine = 'openpyxl',
)

# DATA MANIPULATION #############################

df_total = df_main.groupby('year').sum().reset_index()

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

ax.set_xlim(1949, 2024)

# TICKS AND LABELS ###########

ax.set_xlabel('Year')
ax.set_ylabel('Number of Aircraft in Service')

import matplotlib.ticker as ticker
def thousand_formatter(value, tick_number):
    """
    Formats the tick label with thousand separators: 1000 = 1'000.
    """
    return f"{int(value):,}".replace(",", "'")

ax.yaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################


# PLOTTING ###################


ax.bar(
    x = df_total['year'],
    height = df_total['sum(countAc)'],
    label = 'Total',
    color = 'blue'
)


# LEGEND ####################

ax.legend(
    loc = 'upper left',
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
# %%
