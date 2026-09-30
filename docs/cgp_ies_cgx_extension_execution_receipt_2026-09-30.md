# CGP-IES → Cognigrex/.CGX functional implementation receipt — 2026-09-30

**Role of this file:** execution/provenance mirror only. It is **not** a semantic master and does not supersede the living owners.

## Current owners and boundaries

- Shared extension target: `Cognigrex.cgx:/extensions/cgp-ies`.
- Executable source / generator / validator / runtime-preflight owner: `achillesromer-coder/LightSpeed`.
- Review branch: `cgp-ies-functional-handoff-20260930`.
- Draft PR: LightSpeed #57 — `CGP-IES: source-driven custodial extension and guarded parent handoff`.
- Finite lifecycle/equilibrium living owner: Google Drive `Type 1 Romer Cognigrex`, sheet `163_EQUILIBRIUM_LIFECYCLE_GOV_v0_1`.
- Existing lifecycle execution mirror: `Data/docs/equilibrium_lifecycle_execution_mirror.md`.
- ACR3: historical transition/provenance only; this receipt does not reopen ACR3 or create a new handoff authority.
- Parent Recovery authority remains exact S91/v1.61; it has **not** been overwritten or promoted by this work.

## Source-driven extension architecture

```text
Cognigrex.cgx:/extensions/cgp-ies
    ├── registry / toggle + escalation
    ├── policy
    ├── terminology
    ├── domain-adapters
    ├── decision-receipt schema
    ├── fixtures
    └── owner-confirmation register
          │
          ├── Romer.cgx  -> extensions/bindings.json (REFERENCE)
          ├── Eco.cgx    -> extensions/bindings.json (REFERENCE)
          └── EMASSC.cgx -> extensions/bindings.json (REFERENCE)
                └── LS.cgx -> extensions/bindings.json (REFERENCE)
```

Children do not carry a duplicate policy body. Bindings contain source pointers, modes, fail behaviour and component references only.

## Functional expansion completed on review branch

Added:

- `cgp_ies_terminology_map.json` — neutral inter-special terminology + epistemic states.
- `cgp_ies_domain_adapter_registry.json` — Romer/Eco/EMASSC/LightSpeed applicability.
- `cgp_ies_decision_receipt_schema.json` — affected parties, agency, representation, ceiling, dissent, inheritance and protective-perpetuity receipt.
- `cgp_ies_parent_extension_manifest.json` — exact-S91 guarded parent install contract.
- `scripts/build_cgp_ies_parent_candidate.py` — exact-S91 descendant builder that cannot overwrite Recovery and emits PRE_CANONICAL candidate only.

Refactored:

- `resolve_cgx_extensions.py` now hydrates applicable checks and hard predicates from parent-owned source files.
- `cgx_custodial_preflight.py` no longer duplicates the eight hard predicates in Python.
- `build_cgx_domain_children.py` emits reference-only terminology/adapter/receipt/policy pointers and an inheritance rule preventing a nested child from weakening required GATE/ENFORCE_SAFETY.
- validators now enforce the source components and exact S91 parent-seed boundary.

Fixtures expanded from 6 to **18**, including communications loss, civilization loss, successor restart, incoming/outgoing contact, planetary defence, inter-special communication, habitat translocation, artificial moral-patient uncertainty, pristine worlds, hazard closure and Raphael conceptual-boundary cases.

## Toggle modes

`OFF < OBSERVE < ADVISE < GATE < ENFORCE_SAFETY`

`ENFORCE_SAFETY` remains narrow: pre-declared replication/stop/containment/life-support/hazard controls only. It is not general moral sovereignty.

## Verification

- Branch CI run `36695178269`: **SUCCESS**.
- Pull-request CI run `36695215117`: **SUCCESS**.
- Verified steps include:
  - CGX domain template validation;
  - CGP-IES 18-scenario fixture validation;
  - guarded parent-candidate builder compile;
  - assurance fixtures;
  - consequence-preflight chain;
  - InterSol assurance route;
  - low-consequence runtime preflight;
  - unclassified C2 execution fail-closed behaviour.

## Owner / governance review boundary

`cgp_ies_owner_confirmation_values.json` now exposes **OC-001..OC-020**. Added discussion values include:

- protective perpetuity baseline and candidate protective functions;
- contact default;
- artificial moral-patient uncertainty;
- founder/architect authority;
- neutral inter-special terminology;
- multidimensional agency / explicit representation;
- successor restart;
- adaptive translation;
- child extension inheritance.

None is canonical merely because functional code exists.

## Parent / child promotion sequence

1. Review and explicitly confirm/amend OC-001..OC-020.
2. Materialize exact S91 Recovery bytes:
   - State `S91`, release `v1.61`
   - SHA-256 `1138da5af4e1c66eb60120dd050e2037fc8d7799a9ccebb01ad48089b234785f`
3. Run the guarded parent candidate builder to create a NEW descendant.
4. Independently verify canonical verifier + DBR continuity + packed reopen/hash + extension content/source integrity.
5. Explicitly decide whether the exact candidate becomes the next Recovery authority.
6. Only after promotion, regenerate `Romer.cgx`, `Eco.cgx`, `EMASSC.cgx`, `LS.cgx`.
7. Verify child `extensions/bindings.json` remains reference-only and cannot weaken required consequence escalation.
8. Bind live Task_ID/Run_ID/DBR receipts and begin object-level parameterisation.

## Current object-level implementation frontier

The architecture phase is sufficiently mature that the next highest-value work is real-object binding, not more generic doctrine:

- stable `Object_ID`;
- affected-party / representation state;
- evidence-state / source;
- effective ceilings;
- MVSL;
- cascade class;
- replication budget;
- stop/passivation path;
- restart authority;
- inheritance package;
- protective-vs-productive perpetuity state;
- residual hazards / closure path.

## No-parallel-master rule

This file is a receipt. Once parent carrier + DBR + child carriers contain verified promoted state, this receipt becomes ordinary provenance. Lifecycle semantics remain in their owning canon; code remains executable implementation; ACR3 remains historical provenance.
