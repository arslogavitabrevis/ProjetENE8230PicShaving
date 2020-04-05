import pulp as plp
from parameters import T, M
from decisionVariables import (
Ppv_bat, Ppv_load, Ppv_gen)

# region # Definition des contraintes

# Solar power distribution to load and batteries
constraints=[]
for t in T:
    constraints.append(
        plp.LpConstraint(
            name="PvPowerDist_{}".format(t),
            e=plp.LpAffineExpression(
                [(Ppv_bat[t], 1), (Ppv_load[t], 1), (Ppv_gen, -1)]),
            sense=plp.LpConstraintLE,
            rhs=0))

# Maximum batteries capacity
for t in T:
    constraints.append(
        plp.LpConstraint(
            name="BatCapacity_{}".format(t),
            e=plp.LpAffineExpression(
                [(Ppv_bat[t], 1), (Ppv_load[t], 1), (Ppv_gen, -1)]),
            sense=plp.LpConstraintLE,
            rhs=0))

