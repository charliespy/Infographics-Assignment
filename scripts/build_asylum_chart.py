#!/usr/bin/env python3
"""
Build asylum grant rates by nationality chart. Illustrates how acceptance varies by
nationality (geopolitical selectivity). Data: TRAC Immigration (EOIR asylum decisions).
Output: assets/images/graphic-2-asylum-rates.png
"""
import csv
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Install matplotlib: pip install matplotlib")
    raise

ROOT = Path(__file__).resolve().parent.parent
DATA_CSV = ROOT / "data" / "asylum_grant_rates_by_nationality.csv"
OUT_DIR = ROOT / "assets" / "images"
OUT_PATH = OUT_DIR / "graphic-2-asylum-rates.png"


def load_data():
    nationalities = []
    rates = []
    with open(DATA_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            nationalities.append(row["nationality"])
            rates.append(float(row["grant_rate_pct"]))
    return nationalities, rates


def main():
    nationalities, rates = load_data()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    BG = "#1B262C"
    SURFACE = "#0F4C75"
    PRIMARY = "#3282B8"
    LIGHT = "#BBE1FA"
    MUTED = "#6ba3c7"

    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
    ax.set_facecolor(BG)

    x = range(len(nationalities))
    bars = ax.bar(x, rates, color=PRIMARY, edgecolor=LIGHT, linewidth=1)
    ax.set_xticks(x)
    ax.set_xticklabels(nationalities, rotation=45, ha="right")
    ax.set_ylabel("Asylum grant rate (%)", fontsize=11, color=LIGHT)
    ax.set_title(
        "U.S. asylum grant rate by nationality (Immigration Court)",
        fontsize=12,
        fontweight="bold",
        color="#fff",
    )
    ax.set_ylim(0, 80)
    ax.tick_params(axis="both", labelsize=9, colors=MUTED)
    ax.grid(True, axis="y", linestyle="--", alpha=0.2, color=MUTED)
    for spine in ax.spines.values():
        spine.set_color(SURFACE)

    fig.tight_layout()
    fig.savefig(OUT_PATH, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
