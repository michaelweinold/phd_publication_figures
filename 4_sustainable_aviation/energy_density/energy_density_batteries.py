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
    sheet_name = 'Fuels',
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
df_batt_average = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Batteries (General)',
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
    sheet_name = 'Acft Replacement',
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
    sheet_name = 'Historical Li-Ion',
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

df_batt_limits = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Batteries Limits',
    usecols = lambda column: column in [
        'chemistry',
        'limit (practical) [Wh/kg]',
    ],
    dtype={
        'chemistry': str,
        'limit (practical) [Wh/kg]': float,
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
    'Li-metal': 'brown',
    'Li-S': 'purple',
}

import matplotlib.patches as patches
import matplotlib.colors as colors

def build_rectangles(
        dict_battery_technologies: dict,
        df_batt_average: pd.DataFrame
) -> List:
    
    list_rectangles: List = []

    for key, value in dict_battery_technologies.items():
        df_row: pd.DataFrame = df_batt_average.loc[df_batt_average['technology'] == key]
        x_min: float = df_row['range lower [Wh/kg]'].iloc[0]
        x_max: float = df_row['range higher [Wh/kg]'].iloc[0]
        y_min: float = df_row['range lower [Wh/l]'].iloc[0]
        y_max: float = df_row['range higher [Wh/l]'].iloc[0]

        # Convert color name to RGB
        rgb = colors.to_rgb(value)
        
        # Add alpha to create RGBA
        rgba = (*rgb, 0.2)  # adjust alpha value to suit your needs

        rectangle = patches.Rectangle(
            xy = (x_min, y_min),
            width = x_max - x_min,
            height = y_max - y_min,
            edgecolor = value,
            facecolor = rgba,
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
    df_batt_average = df_batt_average
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
            height_ratios=[3.5, 1],
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
ax[1].set_ylabel("Replacable [\%]")
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
    color = 'green',
    linestyle = '-',
    linewidth = 1
)
ax[1].plot(
    df_acft_electrification_icct['battery energy density, commuter traffic, 15% EMF reduction [Wh/kg]'],
    df_acft_electrification_icct['replacable commuter traffic, 15% EMF reduction [%]'],
    color = 'green',
    linestyle = '--',
    linewidth = 1
)
"""
ax[1].plot(
    df_acft_electrification_icct['battery energy density, commuter traffic, 30% EMF reduction [Wh/kg]'],
    df_acft_electrification_icct['replacable commuter traffic, 30% EMF reduction [%]'],
    color = 'green',
    linestyle = '-',
    linewidth = 1
)
"""
ax[1].plot(
    df_acft_electrification_icct['battery energy density, turboprop traffic, current EMF [Wh/kg]'],
    df_acft_electrification_icct['replacable turboprop traffic, current EMF [%]'],
    color = 'red',
    linestyle = '-',
    linewidth = 1
)
ax[1].plot(
    df_acft_electrification_icct['battery energy density, turboprop traffic, 15% EMF reduction [Wh/kg]'],
    df_acft_electrification_icct['replacable turboprop traffic, 15% EMF reduction [%]'],
    color = 'red',
    linestyle = '--',
    linewidth = 1
)
"""
ax[1].plot(
    df_acft_electrification_icct['battery energy density, turboprop traffic, 30% EMF reduction [Wh/kg]'],
    df_acft_electrification_icct['replacable turboprop traffic, 30% EMF reduction [%]'],
    color = 'green',
    linestyle = '--',
    linewidth = 1
)
"""
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

ax[0].axvline(
    x = df_batt_limits.loc[df_batt_limits['chemistry'] == 'Li-ion']['limit (practical) [Wh/kg]'].iloc[0],
    color = 'blue',
    ls = '--',
)
ax[0].axvline(
    x = df_batt_limits.loc[df_batt_limits['chemistry'] == 'Li-metal']['limit (practical) [Wh/kg]'].iloc[0],
    color = 'brown',
    ls = '--',
)
ax[0].axvline(
    x = df_batt_limits.loc[df_batt_limits['chemistry'] == 'Li-S']['limit (practical) [Wh/kg]'].iloc[0],
    color = 'purple',
    ls = '--',
)
ax[0].axvline(
    x = df_batt_limits.loc[df_batt_limits['chemistry'] == 'Li-O2']['limit (practical) [Wh/kg]'].iloc[0],
    color = 'black',
)
ax[0].axvline(
    x = df_batt_limits.loc[df_batt_limits['chemistry'] == 'Zn-O2']['limit (practical) [Wh/kg]'].iloc[0],
    color = 'black',
)

# Create a custom colormap going from white to red to white
from matplotlib.colors import LinearSegmentedColormap
cols = [(1, 1, 1), (0, 0, 0), (1, 1, 1)]  # White -> Red -> White
n_bins = 100  # Number of bins for the colormap
cmap_name = 'white_black_white'
# Register the colormap if it's not already registered
if cmap_name not in plt.colormaps():
    plt.register_cmap(cmap=LinearSegmentedColormap.from_list(cmap_name, cols, N=n_bins))

gradient = np.linspace(0, 1, 256)  # Create a 1D array with 256 values evenly spaced between 0 and 1
gradient = np.vstack((gradient, gradient))  # Stack the 1D array vertically to create a 2D array
ax[0].imshow(
    gradient,
    aspect = 'auto',
    cmap = plt.get_cmap(cmap_name),
    extent = [
        350,
        600,
        320,
        1000
    ]
)

ax[0].text(
    x=420,
    y=650,
    s=r'Electric Acft. \\ Batteries ($\sim$ 2023)',
    ha='left',
    va='center',
    fontsize=11,
    fontweight='bold',
    color='white',
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

# Convert color name to RGB
rgb = colors.to_rgb('black')
# Add alpha to create RGBA
rgba = (*rgb, 0.2)  # adjust alpha value to suit your needs


legend_elements_categories = [
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'black',
        markerfacecolor='black',
        linestyle = 'None',
        markersize=4,
        marker='o',
        label = 'Best Commercial'
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
        facecolor = rgba,
        edgecolor = 'black',
        label = 'Commercial Average'
    ),
    Line2D(
        [0],
        [0],
        color='black',
        lw=2,
        ls='--',
        label='Phys. Limits'
    )
]

legend_elements_battery_technology: list = []
def add_battery_technology_color_legend():
    for technology, legend_color in dict_battery_technologies.items():
        patch = Patch(
            facecolor = legend_color,
            edgecolor = 'none',
            label = technology
        )
        legend_elements_battery_technology.append(patch)

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

legend_elements_categories_2 = [
    Line2D(
        [0],
        [0],
        color='green',
        lw=2,
        ls='-',
        label='Commuter'
    ),
    Line2D(
        [0],
        [0],
        color='red',
        lw=2,
        ls='-',
        label='Turboprop'
    ),
    Line2D(
        [0],
        [0],
        color='black',
        lw=2,
        ls='-',
        label='Current kg'
    ),
    Line2D(
        [0],
        [0],
        color='black',
        lw=2,
        ls='--',
        label='15\% less kg'
    )
]

ax[1].legend(
    handles=legend_elements_categories_2,
    loc='lower left',
    ncol=2
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
