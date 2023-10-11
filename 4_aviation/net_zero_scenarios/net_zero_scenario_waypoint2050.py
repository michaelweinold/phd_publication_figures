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
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 11
})

# DATA IMPORT ###################################

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
list_of_years: list[int] = [i for i in range(2015, 2050+1)]

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
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
)

# AXIS SCALING ###############

# AXIS LIMITS ################

ax.set_ylim(0, 2000)
ax.set_xlim(2013, 2051)

# TICKS AND LABELS ###########

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Aviation Emissions \n (Global) [Mt(CO$_2$)]")

# PLOTTING ###################

ax.bar(
    x = df_WayPoint2050_reduced['year'],
    height = df_WayPoint2050_MarketBased_Measure['y'] - df_WayPoint2050_reduced['y'],
    bottom = df_WayPoint2050_reduced['y'], 
    width=0.8,
    color = 'red',
    label = 'Market Measures',
)
ax.bar(
    x = df_WayPoint2050_reduced['year'],
    height = df_WayPoint2050_SAF['y'] - df_WayPoint2050_MarketBased_Measure['y'],
    bottom = df_WayPoint2050_MarketBased_Measure['y'], 
    width=0.8,
    color = 'green',
    label = 'SAF',
)
ax.bar(
    x = df_WayPoint2050_reduced['year'],
    height = df_WayPoint2050_Operations_and_Infrastructure['y'] - df_WayPoint2050_SAF['y'],
    bottom = df_WayPoint2050_SAF['y'], 
    width=0.8,
    color = 'orange',
    label = 'Operations and Infrastructure',
)
ax.bar(
    x = df_WayPoint2050_reduced['year'],
    height = df_WayPoint2050_Technology['y'] - df_WayPoint2050_Operations_and_Infrastructure['y'],
    bottom = df_WayPoint2050_Operations_and_Infrastructure['y'], 
    width=0.8,
    color = 'blue',
    label = 'Technology',
)

ax.plot(
    df_WayPoint2050_Technology['year'],
    df_WayPoint2050_Technology['y'],
    label = 'Reference Scenario (BAU)',
    color = 'red',
    linestyle = '-.',
)
ax.plot(
    df_WayPoint2050_reduced['year'],
    df_WayPoint2050_reduced['y'],
    label = 'Net Emissions',
    color = 'black'
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
