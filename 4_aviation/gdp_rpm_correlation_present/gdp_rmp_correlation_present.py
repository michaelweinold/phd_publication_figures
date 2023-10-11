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

df_pop = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Population (2022)',
    usecols = lambda column: column in [
        'country code (iso)',
        'Population (2021)'
    ],
    # dtype={'country code (iso)': str, 2021: 'Int64'}, this does not work for some reason
    header = 0,
    engine = 'openpyxl',
    na_values=['..', '']
)
df_gdp = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'GDP (2022USD)',
    usecols = lambda column: column in [
        'country code (iso)',
        'GDP (2021)'
    ],
    # dtype={'country code (iso)': str, 2021: 'Int64'}, this does not work for some reason
    header = 0,
    engine = 'openpyxl',
    na_values=['..', '']
)
df_gdpcapita = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'GDPperCapita (2022USD)',
    usecols = lambda column: column in [
        'country code (iso)',
        'GDPperCapita (2021)'
    ],
    # dtype={'country code (iso)': str, 2021: 'Int64'}, this does not work for some reason
    header = 0,
    engine = 'openpyxl',
    na_values=['..', '']
)
df_pax = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Passengers (pax-km)',
    usecols = lambda column: column in [
        'country code (m49)',
        'PAX (2021)'
    ],
    # dtype={'country code (m49)': str, 2021: int},
    header = 0,
    engine = 'openpyxl',
    na_values=['..', '']
)

# DATA MANIPULATION #############################

def add_country_classifications(
    df: pd.DataFrame,
    country_code_column: str,
) -> pd.DataFrame:
    """
    Add country classifications and corresponding regions to dataframe.

    See Also
    --------
    https://github.com/IndEcol/country_converter?tab=readme-ov-file#classification-schemes
    """
    df['countrycode_iso3'] = coco.convert(
        names = df[country_code_column].tolist(),
        to = 'ISO3',
        not_found = None,
    )
    df.drop(columns = country_code_column, inplace = True)
    return df


df_pop = add_country_classifications(
    df = df_pop,
    country_code_column = 'country code (iso)'
)

df_gdp = add_country_classifications(
    df = df_gdp,
    country_code_column = 'country code (iso)'
)

df_gdpcapita = add_country_classifications(
    df = df_gdpcapita,
    country_code_column = 'country code (iso)'
)

df_pax = add_country_classifications(
    df = df_pax,
    country_code_column = 'country code (m49)'
)

df_combined_pax = pd.concat(
    [
        df_pax.set_index('countrycode_iso3'),
        df_gdp.set_index('countrycode_iso3')
    ],
    axis=1,
    join='inner'
).reset_index()

df_combined_paxcapita = pd.concat(
    [
        df_pax.set_index('countrycode_iso3'),
        df_gdpcapita.set_index('countrycode_iso3')
    ],
    axis=1,
    join='inner'
).reset_index()

df_combined_paxcapita = pd.concat(
    [
        df_combined_paxcapita.set_index('countrycode_iso3'),
        df_pop.set_index('countrycode_iso3')
    ],
    axis=1,
    join='inner'
).reset_index()

df_combined_pax = df_combined_pax[~df_combined_pax['PAX (2021)'].isna()]
df_combined_pax = df_combined_pax[~df_combined_pax['GDP (2021)'].isna()]

df_combined_paxcapita = df_combined_paxcapita[~df_combined_paxcapita['PAX (2021)'].isna()]
df_combined_paxcapita = df_combined_paxcapita[~df_combined_paxcapita['GDPperCapita (2021)'].isna()]
df_combined_paxcapita = df_combined_paxcapita[~df_combined_paxcapita['Population (2021)'].isna()]

df_combined_paxcapita['region'] = coco.convert(
        names = df_combined_paxcapita['countrycode_iso3'].tolist(),
        to = 'UNregion',
        not_found = None,
)

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

df_combined_paxcapita['region'] = df_combined_paxcapita['region'].replace(my_regions_dict)


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


# AXIS SCALE #################

ax.set_yscale('log')
ax.set_xscale('log')

# AXIS LIMITS ################

# COLORBAR ###################

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='both', bottom=False)
ax.tick_params(axis='y', which='both', bottom=False)

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='-', linewidth = 0.5)

# AXIS LABELS ################

ax.set_xlabel("GDP/Capita [2022 USD]")
ax.set_ylabel("Air Transport (Passengers) [Mkm]")

# PLOTTING ###################

colors_for_plotting = {
    'North America':'red',
    'Central and South America': 'orange',
    'Asia': 'blue',
    'Europe':'green',
    'Africa':'black',
    'Oceania': 'magenta',
}

scaling_factor = 0.000001 # determined by experimentation and visual inspection
df_combined_paxcapita['markersize'] = df_combined_paxcapita['Population (2021)'] * scaling_factor

myplot = ax.scatter(
    x = df_combined_paxcapita['GDPperCapita (2021)'],
    y = df_combined_paxcapita['PAX (2021)'],
    s = df_combined_paxcapita['markersize'],
    c = df_combined_paxcapita['region'].map(colors_for_plotting) # replaces regions with corresponding color
)

# LEGEND ####################

colors_for_legend = {
    'N. America':'red',
    'C.+S. America': 'orange',
    'Asia': 'blue',
    'Europe':'green',
    'Africa':'black',
    'Oceania': 'magenta',
}
from matplotlib.patches import Patch # https://matplotlib.org/stable/api/_as_gen/matplotlib.patches.Patch.html
legend1_symbols = [
    Patch(
        color = color,
        label = continent,
    )
    for continent, color in colors_for_legend.items()
]

legend1 = plt.legend(
    handles = legend1_symbols,
    loc = 'lower right',
    title="Region",
)
ax.add_artist(legend1) # https://matplotlib.org/stable/users/explain/axes/legend_guide.html#multiple-legends-on-the-same-axes

kw = dict(
    prop="sizes",
    num=[10, 100, 500, 1000],
    #func=lambda s: s/scaling_factor,
    alpha=0.5
)
plt.legend(
    *myplot.legend_elements(**kw), # https://matplotlib.org/stable/api/collections_api.html#matplotlib.collections.PathCollection.legend_elements
    loc="upper left",
    title="Population [Mio.]",
)

# TITLE #####################


# ANNOTATION ################


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
