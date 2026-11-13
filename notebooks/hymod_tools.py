"""
hymod_tools.py
==============
HyMOD rainfall runoff model and supporting utilities, ported from the original
MATLAB tutorial code (H. V. Gupta, HWR 521, University of Arizona, 2005) to Python
for the CIROH Summer Institute 2026 "Ensemble Forecast Evaluation" series, and
reused in Module 3 of the CUAHSI Water Science Exchange 2026 flash flood workshop.

This module is the engine of the four teaching notebooks. Every function carries a
docstring that says what it computes, and the inner lines carry comments that
explain the hydrology and the numerics behind each step.
"""

# Credit: Humberto Vergara and Mohamed Abdelkader (University of Iowa).
import numpy as np

# ---------------------------------------------------------------------------
# Parameter sets and sampling ranges
# ---------------------------------------------------------------------------
# The original Leaf River tutorial parameters.  NOTE: not well calibrated (the
# tiny Kq over-smooths the hydrograph) -- demonstrated in Notebook 1.
DEFAULT_PARS = {
    "Huz": 64.0949,   # Max height of the soil-moisture accounting tank  [mm]
    "B":   1.6851,    # Shape of the storage-capacity distribution       [0, 2]
    "Alp": 0.5898,    # Quick/slow flow split fraction                   [0, 1]
    "Nq":  3,         # Number of quickflow (Nash) reservoirs            [int >= 1]
    "Kq":  0.0201,    # Quickflow reservoir leakage rate                 [1/day]
    "Ks":  0.0002,    # Slowflow reservoir leakage rate                  [1/day]
}

# Plausible sampling ranges used when we PERTURB parameters (Notebook 2).
PARAM_RANGES = {
    "Huz": (0.0, 100.0), "B": (0.0, 2.0), "Alp": (0.0, 1.0),
    "Kq": (0.0, 1.0), "Ks": (0.0, 1.0),
}

# Calibrated control set found by the Monte-Carlo search in Notebook 1
# (seed 42, 400 samples -> NSE ~ 0.78 over the 5-year window).  Shared by all
# four notebooks so they use one consistent deterministic "best single forecast".
CONTROL_PARS = {
    "Huz": 171.3386, "B": 0.9021, "Alp": 0.5679,
    "Nq": 2, "Kq": 0.6429, "Ks": 0.0559,
}


def load_leaf_river(path="LeafCatch.dat"):
    """Load the 3-column Leaf River file -> PP, PET, QQ arrays (all mm/day).

    column 0 = PP  precipitation (forcing)
    column 1 = PET potential evapotranspiration (atmospheric demand)
    column 2 = QQ  observed streamflow (the 'truth' we verify against)
    """
    raw = np.loadtxt(path)                  # parse scientific-notation columns
    PP = raw[:, 0].astype(float)            # rainfall forcing
    PET = raw[:, 1].astype(float)           # atmospheric demand
    QQ = raw[:, 2].astype(float)            # observed discharge
    return PP, PET, QQ


def pdm_step(Hpar, Bpar, Hbeg, PP, PET):
    """Advance the Probability-Distributed soil-moisture store by ONE time step.

    Designed to convert today's rainfall (PP) and demand (PET) into the
    precipitation EXCESS that becomes runoff and the actual ET, while tracking
    how full the soil store is.  The PDM treats the catchment as many small
    buckets whose capacities follow a distribution set by Bpar, using the
    analytic height<->content relationship instead of simulating each bucket.

    Returns: OV (excess, mm), ET (mm), Hend (end height, mm), Cend (end content, mm).
    """
    if Bpar < 0:
        raise ValueError("B parameter < 0")
    if Bpar > 2:
        raise ValueError("B parameter > 2")
    # Convert bounded shape B in [0,2] to the unbounded exponent b in [0, inf):
    if Bpar == 2:
        b = 1.0e6                                   # B==2 -> ~infinite exponent
    else:
        b = np.log(1.0 - (Bpar / 2.0)) / np.log(0.5)
    Cpar = Hpar / (1.0 + b)                         # max water CONTENT of store
    # Starting content implied by the starting height:
    Cbeg = Cpar * (1.0 - np.power((1.0 - (Hbeg / Hpar)), (1.0 + b)))
    # Saturation-excess overflow OV2 (tank physically overflows):
    OV2 = max(0.0, PP + Hbeg - Hpar)
    PPinf = PP - OV2                                # rain left to infiltrate
    # Intermediate post-infiltration state (height capped at the tank top):
    Hint = min(Hpar, (PPinf + Hbeg))
    Cint = Cpar * (1.0 - np.power((1.0 - (Hint / Hpar)), (1.0 + b)))
    # Capacity-excess runoff OV1 (infiltrated water the buckets cannot hold):
    OV1 = max(0.0, PPinf + Cbeg - Cint)
    OV = OV1 + OV2                                  # total precipitation excess
    # ET is demand-limited (PET) or supply-limited (Cint), whichever is smaller:
    ET = min(PET, Cint)
    Cend = Cint - ET                               # content after ET removed
    # Map final content back to a final height:
    Hend = Hpar * (1.0 - np.power((1.0 - Cend / Cpar), 1.0 / (1.0 + b)))
    return OV, ET, Hend, Cend


