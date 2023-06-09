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

df_gdp = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'GDP (2022USD)',
    usecols = lambda column: column in ['country code (iso)', 2021],
    dtype={'country code (iso)': str, '2021': float},
    header = 0,
    engine = 'openpyxl'
)
df_countrycodes = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'UN Country Codes',
    usecols = ['country code (m49)', 'country code (iso)'],
    dtype={'country code (m49)': str, 'country code (iso)': str},
    header = 0,
    engine = 'openpyxl'
)
df_regions = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'UN Country Code Regions',
    usecols = ['country code (m49)', 'my region'],
    dtype={'country code (m49)': str, 'my region': str},
    header = 0,
    engine = 'openpyxl'
)
df_pax = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Passengers (pax-km)',
    usecols = lambda column: column in ['country code (m49)', 2021],
    dtype={'country code (m49)': str, '2021': int},
    header = 0,
    engine = 'openpyxl'
)
df_freight = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Air Freight (mio. t-km)',
    usecols = lambda column: column in ['country code (iso)', 2021],
    dtype={'country code (iso)': str, '2021': float},
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

def match_countrycodes_and_geography(df_countrycodes: pd.DataFrame, df_regions: pd.DataFrame) -> pd.DataFrame:

    df_return = pd.merge(
        left = df_countrycodes,
        right = df_regions,
        how = 'inner',
        on = ['country code (m49)']
    )
    
    return df_return

def match_freight_and_gdp(
    df_freight: pd.DataFrame,
    df_gdp: pd.DataFrame,
    df_countrycodes: pd.DataFrame,
    year: int) -> pd.DataFrame:
    """
    Matches freight and gdp data by year and country.
    """

    df_freight['2021_freight'] = pd.to_numeric(
        df_freight[year],
        errors='coerce'
    )
    df_gdp['2021_gdp'] = pd.to_numeric(
        df_gdp[year],
        errors='coerce'
    )

    # merge country codes
    df_freight = pd.merge(
        left = df_freight[['country code (iso)', '2021_freight']],
        right = df_countrycodes[['country code (iso)', 'my region']],
        how = 'inner',
        on = 'country code (iso)'
    )

    df_return = pd.merge(
        left = df_freight[['country code (iso)', 'my region', '2021_freight']],
        right = df_gdp[['country code (iso)', '2021_gdp']],
        how = 'inner',
        on = ['country code (iso)']
    )
    return df_return

def match_pax_and_gdp(
    df_pax: pd.DataFrame,
    df_countrycodes: pd.DataFrame,
    df_gdp: pd.DataFrame,
    year: int) -> pd.DataFrame:
    """
    Matches passengers and gdp data by year and country.
    """

    df_pax['2021_passengers'] = pd.to_numeric(
        df_pax[year],
        errors='coerce'
    )
    df_gdp['2021_gdp'] = pd.to_numeric(
        df_gdp[year],
        errors='coerce'
    )

    # merge country codes
    df_pax = pd.merge(
        left = df_pax[['country code (m49)', '2021_passengers']],
        right = df_countrycodes[['country code (m49)', 'country code (iso)', 'my region']],
        how = 'inner',
        on = 'country code (m49)'
    )

    df_return = pd.merge(
        left = df_pax[['country code (iso)', 'my region', '2021_passengers']],
        right = df_gdp[['country code (iso)', '2021_gdp']],
        how = 'inner',
        on = ['country code (iso)']
    )
    return df_return

df_countrycodes: pd.DataFrame = match_countrycodes_and_geography(df_countrycodes, df_regions)

df_plot_pax: pd.DataFrame = match_pax_and_gdp(
    df_pax,
    df_countrycodes,
    df_gdp,
    2021
)
df_plot_freight: pd.DataFrame = match_freight_and_gdp(
    df_freight,
    df_gdp,
    df_countrycodes,
    2021
)

# FIGURE ########################################

# SETUP ######################

fig, ax1 = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm
)
ax2 = ax1.twinx()

# DATA #######################

# AXIS SCALE #################

ax1.set_yscale('log')
ax2.set_yscale('log')
ax1.set_xscale('log')

# AXIS LIMITS ################

# COLORBAR ###################

# TICKS AND LABELS ###########

ax1.minorticks_on()
ax1.tick_params(axis='x', which='both', bottom=False)
ax1.tick_params(axis='y', which='both', bottom=False)

# GRIDS ######################

ax1.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax1.grid(which='both', axis='x', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

ax1.set_xlabel("GDP [2022 USD]")
ax1.set_ylabel("Air Transport (Passengers) [km]")
ax2.set_ylabel("Air Transport (Freight) [Mtkm]")

# PLOTTING ###################

ax1.scatter(
    df_plot_pax['2021_gdp'],
    df_plot_pax['2021_passengers'],
    color = 'black',
    marker = 's',
    label = 'Passengers'
)
ax2.scatter(
    df_plot_freight['2021_gdp'],
    df_plot_freight['2021_freight'],
    color = 'blue',
    marker = 'o',
    label = 'Freight'
)

# LEGEND ####################

ax1.legend(
    loc = 'lower left',
    fontsize = 'small',
    markerscale = 1.0,
    frameon = True,
    fancybox = False,
)
ax2.legend(
    loc = 'lower right',
    fontsize = 'small',
    markerscale = 1.0,
    frameon = True,
    fancybox = False,
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

# %%
