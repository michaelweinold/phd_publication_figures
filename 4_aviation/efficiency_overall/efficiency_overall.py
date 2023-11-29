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

# SETUP #########################################


plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 12
})

# DATA IMPORT ###################################

df_eff = pd.read_excel(
    io = '../efficiency/data/data_29-11-2023.xlsx',
    sheet_name = 'data',
    usecols = lambda column: column in [
        'Company',
        'Name',
        'Type',
        'YOI',
        'EU (MJ/ASK)',
    ],
    dtype={
        'Company': str,
        'Name': str,
        'Type': str,
        'YOI': int,
        'EU (MJ/ASK)': float,
    },
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

def split_data_by_source(df):
    

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

ax_right = ax.twinx()

# AXIS LIMITS ################

ax.set_xlim(1950, 2023)
ax.set_ylim(0,9)
ax_right.set_ylim(0,9)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=False)

# GRIDS ######################

ax.grid(which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='--', linewidth = 0.5)

# AXIS LABELS ################

ax.set_ylabel("Energy Usage [MJ/ASK]")
ax.set_xlabel("Aircraft Year of Introduction")

# PLOTTING ###################

ax.scatter(
    x = df_eff['YOI'],
    y = df_eff['EU (MJ/ASK)'],
    marker = 'o',
    color = 'black',
    label = 'test'
)

# LEGEND ####################

ax.legend(
    loc='upper right',
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
# %%


       ax.scatter(normal['YOI'], normal['MJ/ASK'], marker='^',color='blue', label='US DOT T2')
       ax.scatter(regional['YOI'], regional['MJ/ASK'], marker='^', color='cyan', label='Regional US DOT T2')
       ax.scatter(rest['Year'], rest['EU (MJ/ASK)'], marker='s',color='red', label='Lee')
       ax.plot(fleet_avg_year.index, fleet_avg_year['MJ/ASK'],color='blue', label='US DOT T2 Fleet')
       ax.plot(fleet_avg_year.index, fleet_avg_year['MJ/RPK'],color='blue',linestyle='--', label='US DOT T2 Fleet RPK')
       ax.plot(lee_fleet['Year'], lee_fleet['EU (MJ/ASK)'],color='red', label='Lee Fleet')

       ax.legend()
       future_legend = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title="Historic Data", frameon=False)
       future_legend._legend_box.align = "left"

       #Add projections from Lee et al.
       plot_past_projections = False
       if plot_past_projections:
              ax.scatter([1997, 2007, 2022], [1.443, 1.238, 0.9578], marker='^', color='black', label='NASA 100 PAX')
              ax.scatter([1997, 2007, 2022], [1.2787, 1.0386, 0.741], marker='*', color='black', label='NASA 150 PAX')
              ax.scatter([1997, 2007, 2022], [1.2267, 0.9867, 0.681], marker='s', color='black', label='NASA 225 PAX')
              ax.scatter([1997, 2007, 2022], [1.1704, 0.9259, 0.637], marker='o', color='black', label='NASA 300 PAX')
              ax.scatter([1997, 2007, 2022], [0.91, 0.76, 0.559], marker='P', color='black', label='NASA 600 PAX')
              ax.scatter(2010, 0.6587 , marker='^', color='grey', label='NRC')
              ax.scatter(2015, 0.5866, marker='o', color='grey', label='Greene')
              ax.scatter([2025, 2025, 2025], [0.55449, 0.6, 0.68], marker='s', color='grey', label='Lee')

              # Projection legend
              projection_handles = ax.get_legend_handles_labels()[0][8:]  # Exclude the first 8 handles (historic data)
              projection_labels = ax.get_legend_handles_labels()[1][8:]  # Exclude the first 8 labels (historic data)
              ax.legend(projection_handles, projection_labels, loc='lower left', bbox_to_anchor=(1, -0.05),
                                            title="Historic Projections", frameon=False)
              ax.add_artist(future_legend)
       plot_future_projections = False
       if plot_future_projections:
              ax.scatter(2035,0.592344579, marker='s', color='black', label='SB-Wing')
              ax.scatter(2035,0.381840741, marker='o', color='black', label='Double Bubble')
              ax.scatter(2040,0.82264895, marker='P', color='black', label='Advanced TW')
              ax.scatter(2040,0.797082164, marker='*', color='black', label='BWB')
              ax.scatter(2050,0.618628347, marker='^', color='black', label='TW Limit')

              # Projection legend
              projection_handles = ax.get_legend_handles_labels()[0][8:]  # Exclude the first 8 handles (historic data)
              projection_labels = ax.get_legend_handles_labels()[1][8:]  # Exclude the first 8 labels (historic data)
              ax.legend(projection_handles, projection_labels, loc='lower left', bbox_to_anchor=(1, -0.05),
                                            title="Future Projections", frameon=False)
              ax.add_artist(future_legend)