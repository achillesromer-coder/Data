# Mission Architecture Return and Scenario Matrix

## Workbook

Live workbook:
https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit

## Purpose

This note records the returned manual-review decisions and the resulting workbook restructure. The asteroid workbook now treats Mission 1 as an operational pre-mission pathway that can become a post-operation case study and operating manual, while still keeping source capture, mismatch logging, and publish review traceable.

## New or changed workbook surfaces

- `Appendix & Log` renamed from `Index & Log` and kept as the compact searchable index/log surface.
- `Mission Architecture Control` captures returned A-J decisions and workbook interpretation.
- `Mission 1 Scenario Matrix` provides side-by-side start-window comparison for June 2027, January 2028, and August 2028.
- `Mission Sequence Planner` maps M1 to M3 branch logic for the first three missions.
- `Mission 1 Source Capture` provides SBDB-first capture rows and a Cognigrex comparison route.
- `Publish Review Queue` routes Drive/Git/LS/Cognigrex output artefacts.

## Scenario logic

The three dates are now comparative start states:

- `1.6.27.*` for the June 2027 branch.
- `1.1.28.*` for the January 2028 branch.
- `1.8.28.*` for the August 2028 branch.

The matrix is designed so M2 and M3 are branch-dependent rather than assumed to use the same secondary bodies. Secondary targets remain `x/y/z` until source capture and trajectory-window analysis populate the reachable body set.

## Apophis branch

Apophis has been added as a strategic PHA tag-case row across all three start windows. The workbook raw source row is `Rocks ECSV Sample 200k!A12146:T12146`. Current workbook-known fields include orbit, diameter, albedo, and taxonomy; density remains missing in the workbook raw row.

## Source capture policy

The source-capture flow is:

1. Build route.
2. Pull payload.
3. Compare against workbook fields.
4. Log conflicts in `Appendix & Log` and `Mission 1 Source Capture`.
5. Update canon rows only after Cognigrex comparison and unresolved conflict handling.

External payload values do not automatically overwrite workbook values.

## Publish flow

`Publish Review Queue` now tracks workbook outputs into Drive/Git/LS/Cognigrex review paths. This replaces passive holding with a visible export/review queue while preserving source and conflict traceability.

## Current verification

- `Mission 1 Scenario Matrix!A1:AF80` scanned clean for `#REF!` and `#N/A`.
- `Mission 1 Source Capture!A1:V90` scanned clean for `#REF!` and `#N/A` after header correction.
- Apollo shorthand was patched from `Apo` to `Apl` to avoid collision with Apophis.

## Next execution lane

The next workbook lane is automated SBDB payload capture for the `Mission 1 Source Capture` rows, followed by field comparison and conflict logging.
