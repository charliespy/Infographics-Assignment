#!/usr/bin/env bash
# Download the three reference graphics into assets/images/.
# Run from repo root: bash scripts/download_graphics.sh

set -e
IMGDIR="$(dirname "$0")/../assets/images"
mkdir -p "$IMGDIR"
cd "$IMGDIR"

echo "Downloading Graphic 1 (colonialism)..."
curl -sL "https://ourworldindata.org/grapher/population-living-in-european-colonies-and-colonizers.png" -o graphic-1-colonialism.png

echo "Downloading Graphic 2 (income inequality)..."
curl -sL "https://ourworldindata.org/grapher/global-and-between-country-income-inequality.png" -o graphic-2-income-inequality.png

echo "Downloading Graphic 3 (Mapping Deportations)..."
curl -sL "https://mappingdeportations.com/wp-content/uploads/2025/05/VizThumbnails_RIC.jpg" -o graphic-3-mapping-deportations.jpg

echo "Done. Images in $IMGDIR"
