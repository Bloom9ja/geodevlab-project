# Week 11: Coordinate Reference Systems and Spatial Operations

## What this folder contains
### Guided Practicals
- `set_vs_to.py`: demonstrates the difference between reprojecting coordinates with `.to_crs()` and overwriting metadata labels with `.set_crs()`
- `area_wrong_and_right.py`: compares distorted area calculations in degrees against accurate area calculations in square kilometers using UTM (`EPSG:32631`)
- `spatial_ops.py`: creates 2km buffers around facilities and counts how many facilities fall within each ward
- `clip_dissolve.py`: clips road networks to Agodi ward to measure road length and dissolves ward boundaries to calculate total LGA area
- `coverage_gap.py`: uses buffer, dissolve, and `overlay(how='difference')` to identify ward areas outside a 2km facility reach
- `nearest.py`: calculates the straight-line distance from each ward centroid to its nearest facility using `sjoin_nearest`
- `fix_geometry.py`: detects and repairs self-intersecting ("bowtie") polygons using Shapely and `.make_valid()`

### Independent Challenge
- `my_crs.py`: verifies the CRS of the settlement and school layers (`EPSG:32631`) and computes individual and total settlement areas in square kilometers
- `my_count.py`: uses `gpd.sjoin(..., predicate='within')` and a left merge to count how many schools fall inside each of the 1,523 settlement polygons while preserving zero-count settlements
- `my_reach.py`: models a 1 km walking reach around schools using `buffer(1000)` and `dissolve()`, isolates uncovered settlement gaps via `overlay(how='difference')`, exports processed layers to `data/processed/week11_school_reach.gpkg`, and generates `new_my_map.png`
- `my_validity.py`: checks all settlement polygons for geometry errors with `.is_valid` and repairs any invalid shapes using `.make_valid()`
- `new_my_map.png`: map visualizing settlements, school locations, and uncovered settlement areas beyond a 1 km school buffer

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
uv run month-03/week-11/my_crs.py
uv run month-03/week-11/my_count.py
uv run month-03/week-11/my_reach.py
uv run month-03/week-11/my_validity.py
```

## What I found
- **CRS Selection (`EPSG:32631`):** Both `settlements_utm31.gpkg` and `schools.gpkg` align with `EPSG:32631` (WGS 84 / UTM Zone 31N), which is the appropriate projected CRS for western Nigeria (0°E to 6°E). Using UTM ensures that buffer distances (1,000 m) and area measurements (96.16 km² across 1,523 settlements) are calculated accurately in meters rather than distorted angular degrees.
- **Buffer & Coverage Gap Analysis:** Choosing a **1 km (1,000 m) buffer** models a practical daily walking catchment for students. Combining dissolved 1 km school buffers with `gpd.overlay(..., how='difference')` pinpoints exact settlement pockets that fall outside immediate walking reach.
- **Geometry Validation:** Invalid self-intersecting polygons fail spatial operations until repaired with `.make_valid()`, which splits a bowtie polygon into a valid `MultiPolygon`.

## Method Limitation
- **Euclidean (Straight-Line) Distance vs. Real Travel:** Creating circular 1 km buffers around schools assumes people can walk in a straight line in every direction. In reality, walking access is constrained by the local road and footpath network, physical barriers such as rivers, wetlands, or fenced compounds, and varying road conditions—meaning some settlements inside a 1 km Euclidean buffer may still face a much longer actual walking route.

## What went wrong and how I fixed it
- In `set_vs_to.py`, I tried to print `wrongly_labelled.crs` before defining the variable, raising a `NameError`. I fixed it by assigning `wards.set_crs(epsg=32631, allow_override=True)` to `wrongly_labelled` first.
- In `spatial_ops.py`, I passed `layers='wards'` (plural) instead of `layer='wards'` to `gpd.read_file()`, triggering a `RuntimeWarning`, and accidentally wrote `reach(...)` instead of `print(...)`, causing a `TypeError`. Fixing the parameter spelling and function call resolved both issues.
- In `my_crs.py`, passing `layer='polygons'` to `gpd.read_file('data/processed/settlements_utm31.gpkg')` raised a `pyogrio` layer error because the GeoPackage contained a single unnamed/default layer, and I initially mistyped `.estimate_utm_crs()` as `.estimated_utm_crs()`. Removing the `layer=` parameter and fixing the method name resolved both issues.
- In `my_validity.py` and `my_reach.py`, small filename and method typos (`settlements_31.gpkg` instead of `settlements_utm31.gpkg`, `to_files` instead of `to_file`, and `procesed` instead of `processed`) caused file-not-found and attribute errors, which I fixed by standardizing the paths and saving the files before running.
