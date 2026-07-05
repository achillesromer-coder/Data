# Asteroid Catalogue Workbook Handoff — 2026-07-05

## Scope

This handoff records the live Google Sheet update for `Asteroid_Strategic_Mapping_Base_withRocks`.

Live workbook:
https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit

## Drive update completed

The workbook was updated with two new operating tabs:

- `Catalogue Samples`
- `Task Roadmap`

Existing support registers were also extended:

- `9_Canonical_Control`
- `10_Source_Register_Ext`
- `11_Extraction_Queue`
- `15_Agent_Handoff_Log`
- `16_Backend_Sync_Map`

## Catalogue logic

`Catalogue Samples` uses formula-driven bounded previews rather than copying the full raw import into operating surfaces.

Current sample families:

- Raw Rocks population metrics
- Main-belt inner / middle / outer counts
- Taxonomy-populated sample
- Diameter-populated sample
- IEO orbit sample from the existing inner-orbit tab
- Future metallicity, density, albedo, and strategic shortlist sample queues

## Guardrails

- `Rocks_ECSV_sample200k` remains the raw/staging input.
- `4_Asteroid_Master` remains the curated promotion target.
- Taxonomy, albedo, density, metal-fraction, and mass outputs remain operational proxies unless source-backed and reviewed.
- No public resource/yield claim is created by this pass.
- No backend activation, deployment, or destructive workbook action was performed.
- Existing calculation tabs were not renamed to avoid formula-reference disruption.

## Next queue

1. Review the `Catalogue Samples` query outputs visually in Google Sheets.
2. Expand `12_Field_Dictionary` with exact field types, units, and validation rules.
3. Review taxonomy/density/albedo claims in `13_Provenance_Claims`.
4. Promote only reviewed shortlist rows into `4_Asteroid_Master`.
5. Prepare future schema export only after field dictionary completion.

## Suggested future repository artefacts

- `schemas/asteroid_catalogue_field_dictionary.json`
- `data/asteroid/catalogue_samples.csv`
- `docs/asteroid_catalogue_ingestion.md`

## Status

Git handoff created as documentation only. No code execution or backend activation.