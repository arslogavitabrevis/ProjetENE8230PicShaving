import numpy as np
from calendar import monthrange
from math import floor

# region #Sets definition
deltaT = 0.25 # hours (everything should be in kWh)
M = np.arange(1, 24+1)  # Month

Mrange = [int((monthrange(2015+floor(m/12), (m-1)%12+1)[1])*24/deltaT) for m in M]   # Range of each month

Mbound = [1] + [sum(Mrange[0:m]) for m in M]
T = np.arange(0,sum(Mrange)+1)  # Time of the year for each 15 min
# endregion

# region #Parameter definition
# To be changed
Ppv = np.ones(len(T))*400  #in kWh To be changed
Npv_max = 1000  # To be changed
Cap_bat = 2  # To be changed
ETAbat_ch = 0.8  # To be changed
ETAbat_dc = 0.8
ETA_inv = 0.6 #To be changed

Pbat_ch_max = 200  # To be changed
Pbat_dc_max = 200  # To be changed
Omega = 10000 #Maximum power athorized
D = np.loadtxt("ProjetENE8230PicShaving/Data/Data1.csv",skiprows=1) #kW

#Cost
Ckw = 13.26 #$/kW
CkWh = 0.0346 #$/kWh
Cbat = 100 #$/battery
Cbatop = 20 #$/battery/kWh
Cpv = 100 #$/panel To be changed
Cpvop = 3 #$/panel/year To be changed

#Simulation
numberOfYear = 20 #To be changed
# endregion
