#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.ticker as ticker
# unit conversion
cm = 1/2.54 # for inches-cm conversion
# time manipulation
from datetime import datetime

# data science
import numpy as np
import pandas as pd

# i/o
from pathlib import PurePath, Path

# type hints
from typing import List

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 12
})

# DATA IMPORT ###################################

df_fuels = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Energy Density Fuels',
    usecols = lambda column: column in [
        'substance',
        'Wh/kg',
        'Wh/l'
    ],
    dtype={
        'substance': str,
        'Wh/kg': float,
        'Wh/l': float
    },
    header = 0,
    engine = 'openpyxl'
)
df_batteries_2011 = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Energy Density Batteries (2011)',
    usecols = lambda column: column in [
        'technology',
        'range lower [Wh/kg]',
        'range higher [Wh/kg]',
        'range lower [Wh/l]',
        'range higher [Wh/l]',
    ],
    dtype={
        'technology': str,
        'range lower [Wh/kg]': float,
        'range higher [Wh/kg]': float,
        'range lower [Wh/l]': float,
        'range higher [Wh/l]': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_acft_electrification_icct = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Aircraft Electrification (ICCT)',
    usecols = lambda column: column in [
        'battery energy density, current EMF [Wh/kg]',
        'replacable commuter traffic, current EMF [%]',
        'battery energy density, 15% EMF reduction [Wh/kg]',
        'replacable commuter traffic, 15% EMF reduction [%]',
        'battery energy density, 30% EMF reduction [Wh/kg]',
        'replacable commuter traffic, 30% EMF reduction [%]'
    ],
    dtype={
        'battery energy density, current EMF [Wh/kg]': float,
        'replacable commuter traffic, current EMF [%]': float,
        'battery energy density, 15% EMF reduction [Wh/kg]': float,
        'replacable commuter traffic, 15% EMF reduction [%]': float,
        'battery energy density, 30% EMF reduction [Wh/kg]': float,
        'replacable commuter traffic, 30% EMF reduction [%]': float
    },
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

# BUILD RECTANGLES ###############

dict_battery_technologies: dict = {
    'Lead-Acid': 'red',
    'Ni-Cd': 'green',
    'Ni-MH': 'orange',
    'Li-ion': 'blue',
    'PLiON': 'purple',
    'Li-metal': 'pink',
}

import matplotlib.patches as patches

def build_rectangles(
        dict_battery_technologies: dict,
        df_batteries: pd.DataFrame
) -> List:
    
    list_rectangles: List = []

    for key, value in dict_battery_technologies.items():
        df_row: pd.DataFrame = df_batteries.loc[df_batteries['technology'] == key]
        x_min: float = df_row['range lower [Wh/kg]'].iloc[0]
        x_max: float = df_row['range higher [Wh/kg]'].iloc[0]
        y_min: float = df_row['range lower [Wh/l]'].iloc[0]
        y_max: float = df_row['range higher [Wh/l]'].iloc[0]
        rectangle = patches.Rectangle(
            xy = (x_min, y_min),
            width = x_max - x_min,
            height = y_max - y_min,
            edgecolor = value,
            facecolor = 'none'
        )
        list_rectangles.append(rectangle)

    return list_rectangles

def copy_rectangles_for_inset(list_rectangles: List) -> List:
    rectangles_inset = []
    for rectangle in list_rectangles:
        rectangle_copy = patches.Rectangle(
            rectangle.get_xy(),
            rectangle.get_width(),
            rectangle.get_height(),
            linewidth=rectangle.get_linewidth(),
            edgecolor=rectangle.get_edgecolor(),
            facecolor=rectangle.get_facecolor(),
        )
        rectangles_inset.append(rectangle_copy)
    
    return rectangles_inset

battery_rectangles_2011 = build_rectangles(
    dict_battery_technologies = dict_battery_technologies,
    df_batteries = df_batteries_2011
)

battery_rectangles_2011_inset = copy_rectangles_for_inset(battery_rectangles_2011)

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 2,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm,
        gridspec_kw = dict(
            height_ratios=[4, 1],
        ),
        sharex=True
    )
