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
    io = '../efficiency/data/data_29-11-2023.xlsx',
    sheet_name = 'data',
    usecols = lambda column: column in [
        'Name',
        'Type',
        'YOI',
        'TSFC Cruise',
        'B/P Ratio'
    ],
    dtype={
        'Name': str,
        'Type': str,
        'YOI': int,
        'TSFC Cruise': float,
        'B/P Ratio': float
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

ax.set_ylabel("TSFC (Cruise) [mg(JetA1)/Ns]")
ax.set_xlabel("Aircraft Year of Introduction")

# PLOTTING ###################

sc = ax.scatter(
    x = df_eff['YOI'],
    y = df_eff['TSFC Cruise'],
    marker = 'o',
    c = df_eff['B/P Ratio'],
    label = 'Widebody',
    cmap = 'plasma',
)
plt.colorbar(sc, label='B/P Ratio')

ax.axhline(y=11.1, color='black', linestyle='--', linewidth=2, label='Practical Limit w.r.t. NOx')
ax.axhline(y=10.1, color='black', linestyle='-', linewidth=2, label = 'Theoretical Limit')

# Add a thick arrow pointing down
ax.annotate(
    'lower=better', 
    xy=(2040, 20), 
    xytext=(2040, 27), 
    arrowprops=dict(facecolor='black', width=1, headwidth=10),
        va='center',
    ha='center'
)

ax.scatter(
    x = 2020,
    y = 14.94,
    color='green'
)
ax.scatter(
    x = 2020,
    y = 14.94,
    facecolors='none',
    edgecolors='black',
    s=90,
    label = 'Projection'
)
plt.annotate(
    'GE9X',
    (2020, 14.94),
    xytext=(0, +10),
    textcoords='offset points'
)

ax.scatter(
    x = 2025,
    y = 12.88,
    color='green'
)
ax.scatter(
    x = 2025,
    y = 12.88,
    facecolors='none',
    edgecolors='black',
    s=90,
)
plt.annotate(
    'RR Ultrafan',
    (2020, 12.88),
    xytext=(-43, -10),
    textcoords='offset points'
)

ax.scatter(
    x = 2030,
    y = 12.152,
    color='green'
)
ax.scatter(
    x = 2030,
    y = 12.152,
    facecolors='none',
    edgecolors='black',
    s=90,
)
plt.annotate(
    'Open Rotor',
    (2030, 12.152),
    xytext=(-10, +10),
    textcoords='offset points'
)

ax.scatter(
    x = 2035,
    y = 12,
    color='green'
)
ax.scatter(
    x = 2035,
    y = 12,
    facecolors='none',
    edgecolors='black',
    s=90,
)
plt.annotate(
    'CFM Rise',
    (2035, 12),
    xytext=(+10, -2),
    textcoords='offset points'
)


# LEGEND ####################

from matplotlib.lines import Line2D

legend_elements_categories = [
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'black',
        markerfacecolor='black',
        linestyle = 'None',
        markersize=4,
        marker='o',
        label = 'Acft./Engine Combinations'
    ),
    Line2D(
        xdata = [0],
        ydata = [0],
        color = 'black',
        markerfacecolor='none',
        linestyle = 'None',
        markersize=7,
        marker='o',
        label = 'Projections'
    ),
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
    )
]

ax.legend(
    handles=legend_elements_categories,
    loc='lower right',
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