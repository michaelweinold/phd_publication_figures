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
    'font.size': 12
})

# DATA IMPORT ###################################

df_eff = pd.read_excel(
    io = '../efficiency/data/data_29-11-2023.xlsx',
    sheet_name = 'data',
    usecols = lambda column: column in [
        'Name',
        'Type',
        'YOI',
        'TSFC Cruise',
        'BP Ratio'
    ],
    dtype={
        'Name': str,
        'Type': str,
        'YOI': int,
        'TSFC Cruise': float,
        'BP Ratio': float
    },
    header = 0,
    engine = 'openpyxl'
)

# DATA MANIPULATION #############################

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
ax.set_ylim(0,30)

# TICKS AND LABELS ###########

from matplotlib.ticker import MultipleLocator
ax.xaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_minor_locator(MultipleLocator(1))

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)

ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)


# AXIS LABELS ################

ax.set_ylabel("TSFC (Cruise) [mg/Ns]")
ax.set_xlabel("Aircraft Year of Introduction")

# PLOTTING ###################

ax.scatter(
    x = df_eff['YOI'],
    y = df_eff['TSFC Cruise'],
    marker = 'o',
    color = 'blue',
    label = 'Widebody'
)

ax.axhline(y=11.1, color='black', linestyle='--', linewidth=2, label='Practical Limit w.r.t. NOx')
ax.axhline(y=10.1, color='black', linestyle='-', linewidth=2, label = 'Theoretical Limit')


# LEGEND ####################

ax.legend(
    loc='lower right',
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

 # ------PLOT TSFC CRUISE vs. YOI ------------------------ with Colors for BPR
    cm = 1 / 2.54  # for inches-cm conversion
    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    #  Limits from Kurzke/Singh et al.
    limit = (0.555 * heatingvalue / flight_vel)**-1
    limit_nox = (0.50875 * heatingvalue / flight_vel) ** -1

    # Make Groups of BPR
    bpr = databank.groupby(['Name', 'YOI'], as_index=False).agg({'TSFC Cruise': 'mean',  'B/P Ratio': 'mean', 'Pressure Ratio':'mean'})
    low = bpr.loc[bpr['B/P Ratio'] <= 2]
    medium = bpr.loc[(bpr['B/P Ratio'] >= 2) & (bpr['B/P Ratio'] <= 8)]
    high = bpr.loc[bpr['B/P Ratio'] >= 8]

    ax.scatter(comet1['YOI'], comet1['TSFC Cruise'], color='red')
    ax.scatter(comet4['YOI'], comet4['TSFC Cruise'], color='red')
    ax.scatter(low['YOI'], low['TSFC Cruise'], color='red', label='BPR $<$ 2')
    ax.scatter(medium['YOI'], medium['TSFC Cruise'], color='purple', label='BPR 2 - 8')
    ax.scatter(high['YOI'], high['TSFC Cruise'], color='blue', label='BPR $>$ 8')

    ax.axhline(y=limit_nox, color='black', linestyle='--', linewidth=2, label='Practical Limit w.r.t. NOx')
    ax.axhline(y=limit, color='black', linestyle='-', linewidth=2, label = 'Theoretical Limit')

    # Fuse in Data for Future projections
    ax.scatter(2020, 14.94, color='green', label='Future Projections')
    plt.annotate('GE9X', (2020, 14.94),
                    fontsize=6, xytext=(-10, -10),
                    textcoords='offset points')
    ax.scatter(2025, 12.88, color='green')
    plt.annotate('Ultrafan', (2025, 12.88),
                    fontsize=6, xytext=(-10, 5),
                    textcoords='offset points')
    ax.scatter(2030, 12.152, color='green')
    plt.annotate('Open Rotor', (2030, 12.152),
                    fontsize=6, xytext=(-10, 5),
                    textcoords='offset points')
    ax.scatter(2035, 12, color='green')
    plt.annotate('CFM RISE', (2035, 12),
                    fontsize=6, xytext=(10, 0),
                    textcoords='offset points')
    plt.xlim(1950,2050)