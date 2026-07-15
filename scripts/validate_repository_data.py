#!/usr/bin/env python3
"""Validate committed machine-readable data without modifying repository files."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "data"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def iter_dicts(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from iter_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_dicts(child)


def validate_json(path: Path, errors: list[str]) -> Any | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"JSON unreadable: {path.relative_to(ROOT)}: {exc}")
        return None


def resolve_declared_path(manifest: Path, declared: str) -> Path | None:
    candidate = Path(declared)
    options = [ROOT / candidate, manifest.parent / candidate]
    for option in options:
        resolved = option.resolve()
        if resolved.is_relative_to(ROOT.resolve()) and resolved.is_file():
            return resolved
    return None


def validate_manifest(path: Path, payload: Any, errors: list[str]) -> None:
    for record in iter_dicts(payload):
        declared = record.get("raw_path") or record.get("path")
        expected = record.get("sha256")
        if not isinstance(declared, str) or not isinstance(expected, str):
            continue
        target = resolve_declared_path(path, declared)
        if target is None:
            errors.append(
                f"Manifest target missing: {path.relative_to(ROOT)} -> {declared}"
            )
            continue
        actual = sha256(target)
        if actual.lower() != expected.lower():
            errors.append(
                f"SHA-256 mismatch: {target.relative_to(ROOT)} "
                f"expected={expected} actual={actual}"
            )


def validate_csv(path: Path, errors: list[str]) -> None:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader, None)
            if not header or not any(cell.strip() for cell in header):
                errors.append(f"CSV missing header: {path.relative_to(ROOT)}")
                return
            width = len(header)
            for line_number, row in enumerate(reader, start=2):
                if len(row) != width:
                    errors.append(
                        f"CSV width mismatch: {path.relative_to(ROOT)}:{line_number} "
                        f"expected={width} actual={len(row)}"
                    )
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        errors.append(f"CSV unreadable: {path.relative_to(ROOT)}: {exc}")


def main() -> int:
    if not DATA_ROOT.is_dir():
        print("ERROR: data directory is missing", file=sys.stderr)
        return 1

    errors: list[str] = []
    json_count = 0
    csv_count = 0
    manifest_count = 0

    for path in sorted(DATA_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() == ".json":
            json_count += 1
            payload = validate_json(path, errors)
            if payload is not None and path.name == "manifest.json":
                manifest_count += 1
                validate_manifest(path, payload, errors)
        elif path.suffix.lower() == ".csv":
            csv_count += 1
            validate_csv(path, errors)

    print(
        f"Validated {json_count} JSON files, {csv_count} CSV files, "
        f"and {manifest_count} manifests."
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print("Repository data integrity validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
