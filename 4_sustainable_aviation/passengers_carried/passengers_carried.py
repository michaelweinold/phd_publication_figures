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

df_rail = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Rail Travel Price per Distance',
    usecols = lambda column: column in [
        'year',
        'fare/101km [EURO, 2022]',
    ],
    dtype={
        'year': datetime,
        'fare/101km [EURO, 2022]': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_air = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Air Travel Price per Distance',
    usecols = lambda column: column in [
        'year',
        'revenue/mile [U.S. cents, 2023]',
    ],
    dtype={
        'year': datetime,
        'revenue/mile [U.S. cents, 2023]': float,
    },
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

df_rail.replace('', np.nan)
df_air['revenue/km [U.S. cents, 2023]'] = df_air['revenue/mile [U.S. cents, 2023]'] * 1.609

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

ax_right = ax.twinx()

# AXIS LIMITS ################

ax.set_xlim(1950, 2023)
ax.set_ylim(0,110)
ax_right.set_ylim(0,110)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Approx. Air Fare [U.S. cents/km (2022)]")
ax_right.set_ylabel("Approx. Rail Fare [Euro cents/km (2022)]")

# PLOTTING ###################

ax.plot(
    df_air['year'],
    df_air['revenue/km [U.S. cents, 2023]'],
    color = 'black',
    linewidth = 1,
    label = 'Price Index (Air Travel, U.S. Domestic Routes)'
)
ax_right.plot(
    df_rail['year'],
    df_rail['fare/101km [EURO, 2022]'],
    color = 'black',
    linewidth = 1,
    label = 'Consumer Price Index (U.S. Urban Consumers)',
    linestyle = '--'
)


# LEGEND ####################

from matplotlib.lines import Line2D
legend_elements = [
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'black',
        linestyle = '-',
        label='Air (U.S., Domestic Routes)'
    ),
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'black',
        linestyle = '--',
        label='Rail (Germany, Domestic Routes $>100$km)'
    )
]

ax.legend(
    handles=legend_elements,
    loc='upper right',
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
