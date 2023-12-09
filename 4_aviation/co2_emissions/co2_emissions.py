#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

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

df_co2_all = pd.read_excel(
    io = './data/data.xlsx',
    sheet_name = 'All Sectors',
    usecols = None,
    header = 0,
    engine = 'openpyxl',
    na_values = '',
)
df_co2_agg = pd.read_excel(
    io = './data/data.xlsx',
    sheet_name = 'All Sectors (Aggregated)',
    usecols = lambda column: column in [
        'Entity',
        'Year',
        'Annual Emissions [kg(CO2)]'
    ],
    dtype={
        'Entity': str,
        'Year': int,
        'Annual Emissions [kg(CO2)]': float
    },
    header = 0,
    engine = 'openpyxl',
    na_values = '',
)
df_co2_av = pd.read_excel(
    io = './data/data.xlsx',
    sheet_name = 'Aviation',
    usecols = lambda column: column in [
        'Year',
        'Annual Emissions [kg(CO2)]'
    ],
    dtype={
        'Year': float,
        'Annual Emissions [kg(CO2)]': float
    },
    header = 0,
    engine = 'openpyxl',
    na_values = '',
)

# DATA MANIPULATION #############################

# data is in t(CO2)/year
df_co2_agg = df_co2_agg[df_co2_agg['Entity'] == 'World']
df_co2_agg = df_co2_agg[df_co2_agg['Year'] <= 1970]
df_co2_agg['Annual Emissions [kg(CO2)]'] = df_co2_agg['Annual Emissions [kg(CO2)]']/1E6

# data is in Mt(CO2)/year
df_co2_all = df_co2_all.drop(
    columns=[
        'Substance',
        'EDGAR Country Code',
        'Country',
        'Source',
    ]
)
df_co2_all = df_co2_all.groupby('Sector').sum()
df_co2_all = df_co2_all.transpose()
df_co2_all.index.names = ['Year']
df_co2_all.index = df_co2_all.index.astype(int)
df_co2_all['Total'] = df_co2_all.sum(axis=1)

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

ax.set_xlim(1950, 2023)
#ax.set_ylim(10,30)

# TICKS AND LABELS ###########

from matplotlib.ticker import MultipleLocator
ax.xaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_minor_locator(MultipleLocator(1))

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)

ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)


# AXIS LABELS ################

ax.set_ylabel("Carbon Emissions [Mt(CO$_2$)]")

# PLOTTING ###################

colors = [
    'tab:gray',
    'tab:green',
    'tab:pink',
    'tab:cyan',
    'tab:orange',
    'tab:red',
    'tab:purple',
    'tab:brown',
]

ax.stackplot(
    df_co2_all.index,
    df_co2_all['Transport'],
    df_co2_all['Agriculture'],
    df_co2_all['Buildings'],
    df_co2_all['Fuel Exploitation'],
    df_co2_all['Industrial Combustion'],
    df_co2_all['Power Industry'],
    df_co2_all['Processes'],
    df_co2_all['Waste'],
    colors = colors,
)
ax.plot(
    df_co2_agg['Year'],
    df_co2_agg['Annual Emissions [kg(CO2)]'],
    color = 'black',
    linewidth = 1,
    linestyle = '--',
    label = 'Historical Emissions (Total)'
)
ax.stackplot(
    df_co2_av['Year'],
    df_co2_av['Annual Emissions [kg(CO2)]'],
    colors = ['yellow'],
    labels = ['Aviation'],
)

# LEGEND ####################

from matplotlib.patches import Patch
from matplotlib.lines import Line2D

legend_elements_categories = [
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'black',
        markerfacecolor='black',
        linestyle = '--',
        label = 'Historical Emissions (Total)'
    ),
    Patch(
        facecolor = 'tab:brown',
        label = 'Waste'
    ),
    Patch(
        facecolor = 'tab:purple',
        label = 'Processes'
    ),
    Patch(
        facecolor = 'tab:red',
        label = 'Power Industry (Electricity)'
    ),
    Patch(
        facecolor = 'tab:orange',
        label = 'Industrial Combustion'
    ),
    Patch(
        facecolor = 'tab:cyan',
        label = 'Fuel Exploitation'
    ),
    Patch(
        facecolor = 'tab:pink',
        label = 'Buildings'
    ),
    Patch(
        facecolor = 'tab:green',
        label = 'Agriculture'
    ),
    Patch(
        facecolor = 'tab:gray',
        label = 'Non-Aviation Transport'
    ),
    Patch(
        facecolor = 'yellow',
        label = 'Aviation'
    ),
]

ax.legend(
    handles = legend_elements_categories,
    loc='upper left',
)

# EXPORT #########################################

from pathlib import Path
figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%