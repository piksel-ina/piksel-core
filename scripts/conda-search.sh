#!/bin/bash

# Simple conda package checker
PACKAGES=(
    gh-scoped-creds
    param
    xarray_leaflet
    xarray-spatial
    line_profiler
    memory_profiler
    snakeviz
    watermark
    ipdb
    sparse
    pot
    xgboost
    numpy_groupies
    xarrayutils
    xhistogram
    xmip
    xpublish
    xrft
)

echo "Checking conda packages..."

for pkg in "${PACKAGES[@]}"; do
    if conda search -c conda-forge "$pkg" &>/dev/null; then
        echo "✓ $pkg"
    else
        echo "✗ $pkg"
    fi
done
