import pulp as plp
import numpy as np
from constraints import constraints
from objectiveFunction import objFct

# Initialisation du problème d'optimisation
picShavingProb = plp.LpProblem(name="PicShavingProblem", sense=plp.LpMinimize)

for c in constraints:
    picShavingProb.addConstraint(c)

picShavingProb.setObjective(objFct)

picShavingProb.writeLP("PicShavingProblem.txt")

picShavingProb.solve()

# Check results
print("Status:", plp.LpStatus[picShavingProb.status])
print("Cout ={:,.2f} ".format(plp.value(picShavingProb.objective)))

with open("VariableValue.txt", 'w') as f:
    f.writelines(list(map(lambda v: "{} = {:,.1f}\n".format(v.name, v.varValue),
                          picShavingProb.variables())))
