#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# system
import os
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

# DATA MANIPULATION #############################

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 1,
    dpi = 300,
    figsize=(18*cm, 18*cm), # A4=(210x297)mm,
)

# DATA #######################

# AXIS LIMITS ################

# TICKS AND LABELS ###########

# GRIDS ######################

# AXIS LABELS ################

# PLOTTING ###################

# LEGEND ####################

import matplotlib.patches as patches
import matplotlib.lines as lines

# legend number 1

import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 3

legend_1_elements = [
    patches.Patch(
        facecolor='red',
        edgecolor='black'
    ),
    patches.Patch(
        facecolor='red',
        edgecolor='black',
        hatch='///',
    ),
    plt.errorbar(
        x=0,
        y=0,
        xerr=5,
        capsize=5,
        capthick=2,
        fmt='o',
        color='black',
    ),
]

legend_1 = ax.legend(
    handles = legend_1_elements,
    labels = [
        'Total Effect',
        'Sub-Effect',
        '5/95\% Confidence Interval',
    ],
    loc = 'lower left',
    numpoints=1,
    title = 'Metastudy, Best Estimates (Lee et al., 2021)',
    alignment = 'left',
    title_fontproperties={'weight':'bold'},
)
ax.add_artist(legend_1) # required for multiple legends

# legend number 2

legend_2_elements = [
    lines.Line2D(
        [0],
        [1],
        color='black',
        lw=1,
        marker='|',
        linestyle='-',
    ),
]

ax.legend(
    handles = legend_2_elements,
    labels = [
        'Range (High/Low)',
    ],
    loc = 'lower right',
    numpoints=2,
    title = 'Individual Studies',
    alignment = 'left',
    title_fontproperties={'weight':'bold'},
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
