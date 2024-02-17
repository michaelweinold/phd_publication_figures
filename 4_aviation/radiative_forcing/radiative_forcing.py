# %%
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

df_co2 = pd.read_excel(
    io = 'data/data.xlsx', 
    sheet_name = 'CO2',
    usecols = lambda column: column in [
        'Authors (Label)',
        'ERF Average [mW/m2]',
        'ERF Lower Errorbar [mW/m2]',
        'ERF Upper Errorbar [mW/m2]',
    ],
    dtype={
        'Authors (Label)': str,
        'ERF Average [mW/m2]': float,
        'ERF Lower Errorbar [mW/m2]': float,
        'ERF Upper Errorbar [mW/m2]': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)

df_nox = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'NOx',
    usecols = lambda column: column in [
        'Authors (Label)',
        'ERF Average [mW/m2]',
        'ERF Lower Errorbar [mW/m2]',
        'ERF Upper Errorbar [mW/m2]',
        'Effect',
    ],
    dtype={
        'Authors (Label)': str,
        'ERF Average [mW/m2]': float,
        'ERF Lower Errorbar [mW/m2]': float,
        'ERF Upper Errorbar [mW/m2]': float,
        'Effect': str,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)

df_h2o = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Water Vapor',
    usecols = lambda column: column in [
        'Authors (Label)',
        'ERF Average [mW/m2]',
        'ERF Lower Errorbar [mW/m2]',
        'ERF Upper Errorbar [mW/m2]',
    ],
    dtype={
        'Authors (Label)': str,
        'ERF Average [mW/m2]': float,
        'ERF Lower Errorbar [mW/m2]': float,
        'ERF Upper Errorbar [mW/m2]': float,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)

df_aerosols_rad = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Aerosols-Radiation',
    usecols = lambda column: column in [
        'Authors (Label)',
        'ERF Average [mW/m2]',
        'ERF Lower Errorbar [mW/m2]',
        'ERF Upper Errorbar [mW/m2]',
        'Effect',
    ],
    dtype={
        'Authors (Label)': str,
        'ERF Average [mW/m2]': float,
        'ERF Lower Errorbar [mW/m2]': float,
        'ERF Upper Errorbar [mW/m2]': float,
        'Effect': str,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)

df_aerosols_clouds = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Aerosols-Clouds',
    usecols = lambda column: column in [
        'Authors (Label)',
        'ERF Average [mW/m2]',
        'ERF Lower Errorbar [mW/m2]',
        'ERF Upper Errorbar [mW/m2]',
        'Effect',
    ],
    dtype={
        'Authors (Label)': str,
        'ERF Average [mW/m2]': float,
        'ERF Lower Errorbar [mW/m2]': float,
        'ERF Upper Errorbar [mW/m2]': float,
        'Effect': str,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)

# DATA MANIPULATION #############################

# FIGURE ########################################

# SETUP ######################

# see also:
# https://matplotlib.org/stable/users/explain/axes/arranging_axes.html#fixed-size-axes
fig = plt.figure(
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
)

# CUSTOM PLOTTING FUNCTIONS ##

# create a custom colormap going from white to red to white
from matplotlib.colors import LinearSegmentedColormap
colors = [(1, 1, 1), (1, 0, 0), (1, 1, 1)]  # White -> Red -> White
n_bins = 100  # Number of bins for the colormap
cmap_name = 'white_red_white'
# Register the colormap if it's not already registered
if cmap_name not in plt.colormaps():
    plt.register_cmap(cmap=LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins))

gradient = np.linspace(0, 1, 256)  # Create a 1D array with 256 values evenly spaced between 0 and 1
gradient = np.vstack((gradient, gradient))  # Stack the 1D array vertically to create a 2D array


import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 3

# PLOTTING ###################

# CO2

ax0 = fig.add_axes(
    rect = (0,0,1,0.1), # (left, bottom, width, height), relative to figure size
    label = 'CO2',
)
ax0.set_xlim(-275,100)
ax0.set_ylim(0,1)
ax0.set_yticklabels([]) # no y-tick labels
ax0.tick_params(labelbottom = False) # no x-tick labels, https://stackoverflow.com/a/50037830
ax0.tick_params(axis='y', which='both', length=0) # no y-ticks

