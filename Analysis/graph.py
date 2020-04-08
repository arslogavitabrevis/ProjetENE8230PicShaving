import matplotlib.pyplot as plt
import os
import numpy as np

def generateGraph():
    txtFileNames = os.listdir("./Results")
    variables = {}
    for s in ["AllVariableValue.txt","GeneralInfo.txt","desktop.ini"]:
        txtFileNames.remove(s)

    for txtFileName in txtFileNames:
        plt.plot(np.loadtxt("./Results/{}".format(txtFileName),skiprows=1))
        plt.title(txtFileName.split(".")[0])
        plt.savefig("./ProjetENE8230PicShaving/Analysis/{}.png".format(txtFileName.split(".")[0]))
        plt.close()


    for txtFileName in ["Ppv_bat.txt","Pbdc.txt","Ebat.txt"]:
        varVal = np.loadtxt("./Results/{}".format(txtFileName),skiprows=1)
        plt.plot(np.linspace(0,(len(varVal)/4),len(varVal)),varVal,label=txtFileName.split(".")[0])
        
    plt.title("Comportement des batteries")
    plt.legend()
    plt.savefig("./ProjetENE8230PicShaving/Analysis/ComportementBatteries.png")
    plt.close()

generateGraph()