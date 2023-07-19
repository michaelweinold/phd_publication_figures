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

df_slf = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Aircraft',
    usecols = lambda column: column in [
        'year',
        'plf',
    ],
    dtype={
        'year': int,
        'plf': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_occupancy = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Rail (Germany)',
    usecols = lambda column: column in [
        'year',
        'occupancy rate',
    ],
    dtype={
        'year': int,
        'occupancy rate': float,
    },
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

df_slf['plf'] = df_slf['plf'] * 100

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 1,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm
)

# AXIS LIMITS ################

plt.xlim(1950, 2023)
plt.ylim(0, 100)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='y', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_xlabel("Year")
ax.set_ylabel("Seat Load Factor [\%]")

# PLOTTING ###################

ax.plot(
    df_slf['year'],
    df_slf['plf'],
    color = 'black',
    label = 'Air Transport Seat Load Factor (U.S.)',
    linestyle = '-',
)
ax.plot(
    df_occupancy['year'],
    df_occupancy['occupancy rate'],
    color = 'black',
    label = 'Rail Transport Occupancy Rate (Germany)',
    linestyle = '--',
)

# LEGEND #####################

ax.legend(loc='upper left')

# ANNOTATIONS ###############

ax.axvline(x=1978, color='black', linestyle='--')
ax.annotate(
    'U.S. Airline Deregulation Act',  # Text to display in the annotation box
    xy=(1978+1, 5),  # Position of the upper end of the vertical line
    ha='left',  # Horizontal alignment of the text
    va='bottom'  # Vertical alignment of the text
)

ax.axvline(x=1973, color='black', linestyle='--')
ax.annotate(
    '1973 Oil Crisis',  # Text to display in the annotation box
    xy=(1973-1, 5),  # Position of the upper end of the vertical line
    ha='right',  # Horizontal alignment of the text
    va='bottom'  # Vertical alignment of the text
)

ax.axvline(x=2019, color='black', linestyle='--')
ax.annotate(
    'COVID Lockdowns',  # Text to display in the annotation box
    xy=(2020-2, 5),  # Position of the upper end of the vertical line
    ha='right',  # Horizontal alignment of the text
    va='bottom'  # Vertical alignment of the text
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