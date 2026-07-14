#!/usr/bin/env python3
"""Fetch and normalize JPL SBDB payloads for the active M1-M3 pre-rank set.

Public-data-only runner. It stores canonical raw JSON and a normalized summary.
Repository files are rewritten only when source or normalized state changes.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SBDB_ENDPOINT = "https://ssd-api.jpl.nasa.gov/sbdb.api"
OBJECTS = ("Apophis", "Castalia", "Toutatis", "Anteros", "Apollo", "Eros")
OUTPUT_DIR = Path("data/jpl/sbdb/latest")
SUMMARY_JSON = OUTPUT_DIR / "summary.json"
SUMMARY_CSV = OUTPUT_DIR / "summary.csv"
MANIFEST_JSON = OUTPUT_DIR / "manifest.json"
USER_AGENT = "Romer-Industries-Cognigrex-JPL-Capture/1.1"
TIMEOUT_SECONDS = 45
MAX_RETRIES = 5
REQUEST_DELAY_SECONDS = 1.5


@dataclass(frozen=True)
class FetchResult:
    requested_name: str
    payload: dict[str, Any]
    canonical_json: str
    sha256: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", "-", value.strip()).strip("-")
    return value.lower() or "object"


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def result_from_payload(name: str, payload: dict[str, Any]) -> FetchResult:
    signature = payload.get("signature")
    if not isinstance(signature, dict) or not signature.get("version"):
        raise ValueError("SBDB signature/version is missing")
    text = canonical_json(payload)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return FetchResult(name, payload, text, digest)


def fetch_object(name: str) -> FetchResult:
    query = urllib.parse.urlencode(
        {
            "sstr": name,
            "phys-par": "1",
            "ca-data": "1",
            "ca-time": "both",
            "ca-tunc": "both",
            "ca-unc": "1",
        }
    )
    url = f"{SBDB_ENDPOINT}?{query}"
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )

    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                body = response.read().decode("utf-8")
            payload = json.loads(body)
            if not isinstance(payload, dict):
                raise ValueError("SBDB payload is not a JSON object")
            if payload.get("code") or payload.get("message"):
                raise ValueError(f"SBDB error payload: {payload.get('message') or payload.get('code')}")
            return result_from_payload(name, payload)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                time.sleep(min(20, attempt * 3))

    raise RuntimeError(f"Failed to fetch {name}: {last_error}")


def cached_object(name: str) -> FetchResult | None:
    raw_path = OUTPUT_DIR / f"{slugify(name)}.json"
    if not raw_path.exists():
        return None
    try:
        payload = json.loads(raw_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            return None
        return result_from_payload(name, payload)
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def list_to_map(items: Any, key_names: Iterable[str] = ("name",)) -> dict[str, dict[str, Any]]:
    """Index structured JPL lists by stable field names.

    Labels are intentionally excluded by default. JPL uses case-sensitive q/Q labels
    for perihelion/aphelion, so lower-casing labels would create a destructive collision.
    """
    result: dict[str, dict[str, Any]] = {}
    if not isinstance(items, list):
        return result
    for item in items:
        if not isinstance(item, dict):
            continue
        for key_name in key_names:
            key = item.get(key_name)
            if key:
                result[str(key).strip().lower()] = item
    return result


def value_from(mapping: dict[str, dict[str, Any]], *names: str) -> Any:
    for name in names:
        item = mapping.get(name.lower())
        if item is not None:
            return item.get("value")
    return None


def as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def validate_orbit_invariants(e_value: Any, a_value: Any, q_value: Any, ad_value: Any) -> tuple[str, str]:
    e = as_float(e_value)
    a = as_float(a_value)
    q = as_float(q_value)
    ad = as_float(ad_value)
    if None in (e, a, q, ad):
        return "NOT_CHECKED", "One or more e/a/q/Q values are unavailable."
    if not 0 <= e < 1 or not q < a < ad:
        raise ValueError(f"Orbit invariant failure: expected q < a < Q with 0 <= e < 1; got e={e}, q={q}, a={a}, Q={ad}")
    expected_q = a * (1 - e)
    expected_ad = a * (1 + e)
    tolerance = max(0.01, a * 0.015)
    if abs(q - expected_q) > tolerance or abs(ad - expected_ad) > tolerance:
        raise ValueError(
            "Orbit invariant failure: q/Q do not match a(1-e)/a(1+e) within tolerance; "
            f"got q={q}, Q={ad}, expected q={expected_q:.6g}, Q={expected_ad:.6g}"
        )
    return "PASS", f"q/a/Q ordering and a(1±e) checks passed within {tolerance:.4g} au tolerance."


def close_approach_count(payload: dict[str, Any]) -> int:
    data = payload.get("ca_data")
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        for key in ("data", "rows", "records"):
            if isinstance(data.get(key), list):
                return len(data[key])
    return 0


def normalize(result: FetchResult, previous_manifest: dict[str, Any], refresh_status: str, refresh_error: str | None) -> dict[str, Any]:
    payload = result.payload
    obj = payload.get("object") if isinstance(payload.get("object"), dict) else {}
    orbit = payload.get("orbit") if isinstance(payload.get("orbit"), dict) else {}
    signature = payload.get("signature") if isinstance(payload.get("signature"), dict) else {}
    orbit_class = obj.get("orbit_class") if isinstance(obj.get("orbit_class"), dict) else {}
    elements = list_to_map(orbit.get("elements"), key_names=("name",))
    physical = list_to_map(payload.get("phys_par"), key_names=("name",))

    eccentricity = value_from(elements, "e")
    semimajor_axis = value_from(elements, "a")
    perihelion = value_from(elements, "q")
    inclination = value_from(elements, "i")
    aphelion = value_from(elements, "ad")
    invariant_status, invariant_notes = validate_orbit_invariants(
        eccentricity, semimajor_axis, perihelion, aphelion
    )

    previous = previous_manifest.get("objects", {}).get(slugify(result.requested_name), {})
    captured_at = previous.get("captured_at") if previous.get("sha256") == result.sha256 else utc_now()

    return {
        "requested_name": result.requested_name,
        "fullname": obj.get("fullname"),
        "shortname": obj.get("shortname"),
        "designation": obj.get("des"),
        "spkid": obj.get("spkid"),
        "kind": obj.get("kind"),
        "neo": obj.get("neo"),
        "pha": obj.get("pha"),
        "orbit_class_code": orbit_class.get("code"),
        "orbit_class_name": orbit_class.get("name"),
        "orbit_id": orbit.get("orbit_id"),
        "condition_code": orbit.get("condition_code"),
        "epoch_jd": orbit.get("epoch"),
        "solution_date": orbit.get("soln_date"),
        "first_observation": orbit.get("first_obs"),
        "last_observation": orbit.get("last_obs"),
        "observations_used": orbit.get("n_obs_used"),
        "data_arc_days": orbit.get("data_arc"),
        "eccentricity": eccentricity,
        "semimajor_axis_au": semimajor_axis,
        "perihelion_au": perihelion,
        "inclination_deg": inclination,
        "aphelion_au": aphelion,
        "moid_au": orbit.get("moid") or value_from(elements, "moid"),
        "absolute_magnitude_h": value_from(physical, "h"),
        "diameter_km": value_from(physical, "diameter"),
        "albedo": value_from(physical, "albedo"),
        "density_g_cm3": value_from(physical, "density"),
        "rotation_period_h": value_from(physical, "rot_per"),
        "spectral_type_b": value_from(physical, "spec_b"),
        "spectral_type_t": value_from(physical, "spec_t"),
        "close_approach_records": close_approach_count(payload),
        "orbit_invariant_status": invariant_status,
        "orbit_invariant_notes": invariant_notes,
        "refresh_status": refresh_status,
        "last_refresh_error": refresh_error,
        "signature_source": signature.get("source"),
        "signature_version": signature.get("version"),
        "source_url": f"{SBDB_ENDPOINT}?sstr={urllib.parse.quote(result.requested_name)}&phys-par=1&ca-data=1",
        "sha256": result.sha256,
        "captured_at": captured_at,
        "current_hardware_canon": "Mark III + Mark V only",
        "mark_iv_state": "Post-mission successor/next model of Mark III; not current input",
    }


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def write_if_changed(path: Path, content: str) -> bool:
    previous = path.read_text(encoding="utf-8") if path.exists() else None
    if previous == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def write_csv(path: Path, rows: list[dict[str, Any]]) -> bool:
    fieldnames = list(rows[0].keys()) if rows else []
    from io import StringIO

    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return write_if_changed(path, buffer.getvalue())


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    previous_manifest = load_json(MANIFEST_JSON)
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    changed = False
    manifest_objects: dict[str, Any] = {}

    for index, name in enumerate(OBJECTS):
        refresh_status = "CAPTURED_CURRENT"
        refresh_error: str | None = None
        try:
            result = fetch_object(name)
            raw_path = OUTPUT_DIR / f"{slugify(name)}.json"
            changed |= write_if_changed(raw_path, result.canonical_json)
        except Exception as exc:
            refresh_error = str(exc)
            errors.append(refresh_error)
            result = cached_object(name)
            refresh_status = "RETAINED_VALIDATED_CACHE"
            if result is None:
                errors.append(f"No valid cached payload available for {name}")
                continue

        try:
            row = normalize(result, previous_manifest, refresh_status, refresh_error)
        except ValueError as exc:
            errors.append(f"{name}: {exc}")
            continue

        rows.append(row)
        slug = slugify(name)
        manifest_objects[slug] = {
            "requested_name": name,
            "sha256": result.sha256,
            "captured_at": row["captured_at"],
            "raw_path": (OUTPUT_DIR / f"{slug}.json").as_posix(),
            "source_url": row["source_url"],
            "signature_version": row["signature_version"],
            "orbit_invariant_status": row["orbit_invariant_status"],
            "refresh_status": refresh_status,
            "last_refresh_error": refresh_error,
            "status": "captured" if refresh_status == "CAPTURED_CURRENT" else "retained_validated_cache",
        }

        if index < len(OBJECTS) - 1:
            time.sleep(REQUEST_DELAY_SECONDS)

    if not rows:
        print("No current or cached JPL rows survived validation", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    rows.sort(key=lambda item: OBJECTS.index(str(item["requested_name"])))

    manifest = {
        "schema": "romer.jpl.sbdb.source-capture.v1.2",
        "endpoint": SBDB_ENDPOINT,
        "objects": manifest_objects,
        "errors": errors,
        "operating_state": {
            "current_hardware": ["Mark III", "Mark V"],
            "mark_iv": "Post-mission successor/next model of Mark III; not current capacity input",
            "capacity_basis": "Active Mark III/capture-capable units x 1 m3",
        },
        "normalization_guardrails": [
            "Orbit elements are keyed by JPL element name, not case-folded labels.",
            "Perihelion q and aphelion Q/ad are validated using q < a < Q and a(1±e).",
            "Transient upstream failures retain only previously captured raw payloads that still pass signature and orbit-invariant validation.",
        ],
    }

    summary_text = json.dumps(rows, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    changed |= write_if_changed(SUMMARY_JSON, summary_text)
    changed |= write_csv(SUMMARY_CSV, rows)
    changed |= write_if_changed(MANIFEST_JSON, manifest_text)

    print(json.dumps({"available": len(rows), "errors": errors, "changed": changed}, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
