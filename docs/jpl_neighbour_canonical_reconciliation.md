# JPL Neighbour Canonical Reconciliation

Date: 2026-07-15

## Canonical state

The default-branch JPL workflow has produced the canonical neighbour evidence set:

- `data/jpl/neighbours/sbdb/latest/manifest.json`
- `data/jpl/neighbours/sbdb/latest/summary.csv`
- `data/jpl/neighbours/horizons/latest/manifest.json`
- `data/jpl/neighbours/horizons/latest/summary.csv`

Validation state:

```text
16 / 16 neighbour source captures current
16 / 16 orbit-invariant checks pass
16 bodies x 459 daily Horizons samples
48 / 48 month-window summaries complete
June / January / August coverage = 30 / 31 / 31 samples
Manifest errors = 0
```

The earlier direct bootstrap remains historical fallback evidence. It no longer has canonical authority over the default-branch `latest` manifests.

## Classification reconciliation

Current JPL SBDB classifications supersede stale workbook classification flags after compare-first logging:

| Candidate | Previous workbook state | Canonical state |
|---|---|---|
| Vishnu | non-PHA | PHA |
| Minos | non-PHA | PHA |
| Lugh | non-PHA | PHA |
| Pan | non-PHA | PHA |
| Ptah | non-PHA | PHA |
| Toro | PHA | non-PHA |

These changes are classification corrections only. They do not imply selection or operational suitability.

## Candidate source-hierarchy resolutions

| Candidate | Legacy workbook value | Canonical JPL value | Resolution |
|---|---|---|---|
| Ninkasi | taxonomy A | Bus taxonomy Sq | Canonical value promoted; legacy value retained in reconciliation logs |
| Vishnu | taxonomy Q | Bus taxonomy O | Canonical value promoted; legacy value retained in reconciliation logs |
| Cerberus | taxonomy Q | Bus/Tholen taxonomy S | Canonical value promoted; legacy value retained in reconciliation logs |
| Golevka | diameter 0.34 km | diameter 0.53 km | Canonical value promoted; legacy value retained in reconciliation logs |
| Toro | diameter 3.6 km | diameter 3.4 km | Canonical value promoted; legacy value retained in reconciliation logs |

Minor comparisons remain non-destructive:

- Agni: workbook 0.455 km versus JPL 0.462 km.
- Mithra: workbook 1.826 km versus JPL 1.849 km.

Lugh had no workbook diameter and therefore received the source-backed 1.4 km value without a conflict.

## Anchor source-hierarchy resolutions

The two remaining anchor-level physical comparisons were resolved under the same SBDB-first rule:

| Anchor | Legacy workbook values | Canonical JPL values | Remaining gap |
|---|---|---|---|
| Toutatis | diameter 2.725 km; albedo 0.157; taxonomy S | diameter 5.4 km; albedo 0.405; Bus taxonomy Sk | density |
| Apollo / Apl | diameter 1.2 km; albedo 0.4536 | diameter 1.5 km; albedo 0.25; Bus/Tholen taxonomy Q | density |

Legacy values remain permanently visible in the source-capture and appendix reconciliation trail. Clearing these physical holds returns both branches to comparative use; it does not select either branch.

## Workbook propagation

Asteroid workbook:

```text
Asteroid_Strategic_Mapping_Base_withRocks
Cluster Neighbour Matrix!A1:Y21
Cluster Review Pack
Cluster Source Capture
Cluster Enrichment Queue
Task Roadmap
```

Operations workbook:

```text
Type1_Asteroid_Operating_Workbook
Mission 1 Detail
Mission 2 Detail
Mission 3 Detail
Cluster Sequence!A14:AB43
Cluster Sequence!A45:S55
Cluster Sequence!A57:S67
Cluster Sequence!A69:R79
Readiness Gates
LS Cognigrex Handoff
```

The operations surface contains:

