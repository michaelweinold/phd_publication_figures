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

# DATA MANIPULATION #############################

# select only latest datapoint for Switzerland
df_share.drop(df_share[(df_share['country'] == 'Switzerland') & (df_share['year'] != 2019)].index, inplace=True)

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(13*cm, 10*cm), # A4=(210x297)mm,
    )

# AXIS SCALING ###############

ax.set_yscale('log')

# AXIS LIMITS ################

ax.set_ylim(0.1, 100)

# TICKS AND LABELS ###########

import matplotlib.ticker as ticker
def thousand_formatter(value, tick_number):
    """
    Formats the tick label with thousand separators: 1000 = 1'000.
    """
    return f"{int(value):,}".replace(",", "'")

ax.yaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Share of Air Freight in Total Trade [\%]")

# PLOTTING ###################

width = 0.4
multiplier = 0
x = np.arange(len(df_share['country']))
ax.set_xticks(x + width/2, df_share['country'])

for category in ['share of air freight (weight)', 'share of air freight (value)']:
    offset = width * multiplier
    rects = ax.bar(
        x = x + offset,
        height = df_share[category],
        width = width,
    )
    ax.bar_label(
        rects,
        padding=3,
        fmt = '%.2f'
    )
    multiplier += 1

# LEGEND ####################

from matplotlib.patches import Patch

legend_categories = [
    Patch(
        facecolor = 'orange',
        label = 'Value'
    ),
    Patch(
        facecolor = 'cornflowerblue',
        label = 'Weight'
    ),
]

legend_categories = ax.legend(
    handles = legend_categories,
    loc = 'upper left',
)
ax.add_artist(legend_categories)

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