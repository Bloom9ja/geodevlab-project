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
