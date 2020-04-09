import pulp as plp
from parameters import T, M, Npv_max, Nbat_max, Omega, omega

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
    upBound=Nbat_max,
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

# Maximum power from the grid in this month
Pgridmax = [plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=0,
    upBound=Omega,
    name="Pgridmax_{}".format(m))
    for m in M]

# Power invoice for a month
Pfac = [plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=omega,
    name="Pfac_{}".format(m))
    for m in M]

# Minimum power invoice
Pfacmin = [plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=omega,
    name="Pfacmin_{}".format(m))
    for m in M]

# Power invoice for a month
Pfacfy = [plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=omega,
    name="Pfacfy_{}".format(m))
    for m in M[:12]]

# Minimum power invoice
Pfacminfy = [plp.LpVariable(
    cat=plp.LpContinuous,
    lowBound=omega,
    name="Pfacminfy_{}".format(m))
    for m in M[:12]]

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
    upBound=Omega,
    name="Pgrid_{}".format(t))
    for t in T]

decisionVariables = {"Npv": [Npv], "Nbat": [Nbat], "Ppv_bat": Ppv_bat,
                     "Ppv_load": Ppv_load, "Pbdc": Pbdc, "Pgridmax": Pgridmax,
                     "Pfac": Pfac, "Pfacmin": Pfacmin, "Ppv_gen": Ppv_gen,
                     "Ebat": Ebat, "Pgrid": Pgrid, "Pfacfy": Pfacfy, "Pfacminfy": Pfacminfy}
# endregion

print("Decisions variables defined")
