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

## Week 3 — CRS, Reprojection, and Quality Checks
 
**CRS chosen:** EPSG:32631 (WGS 84 / UTM Zone 31N). Odeda LGA sits in western Nigeria (roughly 7.2°N, 3.5°E), and the project's own CRS rule assigns EPSG:32631 to western Nigeria, EPSG:32632 to central/eastern.
 
**What was reprojected and clipped:** all source layers (boundary, settlements, roads, schools) arrived in EPSG:4326 (WGS 84). The Odeda LGA boundary was isolated from the national GRID3 layer as its own AOI. Roads were pulled via QuickOSM directly to Odeda's extent, then clipped again to the exact boundary polygon (QuickOSM's "Layer Extent" pulls a bounding box, not the true polygon shape, so a manual clip was still required). All four layers — boundary, settlements, roads, schools — were then reprojected to EPSG:32631 and saved into `data/processed/`.
 
**Five quality checks and results:**
 
1. **CRS stated for every layer.** Boundary, settlements, roads, and schools all confirmed as EPSG:32631 after reprojection (checked via Layer Properties → Information on each). Decision: no further action needed — all four consistent.
2. **A study-area file exists containing only the AOI.** `AOI_utm31.gpkg` contains exactly one feature — Odeda LGA. Decision: confirmed, used as the overlay layer for every subsequent clip.
3. **Every layer clipped to the AOI and reprojected, saved in `data/processed/`.** Confirmed for boundary and roads at this stage (settlements and schools were reprojected in this same step but clipped/finalized during Week 4's analysis work, documented further down in this file). Decision: accepted as sufficient for Week 3's boundary+roads deliverable; settlements/schools reprojection carried forward and re-verified in Week 4.
4. **`data/raw/` left unmodified.** Confirmed — all reprojected and clipped outputs were saved as new files into `data/processed/`, nothing in `raw/` was opened for editing. Decision: no action needed.
5. **Area value sanity check.** Odeda's boundary area calculated at approximately 1,320 km² after reprojection, against a commonly cited reference figure of ~1,560 km² for Odeda LGA (this reference traces to an older Wikipedia infobox, not a primary GRID3/NBS source, so it's a ballpark check, not an authoritative one). Decision: **flagged, not silently accepted.** The ~15% gap is plausibly explained by differing boundary vintages/precision between the GRID3 file used here and whatever source the reference figure originally came from, rather than a reprojection error — the CRS and reprojection steps themselves were separately verified as correct (EPSG confirmed on the output layer, and the area order-of-magnitude is right for an LGA, not off by a factor of 1,000 as a metres/degrees mixup would produce). This is left as an open item to revisit if the final analysis needs a more precise area figure, rather than treated as resolved.
**Problems found and how they were handled:**
- QGIS's Field Calculator repeatedly failed with "could not add the new field to the provider" when creating a new field directly, even on a GeoPackage layer. **Fixed**, not just flagged — worked around by adding the field manually via the attribute table's "New Field" button first, then using Field Calculator only to update that existing field's values.
- The initial `$area` calculation on the unprojected (EPSG:4326) layer returned a real-world value in square meters rather than the expected tiny square-degrees number, because QGIS's ellipsoidal area measurement setting was active. **Flagged**, not an error requiring a fix — noted so that any future `$area` output on this project is not blindly trusted without first checking that setting.
**Where the analysis-ready file lives:** `data/processed/AOI_utm31.gpkg` (AOI, EPSG:32631) and `data/processed/Roads_utm31.gpkg` (roads, clipped and reprojected, EPSG:32631). 
---

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
