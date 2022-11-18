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
        dpi = 300,
        figsize=(16.5*cm, 5*cm), # A4=(210x297)mm
    )

# DATA #######################

x_i = df_i.index
y_i = df_i[1]

# AXIS LIMITS ################

# TICKS AND LABELS ###########

# GRIDS ######################

# AXIS LABELS ################

plt.xlabel("Nomenclature")
plt.ylabel("Number of Studies")

# PLOTTING ###################

plt.bar(
    x = x_i,
    height = y_i
)

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
