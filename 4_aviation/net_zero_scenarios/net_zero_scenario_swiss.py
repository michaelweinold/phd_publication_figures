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
import scipy

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

df_swiss = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Swiss',
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

list_of_years: list[int] = [i for i in range(2025, 2050+1)]

def interpolate_df(
    df: pd.DataFrame,
    old_x: str,
    old_y: str,
    new_x: list[int],
    deg: int,
) -> pd.DataFrame:
    df_interpolated = pd.DataFrame()
    df_interpolated['year'] = new_x
    mypol = np.polynomial.polynomial.Polynomial.fit(
        x = df[old_x].dropna(),
        y = df[old_y].dropna(),
        deg = deg,
    )
    df_interpolated[old_y + '_interp'] = [mypol(xval) for xval in new_x]
    return df_interpolated


def interpolate_1d_df(
    df: pd.DataFrame,
    old_x: str,
    old_y: str,
    new_x: list[int],
    deg: int,
) -> pd.DataFrame:
    df_interpolated = pd.DataFrame()
    df_interpolated['year'] = new_x
    mypol = scipy.interpolate.interp1d(
        x = df[old_x].dropna(),
        y = df[old_y].dropna(),
    )
    df_interpolated[old_y + '_interp'] = [mypol(xval) for xval in new_x]
    return df_interpolated


test = interpolate_df(
    df = df_swiss,
    old_x = 'offset_x',
    old_y = 'offset_y',
    new_x = list_of_years,
    deg = 9,
)

test1 = interpolate_1d_df(
    df = df_swiss,
    old_x = 'offset_x',
    old_y = 'offset_y',
    new_x = list_of_years,
    deg = 9,
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


# TICKS AND LABELS ###########


# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################


# PLOTTING ###################


ax.plot(test['year'], test['offset_y_interp'], label = 'Economy', color = 'tab:blue')
ax.plot(test1['year'], test1['offset_y_interp'], label = 'Economy', color = 'tab:blue')


# LEGEND ####################

ax.legend(
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
