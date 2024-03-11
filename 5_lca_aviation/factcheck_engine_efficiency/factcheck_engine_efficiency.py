#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
# unit conversion
cm = 1/2.54 # for inches-cm conversion
# time manipulation
from datetime import datetime
# data science
import numpy as np
import pandas as pd

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 11
})

# DATA IMPORT ###################################

df_eff = pd.read_excel(
    io = 'data/databank_with_engines.xlsx', # description here
    sheet_name = 'Sheet1',
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

data = df_eff

# Prepare DF for plotting
data = data.dropna(subset='thermal_eff')
data = data.loc[data['Type']!='Regional']
data = data.groupby(['Engine Identification', 'YOI'], as_index=False).agg({'thermal_eff':'mean', 'prop_eff':'mean', 'Engine Efficiency':'mean'})

# https://doi.org/10.1016/j.scitotenv.2023.163881
supposed_mean_hamelin_et_al_2035 = (2035, 0.986)
supposed_mean_hamelin_et_al_2045 = (2045, 1.097)
range_hamelin_et_al_2035 = (2035, 0.638, 0.813) # year, min, max
range_hamelin_et_al_2045 = (2045, 0.738, 0.875) # year, min, max

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 1,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
)

# SECONDARY AXES ##############

# AXIS LIMITS ################

ax.set_xlim(1950, 2050)
ax.set_ylim(0,1.6)

# TICKS AND LABELS ###########

ax.minorticks_on()

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)

ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Engine Efficiency [1]")
ax.set_xlabel("Engine Year of Introduction")

# PLOTTING ###################

ax.scatter(
    x = df_eff['YOI'],
    y = df_eff['Engine Efficiency'],
    marker='o',
    color='black',
    label='Actual Engines',
)

ax.axhline(y=0.555, color='black', linestyle='-')
ax.fill_between(
    x = [1950, 2050],
    y1 = 0.555,
    y2 = 1,
    color = 'red',
    alpha = 0.2,
)
ax.axhline(y=1, color='black', linestyle='--')
ax.fill_between(
    x = [1950, 2050],
    y1 = 1,
    y2 = 1.6,
    color = 'blue',
    alpha = 0.2,
)

ax.annotate(
    'Physically Impossible (Engine Efficiency $>$ 0.55)',
    xy=(1955, 0.75),
    xytext=(1955, 0.75),
    fontsize=12,
    ha='left',
    va='center',
    color='black',
)
ax.annotate(
    'Definitely also Physically Impossible (Engine Efficiency $>$ 1)',
    xy=(1955, 1.25),
    xytext=(1955, 1.25),
    fontsize=12,
    ha='left',
    va='center',
    color='black',
)

ax.plot(
    [supposed_mean_hamelin_et_al_2035[0], supposed_mean_hamelin_et_al_2045[0]],
    [supposed_mean_hamelin_et_al_2035[1], supposed_mean_hamelin_et_al_2045[1]],
    color = 'black',
    marker = 's',
    linestyle = '',
    label = 'Su-ungkavatin et al. 2023 Supposed Mean'
)

ax.errorbar(
    x = range_hamelin_et_al_2035[0],
    y = (range_hamelin_et_al_2035[2]-range_hamelin_et_al_2035[1])/2 + range_hamelin_et_al_2035[1],
    yerr = (range_hamelin_et_al_2035[2]-range_hamelin_et_al_2035[1])/2,
    fmt = 'none',
    capsize = 4,
    ecolor = 'black',
    elinewidth = 1,
)
ax.errorbar(
    x = range_hamelin_et_al_2045[0],
    y = (range_hamelin_et_al_2045[2]-range_hamelin_et_al_2045[1])/2 + range_hamelin_et_al_2045[1],
    yerr = (range_hamelin_et_al_2045[2]-range_hamelin_et_al_2045[1])/2,
    fmt = 'none',
    capsize = 4,
    ecolor = 'black',
    elinewidth = 1,
    label = 'Su-ungkavatin et al. 2023 Range (Min/Max)'
)

# LEGEND ####################

ax.legend(
    loc = 'upper right',
)

# EXPORT #########################################

from pathlib import Path
figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)