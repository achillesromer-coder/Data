# InterSol Watch Tower FCStd geometry extraction — 2026-08-13

Status: **G1 GEOMETRY EXTRACTION / REVIEW-GATED**

## Source lock

- File: `InterSol - Watch Tower In Site Footprint.FCStd`
- SHA-256: `c476f9f2f9946ab8e99e58dd399aa7b02bac630c5d9336b80ef66f5f2a397321`
- Size: 48,879,924 bytes
- FreeCAD body label: `Launch Tower`
- Tip: `Pad086`
- Coordinate state: local CAD coordinates, not geodetic.

## Resolved body envelope

- Overall extents: 51.449 m × 75.924 m × 81.530 m.
- Z range: −4.905 m to 76.625 m.
- Central tower shaft (`Pad004`): 55.000 m extrusion from Z 13.300 m to 68.300 m.
- Observation/control head and cap: Z 68.300 m to 76.620 m.
- Final FreeCAD body: one connected solid in this file.

## Pole topology result

The geometry contains nine distinct external vertical pole lines:

- one materially larger/taller standalone pole candidate (`E_candidate`), axis approximately X 681.053 m / Y 393.144 m, group Z −1.600 m to 20.600 m;
- four external poles in the north-west wing cluster;
- four external poles in the south-east wing cluster.

This matches the owner-current `E + L1–L4 + R1–R4` pole-count topology. The FreeCAD object names are generic Pad/Pocket names, so the exact `L1–L4` and `R1–R4` ordering remains intentionally unassigned until the owner label convention is bound.

## Cable / node result

No distinct cable solids or labelled A/C tower node objects were found in this FCStd. Therefore:

- the rule of exactly two primary tower cable-node elevations A/C remains active;
- exact A/C Z and face coordinates remain open;
- cable endpoint rows remain held until the tower face nodes and pole numbering are bound.

## Wing geometry clusters

- North-west cluster bounds: `[677.189889, 393.771598, 0.0, 697.718664, 442.644649, 9.1]`
- South-east cluster bounds: `[681.214722, 366.815892, 0.0, 728.529076, 398.792178, 9.1]`

These are geometry clusters, not a final semantic declaration of left/right numbering.

## Guardrails

1. The accepted sunset render remains aesthetic-only.
2. Legacy 60 m / 18 m / +250 m placeholder values are not used in this extraction.
3. Geometric extraction does not establish structural adequacy, material grade, cable pretension, safety/security rating or build readiness.
4. No pole-level semantic label is invented where the FCStd itself is unlabeled.
5. All coordinates are local CAD coordinates, not geodetic.
