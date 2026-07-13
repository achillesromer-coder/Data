# Mission 1 Source Gate and Review Pack

## Workbook

Live workbook:
https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit

## Completed in this pass

Added three canon Mission 1 operating sheets:

- `Mission 1 Source Gate`
- `Mission 1 Review Pack`
- `Mission 1 Enrichment Queue`

## Mission 1 Source Gate

`Mission 1 Source Gate` routes the known-complete Mission 1 candidate rows to external source-review links.

Rows are pulled from `Mission 1 Target Library` where `Review_Status = SOURCE-GATE REVIEW`, ordered by `Rank_Score` descending.

Route columns now include:

- SBDB object API route
- SBDB query API route
- Horizons June 2027 route
- Horizons January 2028 route
- Horizons August 2028 route
- MPC object route
- ESA NEOCC route
- Source gate status
- Gate notes
- Next action

## Mission 1 Review Pack

`Mission 1 Review Pack` currently includes the top 24 source-gate rows, beginning with:

1. Castalia
2. Toutatis
3. Anteros
4. Apollo
5. Cerberus
6. Ganymed
7. Geographos
8. Icarus
9. Toro
10. Aten

The pack is review-state only. It is not a final target list.

## Mission 1 Enrichment Queue

`Mission 1 Enrichment Queue` splits follow-up work into source-specific rows:

- SBDB object source-gate pulls for each review-pack row.
- Horizons January 2028 ELEMENTS checks for each review-pack row.

This keeps source capture auditable and prevents overwriting workbook source values until the payload and field mapping are reviewed.

## Source basis

JPL's SBDB API is documented as providing machine-readable data for specified small bodies, including object identification, orbital data, selected physical data, and ancillary data such as close approaches and virtual impactor information. The SBDB API requires one of `sstr`, `spk`, or `des` for object lookup.

JPL's Horizons API is documented as supporting ephemeris outputs including observer, vector, and elements output types through URL parameters.

## Guardrails

- API links are routes, not imported source payloads.
- No SBDB/Horizons values were merged into canon fields in this pass.
- No delta-v, accessibility, launch, mining-feasibility, legal, safety, procurement, or operational claim is created.
- External payload capture remains held behind field mapping and review.
