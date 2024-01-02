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
df_eurocontrol = pd.read_excel(
    io = './data/data.xlsx',
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
df_Swiss = pd.read_excel(
    io = './data/data.xlsx',
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
df_WayPoint2050 = pd.read_excel(
    io = './data/data.xlsx',
    sheet_name = 'WayPoint2050',
    usecols = lambda column: column in [
        'reduced (x)',
        'reduced (y)',
        'MarketBased_Measure (x)',
        'MarketBased_Measure (y)',
        'SAF (x)',
        'SAF (y)',
        'Operations_and_Infrastructure (x)',
        'Operations_and_Infrastructure (y)',
        'Technology (x)',
        'Technology (y)',
    ],
    dtype={
        'reduced (x)': float,
        'reduced (y)': float,
        'MarketBased_Measure (x)': float,
        'MarketBased_Measure (y)': float,
        'SAF (x)': float,
        'SAF (y)': float,
        'Operations_and_Infrastructure (x)': float,
        'Operations_and_Infrastructure (y)': float,
        'Technology (x)': float,
        'Technology (y)': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal=','
)

# DATA MANIPULATION #############################

# this is the new list of years
list_of_years: list[int] = [i for i in range(2020, 2050+1)]

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

df_WayPoint2050_reduced: pd.DataFrame = interpolate_1d_dataframe(
    df = df_WayPoint2050,
    name_of_column_to_interpolate_x ='reduced (x)',
    name_of_column_to_interpolate_y ='reduced (y)',
    new_x_values = list_of_years,
)

df_WayPoint2050_MarketBased_Measure: pd.DataFrame = interpolate_1d_dataframe(
    df = df_WayPoint2050,
    name_of_column_to_interpolate_x ='MarketBased_Measure (x)',
    name_of_column_to_interpolate_y ='MarketBased_Measure (y)',
    new_x_values = list_of_years,
)

df_WayPoint2050_Operations_and_Infrastructure: pd.DataFrame = interpolate_1d_dataframe(
    df = df_WayPoint2050,
    name_of_column_to_interpolate_x ='Operations_and_Infrastructure (x)',
    name_of_column_to_interpolate_y ='Operations_and_Infrastructure (y)',
    new_x_values = list_of_years,
)

df_WayPoint2050_Technology: pd.DataFrame = interpolate_1d_dataframe(
    df = df_WayPoint2050,
    name_of_column_to_interpolate_x ='Technology (x)',
    name_of_column_to_interpolate_y ='Technology (y)',
    new_x_values = list_of_years,
)

df_WayPoint2050_SAF: pd.DataFrame = interpolate_1d_dataframe(
    df = df_WayPoint2050,
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
        figsize=(30*cm, 10*cm), # A4=(210x297)mm
    )

# DATA #######################

# AXIS LIMITS ################

ax.set_ylim(0, 110)
ax.set_xlim(2013, 2051)

# TICKS AND LABELS ###########

# GRIDS ######################

ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='y', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Global Aviation Emissions [Mt(CO$_2$)]")

# PLOTTING ###################

list_years_plot = [2020,2025,2030,2035,2040,2045,2050]

# destination 2050

def normalize_to_each_year(
    df_to_normalize: pd.DataFrame,
    df_reference: pd.DataFrame
) -> pd.DataFrame:
    df_normalized = pd.DataFrame()
    df_normalized['year'] = df_to_normalize['year']
    df_normalized['y'] = (df_to_normalize['y'] / df_reference['y'])*100
    return df_normalized

df_destination2050_net_normalized = normalize_to_each_year(df_destination2050_net, df_destination2050_reference)
df_destination2050_effect_SAF_normalized = normalize_to_each_year(df_destination2050_effect_SAF, df_destination2050_reference)
df_destination2050_SAF_normalized = normalize_to_each_year(df_destination2050_SAF, df_destination2050_reference)

ax.bar(
    x = df_destination2050_SAF_normalized[df_destination2050_SAF_normalized['year'].isin(list_years_plot)]['year'],
    height = df_destination2050_SAF_normalized[df_destination2050_SAF_normalized['year'].isin(list_years_plot)]['y'],
    bottom=df_destination2050_net_normalized[df_destination2050_net_normalized['year'].isin(list_years_plot)]['y'] + df_destination2050_net_normalized[df_destination2050_net_normalized['year'].isin(list_years_plot)]['y'],
    width=0.8,
    color = 'green',
    label = 'Not Compensated',
)
ax.bar(
    x = df_destination2050_net_normalized[df_destination2050_net_normalized['year'].isin(list_years_plot)]['year'],
    height = df_destination2050_net_normalized[df_destination2050_net_normalized['year'].isin(list_years_plot)]['y'],
    width=0.8,
    color = 'black',
    label = 'Not Compensated',
)
ax.bar(
    x = df_destination2050_effect_SAF_normalized[df_destination2050_effect_SAF_normalized['year'].isin(list_years_plot)]['year'],
    height = df_destination2050_effect_SAF_normalized[df_destination2050_effect_SAF_normalized['year'].isin(list_years_plot)]['y'],
    bottom=df_destination2050_net_normalized[df_destination2050_net_normalized['year'].isin(list_years_plot)]['y'],
    width=0.8,
    color = 'red',
    label = 'Not Compensated',
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
