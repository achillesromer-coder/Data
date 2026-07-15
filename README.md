# Römer Data

Canonical machine-readable source and evidence repository for Römer Industries operational data pipelines.

## Active pipeline

The current production-capable lane captures and normalises public JPL Small-Body Database and Horizons data for bounded asteroid comparison work.

- Source capture scripts: `scripts/`
- Versioned machine outputs: `data/jpl/`
- Normalized handoff contract: `schemas/jpl_normalized_handoff_contract.json`
- Methodology and evidence limits: `docs/`
- Scheduled capture workflow: `.github/workflows/jpl-sbdb-source-capture.yml`
- Repository validation workflow: `.github/workflows/data-integrity.yml`

## Repository contract

1. Source APIs and raw payload provenance are preserved.
2. Normalised outputs must be reproducible from committed scripts.
3. Generated manifests must remain internally consistent with their referenced files.
4. Interpretive limits travel with the data; descriptive range/time outputs are not mission feasibility, trajectory, mining, launch, delta-v, or target-selection conclusions.
5. Spreadsheet workbooks are downstream operational sources and are not modified by repository automation.
6. Changes to scripts, schemas, workflows, or evidence contracts proceed through a review branch and pull request.

## Local verification

```bash
python -m unittest discover -s tests -v
python scripts/validate_repository_data.py
```

The validator checks JSON readability, manifest path resolution, SHA-256 consistency where declared, CSV structural readability, normalized JSON/CSV parity, unique row identities, manifest completeness, and required evidence guardrails without editing any source file.

## Branch model

- `main`: accepted operational baseline
- `ops/*`: operational controls and repository maturation
- `data/*`: bounded source or schema changes
- `fix/*`: corrective changes

Automated source refreshes may commit only within the explicitly allow-listed JPL output directories in the capture workflow.

## Current boundary

This repository supports data acquisition, provenance, normalisation, validation, and handoff. It does not authorise deployment, public release, backend launch, payment/custody activity, or autonomous mission decisions.
