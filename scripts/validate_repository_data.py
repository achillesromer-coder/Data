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
CONTRACT_PATH = ROOT / "schemas" / "jpl_normalized_handoff_contract.json"


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def declared_sha256(path: Path) -> str:
    if path.suffix.lower() != ".json":
        return sha256(path)
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    canonical = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ) + "\n"
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


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
        errors.append(f"JSON unreadable: {relative(path)}: {exc}")
        return None


def resolve_declared_path(manifest: Path, declared: str) -> Path | None:
    candidate = Path(declared)
    options = [ROOT / candidate, manifest.parent / candidate]
    root = ROOT.resolve()
    for option in options:
        resolved = option.resolve()
        if resolved.is_relative_to(root) and resolved.is_file():
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
            errors.append(f"Manifest target missing: {relative(path)} -> {declared}")
            continue
        try:
            actual = declared_sha256(target)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"Manifest target unreadable: {relative(target)}: {exc}")
            continue
        if actual.lower() != expected.lower():
            errors.append(
                f"SHA-256 mismatch: {relative(target)} "
                f"expected={expected} actual={actual}"
            )


def validate_csv(
    path: Path, errors: list[str]
) -> tuple[list[str], list[dict[str, str]]] | None:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or not any(cell.strip() for cell in reader.fieldnames):
                errors.append(f"CSV missing header: {relative(path)}")
                return None
            rows = list(reader)
            for line_number, row in enumerate(rows, start=2):
                if None in row or any(value is None for value in row.values()):
                    errors.append(
                        f"CSV width mismatch: {relative(path)}:{line_number} "
                        "does not match the declared columns"
                    )
            return list(reader.fieldnames), rows
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        errors.append(f"CSV unreadable: {relative(path)}: {exc}")
        return None


def load_contract(errors: list[str]) -> dict[str, Any] | None:
    payload = validate_json(CONTRACT_PATH, errors)
    if not isinstance(payload, dict):
        errors.append(f"Handoff contract is not an object: {relative(CONTRACT_PATH)}")
        return None
    families = payload.get("families")
    if not isinstance(families, dict) or not families:
        errors.append(f"Handoff contract has no schema families: {relative(CONTRACT_PATH)}")
        return None
    return payload


def row_identity(row: dict[str, Any], fields: list[str]) -> tuple[str, ...]:
    return tuple("" if row.get(field) is None else str(row.get(field)) for field in fields)


def csv_value(value: Any) -> str:
    return "" if value is None else str(value)


def validate_row_contract(
    lane: Path,
    rows: list[dict[str, Any]],
    family: dict[str, Any],
    errors: list[str],
) -> dict[tuple[str, ...], dict[str, Any]]:
    required_fields = family.get("required_fields", [])
    non_empty_fields = family.get("non_empty_fields", [])
    identity_fields = family.get("identity_fields", [])
    required_values = family.get("required_values", {})
    identities: dict[tuple[str, ...], dict[str, Any]] = {}

    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            errors.append(f"Summary row is not an object: {relative(lane)} row={index}")
            continue
        for field in required_fields:
            if field not in row:
                errors.append(
                    f"Summary required field missing: {relative(lane)} "
                    f"row={index} field={field}"
                )
        for field in non_empty_fields:
            if row.get(field) in (None, ""):
                errors.append(
                    f"Summary required value missing: {relative(lane)} "
                    f"row={index} field={field}"
                )
        for field, expected in required_values.items():
            if row.get(field) != expected:
                errors.append(
                    f"Summary guardrail mismatch: {relative(lane)} row={index} "
                    f"field={field} expected={expected!r} actual={row.get(field)!r}"
                )

        identity = row_identity(row, identity_fields)
        if not identity_fields or any(not part for part in identity):
            errors.append(f"Summary identity incomplete: {relative(lane)} row={index}")
        elif identity in identities:
            errors.append(
                f"Summary identity duplicated: {relative(lane)} identity={identity}"
            )
        else:
            identities[identity] = row

    return identities


def validate_json_csv_parity(
    lane: Path,
    json_rows: list[dict[str, Any]],
    csv_table: tuple[list[str], list[dict[str, str]]],
    identity_fields: list[str],
    errors: list[str],
) -> None:
    header, csv_rows = csv_table
    if len(json_rows) != len(csv_rows):
        errors.append(
            f"JSON/CSV row-count mismatch: {relative(lane)} "
            f"json={len(json_rows)} csv={len(csv_rows)}"
        )
    if json_rows and header != list(json_rows[0].keys()):
        errors.append(f"JSON/CSV field-order mismatch: {relative(lane)}")

    json_by_id = {
        row_identity(row, identity_fields): row
        for row in json_rows
        if isinstance(row, dict)
    }
    csv_by_id = {row_identity(row, identity_fields): row for row in csv_rows}
    if set(json_by_id) != set(csv_by_id):
        errors.append(f"JSON/CSV identity-set mismatch: {relative(lane)}")
        return

    for identity, json_row in json_by_id.items():
        csv_row = csv_by_id[identity]
        for field in header:
            if csv_row.get(field, "") != csv_value(json_row.get(field)):
                errors.append(
                    f"JSON/CSV value mismatch: {relative(lane)} "
                    f"identity={identity} field={field}"
                )


