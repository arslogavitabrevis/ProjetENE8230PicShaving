import pulp as plp
import numpy as np
from parameters import (
    T, M, Cap_bat, ETAbat_ch, ETAbat_dc, ETA_inv, Pbat_ch_max, Pbat_dc_max, deltaT, Mbound, Omega, Ppv, D)
from decisionVariables import (
    Ppv_bat, Ppv_load, Ppv_gen, Nbat, Pbdc, Ebat, Pgrid, Pgridmax, Npv)

# region # Definition des contraintes
constraints = []

# Solar power distribution to load and batteries
constraints.extend(list(map(lambda t:
    plp.LpConstraint(
        name="PvPowerDist_{}".format(t),
        e=plp.LpAffineExpression(
            [(Ppv_bat[t], 1), (Ppv_load[t], 1), (Ppv_gen[t], -1)]),
        sense=plp.LpConstraintLE,
        rhs=0), T[1:])))

# Maximum batteries capacity
constraints.extend(list(map(lambda t:
    plp.LpConstraint(
        name="BatCapacity_{:5d}".format(t),
        e=plp.LpAffineExpression(
            [(Pbdc[t], ETAbat_ch), (Nbat, -Cap_bat), (Ebat[t-1], 1)]),
        sense=plp.LpConstraintLE,
        rhs=0), T[1:])))

# Maximum charging power
constraints.extend(list(map(lambda t:
    plp.LpConstraint(
        name="BatChargingPower_{:5d}".format(t),
        e=plp.LpAffineExpression(
            [(Ppv_bat[t], ETAbat_ch), (Nbat, -Pbat_ch_max)]),
        sense=plp.LpConstraintLE,
        rhs=0), T[1:])))

# Available energy in the batteries
constraints.extend(list(map(lambda t:
    plp.LpConstraint(
        name="BatAvailableEnergy_{:5d}".format(t),
        e=plp.LpAffineExpression(
            [(Pbdc[t], deltaT), (Ebat[t-1], -1)]),
        sense=plp.LpConstraintLE,
        rhs=0), T[1:])))

# Battery maximum discharge power
constraints.extend(list(map(lambda t:
    plp.LpConstraint(
        name="BatMaxDischargePower_{:5d}".format(t),
        e=plp.LpAffineExpression(
            [(Pbdc[t], 1), (Nbat, -Pbat_dc_max)]),
        sense=plp.LpConstraintLE,
        rhs=0), T[1:])))

# Mimimun power invoice from winter month
for m in M:
    months = np.arange(m-12+len(M), m+len(M)) % len(M) + 1
    conditions = np.array([months % 12 == 1, months % 12 ==
                           2, months % 12 == 3, months % 12 == 12]).transpose()
    Mwinter = np.select(
        np.array([(months-1) % 12+1 == 1, (months-1) % 12+1 == 2, (months-1) % 12+1 == 3, (months-1) % 12+1 == 12]).transpose(), months)
    for mw in Mwinter:
        if mw != m:  # Avoid adding unuseful constraint for the actual month
            constraints.extend([
                plp.LpConstraint(
                    name="MinPowerInvoiceWint_m{:2d}_mw{:2d}_t{:5d}".format(
                        m, mw, t),
                    e=plp.LpAffineExpression(
                        [(Pgridmax[m-1], 1), (Pgrid[t], -0.75)]),
                    sense=plp.LpConstraintGE,
                    rhs=0)for t in range(Mbound[mw-1], Mbound[mw])])

# Minimum invoiced power from month power
for m in M:
    constraints.extend([
        plp.LpConstraint(
            name="MinPowerInvoiceActualMont_m{:2d}_t{:5d}".format(m, t),
            e=plp.LpAffineExpression(
                [(Pgridmax[m-1], 1), (Pgrid[t], -1)]),
            sense=plp.LpConstraintGE,
            rhs=0)
        for t in range(Mbound[m-1], Mbound[m])])

# Solar power generation
constraints.extend(list(map(lambda t:
    plp.LpConstraint(
        name="GeneratedPvPower_{:5d}".format(t),
        e=plp.LpAffineExpression(
            [(Ppv_gen[t], 1), (Npv, -Ppv[t-1])]),
        sense=plp.LpConstraintEQ,
        rhs=0), T[1:])))

# Energy in the battery
constraints.extend(list(map(lambda t:
    plp.LpConstraint(
        name="BatteryEnergy_{:5d}".format(t),
        e=plp.LpAffineExpression(
            [(Ebat[t], 1), (Ebat[t-1], -1), (Ppv_bat[t], -ETAbat_ch*deltaT), (Pbdc[t], deltaT)]),
        sense=plp.LpConstraintEQ,
        rhs=0), T[1:])))

# Power from the grid
constraints.extend(list(map(lambda t:
    plp.LpConstraint(
        name="PowerFromGrid_{:5d}".format(t),
        e=plp.LpAffineExpression(
            [(Pgrid[t], 1), (Ppv_load[t], ETA_inv), (Pbdc[t], ETAbat_dc*ETA_inv)]),
        sense=plp.LpConstraintEQ,
        rhs=D[t-1]), T[1:])))

# Initial energy in the battery charge (must include Nbat if Ebat[0] != 0)
constraints.append(
    plp.LpConstraint(
        name="BatteryInitialEnergy",
        e=plp.LpAffineExpression(
            [(Ebat[0], 1)]),
        sense=plp.LpConstraintEQ,
        rhs=0))

#Value at 0 for the other variables
for var in [Pgrid[0],Pbdc[0],Ppv_bat[0],Ppv_gen[0],Ppv_load[0]]:
    constraints.append(
        plp.LpConstraint(
            name="ValueAt0_{}".format(var.name),
            e=plp.LpAffineExpression(
                [(var, 1)]),
            sense=plp.LpConstraintEQ,
            rhs=0))
# endregion