def nash_step(K, N, Xbeg, Inp):
    """Advance a Nash cascade of N linear reservoirs by ONE time step.

    Designed to ROUTE a runoff pulse through a chain of leaky tanks in series,
    spreading it out in time into the smooth, lagged shape of a hydrograph limb.
    Each linear tank releases a fraction K of its storage (Out = K*X); stacking N
    of them gives the classic Nash unit hydrograph.

    Returns: Out (outflow of last tank, mm), Xend (end storage of each tank, mm).
    """
    Xbeg = np.atleast_1d(np.asarray(Xbeg, dtype=float))
    OO = np.zeros(N)                               # release from each tank
    Xend = np.zeros(N)                             # end-of-step storage of each
    for res in range(N):
        OO[res] = K * Xbeg[res]                    # tank releases fraction K
        Xend[res] = Xbeg[res] - OO[res]            # what remains after release
        if res == 0:
            Xend[res] += Inp                       # first tank gets external inflow
        else:
            Xend[res] += OO[res - 1]               # others get the tank above's outflow
    Out = OO[N - 1]                                # cascade outflow = last tank
    return Out, Xend


def hymod01(PP, PET, Pars, InState=None):
    """Run the complete HyMOD model over a simulation period.

    Couples ONE soil store (pdm_step) to TWO parallel routing paths: a fast Nash
    cascade of Nq tanks and a single slow tank.  Alp sets the quick fraction of
    the precipitation excess; (1-Alp) is the slow fraction.  Total streamflow Q is
    the sum of the two path outflows.

    PP, PET : forcing arrays for EXACTLY the days to simulate [mm/day].
    Pars    : dict Huz, B, Alp, Nq, Kq, Ks.
    Returns : dict of arrays incl. "Q" (total flow), "Qq", "Qs", "ET", "OV",
              "XCuz" (soil content), "XHuz" (soil height).
    """
    PP = np.asarray(PP, dtype=float)
    PET = np.asarray(PET, dtype=float)
    Hpar = Pars["Huz"]; Bpar = Pars["B"]; Alp = Pars["Alp"]
    Nq = int(Pars["Nq"]); Kq = Pars["Kq"]; Ks = Pars["Ks"]
    # Convert B->b and compute Cpar (needed to seed the soil height):
    if Bpar == 2:
        b = 1.0e6
    else:
        b = np.log(1.0 - (Bpar / 2.0)) / np.log(0.5)
    Cpar = Hpar / (1.0 + b)
    # Initial states (cold start unless InState supplied):
    if InState is None:
        InState = {}
    XCuz = InState.get("XCuz", 0.0)
    XHuz = Hpar * (1.0 - np.power((1.0 - XCuz / Cpar), 1.0 / (1.0 + b)))
    Xq = np.asarray(InState.get("Xq", np.zeros(Nq)), dtype=float)
    Xs = float(InState.get("Xs", 0.0))
    # Output arrays:
    Nday = len(PP)
    OV = np.zeros(Nday); ET = np.zeros(Nday)
    XHuz_o = np.zeros(Nday); XCuz_o = np.zeros(Nday)
    Qq = np.zeros(Nday); Qs = np.zeros(Nday)
    # Time-marching loop:
    for i in range(Nday):
        # (1) soil-moisture accounting: how much rain becomes runoff today
        OV[i], ET[i], XHuz, XCuz = pdm_step(Hpar, Bpar, XHuz, PP[i], PET[i])
        XHuz_o[i] = XHuz; XCuz_o[i] = XCuz
        # (2) route the QUICK fraction through Nq fast tanks
        Qq[i], Xq = nash_step(Kq, Nq, Xq, Alp * OV[i])
        # (3) route the SLOW fraction through 1 slow tank
        Qs_i, Xs_arr = nash_step(Ks, 1, np.array([Xs]), (1.0 - Alp) * OV[i])
        Qs[i] = Qs_i; Xs = Xs_arr[0]
    return {"OV": OV, "ET": ET, "XHuz": XHuz_o, "XCuz": XCuz_o,
            "Qq": Qq, "Qs": Qs, "Q": Qq + Qs}     # Q = quick + slow (forecast)


