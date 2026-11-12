# Week 11: Coordinate Reference Systems and Spatial Operations

## What this folder contains
- set_vs_to.py: demonstrates the difference between reprojecting coordinates with .to_crs()and overwriting metadata labels with `.set_crs()`
- area_wrong_and_right.py: compares distorted area calculations in degrees against accurate area calculations in square kilometers using UTM (`EPSG:32631`)
- spatial_ops.py: creates 2km buffers around facilities and counts how many facilities fall within each ward
- clip_dissolve.py: clips road networks to Agodi ward to measure road length and dissolves ward boundaries to calculate total LGA area
- coverage_gap.py: uses buffer, dissolve, and `overlay(how='difference')` to identify ward areas outside a 2km facility reach
- nearest.py: calculates the straight-line distance from each ward centroid to its nearest facility using `sjoin_nearest`
- fix_geometry.py: detects and repairs self-intersecting ("bowtie") polygons using Shapely and `.make_valid()`

## How to run it
From the repository root:
```bash
uv run month-03/week-11/set_vs_to.py
uv run month-03/week-11/area_wrong_and_right.py
uv run month-03/week-11/spatial_ops.py
uv run month-03/week-11/clip_dissolve.py
uv run month-03/week-11/coverage_gap.py
uv run month-03/week-11/nearest.py
uv run month-03/week-11/fix_geometry.py
```

## What I found
- Calculating area or distance in `EPSG:4326` produces meaningless degree-based values; reprojecting to `EPSG:32631` (UTM Zone 31N) is required for accurate meter and square kilometer measurements across Ibadan North.
- Combining 2km facility buffers with `gpd.overlay(..., how='difference')` clearly highlights underserved ward areas that lack nearby facility coverage.
- Invalid self-intersecting polygons fail spatial operations until repaired with `.make_valid()`, which splits a bowtie polygon into a valid `MultiPolygon`.

## What went wrong and how I fixed it
- In `set_vs_to.py`, I tried to print `wrongly_labelled.crs` before defining the variable, raising a `NameError`. I fixed it by assigning `wards.set_crs(epsg=32631, allow_override=True)` to `wrongly_labelled` first.
- In `spatial_ops.py`, I passed `layers='wards'` (plural) instead of `layer='wards'` to `gpd.read_file()`, triggering a `RuntimeWarning`, and accidentally wrote `reach(...)` instead of `print(...)`, causing a `TypeError`. Fixing the parameter spelling and function call resolved both issues.