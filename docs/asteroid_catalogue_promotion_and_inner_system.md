# Asteroid Catalogue Promotion and Inner-System Notes

## Workbook

Live workbook:
https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit

## Completed in this pass

1. Added a small reviewed promotion batch to `Asteroid Master`.
2. Added `2,000 Body Expansion` as a bounded formula-derived expansion surface.
3. Added `Inner Solar System Knowns` as the consolidated orbit-knowns mapping surface.
4. Updated `Source Register` with new sheet source rows.
5. Updated `Extraction Queue` with expansion and knowns tasks.
6. Updated `QA` with new gates for promotion, 2,000 expansion, and inner-system knowns.
7. Updated `Task Roadmap`, `Backend Sync Map`, and `Agent Handoff Log`.

## Promotion batch

Rows 4 to 13 in `Asteroid Master` were populated from the `Catalogue Samples` review preview.

Promoted fields used:

- Object ID
- Name
- Dynamical class
- Diameter
- Albedo
- Taxonomy class
- Taxonomy complex
- Workbook-source link

Orbit fields were left blank for this batch because the review-preview source block did not include those columns.

## 2,000 body expansion

`2,000 Body Expansion` is formula-derived from `Rocks ECSV Sample 200k` and keeps the raw A:T field structure.

This sheet is a review surface, not a final catalogue.

## Inner Solar System Knowns

`Inner Solar System Knowns` contains:

- Inner-system class counts.
- Orbit-class distribution.
- A 500-row inner-system sample from NEA and Hungaria-labelled rows.

Current visible counts recorded in the workbook include:

- NEA class rows: 1,944
- Hungaria rows: 2,714
- Atira rows: 3
- Aten rows: 151
- Apollo rows: 983
- Amor rows: 807
- Diameter-known inner rows: 630
- Taxonomy-known inner rows: 917

## Review status

The next promotion batch remains held until class labels, proxy caveats, and source-access rows are reviewed.