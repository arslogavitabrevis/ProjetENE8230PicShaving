import pulp as plp
from sys import path
path.append(".")
from ProjetENE8230PicShaving.Model.parameters import (
    M, Mrange, T, numberOfYear, deltaT, Mbound, Ckw, CkWh, Cpv, Cpvop, Cbat, Cbatopvar,Cbatopfix)
from ProjetENE8230PicShaving.Model.decisionVariables import (
    Npv, Nbat, Pgridmax, Pgrid, Pbdc, Pfac, Pfacfy)

periodIn30Days = int(30*24/deltaT)

# Initial cost and solar panel operation cost
objFct = plp.lpSum(
    Npv*(Cpv+numberOfYear*Cpvop)
    + Nbat*(Cbat+Cbatopfix))

# Cost from the first year invoiced power
objFct.update(plp.lpSum(
    Pfacfy[m-1]*Ckw*Mrange[m-1]/periodIn30Days
    for m in M[:12]))

# Cost from others years invoiced power
objFct.update(plp.lpSum(
    ((numberOfYear-1)/2)*Pfac[m-1]*Ckw*Mrange[m-1]/periodIn30Days
    for m in M))

# Energy from grid and battery operation cost first year
objFct.update(plp.lpSum(
    deltaT*(Pgrid[t]*CkWh + Pbdc[t]*Cbatopvar)
    for t in T[:Mbound[12]]))

# Energy from grid and battery operation cost others years
objFct.update(plp.lpSum(
    ((numberOfYear-1)/(len(M)/12))*deltaT*(Pgrid[t]*CkWh + Pbdc[t]*Cbatopvar)
    for t in T))

print("Objective function defined")
