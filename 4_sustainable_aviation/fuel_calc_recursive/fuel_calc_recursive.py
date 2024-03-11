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

oew =  55912.87 # kg
pax = 177
paxweight = 110 # kg
distance = 6654 # km

density_fuel = 0.8 # kg/l

total_fuel_mass = 0 # kg, initialization
total_mass = 0 # kg, initialization


def calculate_total_fuel_mass(
    total_mass: float,
    distance: float,
) -> float:
    """
    See also:
    https://zenodo.org/record/8059751
    “Supplementary data 1.xlsb”, sheet "Aircraft specs", row 84
    and, for the original idea:
    https://data.mendeley.com/datasets/2psysvvfg8/2/files/0506d2d8-8ca0-4c03-966f-57e9b7c2d90d
    """
    a_cruise = 0.0000585830319747814
    b_cruise = 0.97618365400094
    c_cruise = 0.783563064133963
    m_fuel_cruise = (a_cruise * (total_mass ** b_cruise) +  c_cruise) * distance
    
    a_toldg = 0.0904737898235621
    b_toldg = 0.850276475663708
    m_fuel_toldg = a_toldg * (total_mass ** b_toldg)

    a_clbdsc = 1.14401077847832
    b_clbdsc = 0.537401800486297
    m_fuel_clbdsc = a_clbdsc * (total_mass ** b_clbdsc)

    holding_speed = 800
    holding_time = 45/60
    m_reserve = (holding_speed * holding_time) * (m_fuel_cruise / distance)

    return m_fuel_cruise + m_fuel_toldg + m_fuel_clbdsc + m_reserve


def calculate_operating_weight(
    total_fuel_mass: float,
    pax: int,
    paxweight: int,
    oew: int
) -> float:
    """
    See also:
    https://zenodo.org/record/8059751
    “Supplementary data 1.xlsb”, sheet "Scenarios", cell AG8
    """
    return oew + (pax * paxweight) + total_fuel_mass
    

def calculate_fuel_per_100_pax_km(
    total_fuel_mass: float,
    distance: float,
    pax: int
) -> float:
    total_fuel_volume = total_fuel_mass / density_fuel
    return (total_fuel_volume / (distance * pax)) * 100


list_total_fuel_mass = []
list_fuel_per_100_pax_km = []

for x in range(10):
    total_mass = calculate_operating_weight(
        total_fuel_mass = total_fuel_mass,
        pax = pax,
        paxweight = paxweight,
        oew = oew
    )
    total_fuel_mass = calculate_total_fuel_mass(
        total_mass = total_mass,
        distance = distance,
    )
    fuel_per_100_pax = calculate_fuel_per_100_pax_km(
        total_fuel_mass = total_fuel_mass,
        distance = distance,
        pax = pax
    )
    list_total_fuel_mass.append(total_fuel_mass)
    list_fuel_per_100_pax_km.append(fuel_per_100_pax)

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

#ax.set_xlim(500, 12500)
#ax.set_ylim(0, 150)

# TICKS AND LABELS ###########

ax.minorticks_on()
ax.tick_params(axis='x', which='minor', bottom=True)

# GRIDS ######################

ax.grid(which='major', axis='y', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='y', linestyle=':', linewidth = 0.5)
ax.grid(which='major', axis='x', linestyle='-', linewidth = 0.5)
ax.grid(which='minor', axis='x', linestyle=':', linewidth = 0.5)

# axes[0]IS LABELS ################

ax.set_xlabel('Iterations [1]')
ax.set_ylabel("Fuel Mass [kg]")

# PLOTTING ###################

ax.plot(
    np.arange(0, len(list_total_fuel_mass), 1),
    list_total_fuel_mass,
    color = 'black',
    marker = 'o',
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