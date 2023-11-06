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
    'font.size': 12
})

# DATA IMPORT ###################################

emissions_data = [
    [0.21790859349727398, 0.9245575840327378],
    [3.729451993625478, 0.9666012411660689],
    [100, 0]
]

emissions_df = pd.DataFrame(
    emissions_data,
    columns=['x', 'y']
)

# DATA MANIPULATION #############################

def find_x(y, x_coords, y_coords):
    # Calculate the slope of the line
    m = (y_coords[1] - y_coords[0]) / (x_coords[1] - x_coords[0])
    
    # Calculate the y-intercept of the line
    b = y_coords[0] - m * x_coords[0]
    
    # Calculate the corresponding x-coordinate
    x = (y - b) / m
    
    return x


def find_y(x, x_coords, y_coords):
    # Calculate the slope of the line
    m = (y_coords[1] - y_coords[0]) / (x_coords[1] - x_coords[0])
    
    # Calculate the y-intercept of the line
    b = y_coords[0] - m * x_coords[0]
    
    # Calculate the corresponding y-coordinate
    y = m * x + b
    
    return y

# FIGURE ########################################

# SETUP ######################

fig, axes = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 2,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
    sharex=True
)
plt.subplots_adjust(wspace=0.1)

# SECONDARY AXES ##############


# AXIS LIMITS ################

for ax in axes:
    ax.set_xlim(0, 100)
    ax.set_ylim(0,100)

# TICKS AND LABELS ###########

for ax in axes:
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_xticklabels([])

# GRIDS ######################

# AXIS LABELS ################

for ax in axes:
    ax.set_ylabel("Energy Consumption $E$")
    ax.set_xlabel("Energy Service $S$")

# PLOTTING ###################

x_coords_steep = [10, 40]
y_coords_steep = [20, 100]

x_coords_flat = [20, 100]
y_coords_flat = [10, 80]

axes[0].plot(
    x_coords_steep,
    y_coords_steep,
    color='red',
    label='$\epsilon_1$, Low Efficiency'
)

axes[0].plot(
    x_coords_flat,
    y_coords_flat,
    color='green',
    #linestyle='--',
    label='$\epsilon_2$, High Efficiency'
)

source_y = 65
source_x = find_x(source_y, x_coords_steep, y_coords_steep)

target_y = find_y(source_x, x_coords_flat, y_coords_flat)
target_x = source_x

axes[0].axhline(
    y=65,
    color='black'
)

axes[0].axhline(
    y=target_y,
    color='black'
)
    
axes[0].plot(
    (source_x, source_x),
    (0, source_y),
    color='grey',
    linestyle='--',
)

axes[0].annotate(
    '',
    xytext=(
        source_x,
        source_y
    ), # source point
    xy=(
        target_x,
        target_y
    ), # target point
    arrowprops=dict(
        arrowstyle='<->',
        color='black',
        linewidth=2
    )
)
axes[0].plot(
    target_x,
    target_y,
    marker='o',
    color='black'
)
axes[0].plot(
    source_x,
    source_y,
    marker='o',
    color='black'
)

axes[0].text(
    target_x + 2,
    4,
    '$S_0 = S_1$'
)

axes[0].text(
    2,
    target_y + 4,
    '$E_1$'
)

axes[0].text(
    2,
    source_y + 4,
    '$E_0$'
)

axes[0].text(
    source_x + 2,
    target_y + (source_y - target_y)/2 -2,
    '$E_0 - E_1$ = Energy Savings',
    backgroundcolor='white'
)

axes[0].text(
    x=2,
    y=94,
    s=r'\textbf{No Rebound Eff.}',
    ha='left',
    va='center',
    fontsize=12,
    color='black',
)

axes[1].text(
    x=2,
    y=94,
    s=r'\textbf{Rebound Effect}',
    ha='left',
    va='center',
    fontsize=12,
    color='black',
)


axes[1].plot(
    x_coords_steep,
    y_coords_steep,
    color='red',
    label='$\epsilon_1$, Low Efficiency'
)

axes[1].plot(
    x_coords_flat,
    y_coords_flat,
    color='green',
    #linestyle='--',
    label='$\epsilon_2$, High Efficiency'
)

source_y = 65
source_x = find_x(source_y, x_coords_steep, y_coords_steep)

target_y_1 = find_y(source_x, x_coords_flat, y_coords_flat)
target_x_1 = source_x

target_x_2 = source_x + 30
target_y_2 = find_y(target_x_2, x_coords_flat, y_coords_flat)



axes[1].annotate(
    '',
    xytext=(
        target_x_2,
        source_y
    ), # source point
    xy=(
        target_x_2,
        target_y_2
    ), # target point
    arrowprops=dict(
        arrowstyle='<->',
        color='black',
        linewidth=2
    )
)
axes[1].plot(
    target_x_2,
    source_y,
    marker='o',
    color='black'
)
axes[1].plot(
    source_x,
    source_y,
    marker='o',
    color='black'
)

axes[1].annotate(
    '',
    xytext=(
        target_x_2,
        target_y_2
    ), # source point
    xy=(
        target_x_2,
        target_y
    ), # target point
    arrowprops=dict(
        arrowstyle='<->',
        color='black',
        linewidth=2
    )
)
axes[1].plot(
    target_x_2,
    target_y_2,
    marker='o',
    color='black'
)
axes[1].plot(
    source_x,
    source_y,
    marker='o',
    color='black'
)

axes[1].axhline(
    y=65,
    color='black'
)

axes[1].axhline(
    y=target_y_2,
    color='black'
)

axes[1].axhline(
    y=target_y,
    color='black',
    linestyle='-.'
)
    
axes[1].plot(
    (source_x, source_x),
    (0, source_y),
    color='grey',
    linestyle='--',
)

axes[1].plot(
    (target_x_2, target_x_2),
    (0, source_y),
    color='grey',
    linestyle='--',
)


axes[1].annotate(
    '',
    xytext=(
        source_x,
        5
    ), # source point
    xy=(
        target_x_2,
        5
    ), # target point
    arrowprops=dict(
        arrowstyle='->',
        color='grey',
        linewidth=2
    )
)

axes[1].text(
    target_x + 2,
    4,
    '$S_0$',
    backgroundcolor='white'
)

axes[1].text(
    target_x_2 + 2,
    4,
    '$S_1$'
)

axes[1].text(
    2,
    source_y + 4,
    '$E_0$'
)

axes[1].text(
    2,
    target_y_2 + 4,
    '$E_1$'
)

axes[1].text(
    2,
    target_y + 4,
    '$E_1^*$'
)

axes[1].text(
    target_x_2 + 2,
    target_y_2 + (source_y - target_y_2)/2 -2,
    '$E_0 - E_1$ = E. Savings',
    backgroundcolor='white'
)

axes[1].text(
    target_x_2 + 2,
    target_y_1 + (target_y_2 - target_y_1)/2 -2,
    '$E_1 - E_1^*$ = Rebd. Losses',
    backgroundcolor='white'
)

# LEGEND ####################

axes[0].legend(
    loc='upper right',
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
# %%

# %%
