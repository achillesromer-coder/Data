# Asteroid Catalogue Ingestion Notes

## Workbook

Live workbook:
https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit

## Current operating sheets

- `Contents`
- `Sources`
- `Source Register`
- `Extraction Queue`
- `Field Dictionary`
- `Provenance Claims`
- `Catalogue Samples`
- `QA`
- `Task Roadmap`
- `Backend Sync Map`
- `Agent Handoff Log`

## Ingestion posture

`Rocks ECSV Sample 200k` is the raw/staging import. It is not the curated catalogue by itself.

`Catalogue Samples` is the preview and review surface. It contains bounded formula blocks for taxonomy, diameter, albedo, density, and review candidates.

`Asteroid Master` is the curated destination. Rows should be added only after review gates are satisfied.

## Review gates

The live workbook now uses the `QA` sheet for review gates:

- Formula check for the sample surface.
- Field coverage check for the raw header set.
- Source access and release metadata check.
- Provenance and caveat check.
- Curated-row review hold.
- Documentation-only GitHub handoff.
- Slack coordination handoff.

## Source access rows

`Source Register` contains `ACCESS-001` to `ACCESS-006`, covering:

- SsODNet ssoBFT
- SsODNet ssoCard
- JPL SBDB Query
- NEOWISE physical catalogue
- LCDB
- Rocks ECSV Sample 200k

These are review rows. They do not claim that every external source was freshly checked in this pass.

## Promotion rule

Before adding rows to `Asteroid Master`, the object should have:

1. A source ID.
2. Field coverage from the dictionary.
3. Evidence status.
4. Caveat status for taxonomy, albedo, density, mass, and volume-derived values.
5. A reviewer or floor owner.

## Repository status

This repository note is documentation only. It records workbook structure and review flow.