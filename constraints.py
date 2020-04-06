import pulp as plp
import numpy as np
from parameters import (
    T, M, Cap_bat, ETAbat_ch,Pbat_ch_max,Pbat_dc_max,deltaT)
from decisionVariables import (
    Ppv_bat, Ppv_load, Ppv_gen,Nbat,Pbdc,Ebat,Pfacmin)

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
                [(Pbdc[t], ETAbat_ch), (Nbat, -Cap_bat), (Ebat[t-1], 1)]),
            sense=plp.LpConstraintLE,
            rhs=0))

#Maximum charging power
for t in T:
    constraints.append(
        plp.LpConstraint(
            name="BatChargingPower_{}".format(t),
            e=plp.LpAffineExpression(
                [(Ppv_bat[t], ETAbat_ch), (Nbat,-Pbat_ch_max)]),
            sense=plp.LpConstraintLE,
            rhs=0))

#Available energy in the batteries
for t in T:
    constraints.append(
        plp.LpConstraint(
            name="BatAvailableEnergy_{}".format(t),
            e=plp.LpAffineExpression(
                [(Pbdc[t], deltaT), (Ebat[t-1],-1)]),
            sense=plp.LpConstraintLE,
            rhs=0))

#Battery maximum discharge power
for t in T:
    constraints.append(
        plp.LpConstraint(
            name="BatMaxDischargePower_{}".format(t),
            e=plp.LpAffineExpression(
                [(Pbdc[t], 1), (Nbat,-Pbat_dc_max)]),
            sense=plp.LpConstraintLE,
            rhs=0))

#Mimimun power invoice
for m in M:
    months = np.arange(m-11+len(M),m+len(M))%len(M)
    Mwinter = np.select([month%12 == 1,month%12 == 2,month%12 == 3,month%12 == 12], months)
    constraints.append(
        plp.LpConstraint(
            name="MinPowerInvoice_{}".format(m),
            e=plp.LpAffineExpression(
                [(Pfacmin[m], 1)] + [(mw,-Pbat_dc_max) for mw in Mwinter]),
            sense=plp.LpConstraintGE,
            rhs=0))

#endregion