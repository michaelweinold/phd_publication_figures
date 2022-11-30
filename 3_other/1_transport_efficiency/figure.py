#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
from matplotlib.ticker import FuncFormatter
cm = 1/2.54 # for inches-cm conversion

# data science
import numpy as np
import pandas as pd

# i/o
from pathlib import PurePath, Path

# date manipulation
from datetime import timedelta, datetime

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": "Computer Modern",
    'font.size': 8
})

# DATA IMPORT ###################################

df_car = pd.read_csv(
    filepath_or_buffer = 'data/car_efficiency.csv',
    sep = ',',
    header = 'infer',
    index_col = False
)

df_air = pd.read_excel(
    io = '../../2_msc_supervision_proposals/1_combined_rpk_efficiency/data/data_aviation_radiative_forcing.xlsx',
    sheet_name = 'efficiency',
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

# cut off dates
df_car = df_car[~(df_car['year'] < 1950)]
df_air = df_air[~(df_air['year'] < 1950)]
df_car['relative_efficiency'] = 1/(df_car['mileage [miles/gallon]']/df_car['mileage [miles/gallon]'].iloc[0])*100
df_air['relative_efficiency'] = 1/(df_air['RPK/kg fuel']/df_air['RPK/kg fuel'].iloc[0])*100

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(16.5*cm, 5*cm), # A4=(210x297)mm
    )

# DATA #######################

x_car = df_car['year']
x_air = df_air['year']
y_car = df_car['relative_efficiency']
y_air = df_air['relative_efficiency']

# AXIS LIMITS ################

plt.xlim(1950,2010)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

plt.xlabel("Year")
ax.set_ylabel("Relative Carbon Intensity [\%]")

# PLOTTING ###################

ax.plot(
    x_car,
    y_car,
    color = 'black',
    linewidth = 1,
    label = 'Passenger Cars'
)

ax.plot(
    x_air,
    y_air,
    color = 'black',
    linewidth = 1,
    label = 'Passenger Airplanes'
)

# LEGEND ####################

fig.legend(
    bbox_to_anchor=(1,1), bbox_transform=ax.transAxes,
    loc = 'upper right',
    fontsize = 'small',
    markerscale = 1.0,
    frameon = True,
    fancybox = False
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
