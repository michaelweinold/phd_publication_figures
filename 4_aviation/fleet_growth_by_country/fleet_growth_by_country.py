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
    'font.size': 11
})

# DATA IMPORT ###################################

df_main = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'data',
    usecols = lambda column: column in [
        'year',
        'category',
        'country_iso',
        'country_name',
        'country_region',
        'sum(countAc)',
    ],
    dtype={
        'year': int,
        'category': str,
        'country_iso': str,
        'country_name': str,
        'country_region': str,
        'sum(countAc)': int,
    },
    header = 0,
    engine = 'openpyxl',
    keep_default_na=False, na_values=['_'] # otherwise "NA" (Namibia) is read as "NaN", https://stackoverflow.com/a/33952294
)

# DATA MANIPULATION #############################

# compare https://en.wikipedia.org/wiki/United_Nations_geoscheme
# compare https://www.iso.org/obp/ui/#iso:pub:PUB500001:en
historical_country_dict = {
    'AN': 'Western Europe', # https://en.wikipedia.org/wiki/Netherlands_Antilles
    'DD': 'Western Europe', # haha, communism failed!
    'SU': 'Eastern Europe', # haha, communism failed!
    'YU': 'Eastern Europe', # haha, communism failed!
    'KA': 'Middle Africa', # https://en.wikipedia.org/wiki/State_of_Katanga
    'GK': 'Western Europe', # https://en.wikipedia.org/wiki/Guernsey
    'TP': 'Southeastern Asia', # https://en.wikipedia.org/wiki/East_Timor
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
    df[column_name_country_classification] = df[column_name_country_classification].replace(historical_country_dict)
    return df

def fill_empty_years(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Fill empty years with 0.
    """
    all_years = pd.DataFrame({'year': range(1950, 2030)})
    df = pd.merge(
        all_years,
        df,
        on='year',
        how='left'
    ).fillna(0)
    return df



df_grouped_unregion = add_country_classifications(
    df = df_main,
    country_code_column = 'country_iso',
    coco_classification = 'UNregion',
)

df_grouped_region = df_grouped_unregion.copy()
df_grouped_region['region'] = df_grouped_unregion['country_classification_UNregion'].replace(my_regions_dict)
df_grouped_region = df_grouped_region[['year', 'region', 'sum(countAc)']].groupby(['year', 'region']).sum().reset_index()


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

ax.set_xlim(1949, 2024)

# TICKS AND LABELS ###########

ax.set_xlabel('Year')
ax.set_ylabel('Number of Aircraft in Service')

import matplotlib.ticker as ticker
def thousand_formatter(value, tick_number):
    """
    Formats the tick label with thousand separators: 1000 = 1'000.
    """
    return f"{int(value):,}".replace(",", "'")

ax.yaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################


# PLOTTING ###################


df_north_america = df_grouped_region[df_grouped_region['region'] == 'North America']
df_north_america = fill_empty_years(df_north_america)

df_south_america = df_grouped_region[df_grouped_region['region'] == 'Central and South America']
df_south_america = fill_empty_years(df_south_america)

df_europe = df_grouped_region[df_grouped_region['region'] == 'Europe']
df_europe = fill_empty_years(df_europe)

df_asia = df_grouped_region[df_grouped_region['region'] == 'Asia']
df_asia = fill_empty_years(df_asia)

df_oceania = df_grouped_region[df_grouped_region['region'] == 'Oceania']
df_oceania = fill_empty_years(df_oceania)

df_africa = df_grouped_region[df_grouped_region['region'] == 'Africa']
df_africa = fill_empty_years(df_africa)

ax.bar(
    x = df_north_america['year'],
    height=df_north_america['sum(countAc)'],
    label = 'North America',
    color = 'blue',
)
ax.bar(
    x = df_asia['year'],
    height=df_asia['sum(countAc)'],
    bottom=df_north_america['sum(countAc)'],
    label = 'Asia',
    color = 'red',
)
ax.bar(
    x = df_africa['year'],
    height=df_africa['sum(countAc)'],
    bottom=df_north_america['sum(countAc)'] + df_asia['sum(countAc)'],
    label = 'Africa',
    color = 'brown',
)
ax.bar(
    x = df_south_america['year'],
    height=df_south_america['sum(countAc)'],
    bottom=df_north_america['sum(countAc)'] + df_asia['sum(countAc)'] + df_africa['sum(countAc)'],
    label = 'Central and South America',
    color = 'orange',
)
ax.bar(
    x = df_europe['year'],
    height=df_europe['sum(countAc)'],
    bottom=df_north_america['sum(countAc)'] + df_south_america['sum(countAc)'] + df_asia['sum(countAc)'] + df_africa['sum(countAc)'],
    label = 'Europe',
    color = 'green',
)

ax.bar(
    x = df_oceania['year'],
    height=df_oceania['sum(countAc)'],
    bottom=df_north_america['sum(countAc)'] + df_south_america['sum(countAc)'] + df_asia['sum(countAc)'] + df_africa['sum(countAc)'] + df_europe['sum(countAc)'],
    label = 'Oceania',
    color = 'purple',

)




# LEGEND ####################

ax.legend(
    loc = 'upper left',
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
# %%
