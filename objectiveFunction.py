import pulp as plp
from parameters import (
    M, Mrange, T, numberOfYear, deltaT, Mbound, Ckw, CkWh, Cpv, Cpvop, Cbat, Cbatop)
from decisionVariables import (
    Npv, Nbat, Pgridmax, Pgrid, Pbdc)

periodIn30Days = int(30*24/deltaT)

#Initial cost and solar panel operation cost
objFct = plp.lpSum(
    Npv*(Cpv+numberOfYear*Cpvop)
    + Nbat*Cbat)

#Power from grid cost
objFct.update(plp.lpSum(
    (numberOfYear/(len(M)/12))*Pgridmax[m-1]*Ckw*Mrange[m-1]/periodIn30Days
    for m in M))

#Energy from grid and battery operation cost
objFct.update(plp.lpSum(
    (numberOfYear/(len(M)/12))*deltaT*(Pgrid[t]*CkWh + Pbdc[t]*Cbatop)
    for t in T[1:]))
