from sys import path
path.append(".")
from os import listdir
from Model.parameters import Pbat_ch_max,ETAbat_ch
from Model.constraints import constraints
import matplotlib.pyplot as plt
import numpy as np


def generateGraph():

    txtFileNames = listdir("./Results")
    for s in ["AllVariableValue.txt", "GeneralInfo.txt", "desktop.ini","Duals"]:
        try:
            txtFileNames.remove(s)
        except ValueError:
            pass

    Dvar = {txtFileName.split(".")[0]:
            np.loadtxt(
                "./Results/{}".format(txtFileName), skiprows=1)
            for txtFileName in txtFileNames}

    for varName in Dvar.keys():
        plt.plot(Dvar[varName])
        plt.title(varName)
        plt.savefig(
            "./Analysis/{}.png".format(varName))
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
    plt.savefig("./Analysis/ComportementBatteries.png")
    plt.close()

def generateDualGraph():

    txtFileNames = listdir("./Results/Duals")
    for s in ["desktop.ini"]:
        try:
            txtFileNames.remove(s)
        except ValueError:
            pass

    Dvar = {txtFileName.split(".")[0]:
            np.loadtxt(
                "./Results/Duals/{}".format(txtFileName), skiprows=1)
            for txtFileName in txtFileNames}

    for varName in Dvar.keys():
        plt.plot(Dvar[varName])
        plt.title("{}\n{}".format(varName,str(constraints[varName][0])))
        plt.xlabel("Intervalle")
        if varName in ["BatAvailableEnergy","BatCapacity","BatteryEnergy","BatteryInitialEnergy"]:
            plt.ylabel("$/kWh")
        else:
            plt.ylabel("$/kW")
        plt.savefig(
            "./Analysis/Duals/{}.png".format(varName))
        plt.close()

generateGraph()
generateDualGraph()
