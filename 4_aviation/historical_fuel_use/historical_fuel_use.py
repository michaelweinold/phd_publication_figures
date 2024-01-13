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
# country manipulation
import country_converter as coco

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
df_fuel_global_ipcc = pd.read_excel( # no longer needed
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
df_fuel_global = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Fuel Use Global (EIA)',
    header = 0,
    index_col = 0,
    engine = 'openpyxl'
).drop(columns=['Source'])

# DATA MANIPULATION #############################

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

# transpose dataframe
df_fuel_global_t = df_fuel_global.transpose()
df_fuel_global_t = df_fuel_global_t.rename_axis("Year")

# convert million metric tonnes to Gl
# https://aviationbenefits.org/environmental-efficiency/climate-action/sustainable-aviation-fuel/conversions-for-saf/
df_fuel_global_t = df_fuel_global_t.apply(pd.to_numeric, errors='coerce')
df_fuel_global_t = df_fuel_global_t * (1250000/1E9)

# sum total fuel burn after 1980
df_fuel_global_t['Total [Gl]'] = df_fuel_global_t.sum(axis=1)

df_co2_historical = df_co2_historical[df_co2_historical['Year'] <= 1980]

# peg co2 emissions data to fuel burn data
conversion_factor = df_fuel_global_t['Total [Gl]'].iloc[0] / df_co2_historical['Annual Emissions [kg(CO2)]'].iloc[-1]
df_co2_historical['Fuel Burned [Gl]'] = df_co2_historical['Annual Emissions [kg(CO2)]'] * conversion_factor

# classify countries by region

df_fuel_global = df_fuel_global.reset_index()
df_fuel_global = df_reset.melt(id_vars='Country')

unmatched_regions_dict = {
    'Former Serbia and Montenegro': 'Western Europe',
    'Former U.S.S.R.': 'Eastern Europe',
    'Former Yugoslavia': 'Eastern Europe',
    'Germany, East': 'Eastern Europe',
    'Germany, West': 'Western Europe',
    'Hawaiian Trade Zone': 'Oceania',
    'Netherlands Antilles': 'Western Europe',
    'U.S. Pacific Islands': 'Oceania',
    'U.S. Territories': 'North America',
    'Wake Island': 'Oceania',
}

# get list either from Wikipedia https://en.wikipedia.org/wiki/United_Nations_geoscheme
# of from coco.CountryConverter().UNregion['UNregion'].unique().tolist()
my_regions_dict = {
    'Southern Asia': 'Asia',
    'Northern Europe': 'Europe',
    'Southern Europe': 'Europe',
    'Northern Africa': 'Africa',
    'Polynesia': 'Oceania',
    'Middle Africa': 'Africa',
    'Caribbean': 'Central and South America',
    'Antarctica': 'Central and South America',
    'South America': 'Central and South America',
    'Western Asia': 'Asia',
    'Australia and New Zealand': 'Oceania',
    'Western Europe': 'Europe',
    'Eastern Europe': 'Europe',
    'Central America': 'Central and South America',
    'Western Africa': 'Africa',
    'Northern America': 'North America',
    'Southern Africa': 'Africa',
    'Eastern Africa': 'Africa',
    'South-eastern Asia': 'Asia',
    'Eastern Asia': 'Asia',
    'Melanesia': 'Oceania',
    'Micronesia': 'Oceania',
    'Central Asia': 'Asia',
}
my_regions_list = list(set(my_regions_dict.values()))

def add_country_classifications(
    df: pd.DataFrame,
    country_code_column: str,
    coco_classification: str,
) -> pd.DataFrame:
    """
    Group countries according to a country-converter ("coco") supported classification,
    then sum the values of the relevant columns.

    See Also
    --------
    https://github.com/IndEcol/country_converter?tab=readme-ov-file#classification-schemes
    """
    column_name_country_classification: str = 'country_classification_' + coco_classification
    df[column_name_country_classification] = coco.convert(
        names = df[country_code_column].tolist(),
        to = coco_classification,
        not_found = None,
    )
    df[column_name_country_classification] = df[column_name_country_classification].replace(unmatched_regions_dict)
    return df


df_grouped_unregion = add_country_classifications(
    df = df_fuel_global,
    country_code_column = 'Country',
    coco_classification = 'UNregion',
)

df_grouped_region = df_grouped_unregion.copy()
df_grouped_region['region'] = df_grouped_unregion['country_classification_UNregion'].replace(my_regions_dict)
df_grouped_region['value'] = df_grouped_region['value'].apply(pd.to_numeric, errors='coerce')
df_grouped_region['value'] = df_grouped_region['value'] * (1250000/1E9)
df_grouped_region = df_grouped_region[['variable', 'region', 'value']].groupby(['variable', 'region']).sum().reset_index()

# back to wide format
df_fuel_global_regions = df_grouped_region.pivot(index='variable', columns='region', values='value').reset_index()

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
    df_co2_historical['Year'],
    df_co2_historical['Fuel Burned [Gl]'],
    color = 'black',
    linewidth = 1,
    label = 'Lee, Fahey, Skowron et al. (2021)'
)
ax.plot(
    df_fuel_global_t.index,
    df_fuel_global_t['Total [Gl]'],
    color = 'red',
    linewidth = 1,
    label = 'U.S. Energy Inf. Admin. (2023)'
)

ax.stackplot(
    df_fuel_usa_extrapolated['Year'],
    df_fuel_usa_extrapolated['Total [Gl]'],
    df_fuel_ussr_extrapolated['Total [Gl]'],
    colors = ['blue', 'red'],
    linewidth = 1,
    alpha = 0.5,
)

ax.stackplot(
    df_fuel_global_regions['variable'],
    df_fuel_global_regions['North America'],
    df_fuel_global_regions['Asia'],
    df_fuel_global_regions['Africa'],
    df_fuel_global_regions['Central and South America'],
    df_fuel_global_regions['Europe'],
    df_fuel_global_regions['Oceania'],
    colors = ['blue', 'red', 'brown', 'orange', 'green', 'purple'],
    linewidth = 1,
    alpha = 0.5,
    labels = ['North America', 'Asia', 'Africa', 'Central and South America', 'Europe', 'Oceania']
)

ax.axvline(x=1980, color='black', linestyle='--')

# LEGEND ####################

ax.legend(
    loc='upper left',
)
ax.annotate(
    'U.S.S.R. only ($<$ 1980)',  # Text to display in the annotation box
    xy=(1980 - 1, 40),  # Position of the upper end of the vertical line
    ha='right',  # Horizontal alignment of the text
    va='bottom'  # Vertical alignment of the text
)
ax.annotate(
    'U.S.A. only ($<$1980)',  # Text to display in the annotation box
    xy=(1980 - 1, 7),  # Position of the upper end of the vertical line
    ha='right',  # Horizontal alignment of the text
    va='bottom',  # Vertical alignment of the text
    color = 'white'
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