plt.subplots_adjust(wspace=0.075)

# AXIS LIMITS ################

ax[0].callbacks.connect("xlim_changed", convert_xaxis_units_from_MJ_to_Wh)
ax[0].callbacks.connect("ylim_changed", convert_yaxis_units_from_MJ_to_Wh)

ax[0].set_xlim(0,1000)

ax[0].set_ylim(0,500)
ax[1].set_ylim(0,100)

# TICKS AND LABELS ###########

def thousand_formatter(value, tick_number):
    """
    Formats the tick label with thousand separators: 1000 = 1'000.
    """
    return f"{int(value):,}".replace(",", "'")

ax[0].xaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))
ax[0].yaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))

ax[1].xaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))

ax[0].minorticks_on()
ax[0].tick_params(axis='x', which='both', bottom=False)
ax[0].tick_params(axis='y', which='both', bottom=False)

ax[1].minorticks_on()
ax[1].tick_params(axis='x', which='both', bottom=False)
ax[1].tick_params(axis='y', which='both', bottom=False)

# GRIDS ######################

ax[0].grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax[0].grid(which='both', axis='x', linestyle='-', linewidth = 0.5)

ax[1].grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax[1].grid(which='both', axis='x', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

ax[1].set_xlabel("Gravimetric Energy Density [Wh/kg]")
ax[1].set_ylabel("[\%]")
ax[0].set_ylabel("Vol. Energy Density [Wh/l]")

# PLOTTING ###################

ax[0].scatter(
    df_fuels['Wh/kg'],
    df_fuels['Wh/l'],
    color = 'black',
    s = 10
)
ax[1].scatter(
    df_fuels['Wh/kg'],
    df_fuels['Wh/l'],
    color = 'black',
    s = 10
)
for rectangle in battery_rectangles_2011:
    ax[0].add_patch(rectangle)

ax[1].plot(
    df_acft_electrification_icct['battery energy density, current EMF [Wh/kg]'],
    df_acft_electrification_icct['replacable commuter traffic, current EMF [%]'],
    color = 'red',
    linestyle = '-',
    linewidth = 1
)
ax[1].plot(
    df_acft_electrification_icct['battery energy density, 15% EMF reduction [Wh/kg]'],
    df_acft_electrification_icct['replacable commuter traffic, 15% EMF reduction [%]'],
    color = 'orange',
    linestyle = '-',
    linewidth = 1
)
ax[1].plot(
    df_acft_electrification_icct['battery energy density, 30% EMF reduction [Wh/kg]'],
    df_acft_electrification_icct['replacable commuter traffic, 30% EMF reduction [%]'],
    color = 'green',
    linestyle = '-',
    linewidth = 1
)

# LEGEND ####################

from matplotlib.patches import Patch
from matplotlib.lines import Line2D

legend_elements = [
    Line2D(
        xdata = [0],
        ydata = [0],
        marker='o',
        color = 'black',
        markerfacecolor='black',
        linestyle = 'None',
        markersize=3,
        label='Fuels'
    ),
    Patch(
        facecolor = 'none',
        edgecolor = 'black',
        label = 'Batteries'
    ),
]

ax[0].legend(
    handles=legend_elements,
    loc='upper right',
)

# ANNOTATION ################

for idx, row in df_fuels.iterrows():
    ax[0].annotate(
        text = row['substance'],
        xy = (row['Wh/kg']+100, row['Wh/l']),
        ha='right',
        va='bottom',
        fontsize=9
    )
    ax[1].annotate(
        row['substance'],
        (row['Wh/kg'], row['Wh/l']),
        ha='left',
        va='bottom',
        fontsize=9
    )


# EXPORT #########################################

file_path = os.path.abspath(__file__)
file_name = os.path.basename(file_path)
figure_name: str = str(file_name + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%
