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

df_share = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'share of air freight',
    usecols = lambda column: column in [
        'year',
        'country',
        'share of air freight (weight)',
        'share of air freight (value)',
    ],
    dtype={
        'year': int,
        'country': str,
        'share of air freight (weight)': float,
        'share of air freight (value)': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_us_trade = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'US air freight trade',
    usecols = lambda column: column in [
        'weight (1000 tons)',
        'value (mio. $(2022))',
        'country (import/export to U.S.)',
    ],
    dtype={
        'weight (1000 tons)': float,
        'value (mio. $(2022))': float,
        'country (import/export to U.S.)': str,
    },
    header = 0,
    engine = 'openpyxl'
)
		
# DATA MANIPULATION #############################

# select only latest datapoint for Switzerland
df_share.drop(df_share[(df_share['country'] == 'Switzerland') & (df_share['year'] != 2019)].index, inplace=True)

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 2,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm,
    )

# AXIS SCALING ###############

ax[0].set_yscale('log')

# AXIS LIMITS ################

ax[0].set_ylim(0, 100)
ax[0].set_xlim(0, 3)

ax[1].set_xlim(0, 700)
ax[1].set_ylim(0, 80000)

# TICKS AND LABELS ###########

ax[1].minorticks_on()
ax[1].tick_params(axis='x', which='minor', bottom=False)

import matplotlib.ticker as ticker
def thousand_formatter(value, tick_number):
    """
    Formats the tick label with thousand separators: 1000 = 1'000.
    """
    return f"{int(value):,}".replace(",", "'")

ax[1].yaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))

# GRIDS ######################

ax[1].grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax[1].grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax[0].set_xlabel("Countries")
ax[0].set_ylabel("Share of Air Freight in Total Trade [\%]")

ax[1].set_xlabel("Trade by Air Freight (Tonnage) [kt]")
ax[1].set_ylabel("Trade by Air Freight (Value) [mio. USD]")

# PLOTTING ###################

width = 0.5
multiplier = 0
x = np.arange(len(df_share['country']))

for category in ['share of air freight (weight)', 'share of air freight (value)']:
    offset = width * multiplier
    ax[0].bar(
        x = x + offset,
        height = df_share[category],
        width = width,
        label = df_share['country'],
    )
    multiplier += 1

ax[1].scatter(
    df_us_trade['weight (1000 tons)'],
    df_us_trade['value (mio. $(2022))'],
    color = 'blue',
    s = 10,
)

# LEGEND ####################


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