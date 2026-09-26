# Data Notes
 
Running log of every dataset used in this project so far
 
---
 
## GRID3 Nigeria LGA Boundaries (Odeda LGA)
- Source: https://data.grid3.org/datasets/GRID3::grid3-nga-operational-lga-boundaries/about
- File: AOI
- Date downloaded: 12/09/2026
- Columns: uniq_id (numbers), timestamp (date), editor (text), lganame (text), lgacode (numbers), statename (text), statecode (text), source (text), amapcode (text)
- Nulls found: Nil
- Geometry type: polygon
- Feature count: 1
- Coverage notes: Covers properly
---
 
## GRID3 NGA — Ogun Settlement Extents v1.0
- Source: https://www.africageoportal.com/datasets/GRID3::grid3-nga-ogun-settlement-extents-v1-0
- File: Odeda_Settlements
- Date downloaded: 05/09/2026
- Columns: object_id (numbers), Country (text), ISO (text), Type (numbers), Population (Numbers), shape_are (Numbers)
- Nulls found: Nil
- Geometry type: Polygon (MultiPolygon)
- Feature count: 1523
- Coverage notes: Covers the LGA
---
 
## OpenStreetMap Roads (via QuickOSM, Odeda extent)
- Source: OpenStreetMap, pulled via QuickOSM plugin (Key: highway), clipped to the actual Odeda polygon (QuickOSM's "Layer Extent" pulls a bounding box, not the polygon shape — clipped afterward with Vector → Geoprocessing Tools → Clip)
- File: Odeda_Roads.gpkg
- Date extracted: 12/09/2026
- Columns: highway (text), name, osm_id, osm_type, alt_name, juntion, surface
- Nulls found: none in the highway field
- Geometry type: line (MultiLineString)
- Feature count: 2,642
- Values present in highway: footway, path, primary, primary_link, residential, secondary, service, tertiary, track, trunk, trunk_link, unclassified
- Coverage notes: visually complete for the area

## CRS and reprojection
- All source layers (boundary, roads) arrived in EPSG:4326 (WGS 84)
- Study area: Odeda LGA boundary, exported from the GRID3 Operational LGA layer
- Reprojected to EPSG:32631 (WGS 84 / UTM Zone 31N); correct zone for western Nigeria per project rule
- Area check: Odeda boundary calculated at approximately 1319.879 km² after reprojection, compared against a commonly cited figure of ~1,560 km² for Odeda LGA (unverified against an authoritative source. Worth checking against the GRID3 dataset's own documentation if precision matters later
- Also noted: initial $area calculation on the unprojected (EPSG:4326) layer returned a real-world value in square meters rather than square degrees; QGIS's ellipsoidal area measurement setting was active, which meant the "wrong" area wasn't actually wrong in magnitude, just not yet the deliberate exercise the pack expected
- Working files saved in data/processed/; raw/ files untouched
- All source layers (boundary, roads) arrived in EPSG:4326 (WGS 84)
- Study area: Odeda LGA boundary, exported from the GRID3 Operational LGA layer
- Roads (clipped to Odeda via QuickOSM + manual Clip) and the settlements were both reprojected to EPSG:32631 (WGS 84 / UTM Zone 31N)

- ## Multipart to Singleparts (Settlements)
- Operation: Vector → Geometry Tools → Multipart to Singleparts
- Input: clipped, reprojected settlements layer (1,523 features)
- Output: odeda_settlements_singlepart.gpkg> → 1,532 features (9 extra genuine physical pieces)
- Why: one "Built-up Area" settlement feature (OBJECTID 2356) turned out to be a multipart geometry — several disconnected polygon pieces bundled under a single feature ID. Splitting to singleparts gives each physical piece its own geometry, which is the correct basis for a per-piece nearest-distance calculation.
---
 
## Join Attributes by Nearest — Settlements to Schools (first attempt, then corrected)
- Operation: Vector → Data Management Tools → Join attributes by nearest, Maximum nearest features = 1
- First attempt: run on the pre-singlepart settlements layer (1,523 features) → output had 1,591 rows, more than the input
- Second attempt: rerun on the singlepart settlements layer (1,532 features) → output had 1,599 rows, still more than input
- Investigation (via Processing Toolbox → Statistics by Categories, grouped by OBJECTID): traced the extra rows to a small number of large settlement polygons (OBJECTID 2356, 282, 9862, 10219) that geometrically **contain multiple schools inside their own boundary**. A point inside a polygon has distance 0 to it, so every contained school tied at distance 0, and the join tool correctly returned every tied match rather than picking one arbitrarily. OBJECTID 2356 alone matched 55 different schools, all at distance 0.
- OBJECTID 10321 also appeared as a duplicate (5 rows) but for an unrelated, unproblematic reason: it is a genuine multipart settlement split into 5 real pieces by the earlier singlepart step, each with a different, real distance value (2,428–3,103 m) — not a tie, and correctly left in the main dataset.
- Separately, 79 ordinary (non-outlier) settlements returned a genuine 0 m distance because exactly one school happens to sit inside that specific settlement's own footprint — a different, unproblematic situation from the multi-school containment cases above.
---
 
## Outlier Split and Clean Dataset
- OBJECTID 2356, 282, 9862, and 10219 (the multi-school-containment settlements) exported separately to data/processed/odeda_settlements_urban_core.gpkg — kept as a documented finding, not discarded
- All remaining settlements exported to data/processed/odeda_settlements_nearest_school_clean.gpkg — 1,528 features
- Checks run on the clean dataset: map placement looked sensible; row count (1,528) roughly matched expectation; one feature (OBJECTID 197762) hand-verified — tool reported ~125 m, manual Measure-tool check gave ~129 m, considered a pass; no null values in the distance field
---
 
## Settlement Centroids (map visualization only)
- Source: derived from odeda_settlements_nearest_school_clean.gpkg via Vector → Geometry Tools → Centroids
- File: odeda_settlements_centroids.gpkg
- Date created: 26/09/2026
- Purpose: settlement polygons were too small at LGA-wide map scale for graduated color to register visually; centroids used purely for map legibility. The actual join/analysis was performed on the original polygon geometries, not these centroids.
- Feature count: 1,528 (matches the clean settlements dataset)
- Geometry type: point
- Coverage notes: centroid placement looks reasonable against settlement locations known from the map; not checked feature-by-feature.