def rmse(sim, obs):
    """Root-mean-square error: sqrt(mean((sim-obs)^2)) [mm/day]. Lower is better."""
    sim = np.asarray(sim, float); obs = np.asarray(obs, float)
    return float(np.sqrt(np.mean((sim - obs) ** 2)))


def nse(sim, obs):
    """Nash-Sutcliffe Efficiency = 1 - SSE/variance(obs).

    1 = perfect; 0 = no better than predicting the mean flow; <0 = worse.
    """
    sim = np.asarray(sim, float); obs = np.asarray(obs, float)
    denom = np.sum((obs - np.mean(obs)) ** 2)
    return float(1.0 - np.sum((sim - obs) ** 2) / denom)


def kge(sim, obs):
    """Kling-Gupta Efficiency = 1 - sqrt((r-1)^2+(alpha-1)^2+(beta-1)^2).

    r = correlation, alpha = std ratio (variability), beta = mean ratio (bias).
    1 = perfect.
    """
    sim = np.asarray(sim, float); obs = np.asarray(obs, float)
    r = np.corrcoef(sim, obs)[0, 1]
    alpha = np.std(sim) / np.std(obs)
    beta = np.mean(sim) / np.mean(obs)
    return float(1.0 - np.sqrt((r - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2))


def flow_duration_curve(Q):
    """Empirical flow-duration curve.

    Sorts flows descending and assigns exceedance probability p = rank/(n+1)
    (Weibull). Returns (exceedance_pct, sorted_flows) for a semilog-y plot.
    """
    Q = np.asarray(Q, float)
    ranked = np.sort(Q)[::-1]
    n = len(Q)
    exceed = np.arange(1, n + 1) / (n + 1) * 100.0
    return exceed, ranked


def flood_threshold(QQ, fraction=0.25):
    """Operational high-flow threshold = fraction of the mean annual maximum flow.

    Splits the record into 365-day years, averages the yearly peaks, scales by
    `fraction`. Flows >= threshold count as an 'event'. Returns a float [mm/day].
    """
    QQ = np.asarray(QQ, float)
    annual_max = [QQ[t:t + 365].max() for t in range(0, len(QQ), 365)
                  if len(QQ[t:t + 365]) > 0]
    return float(np.mean(annual_max) * fraction)


def generate_ensemble(PP, PET, n_days, Nens=100, seed=7, max_rain_multiplier=1.2):
    """Generate a HyMOD forecast ENSEMBLE by perturbing forcing + parameters.

    Reproduces EnsembleGeneration_HyModMain.m. Each member is one plausible
    catchment+storm: the whole rain series is scaled by a random factor in
    [0, max_rain_multiplier) (rainfall uncertainty), and Huz, B, Alp, Kq are drawn
    from their ranges (Nq, Ks fixed, as in the source). Kq ~ Exponential(1)
    normalised to (0,1].

    Returns: ensemble (Nens x n_days streamflow array), members (list of dicts).
    """
    rng = np.random.default_rng(seed)
    # Pre-draw Kq for all members, normalise to (0,1] (mirrors MATLAB randg/max):
    kq_draws = rng.gamma(shape=1.0, size=Nens)     # Exp(1) == Gamma(shape=1)
    kq_draws = kq_draws / kq_draws.max()
    ensemble = np.zeros((Nens, n_days))
    members = []
    for i in range(Nens):
        mult = max_rain_multiplier * rng.random()  # rainfall perturbation
        Pars = {"Huz": 100.0 * rng.random(), "B": 2.0 * rng.random(),
                "Alp": rng.random(), "Nq": 3,
                "Kq": float(kq_draws[i]), "Ks": 0.0002}
        ensemble[i] = hymod01(PP[:n_days] * mult, PET[:n_days], Pars)["Q"]
        members.append({"multiplier": mult, **Pars})
    return ensemble, members
