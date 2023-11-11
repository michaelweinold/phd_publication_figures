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

df_ets_price = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Emissions Prices',
    usecols = lambda column: column in [
        'date',
        '[EUR/t]',
    ],
    dtype={
        'date': datetime,
        '[EUR/t]': float,
    },
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 2,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm,
        gridspec_kw = dict(
            height_ratios=[3,2],
        ),
        sharex=True
    )

# DATA #######################

# AXIS LIMITS ################

ax[0].set_xlim(
    datetime.strptime('2004', '%Y'),
    datetime.strptime('2023', '%Y')
)

ax[0].set_ylim(1,65)

ax[1].set_ylim(0, 100)

# TICKS AND LABELS ###########

for axis in ax:
    axis.minorticks_on()
    axis.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

for axis in ax:
    axis.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
    axis.grid(which='major', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax[0].set_ylabel("Producer Price Index \n (Aviation Fuel) [1950=1]")
ax[1].set_xlabel("Year")
ax[1].set_ylabel("EUA Spot Price \n [EUR/t(CO$_2$)]")

# PLOTTING ###################

ax[1].plot(
    df_ets_price['date'],
    df_ets_price['[EUR/t]'],
    color = 'black',
    linewidth = 1,
)

ax[1].axvspan(
    xmin = datetime.strptime('2005', '%Y'),
    xmax = datetime.strptime('2008', '%Y'),
    facecolor='blue',
    alpha=0.2,
    label = 'Phase 1'
)
ax[1].annotate(
    'Phase 1',
    xy=(datetime.strptime('2006', '%Y'), 75),
)
ax[1].axvspan(
    xmin = datetime.strptime('2008', '%Y'),
    xmax = datetime.strptime('2013', '%Y'),
    facecolor='purple',
    alpha=0.2,
    label = 'Phase 2'
)
ax[1].annotate(
    'Phase 2',
    xy=(datetime.strptime('2010', '%Y'), 75),
)
ax[1].axvspan(
    xmin = datetime.strptime('2013', '%Y'),
    xmax = datetime.strptime('2021', '%Y'),
    facecolor='red',
    alpha=0.2,
    label = 'Phase 3'
)
ax[1].annotate(
    'Phase 3',
    xy=(datetime.strptime('2016', '%Y'), 75),
)
ax[1].axvspan(
    xmin = datetime.strptime('2021', '%Y'),
    xmax = datetime.strptime('2030', '%Y'),
    facecolor='orange',
    alpha=0.2,
    label = 'Phase 4'
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
