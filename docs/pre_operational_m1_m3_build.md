# Pre-Operational Expansion and Missions 1-3 Build

## Workbooks

- Asteroid workbook: `Asteroid_Strategic_Mapping_Base_withRocks`
- Operations workbook: `Type1_Asteroid_Operating_Workbook`

## Completed surfaces

The operations workbook now contains the pre-operational expansion and first-loop mission surfaces:

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

The operations workbook now owns the mission sequence, capacity model, start-window comparison, cluster sequencing, pre-operational task closure and LS/Cognigrex handoff.

## First three-mission loop

The first loop is represented as M1, M2 and M3 detail pages.

- M1: primary case-study/manual seed and first branch surface; planning capacity 3 m3.
- M2: follow-on reinforcement or extension branch; planning capacity 4 m3.
- M3: consolidation and first-loop review/export branch; planning capacity 5 m3.

The pages reference candidate branches such as Eros, Apophis, Castalia, Toutatis, Anteros and Apollo/Apl without asserting final target selection.

## Source-backed state

Eros is carried as the first source-backed orbit baseline from the asteroid workbook's `Cluster Source Capture` surface. Other candidates remain route-ready/payload-pending until SBDB/Horizons payload expansion is completed.

## Open tasks now explicit

The `Open Build Tasks` sheet tracks:

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
- Git acts as operational routing/schema/docs memory; Drive workbooks remain durable backend/source surfaces.
