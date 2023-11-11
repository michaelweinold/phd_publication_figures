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

df_ets_price = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Emissions Prices',
    usecols = lambda column: column in [
        'date',
        '[EUR/t]',
    ],
    dtype={
        'date': datetime,
        '[EUR/t]': float,
    },
    header = 0,
    engine = 'openpyxl'
)

df_emissions_proj_input = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'EU Emissions Projection',
    usecols = lambda column: column in [
        'year',
        'emissions [Mt(CO2)]'
    ],
    dtype={
        'year': int,
        'emissions [Mt(CO2)]': float
    },
    header = 0,
    engine = 'openpyxl'
)

df_emissions_hist = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'EU Emissions History',
    usecols = lambda column: column in [
        'year',
        'free allowances [t(CO2)]',
        'state auction [t(CO2)]',
        'EUA purchases [t(CO2)]',
        'special reserve [t(CO2)]'
    ],
    dtype={
        'year': int,
        'free allowances [t(CO2)]': float,
        'state auction [t(CO2)]': float,
        'EUA purchases [t(CO2)]': float,
        'special reserve [t(CO2)]': float
    },
    header = 0,
    engine = 'openpyxl'
)


# DATA MANIPULATION #############################

# this is the new list of years
list_of_years: list[int] = [i for i in range(2005, 2050+1)]

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


df_emissions_proj: pd.DataFrame = interpolate_1d_dataframe(
    df = df_emissions_proj_input,
    name_of_column_to_interpolate_x ='year',
    name_of_column_to_interpolate_y ='emissions [Mt(CO2)]',
    new_x_values = list_of_years,
)
loc_2019 = df_emissions_proj[df_emissions_proj['year'] == 2019].index
df_emissions_proj['y'] = df_emissions_proj['y'] / df_emissions_proj['y'].loc[loc_2019]

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 2,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm,
        gridspec_kw = dict(
            height_ratios=[3,2],
        ),
        sharex=True
    )

# DATA #######################

# AXIS LIMITS ################

ax[0].set_xlim(
    datetime.strptime('2004', '%Y'),
    datetime.strptime('2050', '%Y')
)

ax[0].set_ylim(1,300)

ax[1].set_ylim(0, 100)

# TICKS AND LABELS ###########

for axis in ax:
    axis.minorticks_on()
    axis.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

for axis in ax:
    axis.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
    axis.grid(which='major', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax[0].set_ylabel("Aviation Emissions \n (cov. by ETS) [Mt(CO$_2$)]")
ax[1].set_xlabel("Year")
ax[1].set_ylabel("EUA Spot Price \n [EUR/t(CO$_2$)]")

# PLOTTING ###################

ax[0].plot(
    pd.to_datetime(df_emissions_proj['year'], format='%Y'),
    df_emissions_proj['y'],
    color = 'black',
    linewidth = 1,
)

ax[0].bar(
    x = pd.to_datetime(df_emissions_hist['year'], format='%Y'),
    height = df_emissions_hist['free allowances [t(CO2)]']/(1E6),
    width=250,
    color = 'blue',
    label = 'Free Allowances',
)
ax[0].bar(
    x = pd.to_datetime(df_emissions_hist['year'], format='%Y'),
    height = df_emissions_hist['state auction [t(CO2)]']/(1E6),
    bottom = df_emissions_hist['free allowances [t(CO2)]']/(1E6),
    width=250,
    color = 'orange',
    label = 'State Auctions',
)
ax[0].bar(
    x = pd.to_datetime(df_emissions_hist['year'], format='%Y'),
    height = df_emissions_hist['EUA purchases [t(CO2)]']/(1E6),
    bottom = df_emissions_hist['free allowances [t(CO2)]']/(1E6) + df_emissions_hist['state auction [t(CO2)]']/(1E6),
    width=250,
    color = 'green',
    label = 'EUA Market Purchases',
)
ax[0].bar(
    x = pd.to_datetime(df_emissions_hist['year'], format='%Y'),
    height = df_emissions_hist['special reserve [t(CO2)]']/(1E6),
    bottom = df_emissions_hist['free allowances [t(CO2)]']/(1E6) + df_emissions_hist['state auction [t(CO2)]']/(1E6) + df_emissions_hist['EUA purchases [t(CO2)]']/(1E6),
    width=250,
    color = 'brown',
    label = 'Special Reserve Allocation',
)

ax[1].plot(
    df_ets_price['date'],
    df_ets_price['[EUR/t]'],
    color = 'black',
    linewidth = 1,
)

ax[1].axvspan(
    xmin = datetime.strptime('2005', '%Y'),
    xmax = datetime.strptime('2008', '%Y'),
    facecolor='blue',
    alpha=0.2,
    label = 'Phase 1'
)
ax[1].annotate(
    'Phase 1',
    xy=(datetime.strptime('2005', '%Y'), 75),
)
ax[1].axvspan(
    xmin = datetime.strptime('2008', '%Y'),
    xmax = datetime.strptime('2013', '%Y'),
    facecolor='purple',
    alpha=0.2,
    label = 'Phase 2'
)
ax[1].annotate(
    'Phase 2',
    xy=(datetime.strptime('2009', '%Y'), 75),
)
ax[1].axvspan(
    xmin = datetime.strptime('2013', '%Y'),
    xmax = datetime.strptime('2021', '%Y'),
    facecolor='red',
    alpha=0.2,
    label = 'Phase 3'
)
ax[1].annotate(
    'Phase 3',
    xy=(datetime.strptime('2015', '%Y'), 75),
)
ax[1].axvspan(
    xmin = datetime.strptime('2021', '%Y'),
    xmax = datetime.strptime('2030', '%Y'),
    facecolor='orange',
    alpha=0.2,
    label = 'Phase 4'
)
ax[1].annotate(
    'Phase 4',
    xy=(datetime.strptime('2025', '%Y'), 75),
)


# LEGEND ####################

ax[0].legend(
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
