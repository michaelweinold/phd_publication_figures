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

df_acft = pd.read_excel(
    io = '../efficiency/data/data_29-11-2023.xlsx',
    sheet_name = 'data',
    usecols = lambda column: column in [
        'Name',
        'Type',
        'YOI',
        'EU (MJ/ASK)',
    ],
    dtype={
        'Name': str,
        'Type': str,
        'YOI': int,
        'EU (MJ/ASK)': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_annual = pd.read_excel(
    io = 'data/annualdata.xlsx',
    sheet_name = 'Sheet1',
    usecols = lambda column: column in [
        'Year',
        'EU (MJ/ASK)',
    ],
    dtype={
        'Year': int,
        'EU (MJ/ASK)': float,
    },
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

list_dehavilland = ['Comet 1', 'Comet 4']
df_acft_dehavilland = df_acft[df_acft['Name'].isin(list_dehavilland)]

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 1,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
)

# AXIS LIMITS ################

ax.set_xlim(1950, 2024)
ax.set_ylim(0, 9)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# axes[0]IS LABELS ################

ax.set_xlabel('Aircraft Year of Introduction')
ax.set_ylabel("$\eta$ = EU (MJ/ASK)")

# PLOTTING ###################

ax.axvline(x=1958, color='grey', linestyle='-')

ax.scatter(
    df_acft['YOI'],
    df_acft['EU (MJ/ASK)'],
    label = 'Individual Aircraft',
    color = 'black',
    marker = 'o',
)
ax.plot(
    df_annual['Year'],
    df_annual['EU (MJ/ASK)'],
    label = 'US Fleet Average',
    color = 'red',
    linestyle = '--',
    linewidth = 2
)

for index, row in df_acft_dehavilland.iterrows():
    ax.annotate(row['Name'], (row['YOI'], row['EU (MJ/ASK)']), textcoords="offset points", xytext=(10,4), ha='left', bbox=dict(facecolor='white', edgecolor='none'))

# LEGEND ####################

ax.legend(loc = 'upper right')

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