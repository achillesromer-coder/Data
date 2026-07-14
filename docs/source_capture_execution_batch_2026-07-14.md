# Mission 1 Source Capture Execution Batch — 2026-07-14

Workbook: `Asteroid_Strategic_Mapping_Base_withRocks`

Workbook URL: https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit

## Purpose

This batch begins the source-capture execution lane for Mission 1 by moving from route-built rows into payload-aware operating rows.

## Completed

- Converted `Mission 1 Source Capture` rows 4–27 from spill formulas to static operating rows.
- Captured the official JPL SBDB API object/orbit payload for Eros where the chat browser could safely access the API URL.
- Recorded the Eros payload status in `Mission 1 Source Capture!A16:V16`.
- Logged `M1SRC-EROS-001` in `Appendix & Log!A6160:R6160`.
- Marked `Eros` as the first source-backed orbit baseline in `Cluster Sequence Optimiser!A16:AB16`.
- Updated `Mission 1 Enrichment Queue` so Eros physical-parameter capture and Horizons Jan 2028 ELEMENTS checks remain queued.

## Captured Eros source fields

Source URL: `https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=Eros`

Captured fields:

- SBDB API signature version: `1.3`
- Object: `433 Eros (A898 PA)`
- SPK ID: `20000433`
- NEO: `true`
- PHA: `false`
- Orbit class: `Amor`
- Orbit ID: `659`
- e: `0.223`
- a: `1.46 au`
- q: `1.13 au`
- i: `10.8 deg`
- Q: `1.78 au`
- MOID: `0.149 au`
- condition code: `0`
- solution date: `2021-05-24 17:55:05`

## Comparison result

- No material conflict was found on rounded core orbit fields compared with workbook values.
- Workbook q/Q values align within rounding.
- Physical fields such as diameter, density, albedo and taxonomy remain workbook/raw-derived proxies until a physical-parameter payload is captured and reviewed.

## Limitation disclosure

Only the Eros object URL was accessible directly in this chat browser because it appears in the official SBDB API documentation examples. Arbitrary object API URLs were not safely openable through the browser in this pass. Other source-capture rows therefore remain `ROUTE READY / PAYLOAD PENDING` and should be executed by the LS/Cognigrex API runner or another approved API path.

## Next

1. Run physical-parameter capture for Eros.
2. Run SBDB object payload capture for Apophis + top source-gate NEA rows through the LS/Cognigrex API runner.
3. Run Horizons Jan 2028 ELEMENTS checks only after identity/orbit source capture.
4. Continue to log conflicts into `Appendix & Log` rather than overwriting workbook fields silently.
