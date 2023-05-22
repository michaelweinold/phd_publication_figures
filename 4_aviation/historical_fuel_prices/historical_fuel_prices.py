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

df_jetfuel = pd.read_csv(
    filepath_or_buffer = 'data/data_jetfuel.csv',
    sep = ',',
    header = 'infer',
    index_col = False,
    parse_dates = [0],
    infer_datetime_format = True,
)

df_gasoline = pd.read_csv(
    filepath_or_buffer = 'data/data_gasoline.csv',
    sep = ',',
    header = 'infer',
    index_col = False,
    parse_dates = [0],
    infer_datetime_format = True,
)

# DATA MANIPULATION #############################
'''
Normalize data to 1950 = 1
'''
df_jetfuel['WPU0572_normalized_1950'] = df_jetfuel['WPU0572'] / df_jetfuel['WPU0572'].loc[df_jetfuel['DATE'] == '1950-01-01'].values[0]

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

x_jetfuel = df_jetfuel['DATE']
y_jetfuel = df_jetfuel['WPU0572_normalized_1950']

# AXIS LIMITS ################

plt.xlim(
    datetime.strptime('1950', '%Y'),
    datetime.strptime('2023', '%Y')
)
ax.set_ylim(1,80)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_xlabel("Year")
ax.set_ylabel("Producer Price Index \n (Aviation Fuel)")

# PLOTTING ###################


ax.plot(
    x_jetfuel,
    y_jetfuel,
    color = 'black',
    linewidth = 1,
    label = 'Jet Fuel (Kerosene)'
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
