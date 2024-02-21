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

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 12
})

# DATA IMPORT ###################################

df_dashboard = pd.read_excel(
    io = '../efficiency/data/data_dashboard_29-11-2023.xlsx',
    sheet_name = 'Sheet1',
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

dashboard = df_dashboard

start_year = 1958
middle_year = 2000
end_year = 2020

# Code from the Dashboard, Bokeh Properties converted to Matplotlib
ida = dashboard.set_index('YOI')
ida.loc[1958] = 0
ida = ida.sort_index()
# Get Columns for the technological improvements
ida_tech = ida[['deltaC_Engine', 'deltaC_Aerodyn', 'deltaC_Structural', 'deltaC_Res', 'deltaC_Tot']]
ida_tech = ida_tech.rename(columns={
    'deltaC_Engine': 'Engine',
    'deltaC_Aerodyn': 'Aerodynamic',
    'deltaC_Structural': 'Structural',
    'deltaC_Res': 'Residual',
    'deltaC_Tot': 'Overall'})
df = ida_tech
colors = ["dimgrey", 'red', 'blue', 'orange', 'green',
            "dimgrey", 'red', 'blue', 'orange', 'green',
            "dimgrey"]

df['Overall_1'] = 10000 / (df['Overall'] + 100)
df['Total'] = df['Engine'] + df['Aerodynamic'] + df['Structural'] + df['Residual']
df['Overall Inverse'] = 100 - df['Overall_1']
cols_to_update = ['Engine', 'Aerodynamic', 'Structural', 'Residual']
for col in cols_to_update:
    df.loc[df.index[1:], col] = -1 * (df.loc[df.index[1:], col] / df.loc[df.index[1:], 'Total']) * df.loc[
        df.index[1:], 'Overall Inverse']

df = df.drop(columns=['Overall Inverse', 'Total', 'Overall'])
# Code to create the waterfall charts with the start, middle and end year.
df_dif_first = pd.DataFrame((df.loc[middle_year] - df.loc[start_year])).reset_index()
df_dif_first.columns = ['Eff', 'Value']
df_dif_first['Offset'] = df_dif_first['Value'].cumsum() - df_dif_first['Value'] + df.loc[start_year][
        'Overall_1']
df_dif_first['Offset'].iloc[-1] = 0
df_dif_first['ValueSum'] = df_dif_first['Value'].cumsum() + df.loc[start_year]['Overall_1']
df_dif_first['Value'].iloc[-1] = df_dif_first['Value'].iloc[-1] + df.loc[start_year]['Overall_1']

df_dif_second = pd.DataFrame((df.loc[end_year] - df.loc[middle_year])).reset_index()
df_dif_second.columns = ['Eff', 'Value']
df_dif_second['Offset'] = df_dif_second['Value'].cumsum() - df_dif_second['Value'] + df.loc[middle_year][
        'Overall_1']
df_dif_second['Offset'].iloc[-1] = 0
df_dif_second['ValueSum'] = df_dif_second['Value'].cumsum() + df.loc[middle_year]['Overall_1']
df_dif_second['Value'].iloc[-1] = df_dif_second['Value'].iloc[-1] + df.loc[middle_year]['Overall_1']
df_dif = pd.concat([df_dif_first, df_dif_second])

df_dif['Eff'] = df_dif.groupby('Eff').cumcount().astype(str).replace('0', '') + '_' + df_dif['Eff']

value = df_dif.loc[df_dif['Eff'] == '_Engine', 'Offset']
overall_baseline = pd.DataFrame({'Eff': 'Overall', 'Value': value, 'Offset': 0, 'ValueSum': value})
df_dif = pd.concat([overall_baseline, df_dif]).reset_index(drop=True)
df_dif['Color'] = colors[:len(df_dif)]
df = df_dif

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 1,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
)

# AXIS LIMITS ################

#ax.set_xlim(1950, 2024)
#ax.set_ylim(0, 4)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# axes[0]IS LABELS ################

ax.set_ylabel('Relative EU [\%], 1958=100')

# PLOTTING ###################

# Plot the bars and add text values
for i in range(len(df)):
    color = df['Color'][i]
    value = df['Value'][i]
    offset = df['Offset'][i]
    label = df['Eff'][i]

    if i == 0:
        ax.bar(label, value, bottom=offset, color=color, label='_nolegend_')
        prev_value = value
        prev_offset = offset
        continue

    ax.bar(label, value, bottom=offset, color=color, label='_nolegend_')

    # Add a horizontal line connecting adjacent bars starting from the second bar
    ax.hlines(prev_offset + prev_value, i-1.4, i+0.4, color='black', linestyle='-', linewidth=1)

    # Add text value below each bar (with absolute value and percentage), except for i = 5 and i = 10
    if i != 5 and i != 10:
        if value >= 0:
            ax.text(label, offset + value + 7, f'{value:.1f}\%', ha='center', va='top', color='black')
        else:
            ax.text(label, offset + value -8, f'{value:.1f}\%', ha='center', va='bottom', color='black')

    prev_value = value
    prev_offset = offset

# Set y-axis labels to have + or - symbols
from matplotlib.ticker import FuncFormatter
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.1f}' if x >= 0 else f'{-x:.1f}'))

# Add gridlines and labels
ax.axhline(0, color='black', linewidth=1)

# Show the plot
custom_ticks = [0, 5, 10]  # Example arbitrary tick positions
custom_tick_labels = ['1958', '2000', '2020']  # Example tick labels
ax.set_xticks(custom_ticks)
ax.set_xticklabels(custom_tick_labels)

# Dummy scatter points to represent the legend markers
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
dummy_patches = [
    Patch(facecolor='dimgrey', edgecolor='w', label='Overall'),
    Patch(facecolor='red', edgecolor='w', label='Engine'),
    Patch(facecolor='blue', edgecolor='w', label='Aerodynamic'),
    Patch(facecolor='orange', edgecolor='w', label='Structural'),
    Patch(facecolor='green', edgecolor='w', label='Residual')
]

# LEGEND ####################

ax.legend(dummy_patches, ["Overall", "Engine", "Aerodynamic", "Structural", "Residual"], loc='upper right')

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