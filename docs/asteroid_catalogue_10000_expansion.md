# Asteroid Catalogue 10,000 Body Expansion

## Workbook

Live workbook:
https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit

## Completed in this pass

- Added `10,000 Body Expansion` as a bounded formula-derived expansion sheet.
- Added `Catalogue Expansion Control` as a human-readable control surface.
- Added a 10k candidate review preview block to `Catalogue Samples`.
- Added a 10k inner-system availability section to `Inner Solar System Knowns`.
- Updated source, extraction, QA, task, backend-sync, and handoff rows.

## 10,000 body control metrics

Current workbook values from `Catalogue Expansion Control`:

- Raw catalogue rows: 200,000
- 2,000 expansion rows: 2,000
- 10,000 expansion rows: 10,000
- 10k diameter-known rows: 7,348
- 10k taxonomy-known rows: 6,973
- 10k albedo-known rows: 7,348
- 10k density.value rows: 384
- 10k normalized density rows: 384
- 10k inner-system rows: 204
- Asteroid Master rows: 12

## 10k inner-system availability

Current workbook values from `Inner Solar System Knowns`:

- 10k NEA rows: 81
- 10k Hungaria rows: 123
- 10k Atira rows: 0
- 10k Aten rows: 5
- 10k Apollo rows: 42
- 10k Amor rows: 34
- 10k diameter-known inner rows: 125
- 10k taxonomy-known inner rows: 156

## Verification

The 10,000-body surface was checked in four bounded scan ranges:

- A1:T2500
- A2501:T5000
- A5001:T7500
- A7501:T10050

No formula-error rows were found in those scans.

The 10k candidate preview block in `Catalogue Samples` was also checked for formula errors.

## Guardrails

- `10,000 Body Expansion` is a review surface, not a final catalogue.
- `Catalogue Expansion Control` is a control/KPI surface.
- `Asteroid Master` remains the curated promotion target.
- Additional promotion remains held until candidate rows, orbit fields, source access, and caveat states are reviewed.
- This repository file is documentation only.
