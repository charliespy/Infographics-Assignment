#!/usr/bin/env python3
"""
Build Vietnam War evacuation routes map: Saigon -> U.S. military bases -> U.S. mainland.
Illustrates Espiritu's argument that the same military infrastructure channeled refugee movement.
Output: assets/images/graphic-1-evacuation-routes.png
"""
import os
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ImportError:
    print("Install matplotlib: pip install matplotlib")
    raise

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "images"
OUT_PATH = OUT_DIR / "graphic-1-evacuation-routes.png"

# Approximate coordinates (lon, lat) for a Pacific-centered map
# Saigon (Ho Chi Minh City)
SAIGON = (106.7, 10.8)
# Clark Air Base, Philippines
CLARK = (120.6, 15.2)
# Andersen AFB, Guam
GUAM = (144.9, 13.5)
# Utapao, Thailand
UTAPAO = (101.0, 12.7)
# U.S. West Coast (Camp Pendleton area - refugee processing)
USA = (-117.4, 33.2)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    BG = "#1B262C"
    SURFACE = "#0F4C75"
    PRIMARY = "#3282B8"
    LIGHT = "#BBE1FA"
    MUTED = "#6ba3c7"

    fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG)
    ax.set_facecolor(BG)

    # Plot in lon/lat (Pacific view: x roughly 80 to -120, y -10 to 50)
    ax.set_xlim(85, -130)
    ax.set_ylim(-5, 45)
    ax.set_aspect("equal")
    ax.axis("off")

    # Draw route segments with arrows (Saigon -> bases -> USA)
    def draw_arrow(x0, y0, x1, y1, color=LIGHT, lw=2):
        ax.annotate(
            "",
            xy=(x1, y1),
            xytext=(x0, y0),
            arrowprops=dict(arrowstyle="->", color=color, lw=lw),
        )

    # Saigon -> Clark
    draw_arrow(SAIGON[0], SAIGON[1], CLARK[0], CLARK[1])
    # Saigon -> Guam (some evacuees went via Guam)
    draw_arrow(SAIGON[0], SAIGON[1], GUAM[0], GUAM[1])
    # Saigon -> Utapao
    draw_arrow(SAIGON[0], SAIGON[1], UTAPAO[0], UTAPAO[1])
    # Clark -> USA
    draw_arrow(CLARK[0], CLARK[1], USA[0], USA[1])
    # Guam -> USA
    draw_arrow(GUAM[0], GUAM[1], USA[0], USA[1])
    # Utapao -> USA
    draw_arrow(UTAPAO[0], UTAPAO[1], USA[0], USA[1])

    # Plot points and labels
    for (lon, lat), label in [
        (SAIGON, "Saigon"),
        (CLARK, "Clark (Philippines)"),
        (GUAM, "Guam"),
        (UTAPAO, "Utapao (Thailand)"),
        (USA, "U.S. mainland"),
    ]:
        ax.plot(lon, lat, "o", color=PRIMARY, markersize=10, markeredgecolor=LIGHT, markeredgewidth=1.5)
        ax.annotate(
            label,
            (lon, lat),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=9,
            color=LIGHT,
            ha="left",
            va="bottom",
        )

    ax.set_title(
        "Vietnam War evacuation routes through U.S. military bases",
        fontsize=12,
        fontweight="bold",
        color="#fff",
    )
    for spine in ax.spines.values():
        spine.set_color(SURFACE)

    fig.tight_layout()
    fig.savefig(OUT_PATH, dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()
