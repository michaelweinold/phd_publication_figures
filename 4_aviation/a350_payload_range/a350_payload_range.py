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

# DATA MANIPULATION #############################

# https://www.airbus.com/sites/g/files/jlcbta136/files/2021-11/Airbus-Commercial-Aircraft-AC-A350-900-1000.pdf
point_a = (500,54)
point_b = (5830,54)
point_c = (8575, 25)
point_d = (9620,0)
point_a_325pax = (500, 30.5)
point_b_325pax = (8050, 30.5)

# https://doi.org/10.1016/j.scitotenv.2023.163881
point_hamelin_et_al = (15550*0.539957, 143.81)

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

ax.set_xlim(500, 12500)
ax.set_ylim(0, 150)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)

import matplotlib.ticker as ticker
def thousand_formatter(value, tick_number):
    """
    Formats the tick label with thousand separators: 1000 = 1'000.
    """
    return f"{int(value):,}".replace(",", "'")

ax.xaxis.set_major_formatter(ticker.FuncFormatter(thousand_formatter))

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# axes[0]IS LABELS ################

ax.set_xlabel('Range [NM]')
ax.set_ylabel("Payload [t]")

# PLOTTING ###################

plt.plot(
    [point_a[0], point_b[0], point_c[0], point_d[0]],
    [point_a[1], point_b[1], point_c[1], point_d[1]],
    color = 'black',
    linestyle = '-',
    linewidth = 1,
    marker = 'o',
    label = 'Max. Structural Payload',
)
plt.plot(
    [point_a_325pax[0], point_b_325pax[0]],
    [point_a_325pax[1], point_b_325pax[1]],
    color = 'black',
    linestyle = '--',
    linewidth = 1,
    marker = 'o',
    label = 'Payload at 325 pax.',
)

ax.annotate(
    'A',
    xy = point_a,
    xytext = (point_a[0]+100, point_a[1]+2),
    fontsize = 12,
)
ax.annotate(
    'B',
    xy = point_b,
    xytext = (point_b[0]+100, point_b[1]+2),
    fontsize = 12,
)
ax.annotate(
    'C',
    xy = point_c,
    xytext = (point_c[0]+100, point_c[1]+2),
    fontsize = 12,
)
ax.annotate(
    'D',
    xy = point_d,
    xytext = (point_d[0]+100, point_d[1]+2),
    fontsize = 12,
)

ax.fill_between(
    x = [point_a[0], point_b[0]],
    y1 = [point_a[1], point_b[1]],
    y2 = 0,
    color = 'tab:blue',
    alpha = 0.35,
    label = 'Max. Payload',
)
ax.fill_between(
    x = [point_b[0], point_c[0]],
    y1 = [point_b[1], point_c[1]],
    y2 = 0,
    color = 'tab:orange',
    alpha = 0.35,
    label = 'Fuel/Payload Tradeoff',
)
ax.fill_between(
    x = [point_c[0], point_d[0]],
    y1 = [point_c[1], point_d[1]],
    y2 = 0,
    color = 'tab:red',
    alpha = 0.35,
    label = 'Payload/Range Tradeoff',
)

ax.plot(
    [point_hamelin_et_al[0]],
    [point_hamelin_et_al[1]],
    color = 'red',
    marker = 'o',
    markersize = 8,
)

ax.annotate(
    'Su-ungkavatin et al. (2023) \n $\sim$8\'400NM at 143t',
    xy = point_hamelin_et_al,
    xytext = (point_hamelin_et_al[0]-2000, point_hamelin_et_al[1]-30),
    arrowprops=dict(arrowstyle='->', color='black'),
    fontsize = 12,
)

# LEGEND ####################

ax.legend(
    loc = 'upper left',
    title = r'\textbf{Airbus A350-900}',
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