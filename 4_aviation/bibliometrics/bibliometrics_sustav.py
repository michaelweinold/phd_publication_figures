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
    'font.size': 11
})

# DATA IMPORT ###################################

df_google = pd.read_csv(
    filepath_or_buffer = 'data/google_trend_sustav.csv',
    sep = ',',
    decimal = '.',
    index_col = 0,
    parse_dates = True,
    encoding = 'utf-8'
).reset_index()

df_scopus_sustav = pd.read_csv(
    filepath_or_buffer = 'data/scopus_trend_sustav.csv',
    sep = ',',
    decimal = '.',
    index_col = 0,
    parse_dates = True,
    encoding = 'utf-8'
).reset_index()

df_scopus_allaviation = pd.read_csv(
    filepath_or_buffer = 'data/scopus_trend_all_aviation.csv',
    sep = ',',
    decimal = '.',
    index_col = 0,
    parse_dates = True,
    encoding = 'utf-8'
).reset_index()

# DATA MANIPULATION #############################

df_scopus_allaviation = df_scopus_allaviation.merge(df_scopus_sustav[['YEAR']], on='YEAR', how='inner')

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 1,
    dpi = 300,
    figsize=(30*cm, 5*cm), # A4=(210x297)mm,
)
ax1 = ax.twinx()

# SECONDARY AXES ##############

# AXIS LIMITS ################

ax.set_xlim(
    datetime(2005, 1, 1),  # Start date
    datetime(2024, 12, 31)  # End date
)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Google Search Inter. [\%]")
ax1.set_ylabel("\"SustAv\" Research \n [\% of all Aviation Publs.]", color='blue')

# PLOTTING ###################

ax1.bar(
    df_scopus['YEAR'],
    df_scopus['RESULT'] / df_scopus_allaviation['RESULT'],
    color = 'blue',
    width = 100,
    label = 'Scientific Publications'
)
ax.plot(
    df_google['YEARMONTH'],
    df_google['SEARCHINTEREST'],
    color = 'black',
    linestyle = '-',
    linewidth = 1.5,
    label = 'Google Search Interest'
)

ax1.text(
    x = 0.01,  # Relative x-coordinate
    y = 0.9,   # Relative y-coordinate
    s = r'\texttt{TITLE-ABS-KEY(sustainab* AND aviation) AND SUBJAREA(EART OR ENER OR ENGI OR ENVI OR MATE OR MATH OR PHYS)}',
    ha = 'left',
    va = 'center',
    fontsize = 10,
    color = 'black',
    transform = ax1.transAxes,  # Use axis coordinates
    backgroundcolor = 'white'
)


# LEGEND ####################

# Get the handles and labels from both axes
handles1, labels1 = ax.get_legend_handles_labels()
handles2, labels2 = ax1.get_legend_handles_labels()

# Combine the handles and labels
handles = handles1 + handles2
labels = labels1 + labels2

ax.legend(
    handles=handles,
    labels=labels,
    loc=(0.01, 0.49),
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