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

df_japan = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Japan',
    usecols = lambda column: column in [
        'distance bin [km]',
        'distance mean [km]',
        'rail [%]',
        'car [%]',
        'air [%]',
        'other [%]',
        'year'
    ],
    dtype={
        'distance bin [km]': str,
        'distance mean [km]': float,
        'rail [%]': float,
        'car [%]': float,
        'air [%]': float,
        'other [%]': float,
        'year': str
    },
    header = 0,
    engine = 'openpyxl'
)
df_eu = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'EU',
    usecols = lambda column: column in [
        'distance [km]',
        'rail [%]',
        'car [%]',
        'air [%]',
        'other [%]',
        'year'
    ],
    dtype={
        'distance [km]': str,
        'rail [%]': float,
        'car [%]': float,
        'air [%]': float,
        'other [%]': float,
        'year': str
    },
    header = 0,
    engine = 'openpyxl'
)
		
# DATA MANIPULATION #############################

df_japan = df_japan[df_japan['year'] == '2019?']

mypol = np.polynomial.polynomial.Polynomial.fit(
    x = df_japan['distance mean [km]'],
    y = df_japan['rail [%]'],
    deg = 3,
    domain=None
)

# FIGURE ########################################

# SETUP ######################

fig, axes = plt.subplots(
    num = 'main',
    sharey = True,
    sharex = True,
    nrows = 1,
    ncols = 3,
    gridspec_kw = {'wspace': 0.1},
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
)

# AXIS SCALING ###############

# AXIS LIMITS ################

for ax in axes.flat:
    ax.set_ylim(0, 100)

# TICKS AND LABELS ###########

labels = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
for ax in axes.flat:
    ax.set_xticks(
        ticks = labels,
        labels = labels,
        rotation=45,
        ha='right'
    )

# GRIDS ######################

for ax in axes.flat:
    ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
    ax.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

axes[0].set_ylabel("Modal Share [\%]")
for ax in axes.flat:
    ax.set_xlabel("Trip Distance [km]")

# TITLE ######################

axes[0].set_title("EU (2015)", pad=7.5)
axes[1].set_title("Japan (2019)", pad=7.5)
axes[2].set_title("USA (2001)", pad=7.5)

# PLOTTING ###################

width = 0.4
x = np.arange(len(labels))
axes[0].set_xticks(x, labels)

# EU
axes[0].bar(
    x = x,
    height = df_eu['rail [%]'],
    width = width,
    label = 'Rail',
    color = 'darkorange',
)
axes[0].bar(
    x = x,
    bottom = df_eu['rail [%]'],
    height = df_eu['air [%]'],
    width = width,
    label = 'Air',
    color = 'royalblue',
)
axes[0].bar(
    x = x,
    bottom = df_eu['rail [%]'] + df_eu['air [%]'],
    height = df_eu['car [%]'],
    width = width,
    label = 'Car',
    color = 'brown',
)
axes[0].bar(
    x = x,
    bottom = df_eu['rail [%]'] + df_eu['air [%]'] + df_eu['car [%]'],
    height = df_eu['other [%]'],
    width = width,
    label = 'Other',
    color = 'grey',
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
# %%
