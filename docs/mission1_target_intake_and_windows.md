# Mission 1 Target Intake and Launch-Window Workbook Notes

## Workbook

Live workbook:
https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit

## Completed in this pass

Added Mission 1 canon workbook surfaces:

- `Mission Source Intake`
- `Mission 1 Control`
- `Mission 1 Target Library`
- `Mission 1 Flight Windows`
- `Mission 1 Operations Path`

Expanded `Index & Log` to include Mission 1 target-library index rows beginning at row 1004.

## Current Mission 1 library metrics

From `Mission 1 Control`:

| Metric | Count |
|---|---:|
| Target-library rows | 5,000 |
| M1 tag/mine primary-review rows | 56 |
| M1 flight-path review rows | 30 |
| Mission 27 context rows | 4,914 |
| Source-gate review rows | 74 |
| Enrichment-required rows | 4,926 |
| June 2027 scout/simulation rows | 86 |
| January 2028 primary launch-readiness rows | 56 |
| August 2028 buffer/secondary rows | 86 |
| Mission-zone NEA rows | 86 |
| Known-complete rows | 74 |

## Source intake routes

Registered source routes:

- JPL SBDB Query API: `https://ssd-api.jpl.nasa.gov/sbdb_query.api`
- JPL Horizons API: `https://ssd.jpl.nasa.gov/api/horizons.api`
- Minor Planet Center data: `https://www.minorplanetcenter.net/data`
- ESA NEOCC catalogue: `https://neo.ssa.esa.int/catalogue-of-nea`
- Internal workbook source: `Rocks ECSV Sample 200k`
- Canon review surface: `Body Catalogue Review`

## Window posture

The windows are currently workbook review gates only:

- June 2027: simulation / scout / pre-clearance review window.
- January 2028: primary launch-readiness review window.
- August 2028: buffer / secondary launch-review window.

No launch authorization, procurement, runtime activation, deployment, or public mission claim is created by this documentation.

## Mission 27 dependency

Mission 1 candidate/context data is tagged so that return-chain, cislunar, lunar-supply, Mars-supply, and Earth-supply lessons remain reusable for the future Mission 27 near-Lagrange central hub architecture.

## Guardrails

- `Mission 1 Target Library` is a review-state candidate/context library, not a final target list.
- `Rank_Score` is an internal screening score, not a delta-v, accessibility, profitability, legality, or feasibility score.
- External SBDB/Horizons/MPC/ESA enrichment requires field mapping and review before import.
- Cognigrex and RSOC references are planning/reporting routes only; no autonomous operation or runtime activation is implied.
