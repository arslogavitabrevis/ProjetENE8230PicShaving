import numpy as np
from calendar import monthrange
from math import floor

#region #Sets definition
M = np.arange(1,24) #Month

Mrange = [1] #Range of each month
for m in M:
    Mrange.append(sum(Mrange)+monthrange(2015+floor(m/12),m%12))

T = np.arrange(sum(Mrange)) #Time of the year for each 15 min
deltaT = 0.25 #hours (everything should be in kWh)
# endregion

# region #Parameter definition
#To be changed
Ppv = np.one(len(T))*400 #To be changed 
Npv_max = 1000 #To be changed
Cap_bat = 2 #To be changed
ETAbat_ch = 0.8 #To be changed
Pbat_ch_max = 200 #To be changed
Pbat_dc_max = 200 #To be changed


# endregion