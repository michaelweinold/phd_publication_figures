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
    'font.size': 11
})

# DATA IMPORT ###################################

# see also this StackOverflow questions:
# https://stackoverflow.com/q/22787209
# https://stackoverflow.com/q/69242928
# it will be best to have separate plots for each country

df_japan = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Japan',
    usecols = lambda column: column in [
        'distance bin [km]',
        'distance mean [km]',
        'rail [%]',
        'car [%]',
        'air [%]',
        'other [%]',
        'year'
    ],
    dtype={
        'distance bin [km]': str,
        'distance mean [km]': float,
        'rail [%]': float,
        'car [%]': float,
        'air [%]': float,
        'other [%]': float,
        'year': str
    },
    header = 0,
    engine = 'openpyxl'
)
df_eu = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'EU',
    usecols = lambda column: column in [
        'distance [km]',
        'rail [%]',
        'car [%]',
        'air [%]',
        'other [%]',
        'year'
    ],
    dtype={
        'distance [km]': str,
        'rail [%]': float,
        'car [%]': float,
        'air [%]': float,
        'other [%]': float,
        'year': str
    },
    header = 0,
    engine = 'openpyxl'
)
df_usa = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'USA',
    usecols = lambda column: column in [
        'distance (air) [miles]',
        'air [%]',
        'distance (car) [miles]',
        'car [%]',
    ],
    dtype={
        'distance (air) [miles]': float,
        'air [%]': float,
        'distance (car) [miles]': float,
        'car [%]': float,
    },
    header = 0,
    engine = 'openpyxl'
)
		
# DATA MANIPULATION #############################

unified_distance = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

df_japan = df_japan[df_japan['year'] == '2019?']

def interpolate_japan(
    df: pd.DataFrame,
    columns: list[str],
    new_x: list[float]
) -> pd.DataFrame:
    df_interpolated = pd.DataFrame()
    df_interpolated['distance [km]'] = new_x
    for col in columns:
        mypol = np.polynomial.polynomial.Polynomial.fit(
            x = df['distance mean [km]'],
            y = df[col],
            deg = 5,
        )
        df_interpolated[col] = [mypol(xval) for xval in new_x]
    return df_interpolated

def interpolate_usa(
    df: pd.DataFrame,
    column_pairs: dict,
    new_x: list[float]
) -> pd.DataFrame:
    df_interpolated = pd.DataFrame()
    df_interpolated['distance [km]'] = new_x
    for old_x in column_pairs.keys():
        mypol = np.polynomial.polynomial.Polynomial.fit(
            x = df[old_x].dropna(),
            y = df[column_pairs[old_x]].dropna(),
            deg = 5,
        )
        df_interpolated[column_pairs[old_x]] = [mypol(xval) for xval in new_x]
    return df_interpolated

df_japan = interpolate_japan(
    df = df_japan,
    columns = ['rail [%]', 'car [%]', 'air [%]', 'other [%]'],
    new_x = unified_distance
)

df_usa = interpolate_usa(
    df = df_usa,
    column_pairs = {
        'distance (air) [miles]': 'air [%]',
        'distance (car) [miles]': 'car [%]'
    },
    new_x = unified_distance
)

df_usa['other [%]'] = 100 - (df_usa['air [%]'] + df_usa['car [%]'])

# FIGURE ########################################

# SETUP ######################

fig, axes = plt.subplots(
    num = 'main',
    sharey = True,
    sharex = True,
    nrows = 1,
    ncols = 3,
    gridspec_kw = {'wspace': 0.1},
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
)

# AXIS SCALING ###############

# AXIS LIMITS ################

for ax in axes.flat:
    ax.set_ylim(0, 100)

# TICKS AND LABELS ###########

labels = unified_distance
for ax in axes.flat:
    ax.set_xticks(
        ticks = labels,
        labels = labels,
        rotation=45,
        ha='right'
    )

# GRIDS ######################

for ax in axes.flat:
    ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
    ax.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

axes[0].set_ylabel("Modal Share [\%]")
for ax in axes.flat:
    ax.set_xlabel("Trip Distance [km]")

# TITLE ######################

axes[0].set_title("EU (2015)", pad=7.5)
axes[1].set_title("Japan (2019)", pad=7.5)
axes[2].set_title("USA (2001)", pad=7.5)

# PLOTTING ###################

width = 0.4
x = np.arange(len(labels))
axes[0].set_xticks(x, labels)

# EU
axes[0].bar(
    x = x,
    height = df_eu['rail [%]'],
    width = width,
    label = 'Rail',
    color = 'darkorange',
)
axes[0].bar(
    x = x,
    bottom = df_eu['rail [%]'],
    height = df_eu['air [%]'],
    width = width,
    label = 'Air',
    color = 'royalblue',
)
axes[0].bar(
    x = x,
    bottom = df_eu['rail [%]'] + df_eu['air [%]'],
    height = df_eu['car [%]'],
    width = width,
    label = 'Car',
    color = 'brown',
)
axes[0].bar(
    x = x,
    bottom = df_eu['rail [%]'] + df_eu['air [%]'] + df_eu['car [%]'],
    height = df_eu['other [%]'],
    width = width,
    label = 'Other',
    color = 'grey',
)

# Japan
axes[1].bar(
    x = x,
    height = df_japan['rail [%]'],
    width = width,
    label = 'Rail',
    color = 'darkorange',
)
axes[1].bar(
    x = x,
    bottom = df_japan['rail [%]'],
    height = df_japan['air [%]'],
    width = width,
    label = 'Air',
    color = 'royalblue',
)
axes[1].bar(
    x = x,
    bottom = df_japan['rail [%]'] + df_japan['air [%]'],
    height = df_japan['car [%]'],
    width = width,
    label = 'Car',
    color = 'brown',
)
axes[1].bar(
    x = x,
    bottom = df_japan['rail [%]'] + df_japan['air [%]'] + df_japan['car [%]'],
    height = df_japan['other [%]'],
    width = width,
    label = 'Other',
    color = 'grey',
)

# USA
axes[2].bar(
    x = x,
    height = df_usa['air [%]'],
    width = width,
    label = 'Air',
    color = 'royalblue',
)
axes[2].bar(
    x = x,
    bottom = df_usa['air [%]'],
    height = df_usa['car [%]'],
    width = width,
    label = 'Car',
    color = 'brown',
)
axes[2].bar(
    x = x,
    bottom = df_usa['air [%]'] + df_usa['car [%]'],
    height = df_usa['other [%]'],
    width = width,
    label = 'Other',
    color = 'grey',
)

# LEGEND ####################

axes[0].legend(
    loc = 'lower left',
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
