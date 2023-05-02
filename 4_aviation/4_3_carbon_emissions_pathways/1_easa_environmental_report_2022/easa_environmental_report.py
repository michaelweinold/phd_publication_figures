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
    'font.size': 8
})

# DIRECTORIES ###################################

path_dir_data: PurePath = Path.cwd().joinpath('data/bars')

# DATA IMPORT ###################################

dict_files: dict = dict()
list_files: list = list()
for file in path_dir_data.glob('*.csv'):
    dict_files[file.stem] = pd.read_csv(filepath_or_buffer = file)
    list_files.append(file.stem)

# DATA MANIPULATION #############################

for file in list_files:
    df: pd.DataFrame = dict_files[file]
    df['data_absolute'] = df['data_upper'] + df['data_lower']
    dict_files[file] = df

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(30*cm, 15*cm), # A4=(210x297)mm
    )

# DATA #######################

x = dict_files['sustainable_aviation_fuels']['year']
y = dict_files['sustainable_aviation_fuels']['data_absolute']

# AXIS LIMITS ################

#plt.xlim(
#    datetime.strptime('2020', '%Y'),
#    datetime.strptime('2050', '%Y')
#)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

#ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
#ax.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

plt.xlabel("Year")
ax.set_ylabel("Fuel Price")

# PLOTTING ###################

ax.bar(
    x = x,
    height = dict_files['sustainable_aviation_fuels']['data_lower'],
    bottom = dict_files['sustainable_aviation_fuels']['data_upper'],
    width=0.8
)

# LEGEND ####################

# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%
