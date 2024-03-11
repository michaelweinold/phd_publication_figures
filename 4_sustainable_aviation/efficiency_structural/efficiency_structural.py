#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

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

df_eff = pd.read_excel(
    io = '../efficiency/data/data_29-11-2023.xlsx',
    sheet_name = 'data',
    usecols = lambda column: column in [
        'Name',
        'Type',
        'YOI',
        'OEW/Exit Limit',
    ],
    dtype={
        'Name': str,
        'Type': str,
        'YOI': int,
        'OEW/Exit Limit': float,
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
    ncols = 1,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
)

# SECONDARY AXES ##############

x1, x2, y1, y2 = 2013, 2020, 200, 400  # subregion of the original image
axins = ax.inset_axes(
    bounds = [0.75, 0.5, 0.2, 0.4],
    xlim=(x1, x2), ylim=(y1, y2), xticklabels=[], yticklabels=[])
ax.indicate_inset_zoom(axins, edgecolor="black")

# AXIS LIMITS ################

ax.set_xlim(1950, 2050)
ax.set_ylim(0,800)

# TICKS AND LABELS ###########

from matplotlib.ticker import MultipleLocator
ax.xaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_minor_locator(MultipleLocator(1))

for axis in [ax, axins]:
    axis.minorticks_on()
    axis.tick_params(axis='x', which='minor', bottom=True)

# GRIDS ######################

for axis in [ax, axins]:
    axis.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
    axis.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
    axis.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
    axis.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)


# AXIS LABELS ################

ax.set_ylabel("OEW/PEL [kg/pax]")
ax.set_xlabel("Aircraft Year of Introduction")

# PLOTTING ###################



for axis in [ax, axins]:
    axis.scatter(
        x = df_eff.loc[df_eff['Type']=='Wide']['YOI'],
        y = df_eff.loc[df_eff['Type']=='Wide']['OEW/Exit Limit'],
        marker = 'o',
        color = 'blue',
        label = 'Widebody'
    )
    axis.scatter(
        x = df_eff.loc[df_eff['Type']=='Narrow']['YOI'],
        y = df_eff.loc[df_eff['Type']=='Narrow']['OEW/Exit Limit'],
        marker = 's',
        color = 'orange',
        label = 'Narrowbody'
    )
    axis.scatter(
        x = df_eff.loc[df_eff['Type']=='Regional']['YOI'],
        y = df_eff.loc[df_eff['Type']=='Regional']['OEW/Exit Limit'],
        marker = '^',
        color = 'red',
        label = 'Narrowbody'
    )

axins.annotate('A330-900', (2018, 299), fontsize=8, xytext=(-20, -10), textcoords='offset points')
axins.annotate('B787-10', (2018, 308), fontsize=8, xytext=(-20, 5), textcoords='offset points')

ax.annotate(
    'lower=better', 
    xy=(1960, 500), 
    xytext=(1960, 700), 
    arrowprops=dict(facecolor='black', width=1, headwidth=10),
        va='center',
    ha='center'
)

# LEGEND ####################

ax.legend(
    loc='lower right',
)

# EXPORT #########################################

from pathlib import Path
figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%