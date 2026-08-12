# InterSol Watch Tower digital-twin boundary — 2026-08-13

Status: **SCHEMA / PARAMETRIC BUILD ACTIVE — IMPLEMENTATION BLOCKED**

Canonical operational source: **Type 1 Romer Cognigrex** Google workbook. This Git branch is a machine-readable review mirror; it does not replace the workbook or owner source geometry.

## Current authority order

1. Owner-current Watch Tower sketches/instructions and attributable current FreeCAD geometry.
2. Current Type 1 Romer Cognigrex qualification, source, object, edge, task and gate surfaces.
3. Historical owner-authored InterSol records (2022–2023) for provenance and functional lineage.
4. Derived twin schemas/models.
5. Locked Watch Tower artistic render for aesthetic/material/lighting language only.

## Current topology lock

- `WT-T`: central tower.
- Exactly two primary tower cable-node elevations: `WT-A` and `WT-C`.
- `WT-A-F1..F4`: four face-specific anchors at A.
- `WT-C-F1..F4`: four face-specific anchors at C.
- `WT-L1..L4`: four left-wing physical poles.
- `WT-R1..R4`: four right-wing physical poles.
- `WT-E`: physical pole/node referenced by the current FreeCAD top view; exact identity/equivalence and coordinates remain source-extraction blockers.
- Mirrored wing architecture is a design/QA constraint, not permission to fabricate missing coordinates.
- Exact cable targets and counts derive from the resolved edge graph, not from artistic renders.

## Geometry hold

The Type1 FreeCAD foundation kit dated 2026-08-11 created a simple Watch Tower anchor because no attributable current geometry had then been located. Its 60 m total height, 18 m envelope and +250 m X relationship are explicitly placeholder values. They remain useful provenance and must not be promoted into the current Watch Tower.

The immediate G1 task is therefore read-only extraction of the exact current FCStd geometry into the canonical object and edge registries, with revision/hash and explicit unresolved fields.

## Material and subsystem boundary

Owner-current material routing is recorded as a classification rule only:

- solid structural thickness `>=120 mm` → reinforced-concrete family;
- thinner structural elements → steel-frame family by default;
- glazing, cables, coatings, membranes, gaskets, Solar Hull and living systems remain dedicated families.

This rule does **not** size or certify any member.

Current subsystem intents include:

- reinforced-concrete base/core and tower;
- emergency spiral stair within the core;
- protected laminated exterior glazing and observation-deck guardrail;
- smooth shallow-curved roof geometry;
- terrestrial Solar Hull application as a separately qualification-gated R&D skin;
- roof garden/living canopy with time-varying growth, wet-mass, windage, irrigation and maintenance states;
- graph-driven cable topology with nominal, weather-slack, safety-relax, N-1 cable-loss and maintenance-isolated state classes;
- condition/telemetry/data layer for the eventual operational twin.

## Historical lineage now recovered

The 2022 Inter-Sol Development record explicitly describes a dedicated mission-control base and air-control tower intended to monitor, track and command missions and oversee landing/launch infrastructure and a prospective remote airstrip. The April 2023 InterSol overview carries this mission-control headquarters + air-control-tower concept forward. These records establish functional lineage only; they do not establish current geometry, site, partners, approvals or engineering readiness.

## Gate posture

- **G0 — READY / LOCKED:** identity, provenance and authority order.
- **G1 — PARTIAL / ACTIVE:** exact current FCStd geometry/object/edge package.
- **G2 — BLOCKED:** engineering basis, current standards and launch/security hazard basis.
- **G3 — BLOCKED:** coupled structural/cable/wind/glazing/roof/living-system screening.
- **G4 — BLOCKED:** materials, components and complete assembly validation.
- **G5 — BLOCKED:** repeatability, inspection and commissioning model.
- **G6 — BLOCKED:** integrated fire/egress/access/rescue/electrical/water/security/O&M safety.
- **G7 — CONTROLLED HOLD:** implementation/as-built/publication promotion.
- **P∞ — FOUNDATION NEEDED:** immutable hashes, inspection/maintenance history, revalidation and rollback.

## Repository contract

This branch introduces **schemas and interpretive boundaries only**. It intentionally does not commit guessed Watch Tower coordinates, cable targets, member sizes, blast/ballistic ratings, Solar Hull performance values, site data or public deployment state.

The next machine-data object should be created only after the current FCStd source is located and read back into the workbook object/edge registry.