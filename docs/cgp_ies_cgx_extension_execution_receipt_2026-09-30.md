# CGP-IES → Cognigrex/.CGX functional implementation receipt — 2026-09-30

**Role of this file:** execution/provenance mirror only. It is **not** a new semantic master and must not supersede the living owners.

## Current owners and boundaries

- Shared extension target: `Cognigrex.cgx:/extensions/cgp-ies` (parent-carrier hydration pending).
- Executable source / generator / validator / runtime-preflight owner: `achillesromer-coder/LightSpeed`.
- Finite lifecycle/equilibrium living owner: Google Drive `Type 1 Romer Cognigrex`, sheet `163_EQUILIBRIUM_LIFECYCLE_GOV_v0_1`.
- Existing lifecycle execution mirror: `Data/docs/equilibrium_lifecycle_execution_mirror.md`.
- ACR3: historical transition/provenance only; this receipt does not reopen ACR3 or create a new handoff authority.

## Implemented source and runtime path

LightSpeed commits:

- `63e54c975f659d8146d7ac260d3eb8143d5e8c11` — shared CGP-IES extension registry, policy pack, fixtures, resolver, child-generator binding, template validation.
- `c5ce265b20eb38eb6ff4a075c0633112f6259aa6` — consequential-action custodial preflight executable.
- `d13c098d963ff67714c97f1147402836ddc8434f` — workflow registry binding.
- `37b18fc04bf4a23581f11df4c39eb55a11b35337` — work-mode binding.
- `46a40690a8d81c4925e1a8e00cbccc4fea89a1df` — CGX core toolkit capability binding.
- `f05abab606d87388a2059ee17cf657eca5847bda` — GitHub validation workflow.
- `08efc390dd3fa8de3b2f3140d035b8fa24a8a3b0` — current-CGX chat-close handoff.
- `686012036be45f3950dc11a6fcebfaa2b6a3c460` — proposed owner-confirmation values.

GitHub Actions run `36680108939`: **SUCCESS**.

## Functional architecture

One parent source is referenced by child carriers rather than duplicated:

```text
Cognigrex.cgx:/extensions/cgp-ies
    ├── Romer.cgx      -> extensions/bindings.json
    ├── Eco.cgx        -> extensions/bindings.json
    └── EMASSC.cgx     -> extensions/bindings.json
          └── LS.cgx   -> extensions/bindings.json
```

The child binding carries the source pointer, default mode, allowed modes and fail behaviour; it does not copy the policy body or transfer authority.

Extension modes:

```text
OFF < OBSERVE < ADVISE < GATE < ENFORCE_SAFETY
```

`ENFORCE_SAFETY` is restricted to declared hard safety, authority, replication, containment, stop and life/ecology-preservation controls. It is not general moral or semantic sovereignty.

## Consequential-action behaviour

The resolver evaluates domain, execution depth, cascade class and task tags. Current proposed defaults:

- Römer: ADVISE
- Eco-Grex: ADVISE
- EMASSC: OBSERVE
- LightSpeed: OBSERVE

Execute/build/publish work at cascade C2+ escalates to at least GATE. High-consequence custodial tags also escalate. Replication-control / hard-stop / containment / life-support / hazard-control execution may escalate to the narrow ENFORCE_SAFETY mode.

At GATE or above, missing source verification, missing authority confirmation or an unresolved hard admissibility predicate returns **HOLD**.

## Verified fixture coverage

Six current fixture scenarios cover:

1. Römer C3 resource extraction / autonomous fleet → GATE.
2. Eco field observation C1 → ADVISE.
3. Eco ecosystem intervention / life impact C2 → GATE.
4. EMASSC hypothesis simulation C1 → OBSERVE.
5. LightSpeed replication-control C3 → ENFORCE_SAFETY.
6. LightSpeed runtime read C0 → OBSERVE.

## Open gates

This receipt does **not** claim:

- that the S91/v1.61 parent Recovery carrier has been mutated;
- that `Cognigrex.cgx:/extensions/cgp-ies` is yet present in a promoted carrier;
- that Romer/Eco/EMASSC/LS child carriers have been regenerated with the new binding;
- that the policy is canonical rather than pre-canonical;
- that any standards alignment constitutes certification.

The exact next gate is: owner review of `cgp_ies_owner_confirmation_values.json`, then a new parent descendant mutation + verifier + packed reopen/hash readback, followed by child regeneration and runtime binding verification.

## No-parallel-master rule

This file is a receipt. It should be retired to ordinary provenance once the parent carrier and DBR record contain the durable promoted state.
