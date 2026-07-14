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

## Source basis

- Phase I Analysis: Mission 1 is the first coordinated field deployment of Mark III / Mark V systems, RFS, EMFF, Solar Hull, Free Flow and Cognigrex/RSOC integration.
- Phase II Analysis: Missions 2-12 use Mark III and Mark V units, with 3/5/7-unit batch envelopes and multi-unit redundancy logic.
- Phase II Analysis: each Mark unit has a 1 m3 capture-zone / interface volume.
- Operational Efficiency and Revenue Projections: deployment strategy extends through Missions 1-16 and beyond.
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

## Guardrail

Do not reduce M4/M5 and later capacity to +1 m3 per mission. Capacity must reference active Mark III / capture-capable units and tag-capacity fields separately.

## Open evidence note

Attached and retrieved files repeatedly evidence Mark III and Mark V. A direct Mark IV capacity-bearing source was not located in this correction pass. Treat Mark IV wording as a user/project shorthand or future source-backed override until a direct Mark IV source row is added.
