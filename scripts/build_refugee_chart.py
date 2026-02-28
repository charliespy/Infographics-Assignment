#!/usr/bin/env python3
"""
Build the original infographic chart: U.S. refugee arrivals by fiscal year (1980–2023).
Data source: DHS OHSS Yearbook of Immigration Statistics, Table 13.
Output: assets/images/original-graphic-refugee-admissions.png
"""
import csv
import os
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
except ImportError:
    print("Install matplotlib: pip install matplotlib")
    raise

ROOT = Path(__file__).resolve().parent.parent
DATA_CSV = ROOT / "data" / "refugee_arrivals_1980_2023.csv"
OUT_DIR = ROOT / "assets" / "images"
OUT_PATH = OUT_DIR / "original-graphic-refugee-admissions.png"


def load_data():
    years = []
    arrivals = []
    with open(DATA_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            years.append(int(row["year"]))
            arrivals.append(int(row["arrivals"]))
    return years, arrivals


def main():
    years, arrivals = load_data()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    BG = "#1B262C"
    SURFACE = "#0F4C75"
    PRIMARY = "#3282B8"
    LIGHT = "#BBE1FA"
    MUTED = "#6ba3c7"

    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
    ax.set_facecolor(BG)

    ax.grid(True, linestyle="--", alpha=0.2, color=MUTED)
    ax.fill_between(years, arrivals, alpha=0.3, color=PRIMARY)
    ax.plot(years, arrivals, color=LIGHT, linewidth=2)

    ax.set_xlabel("Fiscal year", fontsize=11, color=LIGHT)
    ax.set_ylabel("Refugee arrivals", fontsize=11, color=LIGHT)
    ax.set_title("U.S. Refugee Arrivals, 1980\u20132023", fontsize=13, fontweight="bold", color="#fff")
    ax.set_xlim(1979, 2024)
    ax.set_ylim(0, None)
    ax.tick_params(axis="both", labelsize=9, colors=MUTED)
    for spine in ax.spines.values():
        spine.set_color(SURFACE)

    ax.axvline(x=2001, color=MUTED, linestyle="--", alpha=0.5, linewidth=1)
    ax.annotate("9/11", xy=(2001, 50000), fontsize=8, color=MUTED, ha="center")
    ax.axvline(x=2017, color=MUTED, linestyle="--", alpha=0.5, linewidth=1)
    ax.annotate("Policy shift", xy=(2017, 50000), fontsize=8, color=MUTED, ha="center")

    fig.tight_layout()
    fig.savefig(OUT_PATH, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
