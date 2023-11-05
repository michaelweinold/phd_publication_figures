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
df_batteries_2011 = pd.read_excel(
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

# DATA MANIPULATION #############################

# BUILD RECTANGLES ###############

dict_battery_technologies: dict = {
    'Lead-Acid': 'red',
    'Ni-Cd': 'green',
    'Ni-MH': 'orange',
    'Li-ion': 'blue',
    'Li-S': 'purple',
    'Li-metal': 'brown',
}

import matplotlib.patches as patches
import matplotlib.colors as colors

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
    df_batteries = df_batteries_2011
)

battery_rectangles_2011_inset = copy_rectangles_for_inset(battery_rectangles_2011)

# FIGURE ########################################

# SETUP ######################

fig, ax_Wh = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 2,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm,
        gridspec_kw = dict(
            width_ratios=[9, 1],
        ),
        sharey=True
    )
plt.subplots_adjust(wspace=0.075)

# AXIS UNIT CONVERSION #######
# compare: https://stackoverflow.com/a/64922723/
# compare: https://matplotlib.org/stable/gallery/subplots_axes_and_figures/fahrenheit_celsius_scales.html

ax_MJ_x = ax_Wh[0].twiny() # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.twiny.html
ax_MJ_y = ax_Wh[1].twinx() # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.twinx.html

def convert_xaxis_units_from_MJ_to_Wh(axis_Wh = ax_Wh[0]):
    x_lower_Wh, x_upper_Wh = axis_Wh.get_xlim()
    x_lower_MJ = x_lower_Wh * 0.0036 # https://www.wolframalpha.com/input?i=1+Wh+in+MJ
    x_upper_MJ = x_upper_Wh * 0.0036 # https://www.wolframalpha.com/input?i=1+Wh+in+MJ
    ax_MJ_x.set_xlim(x_lower_MJ, x_upper_MJ)
    ax_MJ_x.figure.canvas.draw()

def convert_yaxis_units_from_MJ_to_Wh(axis_Wh = ax_Wh[0]):
    y_lower_Wh, y_upper_Wh = axis_Wh.get_ylim()
    y_lower_MJ = y_lower_Wh * 0.0036 # https://www.wolframalpha.com/input?i=1+Wh+in+MJ
    y_upper_MJ = y_upper_Wh * 0.0036 # https://www.wolframalpha.com/input?i=1+Wh+in+MJ
    ax_MJ_y.set_ylim(y_lower_MJ, y_upper_MJ)
    ax_MJ_y.figure.canvas.draw()

# AXIS LIMITS ################

ax_Wh[0].callbacks.connect("xlim_changed", convert_xaxis_units_from_MJ_to_Wh)
ax_Wh[0].callbacks.connect("ylim_changed", convert_yaxis_units_from_MJ_to_Wh)

ax_Wh[0].set_xlim(0,16000)
ax_Wh[0].set_ylim(0,10000)

ax_Wh[1].set_xlim(39700,40000)

# TICKS AND LABELS ###########

def thousand_formatter(value, tick_number):
    """
    Formats the tick label with thousand separators: 1000 = 1'000.
    """
    return f"{int(value):,}".replace(",", "'")

ax_Wh[0].xaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))
ax_Wh[0].yaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))

ax_Wh[1].xaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))

ax_Wh[0].minorticks_on()
ax_Wh[0].tick_params(axis='x', which='both', bottom=False)
ax_Wh[0].tick_params(axis='y', which='both', bottom=False)

ax_Wh[1].minorticks_on()
ax_Wh[1].tick_params(axis='x', which='both', bottom=False)
ax_Wh[1].tick_params(axis='y', which='both', bottom=False)

# GRIDS ######################

ax_Wh[0].grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax_Wh[0].grid(which='both', axis='x', linestyle='-', linewidth = 0.5)

ax_Wh[1].grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax_Wh[1].grid(which='both', axis='x', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

ax_Wh[0].set_xlabel("Gravimetric Energy Density [Wh/kg]")
ax_Wh[0].set_ylabel("Volumetric Energy Density [Wh/l]")

ax_MJ_x.set_xlabel("Gravimetric Energy Density [MJ/kg]")
ax_MJ_y.set_ylabel("Volumetric Energy Density [MJ/l]")

# PLOTTING ###################

ax_Wh[0].scatter(
    df_fuels['Wh/kg'],
    df_fuels['Wh/l'],
    color = 'black',
    s = 10
)
ax_Wh[1].scatter(
    df_fuels['Wh/kg'],
    df_fuels['Wh/l'],
    color = 'black',
    s = 10
)
for rectangle in battery_rectangles_2011:
    ax_Wh[0].add_patch(rectangle)

# LEGEND ####################

from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# Convert color name to RGB
rgb = colors.to_rgb('black')
# Add alpha to create RGBA
rgba = (*rgb, 0.2)  # adjust alpha value to suit your needs

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
        facecolor = rgba,
        edgecolor = 'black',
        label = 'Batteries'
    ),
]

ax_Wh[0].legend(
    handles=legend_elements,
    loc='lower left',
    bbox_to_anchor=(0.1, 0.01),
)

# ANNOTATION ################

for idx, row in df_fuels.iterrows():
    ax_Wh[0].annotate(
        text = row['substance'],
        xy = (row['Wh/kg']+100, row['Wh/l']),
        ha='right',
        va='bottom',
        fontsize=9
    )
    ax_Wh[1].annotate(
        row['substance'],
        (row['Wh/kg'], row['Wh/l']),
        ha='left',
        va='bottom',
        fontsize=9
    )

# ZOOM #######################

from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes

ax_battery_inset = zoomed_inset_axes(
    parent_axes = ax_Wh[0],
    zoom = 8.5,
    loc = 'upper left',
    #bbox_to_anchor = [0.05, 0.1, 0.5, 0.5]
)
mark_inset(
    parent_axes = ax_Wh[0],
    inset_axes = ax_battery_inset,
    loc1=2,
    loc2=4,
    fc="none",
    ec="black"
)
ax_battery_inset.axis([0, 400, 0, 600])
ax_battery_inset.xaxis.set_major_locator(ticker.MultipleLocator(base=100))
ax_battery_inset.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax_battery_inset.grid(which='both', axis='x', linestyle='-', linewidth = 0.5)
ax_battery_inset.yaxis.tick_right()

battery_rectangles_2011_copy = battery_rectangles_2011.copy()

for rectangle in battery_rectangles_2011_inset:
    ax_battery_inset.add_patch(rectangle)


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
