# Workbook Split: Asteroid Database vs Operations Sequencing

Date: 2026-07-14

## Purpose

The asteroid workbook has been refocused as the canonical asteroid/body/source/cluster evidence workbook. Mission sequencing, capacity, launch-window comparison, route/path logic, and LightSpeed/Cognigrex operational handoff have moved into the operations workbook.

## Canon workbooks

| Workbook | URL | Canon role |
|---|---|---|
| Asteroid_Strategic_Mapping_Base_withRocks | https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit | Asteroid/body catalogue, inner-system map, cluster library, source gate, source capture, enrichment queue, evidence/conflict log |
| Type1_Asteroid_Operating_Workbook | https://docs.google.com/spreadsheets/d/1Uy04F5gtf2mXf9tDmAyIvNrsCn1kn4Csa2oc-skSZxY/edit | Mission sequence, capacity, branch/window comparison, route/path, cluster sequence, LS/Cognigrex handoff |

## Asteroid workbook retained/refocused surfaces

- Cluster Source Intake
- Cluster Library
- Cluster Source Gate
- Cluster Review Pack
- Cluster Source Capture
- Cluster Enrichment Queue
- Operations Export Interface
- Inner Solar System Knowns
- Asteroid Master
- Body Catalogue Review
- Appendix & Log
- Source Register / QA / Backend Sync Map / Publish Review Queue

## Operations workbook created/refactored surfaces

- Operations Control
- System Operating Register
- Credential Reference Register
- Mission Architecture Control
- Mining Capacity Model
- Mission Scenario Matrix
- Mission Sequence Planner
- Mission Flight Windows
- Mission Operations Path
- Cluster Sequence
- Asteroid Workbook Interface
- Appendix & Log
- QA
- Backend Sync Map
- Publish Review Queue
- LS Cognigrex Handoff

## Migration actions

The following asteroid-workbook mission-operation tabs were moved/refactored into the operations workbook and then deleted from the asteroid workbook after verification:

- Mission 1 Control
- Mission Architecture Control
- System Operating Register
- Credential Reference Register
- Mining Capacity Model
- Cluster Sequence Optimiser
- Mission 1 Scenario Matrix
- Mission Sequence Planner
- Mission 1 Flight Windows
- Mission 1 Operations Path
- Mission Planning Toolkit
- LS Integration Map

## Operating principles

- Asteroid workbook owns body data, source capture, evidence, conflicts, and cluster candidate rows.
- Operations workbook owns M1-n mission logic, capacity, timing, route/path, node/facility sequencing, LS Desktop/Go and Cognigrex handoff.
- Drive is durable source, portfolio and workbook layer.
- Git is operational RAM, routing, schemas, documentation and scaffold memory.
- Public/web outputs route through reviewed publish queues.
- No physical/mining/trajectory claims are promoted from source routes alone.
- Access values are not stored in shared workbooks or committed to Git; shared registers record references only.

## Current source-backed baseline

Eros is the first source-backed orbit baseline from SBDB object/orbit capture. Physical fields remain proxy/pending until physical-source capture and comparison are complete.
