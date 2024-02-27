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

# i/o
from pathlib import PurePath, Path

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 12
})

# DATA IMPORT ###################################

emissions_data = [
    [0.21790859349727398, 0.9245575840327378],
    [3.729451993625478, 0.9666012411660689],
    [100, 0]
]

emissions_df = pd.DataFrame(
    emissions_data,
    columns=['x', 'y']
)

# DATA MANIPULATION #############################

from scipy.stats import norm
xnew = np.linspace(0, 100, 200)
ynew = norm.pdf(xnew, loc = 1.5, scale = 9)

# FIGURE ########################################

# SETUP ######################

fig, axes = plt.subplots(
    num = 'main',
    nrows = 1,
    ncols = 2,
    dpi = 300,
    figsize=(30*cm, 10*cm), # A4=(210x297)mm,
    sharex=True
)
plt.subplots_adjust(wspace=0.1)

# SECONDARY AXES ##############


# AXIS LIMITS ################

for ax in axes:
    ax.set_xlim(0, 100)
    ax.set_ylim(0,0.05)

# TICKS AND LABELS ###########

for ax in axes:
    ax.set_yticks([])
    ax.set_yticklabels([])

# GRIDS ######################

# AXIS LABELS ################

for ax in axes:
    ax.set_ylabel("Climate Impact")
    ax.set_xlabel("Years")

# PLOTTING ###################

axes[0].plot(
    xnew,
    ynew,
    color = 'blue',
    linewidth = 2,
    label = 'Short-Lived Emissions'
)
axes[0].plot(
    xnew,
    [0.02 for i in xnew],
    color = 'red',
    linewidth = 2,
    label = 'Long-Lived Emissions'
)
axes[0].errorbar(
    x = xnew[40],
    y = ynew[40]/2,
    yerr = ynew[40]/2,
    fmt = 'none',
    capsize = 4,
    capthick = 2,
    ecolor = 'blue',
    elinewidth = 2,
    label = 'C'
)
axes[0].errorbar(
    x = xnew[40],
    y = ynew[40] + (0.02 - ynew[40])/2,
    yerr = (0.02 - ynew[40])/2,
    fmt = 'none',
    capsize = 4,
    capthick = 2,
    ecolor = 'red',
    elinewidth = 2,
    label = 'D'
)
axes[0].text(
    x=2,
    y=0.04675,
    s=r'\textbf{Single Emission}',
    ha='left',
    va='center',
    fontsize=12,
    color='black',
)

axes[0].fill_between(
    x = xnew[0:41],
    y1 = 0,
    y2 = ynew[0:41],
    edgecolor='blue',
    facecolor='none',
    hatch = '///',
    alpha=0.3,
    label = 'A'
)
axes[0].fill_between(
    x = xnew[0:41],
    y1 = 0,
    y2 = [0.02 for i in xnew[0:41]],
    color='red',
    #hatch = '\\\\\\',
    alpha=0.3,
    label = 'B'
)

axes[1].plot(
    xnew,
    [0.01 for i in xnew],
    color = 'blue',
    linewidth = 2,
    label = 'Short-Lived Emissions'
)
axes[1].plot(
    xnew,
    [0.005+ 0.0002*i for i in xnew],
    color = 'red',
    linewidth = 2,
    label = 'Long-Lived Emissions'
)
axes[1].text(
    x=3,
    y=0.04675,
    s=r'\textbf{Continous Emissions}',
    ha='left',
    va='center',
    fontsize=12,
    color='black',
)


# LEGEND ####################

axes[0].legend(
    loc='upper right',
    frameon = False
)
axes[1].legend(
    loc='upper right',
    frameon = False
)

# ANNOTATIONS ################

axes[0].text(
    x=0.25,
    y=0.1,
    s=r"GTP$_{20}=$C/D",
    ha='left',
    va='center',
    fontsize=12,
    color='black',
    transform=axes[0].transAxes
)
axes[0].text(
    x=0.25,
    y=0.2,
    s=r"GWP$_{20}=$A/B",
    ha='left',
    va='center',
    fontsize=12,
    color='black',
    transform=axes[0].transAxes
)

# EXPORT #########################################

figure_name: str = str(Path.cwd().stem + '.pdf')

plt.savefig(
    fname = figure_name,
    format="pdf",
    bbox_inches='tight',
    transparent = False
)
# %%
