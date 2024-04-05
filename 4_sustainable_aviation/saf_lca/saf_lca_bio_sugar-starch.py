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

# see also this StackOverflow questions:
# https://stackoverflow.com/q/22787209
# https://stackoverflow.com/q/69242928
# it will be best to have separate plots for each country

df_bio_sugar_co2 = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'CO2 Bio-SugarStarch Fuel',
    usecols = lambda column: column in [
        'feedstock',
        'region',
        'LSf [gCO2e/MJ]'
    ],
    dtype={
        'feedstock': str,
        'region': str,
        'LSf [gCO2e/MJ]': float
    },
    header = 0,
    engine = 'openpyxl'
)
		
# DATA MANIPULATION #############################


# FIGURE ########################################

# SETUP ######################

fig, axes = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 3,
    gridspec_kw = {'wspace': 0.6},
    dpi = 300,
    figsize=(9*cm, 6*cm), # A4=(210x297)mm,
)

# AXIS SCALING ###############

# AXIS LIMITS ################

axes[0].set_ylim(-30, 100)
axes[1].set_ylim(0, 600)
axes[2].set_ylim(120, 2200)

# TICKS AND LABELS ###########

axes[0].set_xticks([])
axes[0].set_xticklabels([])

axes[1].set_xticks([])
axes[1].set_xticklabels([])

axes[2].tick_params(axis='x', labelrotation=90)

for axis in axes:
    axis.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
    axis.grid(which='major', axis='x', linestyle='--', linewidth = 0.5)

import matplotlib.ticker as ticker

def thousands(x, pos):
    'The two args are the value and tick position'
    return '%1.1f' % (x * 1e-3) if x >= 1000 else '%1.2f' % (x * 1e-3)

formatter = ticker.FuncFormatter(thousands)

axes[2].yaxis.set_major_formatter(formatter)

# AXIS LABELS ################


# TITLE ######################

axes[0].set_title('[CO$_2$/MJ]', fontsize=10)
axes[1].set_title('[Mt(weight)]', fontsize=10)
axes[2].set_title('[k\$(2023)]', fontsize=10)

# PLOTTING ###################

axes[0].violinplot(
    df_bio_sugar_co2['LSf [gCO2e/MJ]'],
    #showfliers = True
)
axes[0].axhline(y=86, color='red', linestyle='--')


axes[1].axhline(y=350, color='red', linestyle='--')


axes[2].axhspan(
    ymin = 140,
    ymax = 750,
    facecolor='red',
    alpha=0.25
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