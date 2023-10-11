#%%
# runs code as interactive cell 

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
import scipy
from scipy.interpolate import interp1d

# i/o
from pathlib import PurePath, Path

# SETUP #########################################

plt.rcParams.update({
    # "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 11
})

# DATA IMPORT ###################################

df_Swiss = pd.read_excel(
    io = r'C:\Users\franz\OneDrive - Alte Kantonsschule Aarau\Praktikum PSI\data\data.xlsx',
    sheet_name = 'Swiss',
    usecols = lambda column: column in [
        'efficiency (x)',
        'efficiency (y)',
        'ops (x)',
        'ops (y)',
        'econ (x)',
        'econ (y)',
        'reduced (x)',
        'reduced (y)',
        'offset (x)',
        'offset (y)',
        'saf (x)',
        'saf (y)',
    ],
    dtype={
        'efficiency (x)': float,
        'efficiency (y)': float,
        'ops (x)': float,
        'ops (y)': float,
        'econ (x)': float,
        'econ (y)': float,
        'saf (x)': float,
        'saf (y)': float,
        'offset (x)': float,
        'offset (y)': float,
        'reduced (x)': float,
        'reduced (y)': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal=','
)

# DATA MANIPULATION #############################

# this is the new list of years
list_of_years: list[int] = [i for i in range(2018, 2050+1)]

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
    df_interpolated[name_of_column_to_interpolate_y + '_interpolated'] = [interpolation_polynomial(x_value) for x_value in new_x_values]
    return df_interpolated

df_Swiss_efficiency: pd.DataFrame = interpolate_1d_dataframe(
    df = df_Swiss,
    name_of_column_to_interpolate_x ='efficiency (x)',
    name_of_column_to_interpolate_y ='efficiency (y)',
    new_x_values = list_of_years,
)

df_Swiss_ops: pd.DataFrame = interpolate_1d_dataframe(
    df = df_Swiss,
    name_of_column_to_interpolate_x ='ops (x)',
    name_of_column_to_interpolate_y ='ops (y)',
    new_x_values = list_of_years,
)

df_Swiss_saf: pd.DataFrame = interpolate_1d_dataframe(
    df = df_Swiss,
    name_of_column_to_interpolate_x ='saf (x)',
    name_of_column_to_interpolate_y ='saf (y)',
    new_x_values = list_of_years,
)

df_Swiss_offset: pd.DataFrame = interpolate_1d_dataframe(
    df = df_Swiss,
    name_of_column_to_interpolate_x ='offset (x)',
    name_of_column_to_interpolate_y ='offset (y)',
    new_x_values = list_of_years,
)

df_Swiss_reduced: pd.DataFrame = interpolate_1d_dataframe(
    df = df_Swiss,
    name_of_column_to_interpolate_x ='reduced (x)',
    name_of_column_to_interpolate_y ='reduced (y)',
    new_x_values = list_of_years,
)

df_Swiss_econ: pd.DataFrame = interpolate_1d_dataframe(
    df = df_Swiss,
    name_of_column_to_interpolate_x ='econ (x)',
    name_of_column_to_interpolate_y ='econ (y)',
    new_x_values = list_of_years,
)



# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 1,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
)

# AXIS SCALING ###############

# AXIS LIMITS ################


# TICKS AND LABELS ###########


# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################


# PLOTTING ###################




ax.plot(
    df_Swiss_efficiency['year'],
    df_Swiss_efficiency['efficiency (y)_interpolated'],
    label = 'efficiency',
    color = 'red'
)

ax.plot(
    df_Swiss_ops['year'],
    df_Swiss_ops['ops (y)_interpolated'],
    label = 'ops',
    color = 'yellow'
)

ax.plot(
    df_Swiss_offset['year'],
    df_Swiss_offset['offset (y)_interpolated'],
    label = 'offset',
    color = 'blue'
)

ax.plot(
    df_Swiss_saf['year'],
    df_Swiss_saf['saf (y)_interpolated'],
    label = 'saf',
    color = 'purple'
)

ax.plot(
    df_Swiss_reduced['year'],
    df_Swiss_reduced['reduced (y)_interpolated'],
    label = 'reduced',
    color = 'grey'
)


ax.plot(
    df_Swiss_econ['year'],
    df_Swiss_econ['econ (y)_interpolated'],
    label = 'econ',
    color = 'green'
)

# LEGEND ####################

ax.legend(
    loc = 'lower left',
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
