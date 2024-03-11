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

df_ff = pd.read_csv(
    filepath_or_buffer = r'data/data.csv'
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

# AXIS LIMITS ################

ax.set_xlim(-0.05, 1)
ax.set_ylim(0, 1.1)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)
ax.tick_params(axis='both', which='both', labelbottom=False, labelleft=False)

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# axes[0]IS LABELS ################

ax.set_xlabel('Time [h]')
ax.set_ylabel("Fuel Flow [kg/s]")

# PLOTTING ###################

plt.plot(
    df_ff['time'],
    df_ff['ff'].rolling(window=1).mean(),
    color='black',
    linestyle='-',
    linewidth=1,
    label = 'Fuel Flow'
)

x = df_ff['time'].rolling(window=1).mean()
y = df_ff['ff']

ax.fill_between(
    x,
    y,
    where = (x >= 0.24) & (x <= 0.7),
    alpha = 0.2, color='blue',
    label='Cruise Phase Fuel Volume'
)
ax.fill_between(
    x,
    y,
    where = (x >= 0.08) & (x <= 0.25),
    alpha = 0.2, color='green',
    label='Climb/Descent Fuel Volume'
)
ax.fill_between(
    x,
    y,
    where = (x >= 0.69) & (x <= 0.81),
    alpha = 0.2, color='green',
)
ax.fill_between(
    x,
    y,
    where = (x >= 0) & (x <= 0.08),
    alpha = 0.2, color='red',
    label='TO/Ldg. Fuel Volume'
)
ax.fill_between(
    x,
    y,
    where = (x >= 0.8) & (x <= 1),
    alpha = 0.2, color='red',
)

ax.axvline(x=0.9, color='black', linestyle='--')
ax.annotate(
    'AIBT',
    xy=(0.91, 0.5),
    xytext=(0.91, 0.5),
    fontsize=12,
    ha='left',
    va='center',
    color='black',
)

ax.axvline(x=0, color='black', linestyle='--')
ax.annotate(
    'AOBT',
    xy=(0.01, 0.5),
    xytext=(0.01, 0.5),
    fontsize=12,
    ha='left',
    va='center',
    color='black',
)

# LEGEND ####################

ax.legend(
    loc='upper right',
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