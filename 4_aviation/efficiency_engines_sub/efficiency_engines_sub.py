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

ax.set_xlim(0.7, 0.95)
ax.set_ylim(0.4,0.65)

# TICKS AND LABELS ###########

ax.minorticks_on()

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)

ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Thermal Efficiency [1]")
ax.set_xlabel("Propulsive Efficiency [1]")

# PLOTTING ###################

# Colormap for years
import matplotlib.colors as mcolors

column_data = pd.to_numeric(data['YOI'])
norm = mcolors.Normalize(vmin=column_data.min(), vmax=column_data.max())
norm_column_data = norm(column_data)
cmap = plt.colormaps.get_cmap('viridis')
colors = cmap(norm_column_data)

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

ax.scatter(
    data['prop_eff'],
    data['thermal_eff'],
    marker='o',
    c=colors
)

# LEGEND ####################

ax.vlines(0.925,0.4,0.6, color='black', label='Theoretical Limit')
ax.hlines(0.55,0.7,0.925, color='black', label='Practical Limit NOx', linestyles='--')
ax.hlines(0.6,0.7,0.925, color='black')

plt.colorbar(sm, ax=plt.gca()).set_label('Aircraft Year of Introduction')

from matplotlib.lines import Line2D

legend_elements_categories = [
    Line2D(
        [0],
        [0],
        color='black',
        lw=2,
        ls='--',
        label='Phys. Limit (resp. to NOx)'
    ),
    Line2D(
        [0],
        [0],
        color='black',
        lw=2,
        ls='-',
        label='Phys. Limit'
    ),
        Line2D(
        xdata = [0],
        ydata = [0],
        color = 'black',
        markerfacecolor='black',
        linestyle = 'None',
        markersize=4,
        marker='o',
        label = 'Engines'
    ),
]

ax.legend(
    handles=legend_elements_categories,
    loc='upper left',
    ncol=2
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