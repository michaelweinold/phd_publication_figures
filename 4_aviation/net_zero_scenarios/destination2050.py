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

df_destination2050 = pd.read_excel(
    io = r'C:\Users\franz\OneDrive - Alte Kantonsschule Aarau\Praktikum PSI\data\data.xlsx',
    sheet_name = 'Destination2050',
    usecols = lambda column: column in [
        'hypothetical_reference (x)',
        'hypothetical_reference (y)',
        'kerosene (x)',
        'kerosene (y)',
        'hydrogen (x)',
        'hydrogen (y)',
        'effect_hydrogen (x)',
        'effect_hydrogen (y)',
        'improved_ATM_and_operations (x)',
        'improved_ATM_and_operations (y)',
        'SAF (x)',
        'SAF (y)',
        'effect_SAF (x)',
        'effect_SAF (y)',
        'economic_measures (x)',
        'economic_measures (y)',
        'effect_economic_measures (x)',
        'effect_economic_measures (y)',
        'Net_CO2_emissions (x)',
        'Net_CO2_emissions (y)',
    ],
    dtype={
        'hypothetical_reference (x)': float,
        'hypothetical_reference (y)': float,
        'kerosene (x)': float,
        'kerosene (y)': float,
        'hydrogen (x)': float,
        'hydrogen (y)': float,
        'effect_hydrogen (x)': float,
        'effect_hydrogen (y)': float,
        'improved_ATM_and_operations (x)': float,
        'improved_ATM_and_operations (y)': float,
        'SAF (x)': float,
        'SAF (y)': float,
        'effect_SAF (x)': float,
        'effect_SAF (y)': float,
        'economic_measures (x)': float,
        'economic_measures (y)': float,
        'effect_economic_measures (x)': float,
        'effect_economic_measures (y)': float,
        'Net_CO2_emissions (x)': float,
        'Net_CO2_emissions (y)': float,
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

df_destination2050_hypothetical_reference: pd.DataFrame = interpolate_1d_dataframe(
    df = df_destination2050,
    name_of_column_to_interpolate_x ='hypothetical_reference (x)',
    name_of_column_to_interpolate_y ='hypothetical_reference (y)',
    new_x_values = list_of_years,
)

df_destination2050_kerosene: pd.DataFrame = interpolate_1d_dataframe(
    df = df_destination2050,
    name_of_column_to_interpolate_x ='kerosene (x)',
    name_of_column_to_interpolate_y ='kerosene (y)',
    new_x_values = list_of_years,
)

df_destination2050_hydrogen: pd.DataFrame = interpolate_1d_dataframe(
    df = df_destination2050,
    name_of_column_to_interpolate_x ='hydrogen (x)',
    name_of_column_to_interpolate_y ='hydrogen (y)',
    new_x_values = list_of_years,
)

df_destination2050_effect_hydrogen: pd.DataFrame = interpolate_1d_dataframe(
    df = df_destination2050,
    name_of_column_to_interpolate_x ='effect_hydrogen (x)',
    name_of_column_to_interpolate_y ='effect_hydrogen (y)',
    new_x_values = list_of_years,
)

df_destination2050_improved_ATM_and_operations: pd.DataFrame = interpolate_1d_dataframe(
    df = df_destination2050,
    name_of_column_to_interpolate_x ='improved_ATM_and_operations (x)',
    name_of_column_to_interpolate_y ='improved_ATM_and_operations (y)',
    new_x_values = list_of_years,
)

df_destination2050_SAF: pd.DataFrame = interpolate_1d_dataframe(
    df = df_destination2050,
    name_of_column_to_interpolate_x ='SAF (x)',
    name_of_column_to_interpolate_y ='SAF (y)',
    new_x_values = list_of_years,
)

df_destination2050_effect_SAF: pd.DataFrame = interpolate_1d_dataframe(
    df = df_destination2050,
    name_of_column_to_interpolate_x ='effect_SAF (x)',
    name_of_column_to_interpolate_y ='effect_SAF (y)',
    new_x_values = list_of_years,
)

df_destination2050_economic_measures: pd.DataFrame = interpolate_1d_dataframe(
    df = df_destination2050,
    name_of_column_to_interpolate_x ='economic_measures (x)',
    name_of_column_to_interpolate_y ='economic_measures (y)',
    new_x_values = list_of_years,
)

df_destination2050_effect_economic_measures: pd.DataFrame = interpolate_1d_dataframe(
    df = df_destination2050,
    name_of_column_to_interpolate_x ='effect_economic_measures (x)',
    name_of_column_to_interpolate_y ='effect_economic_measures (y)',
    new_x_values = list_of_years,
)

df_destination2050_Net_CO2_emissions: pd.DataFrame = interpolate_1d_dataframe(
    df = df_destination2050,
    name_of_column_to_interpolate_x ='Net_CO2_emissions (x)',
    name_of_column_to_interpolate_y ='Net_CO2_emissions (y)',
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
    df_destination2050_hypothetical_reference['year'],
    df_destination2050_hypothetical_reference['hypothetical_reference (y)_interpolated'],
    label = 'hypothetical_reference',
    color = 'blue'
)

ax.plot(
    df_destination2050_kerosene['year'],
    df_destination2050_kerosene['kerosene (y)_interpolated'],
    label = 'kerosene',
    color = 'yellow'
)

ax.plot(
    df_destination2050_hydrogen['year'],
    df_destination2050_hydrogen['hydrogen (y)_interpolated'],
    label = 'hydrogen',
    color = 'orange'
)

ax.plot(
    df_destination2050_effect_hydrogen['year'],
    df_destination2050_effect_hydrogen['effect_hydrogen (y)_interpolated'],
    label = 'effect_hydrogen',
    color = 'red'
)

ax.plot(
    df_destination2050_improved_ATM_and_operations['year'],
    df_destination2050_improved_ATM_and_operations['improved_ATM_and_operations (y)_interpolated'],
    label = 'improved_ATM_and_operations',
    color = 'pink'
)

ax.plot(
    df_destination2050_SAF['year'],
    df_destination2050_SAF['SAF (y)_interpolated'],
    label = 'SAF',
    color = 'purple'
)

ax.plot(
    df_destination2050_effect_SAF['year'],
    df_destination2050_effect_SAF['effect_SAF (y)_interpolated'],
    label = 'effect_SAF (x)',
    color = 'green'
)

ax.plot(
    df_destination2050_economic_measures['year'],
    df_destination2050_economic_measures['economic_measures (y)_interpolated'],
    label = 'economic_measures',
    color = 'black'
)

ax.plot(
    df_destination2050_effect_economic_measures['year'],
    df_destination2050_effect_economic_measures['effect_economic_measures (y)_interpolated'],
    label = 'effect_economic_measures',
    color = 'gray'
)

ax.plot(
    df_destination2050_Net_CO2_emissions['year'],
    df_destination2050_Net_CO2_emissions['Net_CO2_emissions (y)_interpolated'],
    label = 'Net_CO2_emissions',
    color = 'navy'
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
