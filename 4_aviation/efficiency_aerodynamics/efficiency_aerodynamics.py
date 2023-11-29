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
    'font.size': 12
})

# DATA IMPORT ###################################

df_eff = pd.read_excel(
    io = '../efficiency/data/data_29-11-2023.xlsx',
    sheet_name = 'data',
    usecols = lambda column: column in [
        'Name',
        'Type',
        'YOI',
        'L/D estimate',
    ],
    dtype={
        'Name': str,
        'Type': str,
        'YOI': int,
        'L/D estimate': float,
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

# AXIS LIMITS ################

ax.set_xlim(1950, 2050)
ax.set_ylim(10,30)

# TICKS AND LABELS ###########

from matplotlib.ticker import MultipleLocator
ax.xaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_minor_locator(MultipleLocator(1))

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)

ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)


# AXIS LABELS ################

ax.set_ylabel("L/D [1]")
ax.set_xlabel("Aircraft Year of Introduction")

# PLOTTING ###################

ax.scatter(
    x = df_eff.loc[df_eff['Type']=='Wide']['YOI'],
    y = df_eff.loc[df_eff['Type']=='Wide']['L/D estimate'],
    marker = 'o',
    color = 'blue',
    label = 'Widebody'
)
ax.scatter(
    x = df_eff.loc[df_eff['Type']=='Narrow']['YOI'],
    y = df_eff.loc[df_eff['Type']=='Narrow']['L/D estimate'],
    marker = 's',
    color = 'orange',
    label = 'Narrowbody'
)

a350 = df_eff.loc[df_eff['Name'] == 'A350-900', 'L/D estimate'].iloc[0]
limit = a350 * 1.05 * 1.15 # Limit based on NLF technology plus 777x
ax.axhline(
    y=limit,
    color='black',
    linestyle='-',
    linewidth=1,
    label='Theor. Limit'
)

ax.scatter(
    x = 2025,
    y = a350*1.05,
    color='green',
    s=30,
)
ax.scatter(
    x = 2025,
    y = a350*1.05,
    facecolors='none',
    edgecolors='black',
    s=90,
    label = 'Projection'
)
plt.annotate(
    '777X',
    (2025, a350*1.05,),
    fontsize=8,
    xytext=(-10, 10),
    textcoords='offset points'
)

a340 = df_eff.loc[df_eff['Name'] == 'A340-500', 'L/D estimate'].iloc[0]
ax.scatter(2030, a340*1.046, color='green', s=30)
ax.scatter(
    x = 2030,
    y = a340*1.046,
    facecolors='none',
    edgecolors='black',
    s=90,
)
plt.annotate('BLADE', (2030, a340*1.046),
                fontsize=8, xytext=(-10, 10),
                textcoords='offset points')
ax.scatter(2035, 27.8, color='green')
ax.scatter(
    x = 2035,
    y = 27.8,
    facecolors='none',
    edgecolors='black',
    s=90,
)
plt.annotate('SB-Wing', (2035, 27.8),
                fontsize=8, xytext=(-10,10),
                textcoords='offset points')

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