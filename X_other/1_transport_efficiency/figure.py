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

df_maritime_general_cargo = pd.read_csv(
    filepath_or_buffer = 'data/maritime/general_cargo.csv',
    sep = ';',
    header = 'infer',
    index_col = False,
    skipinitialspace=True
)
df_maritime_bulk = pd.read_csv(
    filepath_or_buffer = 'data/maritime/bulk.csv',
    sep = ';',
    header = 'infer',
    index_col = False,
    skipinitialspace=True
)
df_maritime_tanker = pd.read_csv(
    filepath_or_buffer = 'data/maritime/tanker.csv',
    sep = ';',
    header = 'infer',
    index_col = False,
    skipinitialspace=True
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
        nrows = 3,
        ncols = 1,
        dpi = 300,
        figsize=(16.5*cm, 5*cm), # A4=(210x297)mm,
        sharex = True
    )

# DATA #######################

x_car = df_car['year']
x_air = df_air['year']
y_car = df_car['relative_efficiency']
y_air = df_air['relative_efficiency']

# AXIS SCALE #################

ax[2].set_yscale('log')

# AXIS LIMITS ################

plt.xlim(1950,2020)
ax[2].set_ylim(1,150)

# TICKS AND LABELS ###########

# ax.minorticks_on()
# ax.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

plt.grid(which='major', axis='both', linestyle='-', linewidth = 0.5)

# ax[0].grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
# ax[0].grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax[0].set_ylabel("EEOI [gCO$_2$/p-km]")
ax[2].set_ylabel("EEOI [gCO$_2$/t-nm]")

# PLOTTING ###################

ax[0].plot(
    x_car,
    y_car,
    color = 'black',
    linewidth = 1,
    label = 'Passenger Cars',
    linestyle = 'dashed',
)

ax[0].plot(
    x_air,
    y_air,
    color = 'black',
    linewidth = 1,
    label = 'Passenger Airplanes'
)

ax[2].plot(
    df_maritime_general_cargo['year'],
    df_maritime_general_cargo['efficiency(gCO2/t-nm)'],
    color = 'black',
    linewidth = 1,
    label = 'General Cargo'
)
ax[2].plot(
    df_maritime_bulk['year'],
    df_maritime_bulk['efficiency(gCO2/t-nm)'],
    color = 'black',
    linewidth = 1,
    label = 'Bulk Cargo'
)
ax[2].plot(
    df_maritime_tanker['year'],
    df_maritime_tanker['efficiency(gCO2/t-nm)'],
    color = 'black',
    linewidth = 1,
    label = 'Tankers'
)


# LEGEND ####################

fig.legend(
    bbox_to_anchor=(1,1),
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

# %%

# %%