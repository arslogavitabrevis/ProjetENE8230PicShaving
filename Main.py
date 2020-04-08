import pulp as plp
import numpy as np
from os import path, makedirs
from datetime import datetime
from constraints import constraints
from objectiveFunction import objFct
from decisionVariables import decisionVariables

# Initialisation du problème d'optimisation
picShavingProb = plp.LpProblem(name="PicShavingProblem", sense=plp.LpMinimize)

for c in constraints:
    picShavingProb.addConstraint(c)

picShavingProb.setObjective(objFct)

picShavingProb.writeLP("PicShavingProblem.txt")
picShavingProb.writeMPS("PicShavingProblem.mps")

picShavingProb.solve()

# Check results
print("Status:", plp.LpStatus[picShavingProb.status])
print("Cout ={:,.2f} ".format(plp.value(picShavingProb.objective)))

if not path.exists('./Results'):
    makedirs('Results')

with open("Results/GeneralInfo.txt", 'w') as f:
    f.write("{}\n".format(datetime.now()))
    f.write("Status: {}\n".format(plp.LpStatus[picShavingProb.status]))
    f.write("Cout ={:,.2f}\n".format(plp.value(picShavingProb.objective)))

with open("Results/AllVariableValue.txt", 'w') as f:
    f.writelines(list(map(lambda v: "{} = {:,.1f}\n".format(v.name, v.varValue),
                          picShavingProb.variables())))

varNames = ["Npv", "Nbat", "Ppv_bat", "Ppv_load", "Pbdc", "Pgridmax",
           "Pfac", "Pfacmin", "Ppv_gen", "Ebat", "Pgrid"]

for varName in varNames:
    with open("Results/VariableValue{}.txt".format(varName), 'w') as f:
        f.write("{}\n".format(varName))
        f.writelines(["{} = {:,.1f}\n".format(v.getName(), v.valueOrDefault())
                          for v in decisionVariables[varName]])
