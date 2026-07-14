# Cluster Neighbour Source Reconciliation — 2026-07-14

## Canonical result

The scheduled/default-branch JPL workflow completed successfully on `main`:

```text
Commit: db1ec4064ffe4b800a897cec251001f8380ede0b
SBDB candidates: 16 / 16 current
Orbit invariants: 16 / 16 PASS
Horizons objects: 16 / 16 current
Window rows: 48 / 48
Samples per object: 459
Window coverage: June 2027 = 30, January 2028 = 31, August 2028 = 31
Manifest errors: 0
```

Canonical data surfaces:

```text
data/jpl/neighbours/sbdb/latest/manifest.json
data/jpl/neighbours/sbdb/latest/summary.csv
data/jpl/neighbours/horizons/latest/manifest.json
data/jpl/neighbours/horizons/latest/summary.csv
```

These `main` surfaces supersede the provisional bootstrap state.

## Workbook reconciliation

| Candidate | Source class / PHA | Workbook comparison | Three-window minima AU (Jun / Jan / Aug) | Disposition |
|---|---|---|---:|---|
| Likho | Amor / non-PHA | Physical values absent; workbook S unverified | 1.079062 / 2.486925 / 2.054100 | Evidence gaps; shared Eros/Anteros edge retained |
| Ninkasi | Amor / non-PHA | Workbook A conflicts with JPL Bus Sq; physical values absent | 2.154622 / 1.807212 / 0.499789 | Taxonomy conflict hold; shared edge retained |
| Pocahontas | Amor / non-PHA | JPL physical/taxonomy absent; workbook 1.196 km and S uncorroborated | 2.160087 / 2.458822 / 0.368038 | Workbook physical evidence remains secondary |
| Duende | Aten / non-PHA | Physical/taxonomy absent; workbook L uncorroborated | 0.805409 / 1.299638 / 1.759937 | Enrichment required |
| Agni | Aten / PHA | Diameter 0.462 km versus workbook 0.455 km; minor variance resolved to JPL | 0.853630 / 1.896826 / 1.663733 | Provisional interface-allocation comparison permitted; density/taxonomy gaps remain |
| Kamo`oalewa | Apollo / non-PHA | Physical/taxonomy absent | 0.258248 / 0.155771 / 0.232599 | Enrichment required; strategic cross-class edge retained |
| Vishnu | Apollo / PHA | PHA corrected true; diameter 0.42 km matches; workbook Q conflicts with JPL O | 0.958501 / 2.250913 / 1.540354 | Taxonomy conflict hold |
| Cerberus | Apollo / non-PHA | Diameter 1.2 km matches; workbook Q conflicts with JPL S/S | 1.166845 / 1.055819 / 0.548885 | Taxonomy conflict hold |
| Minos | Apollo / PHA | PHA corrected true; JPL physical/taxonomy absent; workbook 0.474 km and S uncorroborated | 2.174315 / 1.840660 / 1.968483 | Physical-evidence hold |
| Golevka | Apollo / PHA | Material diameter conflict: workbook 0.34 km versus JPL 0.53 km; Q agrees; JPL density 2.7 g/cm³ | 2.653142 / 2.448841 / 4.386549 | Material diameter conflict hold |
| Lugh | Apollo / PHA | PHA corrected true; JPL diameter 1.4 km added | 1.058428 / 4.459898 / 3.167030 | Provisional allocation comparison permitted; density/taxonomy gaps remain |
| Mithra | Apollo / PHA | Diameter 1.849 km versus workbook 1.826 km; minor variance resolved to JPL | 3.716270 / 2.855319 / 3.910123 | Provisional allocation comparison permitted; density/taxonomy gaps remain |
| Vinciguerra | Amor / non-PHA | Physical/taxonomy absent; workbook X uncorroborated | 0.586092 / 3.046396 / 1.351982 | Enrichment required |
| Pan | Apollo / PHA | PHA corrected true; physical/taxonomy absent | 0.914500 / 1.737970 / 2.481160 | Enrichment required; Apollo/Apl anchor conflict remains independent |
| Ptah | Apollo / PHA | PHA corrected true; physical/taxonomy absent | 1.719222 / 0.570417 / 1.580701 | Enrichment required; Apollo/Apl anchor conflict remains independent |
| Toro | Apollo / non-PHA | PHA corrected false; diameter conflict: workbook 3.6 km versus JPL 3.4 km; S taxonomy agrees | 1.739954 / 2.396285 / 0.348433 | Safety correction applied; diameter conflict hold |

## Safety-state corrections

The canonical source reconciliation changed six workbook PHA states:

```text
Vishnu: No  -> Yes
Minos:  No  -> Yes
Lugh:   No  -> Yes
Pan:    No  -> Yes
Ptah:   No  -> Yes
Toro:   Yes -> No
```

These corrections have been returned to both:

```text
Asteroid workbook: Cluster Neighbour Matrix!A3:Y21
Operations workbook: Cluster Sequence!A14:AB33
```

## Allocation interpretation

The operations matrix uses:

```text
M1 = 3 m³
M2 = 7 m³
M3 = 11 m³
```

These values describe active Mark III/capture-capable interface allocation. They are not whole-body asteroid size or volume limits.

Current hardware remains `Mark III + Mark V only`. Mark IV remains a post-mission successor / next model of Mark III.

## Bootstrap correction

A provisional bootstrap manifest was created while the first scheduled output had not yet appeared. The previously recorded Google Drive archive identifier is not accessible and must not be cited or used as an evidence surface.

The bootstrap record is retained only as execution history. Canonical authority is the `main` source/window data produced by commit `db1ec4064ffe4b800a897cec251001f8380ede0b`.

## Remaining open work

1. Resolve Ninkasi, Vishnu and Cerberus taxonomy conflicts.
2. Resolve Golevka and Toro diameter conflicts.
3. Corroborate Pocahontas and Minos workbook physical values.
4. Continue physical/taxonomy enrichment for rows without JPL physical fields.
5. Preserve Toutatis and Apollo anchor-level physical conflict holds independently of candidate readiness.
6. Do not select a mission branch from orbital analogue distance or Earth-relative range order alone.
