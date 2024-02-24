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
    'font.size': 12
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
    sheet_name = 'Aerosols-NaturalClouds',
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

df_contrail_cirrus = pd.read_excel(
    io = 'data/data.xlsx',
    sheet_name = 'Contrail-Cirrus',
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
    rect = (0,0,1,0.075), # (left, bottom, width, height), relative to figure size
    label = 'CO2',
)
ax0.set_xlim(-275,100)
ax0.set_ylim(0,1)
ax0.set_yticklabels([]) # no y-tick labels
#ax0.tick_params(labelbottom = False) # no x-tick labels, https://stackoverflow.com/a/50037830
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
    x = 0.849,  # Relative x-coordinate
    y = 0.475,   # Relative y-coordinate
    s = r'\textbf{CO$_2$ Emissions}',
    ha = 'left',
    va = 'center',
    fontsize = 11,
    color = 'black',
    transform = ax0.transAxes  # Use axis coordinates
)

# NOx

ax1 = fig.add_axes(
    rect = (0,-0.44,1,0.3), # (left, bottom, width, height)
    label = 'nox',
    sharex = ax0
)
ax1.set_ylim(0,4)
ax1.set_yticklabels([]) # no y-tick labels
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
    x = 0.72,  # Relative x-coordinate
    y = 0.115,   # Relative y-coordinate
    s = r'\textbf{Net NO$_x$ Emissions}',
    ha = 'right',
    va = 'center',
    fontsize = 11,
    color = 'black',
    transform = ax1.transAxes  # Use axis coordinates
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
    x = 0.67,  # Relative x-coordinate
    y = 0.37,   # Relative y-coordinate
    s = r'\textbf{NO$_x$ (Ozone)}',
    ha = 'right',
    va = 'center',
    fontsize = 11,
    color = 'black',
    transform = ax1.transAxes  # Use axis coordinates
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
    x = 0.62,  # Relative x-coordinate
    y = 0.63,   # Relative y-coordinate
    s = r'\textbf{NO$_x$ (Methane)}',
    ha = 'right',
    va = 'center',
    fontsize = 11,
    color = 'black',
    transform = ax1.transAxes  # Use axis coordinates
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
    x = 0.71,  # Relative x-coordinate
    y = 0.873,   # Relative y-coordinate
    s = r'\textbf{NO$_x$ (Water)}',
    ha = 'right',
    va = 'center',
    fontsize = 11,
    color = 'black',
    transform = ax1.transAxes  # Use axis coordinates
)

# Soot/Radiation

ax2 = fig.add_axes(
    rect = (0,-0.66,1,0.075), # (left, bottom, width, height)
    label = 'soot-radiation',
    sharex = ax0
)
ax2.set_ylim(0,1)
ax2.set_yticklabels([]) # no y-tick labels
ax2.tick_params(labelbottom = False) # https://stackoverflow.com/a/50037830
ax2.tick_params(axis='y', which='both', length=0) # no y-ticks

ax2.set_title(
    label = 'Short-Term Effects (Non-Cumulative)',
    fontsize = 11,
    fontweight = 'bold',
)

