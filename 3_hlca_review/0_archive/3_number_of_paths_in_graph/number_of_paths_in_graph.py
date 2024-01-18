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
import math

# type hints
from typing import Tuple

# i/o
from pathlib import PurePath, Path

# SETUP #########################################

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Arial",
    "font.sans-serif": "Computer Modern",
    'font.size': 10
})

# DATA GENERATION ################################

def number_of_paths_two_nodes_graph_theory(n, l) -> int:
    '''
    Returns the number of paths of length l
    associated with an input-output-table with n sectors.
    Compare: https://math.stackexchange.com/a/4704603/
    '''
    result: int = 0
    for k in range(n-l-1, n-2+1): # mathematically: k=[n-l-1, n-2]
        if n-l >0:
            result += math.factorial(n-2) // math.factorial(k) # integer division to avoid overflow error
        else:
            result += 0
    return result


def number_of_paths_all_nodes_graph_theory(n) -> int:
    '''
    Returns the number of paths of length l
    associated with an input-output-table with n sectors.
    Compare: https://math.stackexchange.com/a/4704603/
    '''
    result: int = 0
    for k in range(0, n-2+1): # mathematically: k=[0, n-2]
        if n-2 > 0:
            result += math.factorial(n) // math.factorial(k) # integer division to avoid overflow error
        else:
            result += 0
    return result


def number_of_paths_two_nodes_power_series(n, omega) -> int:
    '''
    Returns the number of omega-order paths
    associated with an input-output-table with n sectors.
    Compare: https://doi.org/10.1017/9781108676212, Section 8.5.1
    '''
    return n**(omega-1)


def number_of_paths_all_nodes_power_series(n, omega) -> int:
    '''
    Returns the number of omega-order paths
    associated with an input-output-table with n sectors.
    Compare: https://doi.org/10.1017/9781108676212, Section 8.5.1
    '''
    return n**(omega+1)


def create_dataframe_number_of_paths(
        n_max: int = 50,
        param_max: int = 10,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    '''
    Creates a dataframe with the number of paths
    for all combinations of n and omega or l.
    '''

    df_two_nodes_power_series = pd.DataFrame()
    df_two_nodes_graph_theory = pd.DataFrame()
    
    df_all_nodes_power_series = pd.DataFrame()
    df_all_nodes_graph_theory = pd.DataFrame()

    index_series = pd.Series(range(1, n_max+1))

    df_two_nodes_power_series.index = index_series
    df_two_nodes_graph_theory.index = index_series

    df_all_nodes_power_series.index = index_series
    df_all_nodes_graph_theory.index = index_series
    
    for param in range(1, param_max):
        column_two_nodes_power_series = pd.Series()
        column_two_nodes_graph_theory = pd.Series()

        column_all_nodes_power_series = pd.Series()
        column_all_nodes_graph_theory = pd.Series()

        for n in index_series:
            column_two_nodes_power_series.loc[n]=number_of_paths_two_nodes_power_series(n, param)
            column_two_nodes_graph_theory.loc[n]=number_of_paths_two_nodes_graph_theory(n, param)

            column_all_nodes_graph_theory.loc[n]=number_of_paths_all_nodes_graph_theory(n)
            column_all_nodes_power_series.loc[n]=number_of_paths_all_nodes_power_series(n, param)
        df_two_nodes_power_series[param]=column_two_nodes_power_series
        df_two_nodes_graph_theory[param]=column_two_nodes_graph_theory
        df_all_nodes_power_series[param]=column_all_nodes_power_series
        df_all_nodes_graph_theory[param]=column_all_nodes_graph_theory

    return df_two_nodes_power_series, df_two_nodes_graph_theory, df_all_nodes_power_series, df_all_nodes_graph_theory

df_two_nodes_power_series, df_two_nodes_graph_theory, df_all_nodes_power_series, df_all_nodes_graph_theory = create_dataframe_number_of_paths()

# DATA MANIPULATION #############################

df_two_nodes_graph_theory = df_two_nodes_graph_theory.replace(0, np.nan)
df_all_nodes_graph_theory = df_all_nodes_graph_theory.replace(0, np.nan)

# FIGURE ########################################

# SETUP ######################

fig, ax = plt.subplots(
        num = 'main',
        nrows = 1,
        ncols = 1,
        sharey=True,
        dpi = 300,
        figsize=(15.5*cm, 6*cm), # A4=(210x297)mm
    )

# DATA #######################

# AXIS SCALE #################

ax.set_yscale('log')

# AXIS LIMITS ################

ax.set_ylim(0, 1E20)
ax.set_xlim(0,300)

# TICKS AND LABELS ###########

ax.tick_params(axis='y', which='both', bottom=False)
ax.tick_params(axis='x', which='both', bottom=False)

# GRIDS ######################

ax.grid(True, which='both', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(True, which='both', axis='x', linestyle='-', linewidth = 0.5)

ax.minorticks_on()

# AXIS LABELS ################

ax.set_ylabel("Number of Paths $(p)$")
ax.set_xlabel("Number of Sectors $(n)$")

# PLOTTING ###################

ax.plot(
    df_two_nodes_power_series.index,
    df_two_nodes_power_series[2],
    color = 'black',
    linewidth = 1,
    linestyle = 'solid',
    label = '$\omega=2$'
)
ax.plot(
    df_two_nodes_power_series.index,
    df_two_nodes_power_series[4],
    color = 'black',
    linewidth = 1,
    linestyle = 'dashdot',
    label = '$\omega=4$'
)
ax.plot(
    df_two_nodes_power_series.index,
    df_two_nodes_power_series[6],
    color = 'black',
    linewidth = 1,
    linestyle = 'dashed',
    label = '$\omega=6$'
)
ax.plot(
    df_two_nodes_power_series.index,
    df_two_nodes_power_series[8],
    color = 'black',
    linewidth = 1,
    linestyle = 'dotted',
    label = '$\omega=8$'
)

ax.plot(
    df_two_nodes_graph_theory.index,
    df_two_nodes_graph_theory[2],
    color = 'blue',
    linewidth = 1,
    linestyle = 'solid',
    label = '$l=2$'
)
ax.plot(
    df_two_nodes_graph_theory.index,
    df_two_nodes_graph_theory[4],
    color = 'blue',
    linewidth = 1,
    linestyle = 'dashdot',
    label = '$l=4$'
)
ax.plot(
    df_two_nodes_graph_theory.index,
    df_two_nodes_graph_theory[6],
    color = 'blue',
    linewidth = 1,
    linestyle = 'dashed',
    label = '$l=6$'
)
ax.plot(
    df_two_nodes_graph_theory.index,
    df_two_nodes_graph_theory[8],
    color = 'blue',
    linewidth = 1,
    linestyle = 'dotted',
    label = '$l=8$'
)

# LEGEND ####################

ax.legend(
    loc = 'upper right',
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

# %%

# %%