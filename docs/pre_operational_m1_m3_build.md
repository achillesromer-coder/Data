# Pre-Operational Expansion and Missions 1-3 Build

## Workbooks

- Asteroid workbook: `Asteroid_Strategic_Mapping_Base_withRocks`
- Operations workbook: `Type1_Asteroid_Operating_Workbook`

## Completed surfaces

The operations workbook contains the pre-operational expansion and first-loop mission surfaces:

- `Pre-Operational Expansion`
- `Mission 1 Detail`
- `Mission 2 Detail`
- `Mission 3 Detail`
- `Open Build Tasks`
- `Readiness Gates`
- Updated `Asteroid Workbook Interface`
- Updated `Cluster Sequence`
- Updated `Operations Control`
- Updated `Publish Review Queue`
- Updated `LS Cognigrex Handoff`

## Mission role separation

The asteroid workbook remains the asteroid/body catalogue, inner-system map, cluster library, source gate, source capture and evidence/conflict surface.

The operations workbook owns mission sequence, capacity model, start-window comparison, cluster sequencing, pre-operational task closure and LS/Cognigrex handoff.

## Current hardware canon

Current / to-date mission hardware is Mark III and Mark V only.

Mark IV is the planned post-mission successor / next model of Mark III. It is not a current capacity input and must not be consumed by M1-M3 ranking.

Luke IV is a facility/logistics layer and must not be conflated with Mark IV.

## First three-mission loop

The corrected first-loop active-capacity model is:

```text
M1 = 3 m3 active capture capacity
M2 = 7 m3 active capture capacity
M3 = 11 m3 active capture capacity
```

The pages reference candidate branches such as Eros, Apophis, Castalia, Toutatis, Anteros and Apollo/Apl without asserting final target selection.

## Current pre-rank state

The first-loop `Cluster Sequence` now records a pre-rank only:

```text
CS-001 Eros: PRE-RANK 1 baseline/control row only
CS-002 Apophis: PRE-RANK 2 strategic tag-case / source pending
CS-003 Castalia: PRE-RANK 3 high candidate / payload pending
CS-004 Toutatis: PRE-RANK 4 PHA comparison / payload pending
CS-005 Anteros: PRE-RANK 5 candidate / payload pending
CS-006 Apollo/Apl: PRE-RANK 6 candidate / payload pending
CS-007 Selected branch: NO FINAL SELECTION / PRE-RANK ONLY
```

## Source-backed state

Eros is carried as the first source-backed orbit baseline from the asteroid workbook's `Cluster Source Capture` surface. It is a baseline/control row only; physical-parameter and neighbour checks remain required before branch selection.

Apophis remains a strategic PHA tag-case branch. It is not mine-first. SBDB payload capture, safety/context comparison and secondary-body pathing remain required.

Castalia, Toutatis, Anteros and Apollo/Apl remain route-ready/payload-pending until SBDB/Horizons payload expansion is completed.

## Open tasks now explicit

The `Open Build Tasks` sheet tracks:

- Mark IV canon correction and drift guardrail
- Apophis source capture
- top candidate source payloads
- Horizons window batch
- M1/M2/M3 detail completion
- operations dashboard summary
- publish/export split
- LS/Cognigrex handoff protocol
- split migration QA closure

## Readiness gates

The `Readiness Gates` sheet separates source identity, window comparison, capacity, cluster sequence, M1 case-study, M2/M3 loop, LS/Cognigrex handoff and publish/export gates.

## Guardrails

- No plaintext credentials are stored.
- No public output is triggered from workbook state alone.
- No physical proxy fields are promoted without source comparison.
- No final target, trajectory, delta-v, window suitability or operational execution claim is inferred from workbook rows alone.
- Capacity uses active Mark III/capture-capable units, not mission number.
- Current hardware is Mark III + Mark V only.
- Mark IV is post-mission successor lineage only.
- Git acts as operational routing/schema/docs memory; Drive workbooks remain durable backend/source surfaces.
