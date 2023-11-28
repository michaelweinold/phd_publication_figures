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
    'font.size': 9
})

# DATA IMPORT ###################################

# DATA MANIPULATION #############################

x = [0,1,2,3]
a = [1, 0.8, 0.8, 0.8]

y_reference = 100

def fill(x):
    y = []
    y_reduced = y_reference
    for i in range(len(x)):
        y_reduced = y_reduced * a[i]
        y.append(y_reduced)
    return y

y = fill(x)

x_emissions = [3]
y_emissions = [y[-1]]

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 1,
    dpi = 300,
    figsize=(7*cm, 4.5*cm), # A4=(210x297)mm,
    sharex=False
)
ax2 = ax.twinx()

# SECONDARY AXES ##############


# AXIS LIMITS ################

ax.set_xlim(-0.5, 3.65)
ax.set_ylim(0,105)

ax2.set_ylim(0,105)

# TICKS AND LABELS ###########

a_labels = ['', '$a_{21}^P=0.8$', '$a_{32}^P=0.8$', '$a_{D3}^S=0.8$']

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

ax.set_xlabel("Production Tier")
ax.set_ylabel("Economic Flow [\$]")

ax2.set_ylabel("Emissions [kg(CO$_2$)]")

# PLOTTING ###################

bars = ax.bar(
    x = x_emissions,
    height = y_emissions,
    color = 'orange',
    width = 0.85,
    label = 'Emissions',
    edgecolor = 'black'
)

bars = ax.bar(
    x = x,
    height = y,
    color = 'green',
    width = 0.5,
    label = 'Econ.Flow',
    edgecolor = 'black'
)
for bar, label in zip(bars, a_labels):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() - 5,
        label,
        ha='center',
        va='top',
        rotation='vertical',
        color = 'white'
    )
for bar in bars[1:]:
    ax.text(
        bar.get_x() + bar.get_width() / 2,  # X position, centered
        bar.get_height(),  # Y position, top of the bar
        f'{bar.get_height():.2f}',  # The value, formatted to 2 decimal places
        ha='center',  # Horizontal alignment
        va='bottom',  # Vertical alignment
        color='black'  # Text color
    )



# LEGEND ####################

ax.legend(
    loc = 'upper right',
    frameon = False
)

# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)