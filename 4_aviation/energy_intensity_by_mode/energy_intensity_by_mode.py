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

df_air = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Aircraft',
    usecols = lambda column: column in [
        'year',
        'energy intensity [kJ/pax-km]'
    ],
    dtype={
        'year': int,
        'energy intensity [kJ/pax-km]': float
    },
    header = 0,
    engine = 'openpyxl'
)

df_car = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Cars',
    usecols = lambda column: column in [
        'year',
        'energy intensity [kJ/pax-km]'
    ],
    dtype={
        'year': int,
        'energy intensity [kJ/pax-km]': float
    },
    header = 0,
    engine = 'openpyxl'
)

df_train = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Trains',
    usecols = lambda column: column in [
        'year',
        'energy intensity [kJ/pax-km]'
    ],
    dtype={
        'year': int,
        'energy intensity [kJ/pax-km]': float
    },
    header = 0,
    engine = 'openpyxl'
)

df_average = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Averages',
    usecols = lambda column: column in [
        'mode',
        'energy intensity lower [kJ/pax-km]',
        'energy intensity upper [kJ/pax-km]',
        'energy intensity average [kJ/pax-km]',
    ],
    dtype={
        'mode': str,
        'energy intensity lower [kJ/pax-km]': float,
        'energy intensity upper [kJ/pax-km]': float,
        'energy intensity average [kJ/pax-km]': float,
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
    ncols = 2,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
    gridspec_kw={'width_ratios': [9, 1]}
)
fig.subplots_adjust(wspace=0.05)  # Adjust horizontal spacing. Use a value that suits your needs.


# AXIS SCALING ###############

# AXIS LIMITS ################

ax[0].set_xlim(1950, 2023)
ax[0].set_ylim(0, 7000)

ax[1].set_xlim(-0.5, 2.5)
ax[1].set_ylim(0, 7000)

# TICKS AND LABELS ###########

ax[1].set_yticklabels([]) # no y-tick labels
ax[1].set_xticks([])

# GRIDS ######################

for axis in ax:
    axis.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
    axis.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax[0].set_ylabel("Energy Intensity [kJ/pax-km]")
ax[0].set_xlabel("Year")

ax[1].set_xlabel("2018 Averages")

# PLOTTING ###################


ax[0].plot(
    df_air['year'],
    df_air['energy intensity [kJ/pax-km]'],
    color = 'black',
    label = 'Air (U.S., Domestic Routes)',
    linestyle = '-',
)

ax[0].plot(
    df_car['year'],
    df_car['energy intensity [kJ/pax-km]'],
    color = 'black',
    label = 'Cars (U.S., \"Light-Duty\")',
    linestyle = '--',
)

ax[0].plot(
    df_train['year'],
    df_train['energy intensity [kJ/pax-km]'],
    color = 'black',
    label = 'Rail (U.S., Inter-City Routes)',
    linestyle = '-.',
)

labels = ['Air', 'Cars', 'Rail']  # replace with your actual labels

ax[1].set_xticks(np.arange(len(labels)))  # set x-ticks at the positions of the labels
ax[1].set_xticklabels(labels, rotation=90)  # set x-tick labels and rotate them 90 degrees
ax[1].xaxis.tick_top()  # move x-ticks to the top

ax[1].xaxis.set_tick_params(pad=-120)

ax[1].plot(
    0,
    df_average[df_average['mode'] == 'air']['energy intensity average [kJ/pax-km]'],
    color = 'black',
    marker = 'o',
)
ax[1].errorbar(
    x = 0,
    y = df_average[df_average['mode'] == 'air']['energy intensity average [kJ/pax-km]'],
    yerr = [
        df_average[df_average['mode'] == 'air']['energy intensity lower [kJ/pax-km]'],
        df_average[df_average['mode'] == 'air']['energy intensity upper [kJ/pax-km]'],
    ],
    color = 'black',
    capsize = 3,
    capthick = 1,
)

ax[1].plot(
    1,
    df_average[df_average['mode'] == 'car']['energy intensity average [kJ/pax-km]'],
    color = 'black',
    marker = 'o',
)
ax[1].errorbar(
    x = 1,
    y = df_average[df_average['mode'] == 'car']['energy intensity average [kJ/pax-km]'],
    yerr = [
        df_average[df_average['mode'] == 'car']['energy intensity lower [kJ/pax-km]'],
        df_average[df_average['mode'] == 'car']['energy intensity upper [kJ/pax-km]'],
    ],
    color = 'black',
    capsize = 3,
    capthick = 1,
)

ax[1].plot(
    2,
    df_average[df_average['mode'] == 'rail']['energy intensity average [kJ/pax-km]'],
    color = 'black',
    marker = 'o',
)
ax[1].errorbar(
    x = 2,
    y = df_average[df_average['mode'] == 'rail']['energy intensity average [kJ/pax-km]'],
    yerr = [
        df_average[df_average['mode'] == 'rail']['energy intensity lower [kJ/pax-km]'],
        df_average[df_average['mode'] == 'rail']['energy intensity upper [kJ/pax-km]'],
    ],
    color = 'black',
    capsize = 3,
    capthick = 1,
)
 
# LEGEND ####################

ax[0].legend(
    loc = 'upper right',
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