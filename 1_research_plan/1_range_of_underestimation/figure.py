#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# plotting
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
cm = 1/2.54 # for inches-cm conversion

# data science
import numpy as np
import pandas as pd

# i/o
from pathlib import PurePath, Path

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": "Computer Modern",
    'font.size': 8
})

# DATA IMPORT ###################################

df = pd.read_csv(
    filepath_or_buffer = 'data/research_plan_data.csv',
    sep = ',',
    header = 'infer',
    index_col = False
)

# DATA MANIPULATION #############################

df['midpoint'] = ((df['max'] - df['min'])/2)+df['min']
df['errorbars'] = (df['max'] - df['min'])/2

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        dpi = 300,
        figsize=(16.5*cm, 5*cm), # A4=(210x297)mm
    )

# DATA #######################

x = df.index
y = df['midpoint']
y_err = df['errorbars']
y_average = df['average']

# AXIS LIMITS ################

plt.ylim(0,150)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

ax.set_xticks(np.arange(df.index.size))
ax.set_xticklabels([1,2,3,4,5,6,7,8,9,10,11])

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

plt.xlabel("Study")
plt.ylabel("Underestimation of Impacts \n $\Delta(I_{PLCI}, I_{HLCI})$ [\%]")


# PLOTTING ###################

plt.errorbar(
    x = x,
    y = y,
    yerr = y_err,
    fmt = 'none',
    capsize = 2,
    ecolor = 'black',
    label = 'Range (min./max.)',
    elinewidth = 1
)
plt.scatter(
    x = x,
    y = y_average,
    c = 'black',
    marker = 'x',
    s = 10,
    label = 'Average',
)

# LEGEND ####################

ax.legend(loc = 'upper right', frameon = True)

# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%
