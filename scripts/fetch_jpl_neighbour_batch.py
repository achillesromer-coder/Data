#!/usr/bin/env python3
"""Run the canonical SBDB capture logic for the bounded neighbour-candidate set."""

from pathlib import Path

import fetch_jpl_source_batch as base

base.OBJECTS = (
    "Likho",
    "Ninkasi",
    "Pocahontas",
    "Duende",
    "Agni",
    "Kamo`oalewa",
    "Vishnu",
    "Cerberus",
    "Minos",
    "Golevka",
    "Lugh",
    "Mithra",
    "Vinciguerra",
    "Pan",
    "Ptah",
    "Toro",
)
base.OUTPUT_DIR = Path("data/jpl/neighbours/sbdb/latest")
base.SUMMARY_JSON = base.OUTPUT_DIR / "summary.json"
base.SUMMARY_CSV = base.OUTPUT_DIR / "summary.csv"
base.MANIFEST_JSON = base.OUTPUT_DIR / "manifest.json"
base.USER_AGENT = "Romer-Industries-Cognigrex-JPL-Neighbour-Capture/1.0"


if __name__ == "__main__":
    raise SystemExit(base.main())
