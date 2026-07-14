# Capacity Model Unit-Count Correction

## Summary

The operations workbook capacity model has been corrected from a per-mission increment model to a per-active-unit model.

The incorrect drift was:

```text
M1 = 3 m3
M2 = 4 m3
M3 = 5 m3
M4 = 6 m3
M5 = 7 m3
```

The corrected active-unit model is:

```text
M1 = 3 m3 active capture capacity
M2 = 7 m3 active capture capacity
M3 = 11 m3 active capture capacity
M4 = 15 m3 active capture capacity
M5 = 19 m3 active capture capacity
```

## Canon rule

Capacity is driven by active Mark III / capture-capable units, not mission index.

Each active Mark III / capture-capable unit contributes one 1 m3 capture-zone / mining-interface volume. The Phase II batch envelope remains recorded separately as a deployment/configuration reference.

## Mark lineage correction

Current / to-date mission hardware is Mark III and Mark V only.

Mark IV is not a current unit class for capacity or branch-ranking inputs. It is the planned post-mission successor / next model of Mark III, to be opened only when the post-mission successor-model surface is intentionally created.

Luke IV is an infrastructure/logistics node and must not be conflated with Mark IV.

## Source basis

- Phase I Analysis: Mission 1 is the first coordinated field deployment of Mark III / Mark V systems, RFS, EMFF, Solar Hull, Free Flow and Cognigrex/RSOC integration.
- Phase II Analysis: Missions 2-12 use Mark III and Mark V units, with 3/5/7-unit batch envelopes and multi-unit redundancy logic.
- Phase II Analysis: each Mark unit has a 1 m3 capture-zone / interface volume.
- Operational Efficiency and Revenue Projections: deployment strategy extends through Missions 1-16 and beyond.
- User correction: Mark IV is the next planned model of Mark III post-mission; current/to-date hardware remains Mark III and Mark V only.
- Prior project memory: Mission 1 active cap remains 3 m3; Mark III serial growth and Mark V tag companions expand per mission, not by a single capacity increment.

## Workbook surfaces patched

```text
Type1_Asteroid_Operating_Workbook
- Mining Capacity Model
- Mission 1 Detail
- Mission 2 Detail
- Mission 3 Detail
- Mission Sequence Planner
- Cluster Sequence
- Appendix & Log
- QA
- Open Build Tasks
```

## Assumption-drift guardrails

- Do not reduce M4/M5 and later capacity to +1 m3 per mission.
- Do not compute capacity from mission number.
- Do not use Mark IV as a current capacity-bearing unit.
- Do not conflate Luke IV with Mark IV.
- Do not treat historical/OCR Mark I-IV fragments as current canon without reconciliation.
- Do not write future planned models, facilities, regulatory steps, or operational states as current; label them To-date, Planned, Post-mission, Phase III, Future, or equivalent.

## Continuation lane

Continue M1-M3 cluster ranking using:

```text
M1 = 3 m3 active cap
M2 = 7 m3 active cap
M3 = 11 m3 active cap
current hardware = Mark III + Mark V only
Mark IV = post-mission successor model only
```
