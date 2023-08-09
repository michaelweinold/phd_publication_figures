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

df_average = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Average',
    usecols = lambda column: column in [
        'rail (MJ/pax-km)',
        'bus (MJ/pax-km)',
        'car (MJ/pax-km)',
        'air (MJ/pax-km)'
    ],
    dtype={
        'rail (MJ/pax-km)': float,
        'bus (MJ/pax-km)': float,
        'car (MJ/pax-km)': float,
        'air (MJ/pax-km)': float
    },
    header = 0,
    engine = 'openpyxl'
)
df_history_air = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Air',
    usecols = lambda column: column in [
        'year',
        'energy intensity (BTU/pax-mile)',
        'energy intensity (kJ/pax-km)'
    ],
    dtype={
        'year': int,
        'energy intensity (BTU/pax-mile)': float,
        'energy intensity (kJ/pax-km)': float
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
    df_history_air['year'],
    df_history_air['energy intensity (kJ/pax-km)'],
    color = 'black',
    label = 'Air (U.S. Domestic)',
    linestyle = '-',
)

width = 0.4
x = np.arange(len(labels))
ax.set_xticks(x, labels)
# Japan
ax.bar(
    x = x,
    height = df_japan['rail [%]'],
    width = width,
    label = 'Rail',
    color = 'darkorange',
)

plt.errorbar(
    2017,
    y_bot,
    yerr=(np.zeros_like(y_bot), y_dif),
    capsize=10,
    ecolor='black',
    ls='',
    lw=5,
    capthick=5
)


# LEGEND ####################

axes[0].legend(
    loc = 'lower left',
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