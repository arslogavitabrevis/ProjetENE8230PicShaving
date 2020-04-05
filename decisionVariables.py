import pulp as plp
from parameters import T, M, Npv_max

# region # Decision variables:

# Number of solar panel
Npv = plp.LpVariable(
    cat=plp.LpInteger,
    lowBound=0,
    upBound=Npv_max,
    name="Npv")

# Number of batteries
Nbat = plp.LpVariable(
    cat=plp.LpInteger,
    lowBound=0,
    name="Nbat")

# Power from PV stored in the batteries
Ppv_bat = [plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=0,
    name="Ppv_bat_{}".format(t))
    for t in T]

# Power from PV dedicated transfered to load
Ppv_load = [plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=0,
    name="Ppv_load_{}".format(t))
    for t in T]

# Discharged power from batteries
Pbdc = [plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=0,
    name="Pbdc_{}".format(t))
    for t in T]

# Invoice power
Pgridmax = [plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=0,
    name="Pgridmax_{}".format(m))
    for m in M]

# Minimum power invoice
Pfacmin = plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=0,
    name="Pfacmin")

# Power generated from all solar panel
Ppv_gen = [plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=0,
    name="Ppv_gen_{}".format(t))
    for t in T]

# Energy stored in the batteries
Ebat = [plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=0,
    name="Ebat_{}".format(t))
    for t in T]

# Power from the network
Pgrid = [plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=0,
    name="Pgrid_{}".format(t))
    for t in T]
# endregion
