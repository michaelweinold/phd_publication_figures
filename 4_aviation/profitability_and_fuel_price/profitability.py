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

df_profit = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Profit',
    usecols = lambda column: column in [
        'year',
        'plot net profit (2022 BUSD)'
    ],
    dtype={
        'year': int,
        'plot net profit (2022 BUSD)': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_fuelprice = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Fuel Price',
    usecols = lambda column: column in [
        'year',
        'kerosene producer price index (100=2022)'
    ],
    dtype={
        'year': int,
        'kerosene producer price index (100=2022)': float,
    },
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

# FIGURE ########################################

# SETUP ######################

fig, ax1 = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm
)
ax2 = ax1.twinx()

# DATA #######################

# AXIS SCALE #################

# AXIS LIMITS ################

ax1.set_xlim(1949,2024)
ax1.set_ylim(-50,50)
ax2.set_ylim(0,110)

# COLORBAR ###################

#colormap = plt.cm.get_cmap('plasma', len(df_freight['year'].unique()))

# TICKS AND LABELS ###########

ax1.minorticks_on()
ax1.tick_params(axis='x', which='both', bottom=False)
ax1.tick_params(axis='y', which='both', bottom=False)

# GRIDS ######################

ax1.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax1.grid(which='both', axis='x', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

ax1.set_xlabel("Year")
ax1.set_ylabel("Airline Net Profit [2022 BUSD]")
ax2.set_ylabel("U.S. Producer Price Index (2022=100)")

# PLOTTING ###################

ax1.bar(
    x = df_profit['year'],
    height = df_profit['plot net profit (2022 BUSD)'],
    width = 0.8,
    bottom = None,
    align = 'center',
    label = 'World Airlines Net Profit'
)
ax2.plot(
    df_fuelprice['year'],
    df_fuelprice['kerosene producer price index (100=2022)'],
    color = 'black',
    label = 'Kerosene and Jet Fuels'
)

# LEGEND ####################

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(
    lines + lines2,
    labels + labels2,
    loc='upper left',
)

# TITLE #####################


# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%