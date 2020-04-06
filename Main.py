import pulp as plp
import numpy as np
from constraints import constraints

# Initialisation du problème d'optimisation
picShavingProb = plp.LpProblem(name="PicShavingProblem", sense=plp.LpMinimize)

for c in constraints:
    picShavingProb.addConstraint(c)

picShavingProb.writeLP("PicShavingProblem.txt")
