# System Operating Register and Capacity Model

## Live workbook

https://docs.google.com/spreadsheets/d/148UObDgK_YsqHDbIkJo89yDvyDcgySTE4wQMEVGwga8/edit

## Purpose

This note records the user-approved operating defaults and exceptions now reflected in the workbook.

## New workbook surfaces

- `System Operating Register`
- `Credential Reference Register`
- `Mining Capacity Model`
- `Cluster Sequence Optimiser`

## Platform role model

| Surface | Role |
|---|---|
| Google Drive | Durable source, portfolio, workbook, document and reviewed export layer |
| GitHub | Operational RAM, routing, schema, code and implementation memory |
| romer.industries | Public and reviewed front-facing web layer |
| /operations workspaces | Operational workspace, tools, dashboards and review consoles |
| LightSpeed | Cognigrex host application name across LS components |
| LS Desktop | CPU, analysis workbench and Neo persistence layer |
| LS Go | Control and review layer |
| Cognigrex | Cross-analysis and automation host under LightSpeed |
| Achilles | Oversight, proof and release control |
| Athene | Reviewed public-facing output preparation |
| Neo | Desktop analysis and LS handoff lead |

## Credential handling

The workbook now tracks credential references, not secret values. No plaintext credential values should be stored in the workbook or committed to Git.

The `Credential Reference Register` records:

- Surface
- Page/workspace/agent
- Purpose
- Storage-location reference
- Owner
- Status
- Linked workbook range
- Linked Git/Drive/Web surface
- Secondary tracking surface

## Capacity rule

The `Mining Capacity Model` now encodes the current planning rule:

- Mission 1 base mining/collection capacity: 3 m3
- Each added unit adds +1 m3
- M1-M3 are treated as the detailed first branch loop
- M4-M16 are scaffolded inside the asteroid workbook
- Mission 17+ should roll up into operations / interplanetary supply chain workbook surfaces

## Delegation between workbooks

Asteroid workbook responsibilities:

- Determine candidate body and cluster combinations
- Maintain source capture and field comparisons
- Maintain mission branch/capacity assumptions
- Feed LS Desktop and Cognigrex with asteroid-side combinations

Operations workbook responsibilities:

- Optimise timing, travel cadence, route timing, tasking and operational windows
- Cross-check mission execution sequence against results from asteroid-side analysis

## Current next lane

1. Run source snapshots for `Mission 1 Source Capture`.
2. Compare source fields against workbook fields.
3. Log conflicts to `Appendix & Log`.
4. Use `Cluster Sequence Optimiser` for target/cluster combination review.
5. Route reviewed outputs through `Publish Review Queue` and LS surfaces.
