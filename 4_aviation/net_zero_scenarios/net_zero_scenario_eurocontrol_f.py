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

df_eurocontrol = pd.read_excel(
    io = r'C:\Users\franz\OneDrive - Alte Kantonsschule Aarau\Praktikum PSI\data\data.xlsx',
    sheet_name = 'Eurocontrol',
    usecols = lambda column: column in [
        'best_case (x)',
        'best_case (y)',
        'Other (x)',
        'Other (y)',
        'SAF (x)',
        'SAF (y)',
        'ATM (x)',
        'ATM (y)',
        'Fleet_revol (x)',
        'Fleet_revol (y)',
        'Fleet_evol (x)',
        'Fleet_evol (y)',
    ],
    dtype={
        'best_case (x)': float,
        'best_case (y)': float,
        'Other (x)': float,
        'Other (y)': float,
        'SAF (x)': float,
        'SAF (y)': float,
        'ATM (x)': float,
        'ATM (y)': float,
        'Fleet_revol (x)': float,
        'Fleet_revol (y)': float,
        'Fleet_evol (x)': float,
        'Fleet_evol (y)': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal=','
)

# DATA MANIPULATION #############################

# this is the new list of years
list_of_years: list[int] = [i for i in range(2022, 2050+1)]

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

df_eurocontrol_Fleet_evol: pd.DataFrame = interpolate_1d_dataframe(
    df = df_eurocontrol,
    name_of_column_to_interpolate_x ='Fleet_evol (x)',
    name_of_column_to_interpolate_y ='Fleet_evol (y)',
    new_x_values = list_of_years,
)

df_eurocontrol_Fleet_revol: pd.DataFrame = interpolate_1d_dataframe(
    df = df_eurocontrol,
    name_of_column_to_interpolate_x ='Fleet_revol (x)',
    name_of_column_to_interpolate_y ='Fleet_revol (y)',
    new_x_values = list_of_years,
)

df_eurocontrol_best_case: pd.DataFrame = interpolate_1d_dataframe(
    df = df_eurocontrol,
    name_of_column_to_interpolate_x ='best_case (x)',
    name_of_column_to_interpolate_y ='best_case (y)',
    new_x_values = list_of_years,
)

df_eurocontrol_Other: pd.DataFrame = interpolate_1d_dataframe(
    df = df_eurocontrol,
    name_of_column_to_interpolate_x ='Other (x)',
    name_of_column_to_interpolate_y ='Other (y)',
    new_x_values = list_of_years,
)

df_eurocontrol_ATM: pd.DataFrame = interpolate_1d_dataframe(
    df = df_eurocontrol,
    name_of_column_to_interpolate_x ='ATM (x)',
    name_of_column_to_interpolate_y ='ATM (y)',
    new_x_values = list_of_years,
)

df_eurocontrol_SAF: pd.DataFrame = interpolate_1d_dataframe(
    df = df_eurocontrol,
    name_of_column_to_interpolate_x ='SAF (x)',
    name_of_column_to_interpolate_y ='SAF (y)',
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
    df_eurocontrol_Fleet_evol['year'],
    df_eurocontrol_Fleet_evol['Fleet_evol (y)_interpolated'],
    label = 'Fleet_evol',
    color = 'blue'
)

ax.plot(
    df_eurocontrol_best_case['year'],
    df_eurocontrol_best_case['best_case (y)_interpolated'],
    label = 'best_case',
    color = 'green'
)

ax.plot(
    df_eurocontrol_Other['year'],
    df_eurocontrol_Other['Other (y)_interpolated'],
    label = 'Other',
    color = 'red'
)

ax.plot(
    df_eurocontrol_SAF['year'],
    df_eurocontrol_SAF['SAF (y)_interpolated'],
    label = 'SAF',
    color = 'yellow'
)

ax.plot(
    df_eurocontrol_ATM['year'],
    df_eurocontrol_ATM['ATM (y)_interpolated'],
    label = 'ATM',
    color = 'orange'
)

ax.plot(
    df_eurocontrol_Fleet_revol['year'],
    df_eurocontrol_Fleet_revol['Fleet_revol (y)_interpolated'],
    label = 'Fleet_revol',
    color = 'purple'
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
