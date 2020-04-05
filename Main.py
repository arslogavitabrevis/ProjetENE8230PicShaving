import pulp as plp
import numpy as np
from constraints import constraints

# Initialisation du problème d'optimisation
picShavingProb = plp.LpProblem(name="PicShavingProblem", sense=plp.LpMinimize)

picShavingProb.writeLp("PicShavingProblem.txt")
