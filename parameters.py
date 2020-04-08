import numpy as np
from calendar import monthrange
from math import floor

# region #Sets definition
deltaT = 0.25  # hours (everything should be in kWh)
M = np.arange(1, 24+1)  # Month

Mrange = [int((monthrange(2015+floor(m/12), (m-1) % 12+1)[1])*24/deltaT)
          for m in M]   # Range of each month

Mbound = [1] + [sum(Mrange[0:m]) for m in M]
T = np.arange(0, sum(Mrange)+1)  # Time of the year for each 15 min
# endregion

# region #Parameter definition
# To be changed
Ppv = np.loadtxt("ProjetENE8230PicShaving/Data/PVpwr.txt")  # kW To be changed

Npv_max = 13404 #2020-04-07
Nbat_max = 100000  # There is no real limit but money

Cap_bat = 5.62  # [kWh]
ETAbat_ch = 0.72  
ETAbat_dc = 1
ETA_inv = 0.9  

Pbat_ch_max = 2.53  # [kW/batterie]
Pbat_dc_max = 2.53  # [kW/batterie]
Omega = 10000  # Maximum power athorized [kW]
omega = 5000  # Minimum invoiced power [kW]

D = np.loadtxt("ProjetENE8230PicShaving/Data/Data1.csv", skiprows=1)  # kW

# Cost
Ckw = 13.26  # $/kW
CkWh = 0.0346  # $/kWh
Cbat = 549*Cap_bat  # $/battery
Cbatop = 4.5  # $/battery/kWh
Cpv = 996  # $/panel
Cpvop =  4.16 # $/panel-year

# Simulation
numberOfYear = 20
# endregion
