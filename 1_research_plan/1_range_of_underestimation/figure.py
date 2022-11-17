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

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.sans-serif": "Computer Modern",
})

# DATA IMPORT ###################################

df = pd.read_csv(
    filepath_or_buffer = 'research_plan_data.csv',
    sep = ',',
    header = 'infer',
    index_col = False
)

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
y_top = df['max']
y_bottom = df['min']
y_average = df['average']

# TICKS AND LABELS ###########

plt.bar(
    x = x,
    height = y_top,
    bottom=y_bottom,
    width = 0.5*cm,
    label = 'Range (min./max.)'
)
plt.scatter(
    x = x,
    y = y_average,
    c = 'black',
    label = 'Average'
)

plt.ylim(0,150)

# GRIDS ######################

ax.grid(visible=None, which='major', axis='y')

# AXIS LABELS ################

plt.xlabel("Study")
plt.ylabel(" Underestimation of Impacts \n $\Delta(I_{PLCI}, I_{HLCI})$ [\%]")

# EXPORT #########################################

ax.legend(loc = 'upper left')

# %%
