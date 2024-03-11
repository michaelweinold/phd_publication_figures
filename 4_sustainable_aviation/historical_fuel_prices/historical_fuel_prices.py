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

df_fuel = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Jet Fuel Price',
    usecols = lambda column: column in [
        'date',
        'producer price index (1950=100)',
    ],
    dtype={
        'date': datetime,
        'producer price index (1950=100)': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_expenses = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Airline Expense Breakdown',
    usecols = lambda column: column in [
        'year',
        'labour expense [%]',
        'fuel expense [%]',
        'other expense [%]',
    ],
    dtype={
        'year': int,
        'labour expense [%]': float,
        'fuel expense [%]': float,
        'other expense [%]': float,
    },
    parse_dates=['year'],
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

df_fuel['producer price index (1950=100)'] = df_fuel['producer price index (1950=100)'] / 100

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 2,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm,
        gridspec_kw = dict(
            height_ratios=[3,1],
        ),
        sharex=True
    )

# DATA #######################

# AXIS LIMITS ################

ax[0].set_xlim(
    datetime.strptime('1949', '%Y'),
    datetime.strptime('2023', '%Y')
)
ax[0].set_ylim(1,65)

ax[1].set_ylim(0, 100)

# TICKS AND LABELS ###########

ax[0].minorticks_on()
ax[0].tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

ax[0].grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax[0].grid(which='major', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax[0].set_ylabel("Producer Price Index \n (Aviation Fuel) [1950=1]")
ax[1].set_xlabel("Year")
ax[1].set_ylabel("Airline \n Expenses [\%]")

# PLOTTING ###################

ax[0].plot(
    df_fuel['date'],
    df_fuel['producer price index (1950=100)'],
    color = 'black',
    linewidth = 1,
    label = 'Jet Fuel (Kerosene)'
)
ax[1].bar(
    x = df_expenses['year'],
    height = df_expenses['fuel expense [%]'],
    width=200,
    bottom=None,
    align='center',
    color = 'purple'
)
ax[1].bar(
    x = df_expenses['year'],
    height = df_expenses['labour expense [%]'],
    width=200,
    bottom=df_expenses['fuel expense [%]'],
    align='center',
    color = 'green'
)
ax[1].bar(
    x = df_expenses['year'],
    height = df_expenses['other expense [%]'],
    width=200,
    bottom=df_expenses['fuel expense [%]'] + df_expenses['labour expense [%]'],
    align='center',
    color = 'orange'
)

# LEGEND ####################

import matplotlib.patches as patches

legend_elements = [
    patches.Patch(
        facecolor = 'purple',
        edgecolor = 'none',
        label = 'Fuel'
    ),
    patches.Patch(
        facecolor = 'green',
        edgecolor = 'none',
        label = 'Labour'
    ),
    patches.Patch(
        facecolor = 'orange',
        edgecolor = 'none',
        label = 'Other'
    ),
]
ax[0].legend(
    handles=legend_elements,
    loc='lower left',
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
