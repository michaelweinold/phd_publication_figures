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

df = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Sheet1',
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

# DATA MANIPULATION #############################

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm
)

# DATA #######################

# AXIS SCALE #################

# AXIS LIMITS ################

ax.set_xlim(1949,2024)
ax.set_ylim(-50,50)

# COLORBAR ###################

#colormap = plt.cm.get_cmap('plasma', len(df_freight['year'].unique()))

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='both', bottom=False)
ax.tick_params(axis='y', which='both', bottom=False)

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

ax.set_xlabel("Year")
ax.set_ylabel("Airline Net Profit [2022 BUSD]")

# PLOTTING ###################

ax.bar(
    x = df['year'],
    height = df['plot net profit (2022 BUSD)'],
    width = 0.8,
    bottom = None,
    align = 'center',
)

# LEGEND ####################


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