# Cluster Neighbour Matrix

## Purpose

`Cluster Neighbour Matrix` is the asteroid-workbook analogue layer for the six active M1-M3 branches:

- Eros
- Apophis
- Castalia
- Toutatis
- Anteros
- Apollo (`Apl` in mission shorthand)

The initial bounded set contains the top three non-anchor orbital analogues for each branch: 18 rows and 16 unique candidate bodies.

## Method

The analogue score is a robust-scaled distance across:

```text
a   semi-major axis
 e  eccentricity
 i  inclination
 q  perihelion distance
 Q  aphelion distance
```

A small preference is applied to candidates in the same NEA subclass (Aten, Apollo or Amor). The workbook stores the normalized distance and raw deltas for review.

## Interpretation limit

The matrix does **not** establish:

- instantaneous spatial proximity;
- pairwise transfer cost;
- launch or route suitability;
- mining feasibility;
- target selection;
- whole-body fit against the 3/7/11 m³ interface-capacity model.

The capacity columns are allocation-modelling states only. Candidate total diameter or volume is never compared directly to mission interface capacity as a whole-body feasibility test.

## Initial candidate sets

```text
Eros     -> Likho, Ninkasi, Pocahontas
Apophis  -> Duende, Agni, Kamo`oalewa
Castalia -> Vishnu, Cerberus, Minos
Toutatis -> Golevka, Lugh, Mithra
Anteros  -> Likho, Ninkasi, Vinciguerra
Apollo   -> Pan, Ptah, Toro
```

Likho and Ninkasi intentionally appear under both Eros and Anteros. These are shared graph edges, not duplicate catalogue objects.

## Source and enrichment route

1. Asteroid workbook `Cluster Library` supplies source rows and orbital elements.
2. `Cluster Neighbour Matrix` records the bounded analogue set.
3. Canonical SBDB and Horizons runners are reused through thin neighbour wrappers.
4. Source and three-window comparisons return to the matrix.
5. Operations workbook combines the verified neighbour set with M1/M2/M3 capacities of 3/7/11 m³.
6. Cognigrex may then compare branch combinations without treating analogue distance as a final score.

## Current hardware canon

```text
Current/to-date: Mark III + Mark V only
Mark IV: post-mission successor / next model of Mark III
```

## Workbook route

```text
Asteroid_Strategic_Mapping_Base_withRocks
Cluster Neighbour Matrix!A1:Y21
```
