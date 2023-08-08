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

df_swiss = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Swiss',
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

def interpolate_df(
    df: pd.DataFrame,
    columns: list[str],
    new_x: list[float]
) -> pd.DataFrame:
    df_interpolated = pd.DataFrame()
    df_interpolated['year'] = new_x
    for col in columns:
        mypol = np.polynomial.polynomial.Polynomial.fit(
            x = df['distance mean [km]'],
            y = df[col],
            deg = 5,
        )
        df_interpolated[col] = [mypol(xval) for xval in new_x]
    return df_interpolated

interpolate_df(
    df = df_swiss,,
    columns = ['rail [%]', 'car [%]', 'air [%]', 'other [%]'],
    new_x = np.linspace(
        start = 2015,
        stop = 2050,
        num = 2050-2015
    )
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

ax.set_ylim(0, 100)

# TICKS AND LABELS ###########

ax.set_xticks(
    ticks = labels,
    labels = labels,
    rotation=45,
    ha='right'
)

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Modal Share [\%]")
ax.set_xlabel("Trip Distance [km]")

# PLOTTING ###################

width = 0.4
x = np.arange(len(labels))
ax.set_xticks(x, labels)

# Japan
axes[1].bar(
    x = x,
    height = df_japan['rail [%]'],
    width = width,
    label = 'Rail',
    color = 'darkorange',
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