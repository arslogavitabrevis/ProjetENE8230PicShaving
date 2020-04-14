import pulp as plp
import numpy as np
from os import path, makedirs
from datetime import datetime
from Model.constraints import constraints
from Model.objectiveFunction import objFct
from Model.decisionVariables import decisionVariables

# Initialisation of the optimisation problem
picShavingProb = plp.LpProblem(name="PicShavingProblem", sense=plp.LpMinimize)

print("Addind constraints")
for c in constraints:
    picShavingProb.addConstraint(c)

print("Setting objective functions")
picShavingProb.setObjective(objFct)

# print("Output some file representing the model")
# picShavingProb.writeLP("ProjetENE8230PicShaving/Model/PicShavingProblem.txt")
# picShavingProb.writeMPS("ProjetENE8230PicShaving/Model/PicShavingProblem.mps")

print("Solving linear problem")
picShavingProb.solve()

# Check results
print("\nStatus:", plp.LpStatus[picShavingProb.status])
print("Cout ={:,.2f} ".format(plp.value(picShavingProb.objective)))

print("Saving variables values")
if not path.exists('./Results'):
    makedirs('Results')

with open("Results/GeneralInfo.txt", 'w') as f:
    f.write("{}\n".format(datetime.now()))
    f.write("Status: {}\n".format(plp.LpStatus[picShavingProb.status]))
    f.write("Cout ={:,.2f}\n".format(plp.value(picShavingProb.objective)))

with open("Results/AllVariableValue.txt", 'w') as f:
    f.writelines(list(map(lambda v: "{} = {:.1f}\n".format(v.name, v.varValue),
                          picShavingProb.variables())))

for varName in decisionVariables.keys():
    with open("Results/{}.txt".format(varName), 'w') as f:
        f.write("{}\n".format(varName))
        f.writelines(["{:.2f}\n".format(v.valueOrDefault())
                      for v in decisionVariables[varName]])

print("Generating graph")
from Analysis.graph import generateGraph
generateGraph()
