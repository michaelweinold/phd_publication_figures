#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# sys
import os
# plotting
import matplotlib.pyplot as plt
# unit conversion
cm = 1/2.54 # for inches-cm conversion
# time manipulation
from datetime import datetime
# data science
import numpy as np
import pandas as pd

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 11
})

# DATA IMPORT ###################################

df_traffic = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'traffic',
    usecols = lambda column: column in [
        'Year',
        'RPKs',
    ],
    dtype={
        'Year': int,
        'RPKs': float,
    },
    header = 0,
    engine = 'openpyxl',
)
df_emissions = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'emissions',
    usecols = lambda column: column in [
        'Year',
        'Annual Emissions [kg(CO2)]',
    ],
    dtype={
        'Year': int,
        'Annual Emissions [kg(CO2)]': float,
    },
    header = 0,
    engine = 'openpyxl',
)
df_efficiency = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'efficiency',
    usecols = lambda column: column in [
        'year',
        'energy intensity [kJ/pax-km]',
    ],
    dtype={
        'year': int,
        'energy intensity [kJ/pax-km]': float,
    },
    header = 0,
    engine = 'openpyxl',
)


# DATA MANIPULATION #############################

df_traffic['traffic_rel'] = df_traffic['RPKs'] / df_traffic['RPKs'].loc[df_traffic['Year'] == 1950].values[0]
df_emissions['emissions_rel'] = df_emissions['Annual Emissions [kg(CO2)]'] / df_emissions['Annual Emissions [kg(CO2)]'].loc[df_emissions['Year'] == 1949].values[0]
df_efficiency['efficiency_rel'] = df_efficiency['energy intensity [kJ/pax-km]'] / df_efficiency['energy intensity [kJ/pax-km]'].loc[df_efficiency['year'] == 1950].values[0]

change_traffic_percent = int(df_traffic['traffic_rel'].loc[df_traffic['Year'] == 2019].values[0] * 100)
change_emissions_percent = int(df_emissions['emissions_rel'].loc[df_emissions['Year'] == 2019].values[0] * 100)
change_efficiency_percent = int(df_efficiency['efficiency_rel'].loc[df_efficiency['year'] == 2019].values[0] * 100)

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 1,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
)

# SECONDARY AXES ##############

# AXIS LIMITS ################

ax.set_xlim(1950, 2024)
#ax.set_ylim(0, 20)

ax.set_yscale('log')

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)

import matplotlib.ticker as ticker

ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:g}'.format(y)))

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Change Relative to 1950 [1]")

# PLOTTING ###################

ax.plot(
    df_traffic['Year'],
    df_traffic['traffic_rel'],
    color = 'black',
    linestyle = '-',
    linewidth = 1.5,
    label = 'Traffic (RPK)'
)
ax.plot(
    df_emissions['Year'],
    df_emissions['emissions_rel'],
    color = 'red',
    linestyle = '-',
    linewidth = 1.5,
    label = 'Emissions (CO$_2$)'
)
ax.plot(
    df_efficiency['year'],
    df_efficiency['efficiency_rel'],
    color = 'blue',
    linestyle = '-',
    linewidth = 1.5,
    label = 'Energy Intensity (kJ/pax-km)'
)
ax.axhline(
    y=1,
    color='orange',
    linestyle='-',
    linewidth=1.5,
    label='Carbon Intensity'
)

ax.axvline(x=2019, color='black', linestyle='-', linewidth=1.5)


# LEGEND ####################

ax.legend(
    loc = 'upper left',
)

ax.text(
    2017.5, 150,
    f"+{change_traffic_percent}\%",
    fontsize = 11,
    color = 'black',
    ha = 'right',
    va = 'center',
)
ax.text(
    2017.5, 7,
    f"+{change_emissions_percent}\%",
    fontsize = 11,
    color = 'black',
    ha = 'right',
    va = 'center',
)
ax.text(
    2017.5, 0.7,
    f"-{change_efficiency_percent}\%",
    fontsize = 11,
    color = 'black',
    ha = 'right',
    va = 'center',
)

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