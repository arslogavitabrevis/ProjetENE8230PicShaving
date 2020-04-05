import numpy as np
from calendar import monthrange
from math import floor

#region #Sets definition
M = np.arange(1,24) #Month

Mrange = [1] #Range of each month
for m in M:
    Mrange.append(sum(Mrange)+monthrange(2015+floor(m/12),m%12))

T = np.arrange(sum(Mrange)) #Time of the year for each 15 min
# endregion

# region #Parameter definition
Ppv = np.one(len(T))*400
Npv_max = 1000

# endregion