ax2.barh(
    y = 0.5,
    width = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Soot']['ERF Average [mW/m2]'],
    height = 0.8,
    align='center',
    color = 'red',
    edgecolor = 'black'
)
# https://stackoverflow.com/a/33857966
average = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Soot']['ERF Average [mW/m2]']
lower = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Soot']['ERF Lower Errorbar [mW/m2]']
upper = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Soot']['ERF Upper Errorbar [mW/m2]']
ax2.errorbar(
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
ax2.errorbar(
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
ax2.text(
    x = 0.755,  # Relative x-coordinate
    y = 0.475,   # Relative y-coordinate
    s = r'\textbf{Soot-Radiation Trapping}',
    ha = 'left',
    va = 'center',
    fontsize = 11,
    color = 'black',
    transform = ax2.transAxes  # Use axis coordinates
)

# Sulfur/Radiation

ax3 = fig.add_axes(
    rect = (0,-0.76,1,0.075), # (left, bottom, width, height)
    label = 'sulfur-radiation',
    sharex = ax0
)
ax3.set_ylim(0,1)
ax3.set_yticklabels([]) # no y-tick labels
ax3.tick_params(labelbottom = False) # https://stackoverflow.com/a/50037830
ax3.tick_params(axis='y', which='both', length=0) # no y-ticks

ax3.barh(
    y = 0.5,
    width = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Sulfur']['ERF Average [mW/m2]'],
    height = 0.8,
    align='center',
    color = 'blue',
    edgecolor = 'black'
)
# https://stackoverflow.com/a/33857966
average = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Sulfur']['ERF Average [mW/m2]']
lower = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Sulfur']['ERF Lower Errorbar [mW/m2]']
upper = df_aerosols_rad[df_aerosols_rad['Effect'] == 'Sulfur']['ERF Upper Errorbar [mW/m2]']
ax3.errorbar(
    x = average,
    y = 0.5,
    xerr = (
        pd.Series([0]),
        abs(average - upper)
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'white',
    elinewidth = 1,
)
ax3.errorbar(
    x = average,
    y = 0.5,
    xerr = (
        abs(average - lower),
        pd.Series([0]),
    ),
    fmt = 'none',
    capsize = 4,
    ecolor = 'black',
    elinewidth = 1,
)
ax3.text(
    x = 0.755,  # Relative x-coordinate
    y = 0.475,   # Relative y-coordinate
    s = r'\textbf{Sulfur-Radiation Trapping}',
    ha = 'left',
    va = 'center',
    fontsize = 11,
    color = 'black',
    transform = ax3.transAxes  # Use axis coordinates
)

# Water Vapor (H2O)

ax4 = fig.add_axes(
    rect = (0,-0.86,1,0.075), # (left, bottom, width, height)
    label = 'water',
    sharex = ax0
)
ax4.set_ylim(0,1)
ax4.set_yticklabels([]) # no y-tick labels
ax4.tick_params(labelbottom = False) # https://stackoverflow.com/a/50037830
ax4.tick_params(axis='y', which='both', length=0) # no y-ticks

ax4.barh(
    y = 0.5,
    width = df_h2o['ERF Average [mW/m2]'],
    height = 0.8,
    align='center',
    color = 'red',
    edgecolor = 'black'
)

average = df_h2o['ERF Average [mW/m2]']
lower = df_h2o['ERF Lower Errorbar [mW/m2]']
upper = df_h2o['ERF Upper Errorbar [mW/m2]']
ax4.errorbar(
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
ax4.errorbar(
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
ax4.text(
    x = 0.755,  # Relative x-coordinate
    y = 0.475,   # Relative y-coordinate
    s = r'\textbf{Water Vapor}',
    ha = 'left',
    va = 'center',
    fontsize = 11,
    color = 'black',
    transform = ax4.transAxes  # Use axis coordinates
)

# Contrail-Cirrus
ax5 = fig.add_axes(
    rect = (0,-0.96,1,0.075), # (left, bottom, width, height)
    label = 'aerosols-clouds',
    sharex = ax0
)
ax5.set_ylim(0,1)
ax5.tick_params(labelbottom = False) # https://stackoverflow.com/a/50037830
ax5.set_yticklabels([]) # no y-tick labels
ax5.tick_params(axis='y', which='both', length=0) # no y-ticks

ax5.barh(
    y = 0.5,
    width = df_contrail_cirrus[df_contrail_cirrus['Authors (Label)'] == 'Lee et al.']['ERF Average [mW/m2]'],
    height = 0.8,
    align='center',
    color = 'red',
    edgecolor = 'black'
)

average = df_contrail_cirrus[df_contrail_cirrus['Authors (Label)'] == 'Lee et al.']['ERF Average [mW/m2]']
lower = df_contrail_cirrus[df_contrail_cirrus['Authors (Label)'] == 'Lee et al.']['ERF Lower Errorbar [mW/m2]']
upper = df_contrail_cirrus[df_contrail_cirrus['Authors (Label)'] == 'Lee et al.']['ERF Upper Errorbar [mW/m2]']
ax5.errorbar(
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
ax5.errorbar(
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

ax5.text(
    x = 0.725,  # Relative x-coordinate
    y = 0.475,   # Relative y-coordinate
    s = r'\textbf{Contrail and Contrail-Cirrus Formation}',
    ha = 'right',
    va = 'center',
    fontsize = 11,
    color = 'black',
    transform = ax5.transAxes  # Use axis coordinates
)

# Aerosols-Clouds

ax6 = fig.add_axes(
    rect = (0,-1.06,1,0.075), # (left, bottom, width, height)
    label = 'aerosols-clouds',
    sharex = ax0
)
ax6.set_ylim(0,2)
ax6.set_yticklabels([]) # no y-tick labels
ax6.tick_params(axis='y', which='both', length=0) # no y-ticks

x_upper = df_aerosols_clouds[df_aerosols_clouds['Authors (Label)'] == 'Righi et al. (2021)']['ERF Upper Errorbar [mW/m2]']
x_lower = df_aerosols_clouds[df_aerosols_clouds['Authors (Label)'] == 'Righi et al. (2021)']['ERF Lower Errorbar [mW/m2]']
ax6.plot(
    (x_lower, x_upper),
    (0.5, 0.5),
    color = 'blue',
    marker = 's',
    markersize = 5,
    markerfacecolor='blue',
    linestyle = '--',
)
average = df_aerosols_clouds[df_aerosols_clouds['Authors (Label)'] == 'Righi et al. (2021)']['ERF Average [mW/m2]']
ax6.plot(
    (average),
    (0.5),
    color = 'black',
    marker = 'o',
    markersize = 5,
    markerfacecolor='blue',
)
ax6.text(
    x = 0.538,  # Relative x-coordinate
    y = 0.28,   # Relative y-coordinate
    s = r'\textbf{Righi et al. (2021)}',
    ha = 'left',
    va = 'center',
    fontsize = 8,
    color = 'black',
    transform = ax6.transAxes  # Use axis coordinates
)

average = df_aerosols_clouds[df_aerosols_clouds['Authors (Label)'] == 'Gettelman and Chen (2013)']['ERF Average [mW/m2]']
ax6.plot(
    (average),
    (1.5),
    color = 'black',
    marker = 'o',
    markersize = 5,
    markerfacecolor='blue',
)
ax6.text(
    x = 0.6,  # Relative x-coordinate
    y = 0.7,   # Relative y-coordinate
    s = r'\textbf{Gettelman/Chen (2013)}',
    ha = 'right',
    va = 'center',
    fontsize = 8,
    color = 'black',
    transform = ax6.transAxes  # Use axis coordinates
)

average = df_aerosols_clouds[df_aerosols_clouds['Authors (Label)'] == 'Kapadia et al. (2016)']['ERF Average [mW/m2]']
ax6.plot(
    (average),
    (1.5),
    color = 'black',
    marker = 'o',
    markersize = 5,
    markerfacecolor='blue',
)
ax6.text(
    x = 0.68,  # Relative x-coordinate
    y = 0.7,   # Relative y-coordinate
    s = r'\textbf{Kapadia et al. (2016)}',
    ha = 'left',
    va = 'center',
    fontsize = 8,
    color = 'black',
    transform = ax6.transAxes  # Use axis coordinates
)

ax6.text(
    x = 0.8,  # Relative x-coordinate
    y = 0.475,   # Relative y-coordinate
    s = r'\textbf{Cloudiness from Sulfur}',
    ha = 'left',
    va = 'center',
    fontsize = 11,
    color = 'black',
    transform = ax6.transAxes  # Use axis coordinates
)


# GRID ######################

for ax in fig.axes:
    ax.grid(
        axis = 'x',
        linestyle = '-',
        linewidth = 1
    )

# LEGEND ####################
    
import matplotlib.patches as patches
import matplotlib.lines as lines

import matplotlib as mpl
mpl.rcParams['hatch.linewidth'] = 3

legend_elements = [
    patches.Patch(
        facecolor='red',
        edgecolor='black'
    ),
    patches.Patch(
        facecolor='red',
        edgecolor='black',
        hatch='///',
    ),
    lines.Line2D(
        [0],
        [1],
        color='black',
        lw=1,
        marker='|',
        linestyle='-',
    ),
    lines.Line2D(
        [0],
        [1],
        color='black',
        lw=2,
        marker='s',
        linestyle='--',
    ),
]

ax1.legend(
    handles = legend_elements,
    labels = [
        'Total Effect (Metastudy)',
        'Sub-Effect (Metastudy)',
        '5/95\% Confidence Interval (Metastudy)',
        'High/Low Range (Individual Study)',
    ],
    loc = 'upper left',
    numpoints=2,
    alignment = 'left',
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
# %%
