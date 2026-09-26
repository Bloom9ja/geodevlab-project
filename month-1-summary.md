# Month 1 Summary — SchoolReach: Odeda LGA

**Question:** Which settlements in Odeda LGA, Ogun State have inadequate road-based access to primary schools?

**Operation run:** Join attributes by nearest (settlements → nearest primary school, straight-line distance), using clipped and reprojected layers (EPSG:32631, UTM Zone 31N). This is the closest available proxy for the actual question this month, since true road-network distance requires routing tools not yet introduced in the program — that's explicitly flagged as still-needed data below, not a finished answer.

**What I expected:** A single row per settlement (matching the 1,523 settlements in the source dataset), with a range of plausible straight-line distances to the nearest primary school across Odeda.

**What I actually got:** After the first join, the output had 1,591–1,599 rows instead of 1,523 — more rows than input. Investigating this (via QGIS's Statistics by Categories tool, and later by inspecting the raw join output directly) traced the extra rows to two distinct causes:

1. **Multipart geometries.** One "Built-up Area" settlement feature (OBJECTID 2356) turned out to be a multipart geometry — several disconnected polygon pieces bundled under a single feature ID. Splitting settlements with Multipart to Singleparts brought the settlement count from 1,523 to 1,532 (9 genuine extra physical pieces), which is the geometrically correct basis for a per-piece distance calculation.
2. **Genuine tied zero-distances from polygon containment.** Even after the multipart fix, a small number of large settlement polygons (OBJECTID 2356, 282, 9862, 10219 — all "Built-up Area" or "Small Settlement Area" types with large populations) geometrically **contain multiple schools within their own boundary**. Since a point inside a polygon has a distance of zero to that polygon, every school inside counted as an equally-valid "nearest" match, and QGIS's nearest-join tool correctly returned every tied match rather than picking one arbitrarily. OBJECTID 2356 alone matched to 55 different schools, all at distance 0.

**What surprised me:** This wasn't a tool error — it's a genuine finding about the data. "Distance to nearest school" as a metric breaks down for Odeda's large, urbanized built-up-area polygons, because the question "how far is this settlement from its nearest school" doesn't really mean anything when the settlement itself is a large urban area that contains dozens of schools inside it. The metric only cleanly applies to smaller, point-like settlements (hamlets), which make up the large majority of the dataset. Separately, 79 ordinary (non-outlier) settlements also returned a genuine 0m distance — these are legitimate cases where exactly one school happens to sit inside that specific settlement's own footprint, which is a different and unproblematic situation from the multi-school containment cases above.

**What I did about it:** Separated the four "contains multiple schools" outlier settlements into their own file (`odeda_settlements_urban_core.gpkg`) rather than forcing them into the main distance analysis, and built a clean working dataset (`odeda_settlements_nearest_school_clean.gpkg`, 1,528 features) from the remaining settlements for the actual accessibility map and analysis. One hand-checked feature (a settlement roughly 125m from its nearest school by the tool, ~129m by manual measurement) confirmed the distance calculation itself is working correctly.

**What data I still need:**
- Road-network distance (this month's result is straight-line only, which was always a known limitation — see the original project brief)
- A defined, justified threshold for what counts as "inadequate" access (distance or travel-time based) — still deliberately left open per the original brief
- A clearer methodological decision on how to treat the four large urban-core settlements in the final accessibility analysis, rather than excluding them by default
