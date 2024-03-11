#%%
# runs code as interactive cell 
# https://code.visualstudio.com/docs/python/jupyter-support-py

# IMPORTS #######################################

# sys
import os
# plotting
import matplotlib.pyplot as plt
# unit conversion
cm = 1/2.54 # for inches-cm conversion
# time manipulation
from datetime import datetime
# data science
import numpy as np
import pandas as pd
import pandas as pd

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 11
})

# DATA IMPORT ###################################

df_my_acft = pd.read_excel(
    io = 'data/data.xlsx', 
    sheet_name = 'my_acft',
    usecols = lambda column: column in [
        'MTOW [kg]',
        'metric value [kg/km]',
        'shortname',
    ],
    dtype={
        'MTOW [kg]': int,
        'metric value [kg/km]': float,
        'shortname': str,
    },
    header = 0,
    engine = 'openpyxl',
    decimal='.'
)

# DATA MANIPULATION #############################

# source: ICAO Annex 16, Vol. 3, Chapter 2.4 ff.

def mv_limit_1(x: float) -> float:
    return 10**(-2.73780+(0.681310*np.log10(x))+(-0.0277861*np.log10(x)**2))

def mv_limit_2(x: float) -> float:
    return 10**(-1.412742+(-0.020517*np.log10(x))+(0.0593831*np.log10(x)**2))


# Generate x values from 0 to 150
x_values_1 = np.linspace(0, 60000, 50)
y_values_1 = [mv_limit_1(y) for y in x_values_1]
x_values_2 = np.linspace(60000, 70394, 2)
y_values_2 = np.linspace(0.764, 0.764, 2)
x_values_3 = np.linspace(70395, 600000, 50)
y_values_3 = [mv_limit_2(y) for y in x_values_3]

df_1 = pd.DataFrame({
    'x': np.concatenate((x_values_1, x_values_2, x_values_3)),
    'y': np.concatenate((y_values_1, y_values_2, y_values_3))
})

def mv_limit_1_1(x: float) -> float:
    return 10**(-2.57535+(0.609766*np.log10(x))+(-0.0191302*np.log10(x)**2))

def mv_limit_2_1(x: float) -> float:
    return 10**(-1.39353+(-0.020517*np.log10(x))+(0.0593831*np.log10(x)**2))


# Generate x values from 0 to 150
x_values_1_1 = np.linspace(0, 60000, 50)
y_values_1_1 = [mv_limit_1_1(y) for y in x_values_1_1]
x_values_2_1 = np.linspace(60000, 70106, 2)
y_values_2_1 = np.linspace(0.797, 0.797, 2)
x_values_3_1 = np.linspace(70107, 600000, 50)
y_values_3_1 = [mv_limit_2_1(y) for y in x_values_3_1]

df_1_1 = pd.DataFrame({
    'x': np.concatenate((x_values_1_1, x_values_2_1, x_values_3_1)),
    'y': np.concatenate((y_values_1_1, y_values_2_1, y_values_3_1))
})

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

ax.set_xlim(0,600000)
ax.set_ylim(0,3)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)


# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("\"CO$_2$ Emissions Evaluation Metric\" [kg/km]")
ax.set_xlabel("MTOW [kg]")

# PLOTTING ###################

ax.plot(
    df_1['x'], df_1['y'],
    color = 'blue',
    linestyle = '-',
    linewidth = 2,
    label = 'CO$_2$ Limit New Types',
)
ax.plot(
    df_1_1['x'], df_1_1['y'],
    color = 'red',
    linestyle = '-',
    linewidth = 2,
    label = 'CO$_2$ Limit Existing Types (in Production)',
)

for i, shortname in enumerate(df_my_acft['shortname']):
    ax.annotate(shortname, (df_my_acft['MTOW [kg]'][i], df_my_acft['metric value [kg/km]'][i]), xytext=(5, 5), textcoords='offset points', bbox=dict(facecolor='white', edgecolor='none'))

ax.scatter(
    df_my_acft['MTOW [kg]'],
    df_my_acft['metric value [kg/km]'],
    label = 'Current Example Aircraft',
    color = 'black',
    marker = 'o',
    zorder = 10,
)

# LEGEND ####################

ax.legend(
    loc = 'upper left',
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
