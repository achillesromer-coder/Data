# Asteroid Catalogue Workbook Handoff — 2026-07-05

## Scope

This handoff records the live Google Sheet update for `Asteroid_Strategic_Mapping_Base_withRocks`.

Live workbook:
https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit

## Post-rename operating surface

The workbook has been shifted away from numbered/version-style operating tab names and now uses human-facing sheet names.

Key renamed surfaces:

- `0_README` → `Contents`
- `1_Sources` → `Sources`
- `2_Parameters` → `Parameters`
- `3_TaxonomyMap` → `Taxonomy Map`
- `4_Asteroid_Master` → `Asteroid Master`
- `5_Classification` → `Classification`
- `8_IEO_Orbit_Sample` → `IEO Orbit Sample`
- `Rocks_ECSV_sample200k` → `Rocks ECSV Sample 200k`
- `9_Canonical_Control` → `Control`
- `10_Source_Register_Ext` → `Source Register`
- `11_Extraction_Queue` → `Extraction Queue`
- `12_Field_Dictionary` → `Field Dictionary`
- `13_Provenance_Claims` → `Provenance Claims`
- `14_Version_Duplicate_Map` → `Version & Duplicate Map`
- `15_Agent_Handoff_Log` → `Agent Handoff Log`
- `16_Backend_Sync_Map` → `Backend Sync Map`

## Drive update completed

The workbook now includes the following operating/support tabs:

- `Catalogue Samples`
- `Task Roadmap`
- `Contents`
- `Field Dictionary`
- `Provenance Claims`
- `Backend Sync Map`
- `Agent Handoff Log`

Existing registers were updated to use the human-facing names.

## Systematic 1-5 status

1. Rename and human-facing operating titles — done.
2. Field Dictionary expansion — done for the raw Rocks A:T header set.
3. Provenance/proxy alignment — done through added claim rows.
4. Catalogue/sample expansion — active, with bounded preview blocks for taxonomy, diameter, albedo, density, and review candidates.
5. Master promotion + handoff — active, with promotion held until review.

## Catalogue logic

`Catalogue Samples` uses formula-driven bounded previews rather than copying the full raw import into operating surfaces.

Current sample families:

- Raw Rocks population metrics
- Main-belt inner / middle / outer counts
- Taxonomy-populated sample
- Diameter-populated sample
- IEO orbit sample
- Review preview using taxonomy plus diameter
- Albedo-known sample
- Density-known sample

## Guardrails

- `Rocks ECSV Sample 200k` remains the raw/staging input.
- `Asteroid Master` remains the curated promotion target.
- Taxonomy, albedo, density, metal-fraction, and mass outputs remain operational proxies unless source-backed and reviewed.
- No unsupported public claim is created by this pass.
- No runtime activation, deployment, or destructive workbook action was performed.
- Existing raw and calculation lanes were kept structurally intact.

## Next queue

1. Review the `Catalogue Samples` query outputs visually in Google Sheets.
2. Add source-version/access metadata to `Field Dictionary` and `Source Register`.
3. Review taxonomy/density/albedo claims in `Provenance Claims`.
4. Promote only reviewed shortlist rows into `Asteroid Master`.
5. Prepare future schema export only after field dictionary validation.

## Suggested future repository artefacts

- `schemas/asteroid_catalogue_field_dictionary.json`
- `data/asteroid/catalogue_samples.csv`
- `docs/asteroid_catalogue_ingestion.md`
- `docs/asteroid_catalogue_operating_notes_2026-07-05.md`

## Status

Git handoff updated as documentation only. No code execution or runtime activation.