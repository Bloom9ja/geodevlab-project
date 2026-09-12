# SchoolReach: Primary School Accessibility in Odeda LGA

*A GeoDev Lab Africa (Cohort 1) project. The aim of this project is to bring to light the accessibility of Primary Schools in Odeda LGA, Ogun state, Nigeria.*

## Part 1 — The Question

Which settlements in Odeda LGA, Ogun State have inadequate road-based access to primary schools?

## Part 2 — Why It Matters

Education planners at the LGA level, the State Universal Basic Education Board (SUBEB), and NGOs running school-access interventions currently have no easy way to see which specific settlements are underserved. A map that identifies these settlements by actual road distance lets limited resources like new schools, feeder roads, school transport go where they're genuinely needed instead of where it's assumed they're needed.

## Part 3 — The Data I Need

1. **Odeda LGA administrative boundary**: defines the area of interest and the clip extent for everything else.
2. **Settlement locations**: the populated places accessibility is measured *from*.
3. **Primary school locations**: the facilities accessibility is measured *to*.
4. **Road network**: required because the question is road-based access, not straight-line distance.
5. **Age-structured population**: used to estimate how many school-age children are affected, replacing the unreliable `student_ct` field in the school dataset.

## Part 4 — Data Sources

| ID | Dataset | Provider | Source |
|----|---------|----------|--------|
| D01 | Odeda LGA boundary | GRID3 Nigeria Administrative Boundaries | https://data.grid3.org (fallback: HDX COD-AB Nigeria — https://data.humdata.org/dataset/cod-ab-nga — if GRID3 doesn't cover ward-level for this state) |
| D02 | Settlement extents | GRID3 NGA — Ogun Settlement Extents v1.0 | https://www.africageoportal.com/datasets/GRID3::grid3-nga-ogun-settlement-extents-v1-0 |
| D03 | Primary schools | GRID3 Nigeria Schools dataset (already acquired nationally; filtered to Odeda) | Local file — full provenance in `docs/data-sources.md` |
| D04 | Road network | OpenStreetMap, queried directly to the Odeda boundary extent via the QuickOSM plugin in QGIS (Key: highway) | Pulled in-app; raw OSM data at https://www.openstreetmap.org |
| D05 | Age-structured population | WorldPop Nigeria age & sex structures, 2025 (constrained, beta R2024B), ~100m resolution | https://hub.worldpop.org/geodata/summary?id=53511 |

Exact download dates, versions, CRS, and any clipping steps applied will be recorded in `docs/data-sources.md` before analysis begins. Note: D04 is the dataset being tested first for feasibility, since without usable road tagging the road-based version of this question doesn't work at all — regardless of acquisition method, its actual completeness in Odeda still needs checking. Note also that D05 is a 2025 beta release (R2024B) per WorldPop's own disclaimer — more current than the older 2020 constrained dataset, but still subject to revision.

## Part 5 — What I Would Build

Initially, a static map identifying which settlements in Odeda fall outside an acceptable road-based distance/travel-time from the nearest primary school, using a threshold that's explicitly justified rather than picked arbitrarily. Over 12 months, this is intended to evolve into a system where an LGA, a facility type, and an accessibility threshold can be selected, and the system automatically identifies underserved settlements, computes nearest-facility road distance, and estimates the affected population — without the analysis being manually re-run each time.

## What "Inadequate Access" Means (not yet finalized)

Deliberately left open until roads and schools are both loaded for Odeda. Candidates to evaluate: a fixed distance threshold, a fixed travel-time threshold, or a relative threshold (each settlement's distance compared to Odeda's own distribution) if the data turns out compressed. Whichever is chosen will be stated and justified in the methodology notes, not assumed upfront.

## Scope Boundary

This project measures **road-based distance to the nearest primary school** — it does not by itself diagnose *why* a settlement is underserved (funding, terrain, population density, etc.), and it does not classify a settlement as "underserved" using any threshold that hasn't been explicitly stated and justified first.

## Week 1 Success Criteria

- [ ] Odeda LGA boundary obtained and documented
- [ ] Settlement extents confirmed for Odeda
- [ ] Primary schools filtered to Odeda from the existing national dataset
- [ ] Road network pulled for Odeda via QuickOSM, with tag completeness checked
- [ ] Age-structured population raster clipped to Odeda
- [ ] All five sources documented with links, versions, and download dates in `docs/data-sources.md`
- [ ] Repository is public, with README and this brief committed, and at least two commits
