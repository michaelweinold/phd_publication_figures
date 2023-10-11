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

# DIRECTORIES ###################################

path_dir_data_bars: PurePath = Path.cwd().joinpath('data/bars')
path_dir_data_lines: PurePath = Path.cwd().joinpath('data/lines')

# DATA IMPORT ###################################

df_destination2050 = pd.read_excel(
    io = './data/data.xlsx',
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
        'Net_CO2_emissions (y)'
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
        'Net_CO2_emissions (y)': float
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
    df_interpolated['y'] = [interpolation_polynomial(x_value) for x_value in new_x_values]
    return df_interpolated

df_destination2050_net: pd.DataFrame = interpolate_1d_dataframe(
    df = df_destination2050,
    name_of_column_to_interpolate_x ='Net_CO2_emissions (x)',
    name_of_column_to_interpolate_y ='Net_CO2_emissions (y)',
    new_x_values = list_of_years,
)

df_destination2050_reference: pd.DataFrame = interpolate_1d_dataframe(
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

ax.set_ylim(0, 300)
ax.set_xlim(2013, 2051)

# TICKS AND LABELS ###########

# GRIDS ######################

ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='y', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Aviation Emissions \n (EU27 $\cup$ UK $\cup$ EFTA) [Mt(CO$_2$)]")


# PLOTTING ###################

ax.plot(
    df_destination2050_reference['year'],
    df_destination2050_reference['y'],
    label = 'Reference Scenario (BAU)',
    color = 'red',
    linestyle = '-.',
)
ax.plot(
    df_destination2050_net['year'],
    df_destination2050_net['y'],
    label = 'Net Emissions',
    color = 'black'
)


ax.bar(
    x = df_destination2050_effect_SAF['year'],
    height = df_destination2050_effect_SAF['y'] - df_destination2050_net['y'],
    bottom = df_destination2050_net['y'], 
    width=0.8,
    color = 'red',
    label = 'Market Measures',
)
ax.bar(
    x = df_destination2050_SAF['year'],
    height = df_destination2050_SAF['y'] - df_destination2050_effect_SAF['y'],
    bottom = df_destination2050_effect_SAF['y'], 
    width=0.8,
    color = 'green',
    label = 'SAF',
)
ax.bar(
    x = df_destination2050_effect_hydrogen['year'],
    height = df_destination2050_effect_hydrogen['y'] - df_destination2050_SAF['y'],
    bottom = df_destination2050_SAF['y'], 
    width=0.8,
    color = 'orange',
    label = 'Operations and Infrastructure',
)
ax.bar(
    x = df_destination2050_reference['year'],
    height = df_destination2050_reference['y'] - df_destination2050_effect_hydrogen['y'],
    bottom = df_destination2050_effect_hydrogen['y'], 
    width=0.8,
    color = 'blue',
    label = 'Technology',
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
