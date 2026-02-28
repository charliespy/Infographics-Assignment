#!/usr/bin/env python3
"""
Build chart: refugees displaced by major U.S. military interventions over time.
Data source: UNHCR Refugee Data Finder (refugee stock by country of origin).
Output: assets/images/graphic-1-displacement.png
"""
import csv
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Install matplotlib: pip install matplotlib")
    raise

ROOT = Path(__file__).resolve().parent.parent
DATA_CSV = ROOT / "data" / "displacement_us_interventions.csv"
OUT_DIR = ROOT / "assets" / "images"
OUT_PATH = OUT_DIR / "graphic-1-displacement.png"


def load_data():
    with open(DATA_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    years = [int(r["year"]) for r in rows]
    vietnam = [float(r["vietnam_thousands"]) for r in rows]
    afghanistan = [float(r["afghanistan_thousands"]) for r in rows]
    iraq = [float(r["iraq_thousands"]) for r in rows]
    return years, vietnam, afghanistan, iraq


def main():
    years, vietnam, afghanistan, iraq = load_data()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    BG = "#1B262C"
    SURFACE = "#0F4C75"
    PRIMARY = "#3282B8"
    LIGHT = "#BBE1FA"
    MUTED = "#6ba3c7"

    fig, ax = plt.subplots(figsize=(10, 5), facecolor=BG)
    ax.set_facecolor(BG)

    ax.fill_between(years, 0, vietnam, alpha=0.5, color=PRIMARY, label="Vietnam")
    ax.fill_between(years, vietnam, [v + a for v, a in zip(vietnam, afghanistan)], alpha=0.5, color=LIGHT, label="Afghanistan")
    ax.fill_between(
        years,
        [v + a for v, a in zip(vietnam, afghanistan)],
        [v + a + i for v, a, i in zip(vietnam, afghanistan, iraq)],
        alpha=0.5,
        color=MUTED,
        label="Iraq",
    )
    ax.plot(years, vietnam, color=PRIMARY, linewidth=1.5, alpha=0.9)
    ax.plot(years, [v + a for v, a in zip(vietnam, afghanistan)], color=LIGHT, linewidth=1.5, alpha=0.9)
    ax.plot(years, [v + a + i for v, a, i in zip(vietnam, afghanistan, iraq)], color=MUTED, linewidth=1.5, alpha=0.9)

    ax.set_xlabel("Year", fontsize=11, color=LIGHT)
    ax.set_ylabel("Refugees (thousands)", fontsize=11, color=LIGHT)
    ax.set_title(
        "Refugees from major U.S. military interventions (stock)",
        fontsize=12,
        fontweight="bold",
        color="#fff",
    )
    ax.set_xlim(1968, 2025)
    ax.set_ylim(0, None)
    ax.legend(loc="upper right", fontsize=9, facecolor=SURFACE, edgecolor=MUTED, labelcolor=LIGHT)
    ax.tick_params(axis="both", labelsize=9, colors=MUTED)
    ax.grid(True, linestyle="--", alpha=0.2, color=MUTED)
    for spine in ax.spines.values():
        spine.set_color(SURFACE)

    fig.tight_layout()
    fig.savefig(OUT_PATH, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
