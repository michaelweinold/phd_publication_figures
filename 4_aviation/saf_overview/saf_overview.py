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

df_fossil = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Fossil Fuel Production',
    usecols = lambda column: column in [
        'year',
        'jet fuel (Mt/y)',
    ],
    dtype={
        'year': int,
        'jet fuel (Mt/y)': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_saf_production_forecast_1 = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'SAF Forecast 1',
    usecols = lambda column: column in [
        'year',
        'SAF production (Mt)',
    ],
    dtype={
        'year': int,
        'SAF production (Mt)': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_saf_production_forecast_2 = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'SAF Forecast 2',
    usecols = lambda column: column in [
        'year',
        'SAF production (Mt)',
    ],
    dtype={
        'year': int,
        'SAF production (Mt)': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_saf_price = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'SAF Price',
    usecols = lambda column: column in [
        'year',
        'price [$(2020)]',
    ],
    dtype={
        'year': int,
        'price [$(2020)]': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_fossil_price = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Fossil Price',
    usecols = lambda column: column in [
        'year',
        'jet fuel price ($(2020)/t)',
    ],
    dtype={
        'year': int,
        'jet fuel price ($(2020)/t)': float,
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
            height_ratios=[1,1],
        ),
        sharex=True
    )

# DATA #######################

# AXIS LIMITS ################

ax[0].set_xlim(1980, 2050)
ax[0].set_ylim(0, 2800)
ax[1].set_ylim(0, 480)

# TICKS AND LABELS ###########

ax[0].minorticks_on()
ax[0].tick_params(axis='x', which='minor', bottom=False)

import matplotlib.ticker as ticker
def thousand_formatter(value, tick_number):
    """
    Formats the tick label with thousand separators: 1000 = 1'000.
    """
    return f"{int(value):,}".replace(",", "'")

ax[0].yaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))

# GRIDS ######################

for axis in ax:
    axis.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
    axis.grid(which='major', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax[0].set_ylabel("Jet Fuel Price \n [\$(2020)/t(weight)]")
ax[1].set_ylabel("Jet Fuel Production \n (Global) [Mt(weight)]")

# PLOTTING ###################

ax[1].plot(
    df_fossil['year'],
    df_fossil['jet fuel (Mt/y)'],
    color = 'black',
    label = 'Fossil Jet Fuel'
)
ax[1].plot(
    df_saf_production_forecast_1['year'],
    df_saf_production_forecast_1['SAF production (Mt)'],
    linestyle = '--',
    color = 'green',
    label = 'SAF Forecast (Industry)'
)
ax[1].plot(
    df_saf_production_forecast_2['year'],
    df_saf_production_forecast_2['SAF production (Mt)'],
    linestyle = '--',
    color = 'blue',
    label = 'SAF Forecast (ICAO)'
)

ax[0].plot(
    df_saf_price['year'],
    df_saf_price['price [$(2020)]'],
    linestyle = '--',
    color = 'green',
    label = 'SAF'
)
ax[0].plot(
    df_fossil_price['year'],
    df_fossil_price['jet fuel price ($(2020)/t)'],
    color = 'black',
    label = 'Fossil'
)

# LEGEND ####################

ax[0].legend(
    loc='upper left',
)

ax[1].legend(
    loc='upper left',
)

# EXPORT #########################################

import os 
file_path = os.path.abspath(__file__)
file_name = os.path.splitext(os.path.basename(file_path))[0]
figure_name: str = str(file_name + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%
