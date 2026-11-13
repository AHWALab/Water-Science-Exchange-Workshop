"""
nb_style.py
===========
Shared look and feel for the ensemble forecast evaluation notebooks (CIROH Summer
Institute 2026 and CUAHSI Water Science Exchange 2026, Module 3).
Importing and calling set_style() once per notebook gives every figure the same
fonts, colours, and grid so the four-notebook series feels like one document.
"""

# Credit: Humberto Vergara and Mohamed Abdelkader (University of Iowa).
import matplotlib as mpl
import matplotlib.pyplot as plt

# A consistent, colour-blind-friendly palette used throughout the workshop.
PALETTE = {
    "obs":      "#1a1a1a",   # observations / truth  -> near-black
    "control":  "#0072B2",   # deterministic control -> blue
    "ensemble": "#9aa3ad",   # ensemble members      -> grey
    "ens_mean": "#D55E00",   # ensemble mean         -> vermillion
    "threshold":"#C00000",   # flood threshold       -> red
    "accent":   "#009E73",   # highlights            -> green
    "accent2":  "#CC79A7",   # secondary highlight   -> magenta
    "skill":    "#E69F00",   # skill/forecast prob   -> orange
}


def set_style():
    """Apply the workshop-wide matplotlib styling. Call once near the top."""
    mpl.rcParams.update({
        "figure.dpi": 110,
        "savefig.dpi": 110,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 11.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#dddddd",
        "grid.linewidth": 0.8,
        "legend.frameon": False,
        "legend.fontsize": 10,
        "lines.linewidth": 1.6,
    })


def threshold_band(ax, thr, label="Flood threshold"):
    """Draw the flood threshold as a labelled horizontal reference line."""
    ax.axhline(thr, color=PALETTE["threshold"], ls="--", lw=1.6, zorder=5)
    ax.text(0.005, thr, f" {label} = {thr:.2f} mm/day",
            color=PALETTE["threshold"], va="bottom", ha="left",
            transform=ax.get_yaxis_transform(), fontsize=9.5, fontweight="bold")
