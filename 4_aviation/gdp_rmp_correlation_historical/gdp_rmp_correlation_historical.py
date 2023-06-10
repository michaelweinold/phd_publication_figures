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

df_freight = pd.read_excel(
    io = 'data/world/data.xlsx',
    sheet_name = 'Freight',
    usecols = lambda column: column in [
        'year',
        'plot world gdp (2022 USD)',
        'plot world air freight (Mtkm)',
    ],
    dtype={
        'year': int,
        'plot world gdp (2022 USD)': float,
        'plot world air freight (Mtkm)': float,
    },
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################


# FIGURE ########################################

# SETUP ######################

fig, ax1 = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm
)
ax2 = ax1.twinx()

# DATA #######################

# AXIS SCALE #################

#ax1.set_yscale('log')
#ax2.set_yscale('log')
#ax1.set_xscale('log')

# AXIS LIMITS ################

# COLORBAR ###################

# TICKS AND LABELS ###########

ax1.minorticks_on()
ax1.tick_params(axis='x', which='both', bottom=False)
ax1.tick_params(axis='y', which='both', bottom=False)

# GRIDS ######################

ax1.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax1.grid(which='both', axis='x', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

ax1.set_xlabel("GDP [2022 USD]")
ax1.set_ylabel("Air Transport (Passengers) [km]")
ax2.set_ylabel("Air Transport (Freight) [Mtkm]")

# PLOTTING ###################

ax1.scatter(
    df_freight['plot world gdp (2022 USD)'],
    df_freight['plot world air freight (Mtkm)'],
    color = 'black',
    marker = 's',
    label = 'Freight'
)

# LEGEND ####################

ax1.legend(
    loc = 'upper left',
    fontsize = 'small',
    markerscale = 1.0,
    frameon = True,
    fancybox = False,
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