def validate_manifest_summary_alignment(
    lane: Path,
    manifest: dict[str, Any],
    rows: list[dict[str, Any]],
    family: dict[str, Any],
    errors: list[str],
) -> None:
    objects = manifest.get("objects")
    if not isinstance(objects, dict) or not objects:
        errors.append(f"Manifest has no objects: {relative(lane / 'manifest.json')}")
        return

    required_object_fields = family.get("manifest_object_required_fields", [])
    match_fields = family.get("manifest_object_match_fields", [])
    mode = family.get("row_mode")
    manifest_names: set[str] = set()
    expected_windows = [
        item.get("label")
        for item in manifest.get("windows", [])
        if isinstance(item, dict) and item.get("label")
    ]

    for slug, record in objects.items():
        if not isinstance(record, dict):
            errors.append(f"Manifest object is not a record: {relative(lane)} key={slug}")
            continue
        for field in required_object_fields:
            if record.get(field) in (None, ""):
                errors.append(
                    f"Manifest object field missing: {relative(lane)} "
                    f"key={slug} field={field}"
                )
        name = record.get("requested_name")
        if not isinstance(name, str) or not name:
            continue
        manifest_names.add(name)
        object_rows = [row for row in rows if row.get("requested_name") == name]

        if mode == "one_row_per_object" and len(object_rows) != 1:
            errors.append(
                f"Manifest/summary object-count mismatch: {relative(lane)} "
                f"object={name} expected=1 actual={len(object_rows)}"
            )
        elif mode == "one_row_per_object_per_window":
            actual_windows = [row.get("window") for row in object_rows]
            if sorted(actual_windows) != sorted(expected_windows):
                errors.append(
                    f"Manifest/summary window mismatch: {relative(lane)} object={name}"
                )
            counts = record.get("window_sample_counts")
            if isinstance(counts, dict):
                for row in object_rows:
                    window = row.get("window")
                    if csv_value(row.get("sample_count")) != csv_value(counts.get(window)):
                        errors.append(
                            f"Manifest/summary sample-count mismatch: {relative(lane)} "
                            f"object={name} window={window}"
                        )

        for row in object_rows:
            for field in match_fields:
                if csv_value(row.get(field)) != csv_value(record.get(field)):
                    errors.append(
                        f"Manifest/summary value mismatch: {relative(lane)} "
                        f"object={name} field={field}"
                    )

    summary_names = {
        str(row.get("requested_name")) for row in rows if row.get("requested_name")
    }
    if summary_names != manifest_names:
        errors.append(f"Manifest/summary object-set mismatch: {relative(lane)}")

    for field in family.get("manifest_row_equal_fields", []):
        expected = manifest.get(field)
        for row in rows:
            if row.get(field) != expected:
                errors.append(
                    f"Manifest/summary guardrail mismatch: {relative(lane)} "
                    f"object={row.get('requested_name')} field={field}"
                )


def validate_handoff_lane(
    manifest_path: Path,
    manifest: dict[str, Any],
    json_payloads: dict[Path, Any],
    csv_tables: dict[Path, tuple[list[str], list[dict[str, str]]]],
    family: dict[str, Any],
    errors: list[str],
) -> None:
    lane = manifest_path.parent
    summary_json_path = lane / "summary.json"
    summary_csv_path = lane / "summary.csv"
    rows = json_payloads.get(summary_json_path)
    csv_table = csv_tables.get(summary_csv_path)
    if not isinstance(rows, list):
        errors.append(f"Normalized summary JSON missing or invalid: {relative(lane)}")
        return
    if csv_table is None:
        errors.append(f"Normalized summary CSV missing or invalid: {relative(lane)}")
        return

    identity_fields = family.get("identity_fields", [])
    validate_row_contract(lane, rows, family, errors)
    validate_json_csv_parity(lane, rows, csv_table, identity_fields, errors)
    validate_manifest_summary_alignment(lane, manifest, rows, family, errors)


def validate_repository() -> tuple[dict[str, int], list[str]]:
    errors: list[str] = []
    stats = {"json": 0, "csv": 0, "manifests": 0, "handoff_lanes": 0}
    if not DATA_ROOT.is_dir():
        errors.append("data directory is missing")
        return stats, errors

    contract = load_contract(errors)
    families = contract.get("families", {}) if contract else {}
    json_payloads: dict[Path, Any] = {}
    csv_tables: dict[Path, tuple[list[str], list[dict[str, str]]]] = {}
    manifests: list[Path] = []

    for path in sorted(DATA_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() == ".json":
            stats["json"] += 1
            payload = validate_json(path, errors)
            if payload is not None:
                json_payloads[path] = payload
                if path.name == "manifest.json":
                    stats["manifests"] += 1
                    manifests.append(path)
                    validate_manifest(path, payload, errors)
        elif path.suffix.lower() == ".csv":
            stats["csv"] += 1
            table = validate_csv(path, errors)
            if table is not None:
                csv_tables[path] = table

    for manifest_path in manifests:
        manifest = json_payloads.get(manifest_path)
        if not isinstance(manifest, dict):
            continue
        family = families.get(manifest.get("schema"))
        if family is None:
            if (manifest_path.parent / "summary.json").exists() or (
                manifest_path.parent / "summary.csv"
            ).exists():
                errors.append(
                    f"Normalized manifest schema has no handoff contract: "
                    f"{relative(manifest_path)} schema={manifest.get('schema')!r}"
                )
            continue
        if not isinstance(family, dict):
            errors.append(f"Handoff contract family is invalid: {manifest.get('schema')}")
            continue
        stats["handoff_lanes"] += 1
        validate_handoff_lane(
            manifest_path,
            manifest,
            json_payloads,
            csv_tables,
            family,
            errors,
        )

    return stats, errors


def main() -> int:
    stats, errors = validate_repository()
    print(
        f"Validated {stats['json']} JSON files, {stats['csv']} CSV files, "
        f"{stats['manifests']} manifests, and {stats['handoff_lanes']} "
        "normalized handoff lanes."
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
