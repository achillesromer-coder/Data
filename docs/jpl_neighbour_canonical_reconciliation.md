# JPL Neighbour Canonical Reconciliation

Date: 2026-07-14

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

## Comparison holds entered for source-hierarchy resolution

| Candidate | Workbook value | Current JPL value | Resolution rule |
|---|---|---|---|
| Ninkasi | taxonomy A | Bus taxonomy Sq | SBDB-first taxonomy promotion after legacy value is logged |
| Vishnu | taxonomy Q | Bus taxonomy O | SBDB-first taxonomy promotion after legacy value is logged |
| Cerberus | taxonomy Q | Bus/Tholen taxonomy S | SBDB-first taxonomy promotion after legacy value is logged |
| Golevka | diameter 0.34 km | diameter 0.53 km | SBDB-first physical promotion after legacy value is logged |
| Toro | diameter 3.6 km | diameter 3.4 km | SBDB-first physical promotion after legacy value is logged |

Minor comparisons remain non-destructive:

- Agni: workbook 0.455 km versus JPL 0.462 km.
- Mithra: workbook 1.826 km versus JPL 1.849 km.

Lugh had no workbook diameter and therefore received the source-backed 1.4 km value without a conflict.

## Workbook propagation

Asteroid workbook:

```text
Asteroid_Strategic_Mapping_Base_withRocks
Cluster Neighbour Matrix!A1:Y21
```

Operations workbook:

```text
Type1_Asteroid_Operating_Workbook
Cluster Sequence!A14:AB43
```

The operations surface contains:

- 18 canonical edge rows;
- six branch evidence summaries;
- candidate classification and evidence state;
- exact canonical Git dependencies;
- M1/M2/M3 interface-allocation states of 3/7/11 m3;
- anchor conflict and shared-edge states;
- no final branch selection.

## Interpretation limits

Neither orbital-analogue distance nor Earth-relative range order establishes:

- present spatial proximity;
- transfer cost;
- launch or route suitability;
- mining feasibility;
- target selection;
- whole-body fit against 3/7/11 m3 interface allocation.

Current hardware remains Mark III and Mark V only. Mark IV remains the post-mission successor / next model of Mark III.
