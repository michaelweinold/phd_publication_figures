#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
cm = 1/2.54 # for inches-cm conversion

# data science
import numpy as np
import pandas as pd

# i/o
from pathlib import PurePath, Path

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": "Computer Modern",
    'font.size': 8
})

# DATA IMPORT ###################################

df_i = pd.read_csv(
    filepath_or_buffer = 'data/i.csv',
    sep = ',',
    header = None,
    index_col = False
)

df_ma = pd.read_csv(
    filepath_or_buffer = 'data/ma.csv',
    sep = ',',
    header = None,
    index_col = False
)

df_pxc = pd.read_csv(
    filepath_or_buffer = 'data/pxc.csv',
    sep = ',',
    header = None,
    index_col = False
)

df_t = pd.read_csv(
    filepath_or_buffer = 'data/t.csv',
    sep = ',',
    header = None,
    index_col = False
)

# DATA MANIPULATION #############################

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 4,
        sharey = True,
        dpi = 300,
        width_ratios = [6,4,3,13],
        figsize=(16.5*cm, 5*cm), # A4=(210x297)mm
    )

# DATA #######################

x_i = df_i.index
y_i = df_i[1]

x_ma = df_ma.index
y_ma = df_ma[1]

x_pxc = df_pxc.index
y_pxc = df_pxc[1]

x_t = df_t.index
y_t = df_t[1]

# AXIS LIMITS ################

plt.ylim(0,21)

# TICKS AND LABELS ###########

ax[0].set_xticks(
    ticks = np.arange(df_i[0].size),
    labels = df_i[0]
)
ax[0].tick_params(direction='out', labelrotation = 90)

ax[1].set_xticks(
    ticks = np.arange(df_ma[0].size),
    labels = df_ma[0]
)
ax[1].tick_params(direction='out', labelrotation = 90)

ax[2].set_xticks(
    ticks = np.arange(df_pxc[0].size),
    labels = df_pxc[0]
)
ax[2].tick_params(direction='out', labelrotation = 90)

ax[3].set_xticks(
    ticks = np.arange(df_t[0].size),
    labels = df_t[0]
)
ax[3].tick_params(direction='out', labelrotation = 90)

# GRIDS ######################

for axis in ax:
    axis.minorticks_on()
    axis.tick_params(axis='x', which='minor', bottom=False)
    axis.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
    axis.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax[0].set_ylabel('Number of Studies')

# PLOTTING ###################

ax[0].bar(
    x = x_i,
    height = y_i
)
ax[0].set_title('Integrated', fontsize = 8)

ax[1].bar(
    x = x_ma,
    height = y_ma
)
ax[1].set_title('Matrix', fontsize = 8)

ax[2].bar(
    x = x_pxc,
    height = y_pxc
)
ax[2].set_title('Path Exchange', fontsize = 8)

ax[3].bar(
    x = x_t,
    height = y_t
)
ax[3].set_title('Tiered', fontsize = 8)

# LEGEND ####################

# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%
