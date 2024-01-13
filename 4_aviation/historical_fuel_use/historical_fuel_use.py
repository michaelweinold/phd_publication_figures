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

df_co2_historical = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Global Aviation CO2',
    usecols = lambda column: column in [
        'Year',
        'Annual Emissions [kg(CO2)]',
    ],
    dtype={
        'year': float,
        'Annual Emissions [kg(CO2)]': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_fuel_global_ipcc = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Fuel Use Global (IPCC)',
    usecols = lambda column: column in [
        'Year',
        'Fuel Burned [Gl]',
    ],
    dtype={
        'Year': float,
        'Fuel Burned [Gl]': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_fuel_usa = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Fuel Use USA',
    usecols = lambda column: column in [
        'Year',
        'Total [Gl]',
    ],
    dtype={
        'Year': float,
        'Total [Gl]': float,
    },
    header = 0,
    engine = 'openpyxl'
)
df_fuel_ussr = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Fuel Use USSR',
    usecols = lambda column: column in [
        'Year',
        'Total [Gl]',
    ],
    dtype={
        'Year': float,
        'Total [Gl]': float,
    },
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

df_co2_historical = df_co2_historical[df_co2_historical['Year'] <= 1971]
df_fuel_global_ipcc = df_fuel_global_ipcc[df_fuel_global_ipcc['Year'] <= 1980]

# peg co2 emissions data to fuel burn data
conversion_factor = df_fuel_global_ipcc['Fuel Burned [Gl]'].iloc[0] / df_co2_historical['Annual Emissions [kg(CO2)]'].iloc[-1]
df_co2_historical['Fuel Burned [Gl]'] = df_co2_historical['Annual Emissions [kg(CO2)]'] * conversion_factor

df_fuel_usa = df_fuel_usa[df_fuel_usa['Year'] <= 1980]
df_fuel_ussr = df_fuel_ussr[df_fuel_ussr['Year'] <= 1980]

# extrapolate data
# https://docs.scipy.org/doc/scipy/tutorial/interpolate/1D.html
years_complete = np.arange(1960, 1981, 1)

df_fuel_ussr_extrapolated = pd.DataFrame()
df_fuel_ussr_extrapolated['Year'] = years_complete
df_fuel_ussr_extrapolated['Total [Gl]'] = np.interp(
    x = years_complete,
    xp = df_fuel_ussr['Year'],
    fp = df_fuel_ussr['Total [Gl]']
)

df_fuel_usa_extrapolated = pd.DataFrame()
df_fuel_usa_extrapolated['Year'] = years_complete
df_fuel_usa_extrapolated['Total [Gl]'] = np.interp(
    x = years_complete,
    xp = df_fuel_usa['Year'],
    fp = df_fuel_usa['Total [Gl]']
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

# DATA #######################

# AXIS LIMITS ################

ax.set_xlim(
    1950,
    2023
)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Aviation Fuel Burned [Gl]")

# PLOTTING ###################

ax.plot(
    df_fuel_global_ipcc['Year'],
    df_fuel_global_ipcc['Fuel Burned [Gl]'],
    color = 'black',
    linewidth = 1,
    label = 'Fuel Burn'
)
ax.plot(
    df_co2_historical['Year'],
    df_co2_historical['Fuel Burned [Gl]'],
    color = 'blue',
    linewidth = 1,
)

ax.stackplot(
    df_fuel_usa_extrapolated['Year'],
    df_fuel_usa_extrapolated['Total [Gl]'],
    df_fuel_ussr_extrapolated['Total [Gl]'],
    colors = ['blue', 'red'],
    linewidth = 1,
    alpha = 0.5,
)

# LEGEND ####################

ax.legend(
    loc='upper left',
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
