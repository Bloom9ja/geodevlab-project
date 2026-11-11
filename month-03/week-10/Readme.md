# Week 10: Geopandas, layers as tables

## What this folder contains
- my_points.py: converts the Odeda schools CSV into a Geopackage
- my_join.py: joins the extracted settlement attribute to Odeda settlements
- my_map.py: generates a static map of schols overlaid on Odeda settlements
- my_map.png: map showing school locations across Odeda LGA

## How to run it
From the repository root:
```bash
uv run month-03/week-10/my_points.py
uv run month-03/week-10/my_join.py
uv run month-03/week-10/my_map.py
```

## What I found
Every record in settlement table matched the settlemet polygons on the first try because the csv was extracted from the geopackage earlier

## What went wrong and how I fixed it
I first assigned EPSH:32631 to raw lat/long coordinates instead of loading them in 4326