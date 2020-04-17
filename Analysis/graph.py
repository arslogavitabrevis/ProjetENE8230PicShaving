from sys import path
path.append(".")
from os import listdir
from Model.parameters import Pbat_ch_max,ETAbat_ch, Cap_bat
import matplotlib.pyplot as plt
import numpy as np


def generateGraph():

    txtFileNames = listdir("./ResultsNoLimit")
    for s in ["AllVariableValue.txt", "GeneralInfo.txt", "desktop.ini"]:
        try:
            txtFileNames.remove(s)
        except ValueError:
            pass

    Dvar = {txtFileName.split(".")[0]:
            np.loadtxt(
                "./ResultsNoLimit/{}".format(txtFileName), skiprows=1)
            for txtFileName in txtFileNames}

    for varName in Dvar.keys():
        plt.plot(Dvar[varName])
        plt.title(varName)
        plt.savefig(
            "./AnalysisNoLimit/{}.png".format(varName))
        plt.close()

    for varName in ["Ppv_bat", "Pbdc", "Ebat"]:
        plt.plot(np.linspace(0, (len(Dvar[varName])/4), len(Dvar[varName])),
                 Dvar[varName], label=varName)

    plt.plot(np.linspace(0, (len(Dvar["Ppv_bat"])/4), len(Dvar["Ppv_bat"])),
             np.ones(len(Dvar["Ppv_bat"]))*Pbat_ch_max*Dvar["Nbat"]/ETAbat_ch, label="Pbat_ch_max avec eff")
    plt.title("Comportement des batteries")
    plt.xlabel("Heures")
    plt.ylabel("kW/kWh")
    plt.legend()
    plt.savefig("./AnalysisNoLimit/ComportementBatteries.png")
    plt.close()

    plt.plot(np.linspace(0, (len(Dvar["Ebat"])/4), len(Dvar["Ebat"])),
    ((Dvar["Ebat"]/(np.ones(len(Dvar["Ebat"]))*Cap_bat*Dvar["Nbat"]))*0.8)+0.2)

    plt.title("Niveau de charge des batteries")
    plt.xlabel("Heures")
    plt.ylabel("SOC")
    plt.grid(True)
    plt.savefig("./AnalysisNoLimit/NiveauChargeBatteries.png")
    plt.close()


generateGraph()
