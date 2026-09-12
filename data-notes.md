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