- 18 canonical edge rows;
- six branch evidence summaries;
- eight first-loop comparative arrangements;
- eight categorical evidence-sensitivity rows;
- eight qualitative perturbation results;
- stable M1/M2/M3 detail scaffolds with selection deferred;
- candidate and anchor classification/evidence states;
- exact canonical Git dependencies;
- M1/M2/M3 interface-allocation states of 3/7/11 m3;
- shared-edge and review-burden context;
- no final branch selection.

## First-loop comparison set

```text
FLC-001 control / shared-edge / expansion
FLC-002 strategic support / expansion / non-PHA context
FLC-003 control / strategic support / expansion
FLC-004 shared-edge / control / expansion
FLC-005 control / expansion / high-PHA comparison
FLC-006 control / shared-edge / mixed-PHA comparison
FLC-007 strategic / high-PHA governance stress comparison
FLC-008 high-PHA negative-control comparator
```

These rows are comparative evidence arrangements. They are not trajectories, launch plans, ranked recommendations or selected sequences.

## Cognigrex stable-freeze

The two workbooks are stable for later Cognigrex continuation under:

```text
Freeze ID: CGX-FREEZE-001
Freeze date: 2026-07-15
Selection state: none
Stable completion gate: Operations Readiness Gate RG-009
Future restart gate: Operations Readiness Gate RG-010
```

The freeze is complete because:

- canonical source and window evidence is registered;
- material candidate and anchor comparisons are resolved and traceable;
- all current comparison and sensitivity surfaces are populated;
- M1/M2/M3 pages are stable deferred-selection scaffolds;
- stale payload-pending, window-pending and conflict-hold operating states have been removed;
- historical roadmap rows are complete, superseded or deferred;
- remaining physical gaps are explicit and non-blocking;
- future Cognigrex read and reviewed-return surfaces are identified.

## Post-freeze repository reconciliation

The repository was tidied and advanced without changing the frozen workbook decision state:

```text
Current Data main head: 767399423c0b180a2bab66ed932a9577c43f5fd3
Latest scheduled source refresh: c4d30c78eb4e9393a747c333cc0f19fa7b8d858c
Stable-freeze documentation commit: 608379df998156eebeb7c78c1eff87bd386ce41e
Open pull requests after reconciliation: 0
```

The scheduled refresh regenerated current SBDB and Horizons payloads, manifests and hashes. It advanced orbit-solution metadata for Anteros, Agni, Vishnu and Toro while retaining the canonical physical, classification, hardware, capacity and no-selection states. Regenerated window data remains compare-first input and does not silently overwrite the frozen workbook comparison layer.

Data pull request #5 was reviewed and merged as the governed repository-integrity layer. It added:

- `.github/workflows/data-integrity.yml`;
- `scripts/validate_repository_data.py`;
- `tests/test_validate_repository_data.py`;
- `schemas/jpl_normalized_handoff_contract.json`;
- the repository operational contract in `README.md`.

The merged validation layer is read-only with respect to evidence files. It detects malformed JSON/CSV, manifest-path or SHA drift, duplicate identities, normalized JSON/CSV mismatch, incomplete lanes and missing interpretation guardrails. It does not rewrite source payloads or mutate Google workbooks.

The two obsolete May-era draft PRs were closed as superseded provenance. Their branches and commit history were not deleted.

## Deferred evidence backlog

The following remains valid future work but does not block the stable freeze:

- density and composition enrichment for anchors and neighbour candidates where primary values are absent;
- selected albedo, diameter and taxonomy confirmation where current evidence is incomplete;
- optional curated Asteroid Master promotion under a separate reviewed catalogue objective;
- rerunning evidence tests after a material source or rule change;
- future public release review.

Unknown values must remain unknown until source-backed. Deferred enrichment must not introduce inferred physical values or selection claims.

## Interpretation limits

Neither orbital-analogue distance nor Earth-relative range order establishes:

- present spatial proximity;
- transfer cost;
- launch or route suitability;
- mining feasibility;
- target selection;
- whole-body fit against 3/7/11 m3 interface allocation.

Current hardware remains Mark III and Mark V only. Mark IV remains the post-mission successor / next model of Mark III. Apophis remains a strategic tag/support case and not mine-first. Apollo shorthand remains `Apl`.