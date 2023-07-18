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
    'font.size': 11
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
        'battery energy density, commuter traffic, current EMF [Wh/kg]',
        'replacable commuter traffic, current EMF [%]',
        'battery energy density, commuter traffic, 15% EMF reduction [Wh/kg]',
        'replacable commuter traffic, 15% EMF reduction [%]',
        'battery energy density, commuter traffic, 30% EMF reduction [Wh/kg]',
        'replacable commuter traffic, 30% EMF reduction [%]',
        'battery energy density, turboprop traffic, current EMF [Wh/kg]',
        'replacable turboprop traffic, current EMF [%]',
        'battery energy density, turboprop traffic, 15% EMF reduction [Wh/kg]',
        'replacable turboprop traffic, 15% EMF reduction [%]',
        'battery energy density, turboprop traffic, 30% EMF reduction [Wh/kg]',
        'replacable turboprop traffic, 30% EMF reduction [%]',
    ],
    dtype={
        'battery energy density, commuter traffic, current EMF [Wh/kg]': float,
        'replacable commuter traffic, current EMF [%]': float,
        'battery energy density, commuter traffic, 15% EMF reduction [Wh/kg]': float,
        'replacable commuter traffic, 15% EMF reduction [%]': float,
        'battery energy density, commuter traffic, 30% EMF reduction [Wh/kg]': float,
        'replacable commuter traffic, 30% EMF reduction [%]': float,
        'battery energy density, turboprop traffic, current EMF [Wh/kg]': float,
        'replacable turboprop traffic, current EMF [%]': float,
        'battery energy density, turboprop traffic, 15% EMF reduction [Wh/kg]': float,
        'replacable turboprop traffic, 15% EMF reduction [%]': float,
        'battery energy density, turboprop traffic, 30% EMF reduction [Wh/kg]': float,
        'replacable turboprop traffic, 30% EMF reduction [%]': float
    },
    header = 0,
    engine = 'openpyxl'
)

df_lion_historical = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Li-ion Historical',
    usecols = lambda column: column in [
        'year',
        'Wh/kg (historical)',
        'Wh/l (historical)',
        'Wh/kg (target)',
        'Wh/l (target)'
    ],
    dtype={
        'year': str,
        'Wh/kg': float,
        'Wh/l': float,
        'Wh/kg (target)': float,
        'Wh/l (target)': float,
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

ax[0].set_xlim(0,1000)

ax[0].set_ylim(0,1250)
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
    df_acft_electrification_icct['battery energy density, commuter traffic, current EMF [Wh/kg]'],
    df_acft_electrification_icct['replacable commuter traffic, current EMF [%]'],
    color = 'red',
    linestyle = '-',
    linewidth = 1
)
ax[1].plot(
    df_acft_electrification_icct['battery energy density, commuter traffic, 15% EMF reduction [Wh/kg]'],
    df_acft_electrification_icct['replacable commuter traffic, 15% EMF reduction [%]'],
    color = 'orange',
    linestyle = '-',
    linewidth = 1
)
ax[1].plot(
    df_acft_electrification_icct['battery energy density, commuter traffic, 30% EMF reduction [Wh/kg]'],
    df_acft_electrification_icct['replacable commuter traffic, 30% EMF reduction [%]'],
    color = 'green',
    linestyle = '-',
    linewidth = 1
)

ax[1].plot(
    df_acft_electrification_icct['battery energy density, turboprop traffic, current EMF [Wh/kg]'],
    df_acft_electrification_icct['replacable turboprop traffic, current EMF [%]'],
    color = 'red',
    linestyle = '--',
    linewidth = 1
)
ax[1].plot(
    df_acft_electrification_icct['battery energy density, turboprop traffic, 15% EMF reduction [Wh/kg]'],
    df_acft_electrification_icct['replacable turboprop traffic, 15% EMF reduction [%]'],
    color = 'orange',
    linestyle = '--',
    linewidth = 1
)
ax[1].plot(
    df_acft_electrification_icct['battery energy density, turboprop traffic, 30% EMF reduction [Wh/kg]'],
    df_acft_electrification_icct['replacable turboprop traffic, 30% EMF reduction [%]'],
    color = 'green',
    linestyle = '--',
    linewidth = 1
)

ax[0].scatter(
    df_lion_historical['Wh/kg (historical)'],
    df_lion_historical['Wh/l (historical)'],
    color = 'blue',
    s = 10
)

ax[0].scatter(
    df_lion_historical['Wh/kg (target)'],
    df_lion_historical['Wh/l (target)'],
    color = 'blue',
    s = 10
)
ax[0].scatter(
    df_lion_historical['Wh/kg (target)'],
    df_lion_historical['Wh/l (target)'],
    color = 'blue',
    s = 80,
    facecolors = 'none',
    edgecolors = 'blue'
)

# ANNOTATION ################

annotation_years_historical: list = [
    '1991',
    '1995',
    '2000',
    '2005',
    '2010',
    '2015',
    '2020'
]
annotation_years_target: list = [
    '2025',
    '2030'
]

for idx, row in df_lion_historical.iterrows():
    if row['year'] in annotation_years_historical:
        ax[0].annotate(
            text = row['year'],
            xy = (row['Wh/kg (historical)'], row['Wh/l (historical)'] - 50),
            ha='left',
            va='top',
            fontsize=9
        )
for idx, row in df_lion_historical.iterrows():
    if row['year'] in annotation_years_target:
        ax[0].annotate(
            text = row['year'],
            xy = (row['Wh/kg (target)'], row['Wh/l (target)'] - 50),
            ha='left',
            va='top',
            fontsize=9
        )

# LEGEND ####################

from matplotlib.patches import Patch
from matplotlib.lines import Line2D

legend_elements_categories = [
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'black',
        markerfacecolor='black',
        linestyle = 'None',
        markersize=4,
        marker='o',
        label = 'Best Commercial (historical)'
    ),
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'black',
        markerfacecolor='none',
        linestyle = 'None',
        markersize=7,
        marker='o',
        label = 'Future Targets'
    ),
    Patch(
        facecolor = 'none',
        edgecolor = 'black',
        label = 'Average (around 2010)'
    ),
]

legend_elements_battery_technology: list = []
def add_battery_technology_color_legend():
    for technology, legend_color in dict_battery_technologies.items():
        colored_line = Line2D(
            xdata = [0],
            ydata = [0],
            marker='none',
            color = legend_color,
            linestyle = '-',
            label = technology
        )
        legend_elements_battery_technology.append(colored_line)

add_battery_technology_color_legend()

legend_categories = ax[0].legend(
    handles = legend_elements_categories,
    loc = 'upper right',
)
ax[0].add_artist(legend_categories)

ax[0].legend(
    handles = legend_elements_battery_technology,
    loc = 'upper left',
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
# %%
