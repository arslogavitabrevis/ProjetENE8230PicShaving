import numpy as np

D = np.loadtxt("ProjetENE8230PicShaving/Data/Data1.csv",skiprows=1) #kW

np.savetxt("firstweek.txt", np.average(D[:24*24*4+1])*np.ones(7*24*4))