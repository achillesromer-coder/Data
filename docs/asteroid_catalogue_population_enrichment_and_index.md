# Asteroid Catalogue Population, Enrichment, and Index Note

## Workbook

Live workbook:
https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit

## Purpose

This note records the transition from staged expansion sheets into canon workbook operation.

The workbook now uses:

- `Asteroid Master` as the populated canon object table.
- `Body Catalogue Review` as the current review population surface.
- `Index & Log` as the searchable one-row-per-object log and index.
- `Mission Planning Toolkit` as the mission-zone planning surface.
- `LS Integration Map` as the Web/Desktop/Go/Drive/Git/Cognigrex handoff map.

## Population and enrichment

`Asteroid Master` has been broadly populated from `Body Catalogue Review`.

The population layer includes:

- Object ID
- Name
- Dynamical class
- Semi-major axis
- Eccentricity
- Inclination
- Perihelion estimate q = a*(1-e)
- Aphelion estimate Q = a*(1+e)
- Diameter
- Albedo
- Normalised density where available
- Taxonomy class
- Taxonomy complex
- Source row/range reference

This is a review-state population, not a publication-state dataset.

## Current workbook metrics

- Asteroid Master populated rows: 992
- Index & Log rows: 992
- Known-complete log rows: 5
- Missing-field log rows: 987
- Ready-for-source-gate rows: 5
- Missing-field logged rows: 987
- NEA / inner mission rows: 16
- LS integration rows: 8

## Index & Log

`Index & Log` now provides one row per populated asteroid.

Each row includes:

- Log ID
- Object ID and name
- Canon sheet and row number
- Canon data range
- Log index range
- Log type
- Known fields
- Missing fields
- Evidence status
- Source surface and source row/range
- Mission zone
- Owner/floor routing
- Review status
- Entry date
- Entry notes

This gives Cognigrex/retrieval and agent workflows a searchable index without duplicating or inventing science data.

## Missing fields

Missing values are intentionally indexed rather than guessed.

The current missing-field majority is expected because many rows in the current master schema lack at least one field such as density or complete orbit/source coverage.

## LS integration

`LS Integration Map` now maps workbook surfaces to:

- LS Web
- LS Desktop
- LS Go
- LS Drive
- LS Git
- Cognigrex / Retrieval
- Agent Workflow
- Archive / Context

This is a planning and handoff map only. It does not activate runtime services, exports, sync jobs, or deployments.

## Verification

Final scans run in this pass found no `#REF!` or `#N/A` formula errors in:

- `Asteroid Master`
- `Index & Log`
- `Mission Planning Toolkit`

A bounded spot check of `Body Catalogue Review` also found no `#REF!` or `#N/A` errors in the scanned review range.

## Guardrails

- `Rocks ECSV Sample 200k` remains the raw/staging source.
- `Body Catalogue Review` remains the current review surface.
- `Asteroid Master` is populated for review and enrichment, not external publication.
- `Index & Log` is a workbook control index, not an independent evidence source.
- Missing fields are preserved and routed for enrichment.
- GitHub and Slack updates are documentation/coordination only.
- No backend, runtime, sync, or deployment activation occurred in this pass.
