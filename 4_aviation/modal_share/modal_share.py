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
    'font.size': 11
})

# DATA IMPORT ###################################

df_japan = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Japan',
    usecols = lambda column: column in [
        'distance [km]',
        'rail [%]',
        'car [%]',
        'air [%]',
        'other [%]',
        'year'
    ],
    dtype={
        'distance [km]': str,
        'rail [%]': float,
        'car [%]': float,
        'air [%]': float,
        'other [%]': float,
        'year': str
    },
    header = 0,
    engine = 'openpyxl'
)
		
# DATA MANIPULATION #############################

df_japan = df_japan[df_japan['year'] == '2019?']

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm,
    )

# AXIS SCALING ###############

# AXIS LIMITS ################

# ax.set_ylim(0, 100)
# ax.set_xlim(0, 1000)

# TICKS AND LABELS ###########

labels = df_japan['distance [km]']

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_xlabel("Trip Distance [km]")
ax.set_ylabel("Modal Share [\%]")

# PLOTTING ###################

width = 0.4
x = np.arange(len(df_japan['distance [km]']))
ax.set_xticks(x, df_japan['distance [km]'])

ax.bar(
    x = x,
    height = df_japan['rail [%]'],
    width = width,
    label = 'Rail',
    color = 'darkorange',
)
ax.bar(
    x = x,
    bottom = df_japan['rail [%]'],
    height = df_japan['air [%]'],
    width = width,
    label = 'Air',
    color = 'royalblue',
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