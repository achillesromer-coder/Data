# Asteroid Catalogue Canon Collapse and Mission Toolkit Notes

## Live workbook

https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit

## Purpose of this pass

This pass begins the move from expansion-building into canon workbook completion.

The earlier expansion sheets existed because the working prompts asked for staged population growth: first a successful small promotion batch, then a 2,000-body expansion, then a 10,000-body expansion. Those were appropriate while validating formula behaviour, bounded review surfaces, and agent routing. They are not ideal as permanent canon titles, because count-based sheet names behave like version labels.

## Canon title collapse applied

- `10,000 Body Expansion` is now `Body Catalogue Review`.
- `2,000 Body Expansion` is now `Body Expansion Archive`.
- `Catalogue Expansion Control` is now `Catalogue Control`.

The old labels remain represented in the workbook logs and control map. No source surface was deleted.

## Current canon live surfaces

- `Contents`
- `Catalogue Control`
- `Asteroid Master`
- `Body Catalogue Review`
- `Catalogue Samples`
- `Mission Planning Toolkit`
- `Inner Solar System Knowns`
- `Rocks ECSV Sample 200k`
- `Source Register`
- `Field Dictionary`
- `Provenance Claims`
- `QA`
- `Task Roadmap`
- `Backend Sync Map`
- `Agent Handoff Log`

## Mission Planning Toolkit

A canon mission-facing sheet was added: `Mission Planning Toolkit`.

It maps the current review population into practical planning zones:

- Interior / IEO
- Aten NEA
- Apollo NEA
- Amor NEA
- Hungaria Boundary
- Mars-Crosser
- Inner Main Belt

For each zone the sheet tracks available rows, diameter coverage, taxonomy coverage, albedo coverage, density coverage, planning use, LS tooling note, gate, owner/floor, and status.

## Current mission-zone counts in the 10k review surface

- Interior / IEO: 0
- Aten NEA: 5
- Apollo NEA: 42
- Amor NEA: 34
- Hungaria Boundary: 123
- Mars-Crosser: 108
- Inner Main Belt: 3,562

These are workbook-derived counts from the current `Body Catalogue Review` surface. They are not external mission-validity claims.

## Completion plan

1. Keep `Rocks ECSV Sample 200k` as the protected raw/staging source.
2. Use `Body Catalogue Review` as the current high-volume review surface.
3. Use `Catalogue Samples` and `Mission Planning Toolkit` to prepare candidate batches.
4. Promote only reviewed rows into `Asteroid Master`.
5. Enrich orbit fields from existing raw orbit columns first, then source-check through registered services before stronger claims.
6. Keep version/count wording in logs, not live titles.
7. Retain archives and contextual docs; collapse their meaning into canon rows rather than deleting them.
8. Use GitHub for documentation/schema handoff only unless runtime activation is explicitly authorised.

## Status

This is a documentation-only handoff. No backend, runtime, wallet, deployment, or destructive file operation is activated by this note.