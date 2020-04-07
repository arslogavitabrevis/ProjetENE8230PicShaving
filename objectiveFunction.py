import pulp as plp
from parameters import (
    M, Mrange, T, numberOfYear, deltaT, Mbound, Ckw, CkWh, Cpv, Cpvop, Cbat, Cbatop)
from decisionVariables import (
    Npv, Nbat, Pgridmax, Pgrid, Pbdc, Pfac)

periodIn30Days = int(30*24/deltaT)

# Initial cost and solar panel operation cost
objFct = plp.lpSum(
    Npv*(Cpv+numberOfYear*Cpvop)
    + Nbat*Cbat)

# Cost from the first year invoiced power
objFct.update(plp.lpSum(
    Pfac[m-1]*Ckw*Mrange[m-1]/periodIn30Days
    for m in M[:12]))

# Cost from others years invoiced power
objFct.update(plp.lpSum(
    ((numberOfYear-1)/2)*Pfac[m-1]*Ckw*Mrange[m-1]/periodIn30Days
    for m in M[12:]))

# Energy from grid and battery operation cost first year
objFct.update(plp.lpSum(
    deltaT*(Pgrid[t]*CkWh + Pbdc[t]*Cbatop)
    for t in T[:Mbound[12]]))

# Energy from grid and battery operation cost others years
objFct.update(plp.lpSum(
    ((numberOfYear-1)/(len(M)/12))*deltaT*(Pgrid[t]*CkWh + Pbdc[t]*Cbatop)
    for t in T[Mbound[12]:]))
