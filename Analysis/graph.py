from sys import path
import matplotlib.pyplot as plt
import os
import numpy as np
path.append(".")
from ProjetENE8230PicShaving.parameters import Pbat_ch_max,ETAbat_ch

def generateGraph():

    txtFileNames = os.listdir("./ProjetENE8230PicShaving/Results")
    for s in ["AllVariableValue.txt", "GeneralInfo.txt", "desktop.ini"]:
        try:
            txtFileNames.remove(s)
        finally:
            pass

    Dvar = {txtFileName.split(".")[0]:
            np.loadtxt(
                "./ProjetENE8230PicShaving/Results/{}".format(txtFileName), skiprows=1)
            for txtFileName in txtFileNames}

    for varName in Dvar.keys():
        plt.plot(Dvar[varName])
        plt.title(varName)
        plt.savefig(
            "./ProjetENE8230PicShaving/Analysis/{}.png".format(varName))
        plt.close()

    for varName in ["Ppv_bat", "Pbdc", "Ebat"]:
        plt.plot(np.linspace(0, (len(Dvar[varName])/4), len(Dvar[varName])),
                 Dvar[varName], label=varName)

    plt.plot(np.linspace(0, (len(Dvar["Ppv_bat"])/4), len(Dvar["Ppv_bat"])),
             np.ones(len(Dvar["Ppv_bat"]))*Pbat_ch_max*Dvar["Nbat"]/ETAbat_ch, label="Pbat_ch_max avec eff")
    plt.title("Comportement des batteries")
    plt.ylabel("Heures")
    plt.xlabel("kW/kWh")
    plt.legend()
    plt.savefig("./ProjetENE8230PicShaving/Analysis/ComportementBatteries.png")
    plt.close()


generateGraph()
