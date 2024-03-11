# %%
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
import scipy as sp

# i/o
from pathlib import PurePath, Path

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 12
})

# DIRECTORIES ###################################

path_dir_data: PurePath = Path.cwd().joinpath('data')

# DATA IMPORT ###################################
'''
Create a dictionary of dataframes from csv files in the data directory:
dict_files: dict = {'file_name_1': pd.DataFrame, 'file_name_2': pd.DataFrame, ...}
list_files: list = ['file_name_1', 'file_name_2', ...]
'''

dict_files: dict = dict()
list_filenames: list = list()
for file in path_dir_data.glob('*.csv'):
    dict_files[file.stem] = pd.read_csv(
        filepath_or_buffer = file,
        skipinitialspace = True
    )
    list_filenames.append(file.stem)

# DATA MANIPULATION #############################

# INTERPOLATION ##############
'''
From two columns (x,y) in the dataframe containing the original data,
return a new dataframe with columns (x_new, y_new) containing interpolated data.
'''

for filename in list_filenames:
    df_raw: pd.DataFrame = dict_files[filename]
    df_interpolated: pd.DataFrame = pd.DataFrame()

    x: pd.Series = df_raw['x']
    y: pd.Series = df_raw['y']

    x_new: np.ndarray = np.linspace(x.min(), 150, 100)
    y_spline: sp.interpolate.BSpline = sp.interpolate.make_interp_spline(x, y, k = 1)
    y_new: np.ndarray = y_spline(x_new)

    df_interpolated['x_new'] = x_new
    df_interpolated['y_new'] = y_new
    
    dict_files['interpolated_' + filename] = df_interpolated

# FIGURE ########################################

# DATAFRAMES #################

variation_cost_quantity: pd.DataFrame = dict_files['interpolated_variation_cost_quantity']
ratio_tool_construction_cost: pd.DataFrame = dict_files['interpolated_ratio_tool_construction_cost']

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 10*cm), # A4=(210x297)mm
    )

# AXIS LIMITS ################

plt.xlim(0, 150)
plt.ylim(0, 100)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)
ax.tick_params(axis='y', which='minor', bottom=False)

# GRIDS ######################

ax.grid(which='both', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='y', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

plt.xlabel("Quantity (Number of Aircraft Produced)")
plt.ylabel('[\%]')

# PLOTTING ###################

ax.plot(
    variation_cost_quantity['x_new'],
    variation_cost_quantity['y_new'],
    label="Variation of Cost with Quantity",
    linestyle = '-',
    color = 'black'
)
ax.plot(
    ratio_tool_construction_cost['x_new'],
    ratio_tool_construction_cost['y_new'],
    label="Ratio of Tool Cost to Construction Cost",
    linestyle = '-.',
    color = 'black'
)

# LEGEND ####################

ax.legend()

# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%
