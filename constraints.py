import pulp as plp
import numpy as np
from parameters import (
    T, M, Cap_bat, ETAbat_ch, ETAbat_dc, ETA_inv, Pbat_ch_max, Pbat_dc_max, deltaT, Mbound, Omega, Ppv, D)
from decisionVariables import (
    Ppv_bat, Ppv_load, Ppv_gen, Nbat, Pbdc, Ebat, Pgrid, Pgridmax, Npv)

# region # Definition des contraintes
constraints = []
# Solar power distribution to load and batteries
for t in T[1:]:
    constraints.append(
        plp.LpConstraint(
            name="PvPowerDist_{}".format(t),
            e=plp.LpAffineExpression(
                [(Ppv_bat[t], 1), (Ppv_load[t], 1), (Ppv_gen[t], -1)]),
            sense=plp.LpConstraintLE,
            rhs=0))

# Maximum batteries capacity
for t in T[1:]:
    constraints.append(
        plp.LpConstraint(
            name="BatCapacity_{:5d}".format(t),
            e=plp.LpAffineExpression(
                [(Pbdc[t], ETAbat_ch), (Nbat, -Cap_bat), (Ebat[t-1], 1)]),
            sense=plp.LpConstraintLE,
            rhs=0))

# Maximum charging power
for t in T[1:]:
    constraints.append(
        plp.LpConstraint(
            name="BatChargingPower_{:5d}".format(t),
            e=plp.LpAffineExpression(
                [(Ppv_bat[t], ETAbat_ch), (Nbat, -Pbat_ch_max)]),
            sense=plp.LpConstraintLE,
            rhs=0))

# Available energy in the batteries
for t in T[1:]:
    constraints.append(
        plp.LpConstraint(
            name="BatAvailableEnergy_{:5d}".format(t),
            e=plp.LpAffineExpression(
                [(Pbdc[t], deltaT), (Ebat[t-1], -1)]),
            sense=plp.LpConstraintLE,
            rhs=0))

# Battery maximum discharge power
for t in T[1:]:
    constraints.append(
        plp.LpConstraint(
            name="BatMaxDischargePower_{:5d}".format(t),
            e=plp.LpAffineExpression(
                [(Pbdc[t], 1), (Nbat, -Pbat_dc_max)]),
            sense=plp.LpConstraintLE,
            rhs=0))

# Mimimun power invoice from winter month
for m in M:
    months = np.arange(m-12+len(M), m+len(M)) % len(M) + 1
    conditions = np.array([months % 12 == 1, months % 12 ==
                           2, months % 12 == 3, months % 12 == 12]).transpose()
    Mwinter = np.select(
        np.array([(months-1) % 12+1 == 1, (months-1) % 12+1 == 2, (months-1) % 12+1 == 3, (months-1) % 12+1 == 12]).transpose(), months)
    for mw in Mwinter:
        if mw != m:  # Avoid adding unuseful constraint for the actual month
            for t in range(Mbound[mw-1], Mbound[mw]):
                constraints.append(
                    plp.LpConstraint(
                        name="MinPowerInvoiceWint_m{:2d}_mw{:2d}_t{:5d}".format(
                            m, mw, t),
                        e=plp.LpAffineExpression(
                            [(Pgridmax[m-1], 1), (Pgrid[t], -0.75)]),
                        sense=plp.LpConstraintGE,
                        rhs=0))

# Minimum invoiced power from month power
for m in M:
    for t in range(Mbound[m-1], Mbound[m]):
        constraints.append(
            plp.LpConstraint(
                name="MinPowerInvoiceActualMont_m{:2d}_t{:5d}".format(m, t),
                e=plp.LpAffineExpression(
                    [(Pgridmax[m-1], 1), (Pgrid[t], -1)]),
                sense=plp.LpConstraintGE,
                rhs=0))

# Solar power generation
for t in T[1:]:
    constraints.append(
        plp.LpConstraint(
            name="GeneratedPvPower_{:5d}".format(t),
            e=plp.LpAffineExpression(
                [(Ppv_gen[t], 1), (Npv, -1)]),
            sense=plp.LpConstraintEQ,
            rhs=0))

# Energy in the battery
for t in T[1:]:
    constraints.append(
        plp.LpConstraint(
            name="BatteryEnergy_{:5d}".format(t),
            e=plp.LpAffineExpression(
                [(Ebat[t], 1), (Ebat[t-1], -1), (Ppv_bat[t], -ETAbat_ch*deltaT), (Pbdc[t], deltaT)]),
            sense=plp.LpConstraintEQ,
            rhs=0))

# Power from the grid
for t in T[1:]:
    constraints.append(
        plp.LpConstraint(
            name="BatteryEnergy_{:5d}".format(t),
            e=plp.LpAffineExpression(
                [(Pgrid[t], 1), (D[t], -1), (Ppv_load[t], ETA_inv), (Pbdc[t], ETAbat_dc*ETA_inv)]),
            sense=plp.LpConstraintEQ,
            rhs=0))

# Initial energy in the battery charge (must include Nbat if Ebat[0] != 0)
constraints.append(
    plp.LpConstraint(
        name="BatteryInitialEnergy_{:5d}".format(t),
        e=plp.LpAffineExpression(
            [(Ebat[0], 1)]),
        sense=plp.LpConstraintEQ,
        rhs=0))

# endregion
