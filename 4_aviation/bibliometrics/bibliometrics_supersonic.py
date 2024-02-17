#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# sys
import os
# plotting
import matplotlib.pyplot as plt
# unit conversion
cm = 1/2.54 # for inches-cm conversion
# time manipulation
from datetime import datetime
# data science
import numpy as np
import pandas as pd

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 12
})

# DATA IMPORT ###################################

df_allaviation = pd.read_csv(
    filepath_or_buffer = 'data/scopus_trend_all_aviation.csv',
    sep = ',',
    decimal = '.',
    index_col = 0,
    parse_dates = False,
    encoding = 'utf-8',
).reset_index()

df_supersonic = pd.read_csv(
    filepath_or_buffer = 'data/scopus_trend_supersonic.csv',
    sep = ',',
    decimal = '.',
    index_col = 0,
    parse_dates = False,
    encoding = 'utf-8'
).reset_index()

# DATA MANIPULATION #############################

df_supersonic['relative_result'] = df_supersonic['RESULT'] / df_allaviation['RESULT']

# FIGURE ########################################

# SETUP ######################

fig, axes = plt.subplots(
    num = 'main',
    nrows = 2,
    ncols = 1,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
    sharex=True
)

# SECONDARY AXES ##############

# AXIS LIMITS ################

axes[0].set_xlim(1945, 2024)
axes[1].set_ylim(0, 1.5)

# TICKS AND LABELS ###########

axes[0].minorticks_on()
axes[0].tick_params(axis='x', which='minor', bottom=True)

# GRIDS ######################

for ax in axes:
    ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
    ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
    ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
    ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# axes[0]IS LABELS ################

axes[0].set_ylabel("\"M$>$1\" Research \n [\# of Publs.]")
axes[1].set_ylabel("\"M$>$1\" Research \n [\% Aviation Publs.]")

# PLOTTING ###################

axes[0].bar(
    df_supersonic['YEAR'],
    df_supersonic['RESULT'],
    color = 'black',
    label = 'Supersonic'
)
axes[0].text(
    x = 0.01,  # Relative x-coordinate
    y = 0.9,   # Relative y-coordinate
    s = r'\texttt{TITLE-ABS-KEY(aviation OR aircraft) AND SUBJAREA(EART OR ENER OR ENGI OR ENVI OR MATE OR MATH OR PHYS)}',
    ha = 'left',
    va = 'center',
    fontsize = 10,
    color = 'black',
    transform = axes[0].transAxes,  # Use axis coordinates
    backgroundcolor = 'white'
)

axes[1].bar(
    df_supersonic['YEAR'],
    df_supersonic['relative_result'],
    color = 'black',
    label = 'All Aviation'
)
axes[1].text(
    x = 0.01,  # Relative x-coordinate
    y = 0.9,   # Relative y-coordinate
    s = r'\texttt{TITLE-ABS-KEY(supersonic AND aircraft) AND SUBJAREA(EART OR ENER OR ENGI OR ENVI OR MATE OR MATH OR PHYS)}',
    ha = 'left',
    va = 'center',
    fontsize = 10,
    color = 'black',
    transform = axes[1].transAxes,  # Use axis coordinates
    backgroundcolor = 'white'
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
# %%
