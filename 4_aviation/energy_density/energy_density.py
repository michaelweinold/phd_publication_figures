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

# DATA MANIPULATION #############################

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

ax_MJ_x = ax_Wh[0].twiny() # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.twiny.html
ax_MJ_y = ax_Wh[0].twinx() # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.twinx.html

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

ax_Wh[1].set_xlim(140,150)

# TICKS AND LABELS ###########

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
)
ax_Wh[1].scatter(
    df_fuels['Wh/kg'],
    df_fuels['Wh/l'],
    color = 'black',
)

# LEGEND ####################

# ANNOTATION ################



# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%
