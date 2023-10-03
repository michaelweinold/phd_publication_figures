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

# DIRECTORIES ###################################

path_dir_data_bars: PurePath = Path.cwd().joinpath('data/bars')
path_dir_data_lines: PurePath = Path.cwd().joinpath('data/lines')

# DATA IMPORT ###################################
'''
Create a dictionary of dataframes from csv files in the data directory:
dict_files: dict = {'file_name_1': pd.DataFrame, 'file_name_2': pd.DataFrame, ...}
list_files: list = ['file_name_1', 'file_name_2', ...]
'''

dict_files_bars: dict = dict()
list_filenames_bars: list = list()
for file in path_dir_data_bars.glob('*.csv'):
    dict_files_bars[file.stem] = pd.read_csv(
        filepath_or_buffer = file,
        skipinitialspace = True
    )
    list_filenames_bars.append(file.stem)

dict_files_lines: dict = dict()
list_filenames_lines: list = list()
for file in path_dir_data_lines.glob('*.csv'):
    dict_files_lines[file.stem] = pd.read_csv(
        filepath_or_buffer = file,
        skipinitialspace = True
    )
    list_filenames_lines.append(file.stem)

# DATA MANIPULATION #############################
'''

'''

for file in list_files:
    df: pd.DataFrame = dict_files_bars[file]
    df['data_absolute'] = df['lower_bar_position'] + df['bar_value']
    dict_files_bars[file] = df

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

x = dict_files_bars['sustainable_aviation_fuels']['year']
y = dict_files_bars['sustainable_aviation_fuels']['data_absolute']

# AXIS LIMITS ################

plt.xlim(2000, 2051)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='both', axis='y', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_xlabel("Year")
ax.set_ylabel("Aviation Emissions \n (EU27+UK+EFTA) [Mt(CO$_2$)]")

# PLOTTING ###################

ax.bar(
    x = x,
    height = dict_files_bars['kerosene']['bar_value'],
    bottom = dict_files_bars['kerosene']['lower_bar_position'],
    width=0.8,
    color = 'darkblue',
    label = 'Innovation: Kerosene',
)
ax.bar(
    x = x,
    height = dict_files_bars['hydrogen']['bar_value'],
    bottom = dict_files_bars['hydrogen']['lower_bar_position'],
    width=0.8,
    color = 'royalblue',
    label = 'Innovation: Hydrogen',
)
ax.bar(
    x = x,
    height = dict_files_bars['hydrogen_on_demand']['bar_value'],
    bottom = dict_files_bars['hydrogen_on_demand']['lower_bar_position'],
    width=0.8,
    color = 'cadetblue',
    label = 'Demand Effect: Hydrogen',
)
ax.bar(
    x = x,
    height = dict_files_bars['operations']['bar_value'],
    bottom = dict_files_bars['operations']['lower_bar_position'],
    width=0.8,
    color = 'gray',
    label = 'Operations',
)
ax.bar(
    x = x,
    height = dict_files_bars['sustainable_aviation_fuels']['bar_value'],
    bottom = dict_files_bars['sustainable_aviation_fuels']['lower_bar_position'],
    width=0.8,
    color = 'lightsteelblue',
    label = 'SAF',
)
ax.bar(
    x = x,
    height = dict_files_bars['sustainable_aviation_fuels_on_demand']['bar_value'],
    bottom = dict_files_bars['sustainable_aviation_fuels_on_demand']['lower_bar_position'],
    width=0.8,
    color = 'mediumseagreen',
    label = 'Demand Effect: SAF',
)
ax.bar(
    x = x,
    height = dict_files_bars['economic_measures']['bar_value'],
    bottom = dict_files_bars['economic_measures']['lower_bar_position'],
    width=0.8,
    color = 'green',
    label = 'Economic Measures',
)
ax.bar(
    x = x,
    height = dict_files_bars['economic_measures_on_demand']['bar_value'],
    bottom = dict_files_bars['economic_measures_on_demand']['lower_bar_position'],
    width=0.8,
    color = 'darkolivegreen',
    label = 'Demand Effect: Economic Measures',
)

ax.plot(
    dict_files_lines['reference_scenario']['year'],
    dict_files_lines['reference_scenario']['data'],
    color = 'black',
    label = 'Reference Scenario (No Policy)',
    linestyle = '-.',
)
ax.plot(
    dict_files_lines['co2_emissions']['year'],
    dict_files_lines['co2_emissions']['data'],
    color = 'black',
    label = 'Net CO$_2$ Emissions',
)

# LEGEND ####################

ax.legend(
    loc = 'upper left',
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
