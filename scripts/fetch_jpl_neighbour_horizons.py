#!/usr/bin/env python3
"""Run the canonical Horizons comparison logic for captured neighbour candidates."""

import json
from pathlib import Path

import fetch_jpl_horizons_windows as base

SBDB_SUMMARY = Path("data/jpl/neighbours/sbdb/latest/summary.json")
if not SBDB_SUMMARY.exists():
    raise SystemExit("Neighbour SBDB summary is missing; run fetch_jpl_neighbour_batch.py first.")

rows = json.loads(SBDB_SUMMARY.read_text(encoding="utf-8"))
objects = []
for row in rows:
    name = row.get("requested_name")
    designation = row.get("designation")
    if name and designation:
        objects.append((str(name), str(designation)))

if not objects:
    raise SystemExit("Neighbour SBDB summary contains no named designations.")

base.OBJECTS = tuple(objects)
base.OUTPUT_DIR = Path("data/jpl/neighbours/horizons/latest")
base.SUMMARY_JSON = base.OUTPUT_DIR / "summary.json"
base.SUMMARY_CSV = base.OUTPUT_DIR / "summary.csv"
base.MANIFEST_JSON = base.OUTPUT_DIR / "manifest.json"
base.USER_AGENT = "Romer-Industries-Cognigrex-Horizons-Neighbour-Capture/1.0"


if __name__ == "__main__":
    raise SystemExit(base.main())
