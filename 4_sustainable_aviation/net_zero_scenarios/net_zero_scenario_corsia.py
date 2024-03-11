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
from scipy.interpolate import interp1d

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

df_input = pd.read_excel(
    io = './data/data.xlsx',
    sheet_name = 'CORSIA',
    usecols = lambda column: column in [
        'net (x)',
        'net (y)',
        'corsia (x)',
        'corsia (y)',
        'tech (x)',
        'tech (y)',
        'baseline (x)',
        'baseline (y)',
    ],
    dtype={
        'net (x)': float,
        'net (y)': float,
        'corsia (x)': float,
        'corsia (y)': float,
        'tech (x)': float,
        'tech (y)': float,
        'baseline (x)': float,
        'baseline (y)': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal=','
)

# DATA MANIPULATION #############################

# this is the new list of years
list_of_years: list[int] = [i for i in range(2015, 2035+1)]

def interpolate_1d_dataframe(
    df: pd.DataFrame,
    name_of_column_to_interpolate_x: str,
    name_of_column_to_interpolate_y: str,
    new_x_values: list[int],
) -> pd.DataFrame:
    df_interpolated = pd.DataFrame()
    df_interpolated['year'] = new_x_values
    interpolation_polynomial = interp1d(
        x = df[name_of_column_to_interpolate_x].dropna(), # 'NaN' values usually cause problems, so we remove them here
        y = df[name_of_column_to_interpolate_y].dropna(), # 'NaN' values usually cause problems, so we remove them here
    )
    df_interpolated['y'] = [interpolation_polynomial(x_value) for x_value in new_x_values]
    return df_interpolated


df_net: pd.DataFrame = interpolate_1d_dataframe(
    df = df_input,
    name_of_column_to_interpolate_x ='net (x)',
    name_of_column_to_interpolate_y ='net (y)',
    new_x_values = list_of_years,
)

df_tech: pd.DataFrame = interpolate_1d_dataframe(
    df = df_input,
    name_of_column_to_interpolate_x ='tech (x)',
    name_of_column_to_interpolate_y ='tech (y)',
    new_x_values = list_of_years,
)

df_corsia: pd.DataFrame = interpolate_1d_dataframe(
    df = df_input,
    name_of_column_to_interpolate_x ='corsia (x)',
    name_of_column_to_interpolate_y ='corsia (y)',
    new_x_values = list_of_years,
)

df_baseline: pd.DataFrame = interpolate_1d_dataframe(
    df = df_input,
    name_of_column_to_interpolate_x ='baseline (x)',
    name_of_column_to_interpolate_y ='baseline (y)',
    new_x_values = list_of_years,
)

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm
    )

# DATA #######################

# AXIS LIMITS ################

ax.set_ylim(0, 1800)
ax.set_xlim(2013, 2051)

# TICKS AND LABELS ###########

# GRIDS ######################

ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='y', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Global Aviation Emissions [Mt(CO$_2$)]")


# PLOTTING ###################

ax.plot(
    df_net['year'],
    df_net['y'],
    label = 'Reference Scenario (BAU)',
    color = 'red',
    linestyle = '-.',
)
ax.plot(
    df_baseline['year'],
    df_baseline['y'],
    label = 'Net Emissions',
    color = 'black'
)

ax.bar(
    x = df_tech['year'],
    height = df_net['y'] - df_tech['y'],
    bottom = df_tech['y'],
    width=0.8,
    color = 'orange',
    label = 'Operations',
)

ax.bar(
    x = df_tech['year'],
    height = df_tech['y'] - df_corsia['y'],
    bottom = df_corsia['y'],
    width=0.8,
    color = 'blue',
    label = 'Technology',
)

ax.bar(
    x = df_corsia['year'],
    height = df_corsia['y'] - df_baseline['y'],
    bottom = df_baseline['y'],
    width=0.8,
    color = 'green',
    label = 'SAF+CORSIA',
)

plt.axvline(
    x = 2024,
    ymin = 0,
    ymax = 1800,
    color = 'black',
    linestyle='--'
)
ax.annotate(
    'Volontary',  # Text to display in the annotation box
    xy=(2023, 250),  # Position of the upper end of the vertical line
    ha='left',  # Horizontal alignment of the text
    va='bottom',  # Vertical alignment of the text
    backgroundcolor = 'white'
)

plt.axvline(
    x = 2027,
    ymin = 0,
    ymax = 1800,
    color = 'black',
    linestyle='--'
)
ax.annotate(
    'Mandatory',  # Text to display in the annotation box
    xy=(2026, 70),  # Position of the upper end of the vertical line
    ha='left',  # Horizontal alignment of the text
    va='bottom',  # Vertical alignment of the text
    backgroundcolor = 'white'
)

# LEGEND ####################

ax.legend(
    loc = 'upper left',
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