ax0.set_title(
    label = 'Long-Term Effects (Cumulative)',
    fontsize = 11,
    fontweight = 'bold',
)
ax0.barh(
    y = 0.5,
    width = df_co2['ERF Average [mW/m2]'],
    height = 0.8,
    align='center',
    color = 'red',
    edgecolor = 'black'
)
# https://stackoverflow.com/a/33857966
average = df_co2['ERF Average [mW/m2]']
lower = df_co2['ERF Lower Errorbar [mW/m2]']
upper = df_co2['ERF Upper Errorbar [mW/m2]']
ax0.errorbar(
    x = average,
    y = 0.5,
    xerr = (
        abs(average - lower),
        pd.Series([0]),
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'white',
)
ax0.errorbar(
    x = average,
    y = 0.5,
    xerr = (
        pd.Series([0]),
        abs(average - upper)
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'black',
)
ax0.text(
    x=-140,
    y=0.5,
    s=r'\textbf{CO$_2$ Emissions}',
    ha='left',
    va='center',
    fontsize=8,
    color='black',
)

# NOx

ax1 = fig.add_axes(
    rect = (0,-0.49,1,0.4), # (left, bottom, width, height)
    label = 'nox',
    sharex = ax0
)
ax1.set_ylim(0,4)
ax1.set_yticklabels([]) # no y-tick labels
ax1.tick_params(labelbottom = False) # https://stackoverflow.com/a/50037830
ax1.tick_params(axis='y', which='both', length=0) # no y-ticks

ax1.set_title(
    label = 'Medium/Short-Term Effects (Non-Cumulative)',
    fontsize = 11,
    fontweight = 'bold',
)

ax1.imshow(
    gradient,
    aspect = 'auto',
    cmap = plt.get_cmap(cmap_name),
    extent = [
        26.7-10, # https://doi.org/10.1088/1748-9326/ab5dd7
        26.7+10,
        0.1,
        0.9
    ]
)
ax1.text(
    x=40,
    y=0.5,
    s=r'new: Grewe et al. (2019)',
    ha='left',
    va='center',
    fontsize=10,
    color='black',
)


ax1.barh(
    y = 0.5,
    width = df_nox[df_nox['Effect'] == 'Net NOx Emissions']['ERF Average [mW/m2]'],
    height = 0.8,
    align='center',
    color = 'red',
    edgecolor = 'black'
)
average = df_nox[df_nox['Effect'] == 'Net NOx Emissions']['ERF Average [mW/m2]']
lower = df_nox[df_nox['Effect'] == 'Net NOx Emissions']['ERF Lower Errorbar [mW/m2]']
upper = df_nox[df_nox['Effect'] == 'Net NOx Emissions']['ERF Upper Errorbar [mW/m2]']
ax1.errorbar(
    x = average,
    y = 0.5,
    xerr = (
        abs(average - lower),
        pd.Series([0]),
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'white',
    elinewidth = 1,
)
ax1.errorbar(
    x = average,
    y = 0.5,
    xerr = (
        pd.Series([0]),
        abs(average - upper)
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'black',
    elinewidth = 1,
)
ax1.text(
    x=-140,
    y=0.5,
    s=r'\textbf{Net NO$_x$}',
    ha='left',
    va='center',
    fontsize=8,
    color='black',
)

ax1.barh(
    y = 1.5,
    width = df_nox[df_nox['Effect'] == 'Short-Term Ozone Increase']['ERF Average [mW/m2]'],
    height = 0.8,
    align='center',
    color = 'red',
    edgecolor = 'black',
    linewidth = 0.5,
    hatch = '///',
)
average = df_nox[df_nox['Effect'] == 'Short-Term Ozone Increase']['ERF Average [mW/m2]']
lower = df_nox[df_nox['Effect'] == 'Short-Term Ozone Increase']['ERF Lower Errorbar [mW/m2]']
upper = df_nox[df_nox['Effect'] == 'Short-Term Ozone Increase']['ERF Upper Errorbar [mW/m2]']
ax1.errorbar(
    x = average,
    y = 1.5,
    xerr = (
        abs(average - lower),
        pd.Series([0]),
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'white',
    elinewidth = 1,
)
ax1.errorbar(
    x = average,
    y = 1.5,
    xerr = (
        pd.Series([0]),
        abs(average - upper)
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'black',
    elinewidth = 1,
)
ax1.text(
    x=-140,
    y=1.5,
    s=r'\textbf{NO$_x$ (Ozone)}',
    ha='left',
    va='center',
    fontsize=8,
    color='black',
)

ax1.barh(
    y = 1.5,
    width = df_nox[df_nox['Effect'] == 'Long-Term Ozone Decrease']['ERF Average [mW/m2]'],
    height = 0.8,
    align='center',
    color = 'blue',
    edgecolor = 'black',
    linewidth = 0.5,
    hatch = '///',
)
average = df_nox[df_nox['Effect'] == 'Long-Term Ozone Decrease']['ERF Average [mW/m2]']
lower = df_nox[df_nox['Effect'] == 'Long-Term Ozone Decrease']['ERF Lower Errorbar [mW/m2]']
upper = df_nox[df_nox['Effect'] == 'Long-Term Ozone Decrease']['ERF Upper Errorbar [mW/m2]']
ax1.errorbar(
    x = average,
    y = 1.5,
    xerr = (
        pd.Series([0]),
        abs(average - upper)
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'white',
    elinewidth = 1,
)
ax1.errorbar(
    x = average,
    y = 1.5,
    xerr = (
        abs(average - lower),
        pd.Series([0]),
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'black',
    elinewidth = 1,
)

ax1.barh(
    y = 2.5,
    width = df_nox[df_nox['Effect'] == 'Methane Decrease']['ERF Average [mW/m2]'],
    height = 0.8,
    align='center',
    color = 'blue',
    edgecolor = 'black',
    linewidth = 0.5,
    hatch = '///',
)
average = df_nox[df_nox['Effect'] == 'Methane Decrease']['ERF Average [mW/m2]']
lower = df_nox[df_nox['Effect'] == 'Methane Decrease']['ERF Lower Errorbar [mW/m2]']
upper = df_nox[df_nox['Effect'] == 'Methane Decrease']['ERF Upper Errorbar [mW/m2]']
ax1.errorbar(
    x = average,
    y = 2.5,
    xerr = (
        pd.Series([0]),
        abs(average - upper)
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'white',
    elinewidth = 1,
)
ax1.errorbar(
    x = average,
    y = 2.5,
    xerr = (
        abs(average - lower),
        pd.Series([0]),
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'black',
    elinewidth = 1,
)
ax1.text(
    x=-140,
    y=2.5,
    s=r'\textbf{NO$_x$ (Methane)}',
    ha='left',
    va='center',
    fontsize=8,
    color='black',
)

ax1.barh(
    y = 3.5,
    width = df_nox[df_nox['Effect'] == 'Water Vapor Decrease']['ERF Average [mW/m2]'],
    height = 0.8,
    align='center',
    color = 'blue',
    edgecolor = 'black',
    linewidth = 0.5,
    hatch = '///',
)
average = df_nox[df_nox['Effect'] == 'Water Vapor Decrease']['ERF Average [mW/m2]']
lower = df_nox[df_nox['Effect'] == 'Water Vapor Decrease']['ERF Lower Errorbar [mW/m2]']
upper = df_nox[df_nox['Effect'] == 'Water Vapor Decrease']['ERF Upper Errorbar [mW/m2]']
ax1.errorbar(
    x = average,
    y = 3.5,
    xerr = (
        pd.Series([0]),
        abs(average - upper)
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'white',
    elinewidth = 1,
)
ax1.errorbar(
    x = average,
    y = 3.5,
    xerr = (
        abs(average - lower),
        pd.Series([0]),
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'black',
    elinewidth = 1,
)
ax1.text(
    x=-140,
    y=3.5,
    s=r'\textbf{NO$_x$ (Water)}',
    ha='left',
    va='center',
    fontsize=8,
    color='black',
)

# GRID ######################

for ax in fig.axes:
    ax.grid(
        axis = 'x',
        linestyle = '-',
        linewidth = 1
    )

# LEGEND ####################

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