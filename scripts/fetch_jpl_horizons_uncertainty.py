#!/usr/bin/env python3
"""Capture sparse JPL Horizons formal XYZ state uncertainties at canonical A09 epochs.

This is a cross-check layer for the nominal table-3 state-vector lane. It does not replace
the full SBDB orbital covariance, does not assume independent state components, and does not
calculate impact probability, route feasibility, delta-v, capture or intervention merit.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HORIZONS_ENDPOINT = "https://ssd.jpl.nasa.gov/api/horizons.api"
OBJECTS: tuple[tuple[str, str], ...] = (
    ("Apophis", "99942"),
    ("Castalia", "4769"),
    ("Toutatis", "4179"),
    ("Anteros", "1943"),
    ("Apollo", "1862"),
    ("Eros", "433"),
)
NOMINAL_SUMMARY = Path("data/jpl/horizons/latest/summary.json")
OUTPUT_DIR = Path("data/jpl/horizons/uncertainty/latest")
MANIFEST_JSON = OUTPUT_DIR / "manifest.json"
SUMMARY_JSON = OUTPUT_DIR / "summary.json"
SUMMARY_CSV = OUTPUT_DIR / "summary.csv"
USER_AGENT = "Romer-Industries-Cognigrex-Horizons-Uncertainty/1.0"
TIMEOUT_SECONDS = 75
MAX_RETRIES = 5
REQUEST_DELAY_SECONDS = 2.0


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "object"


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def load_nominal_rows() -> list[dict[str, Any]]:
    rows = json.loads(NOMINAL_SUMMARY.read_text(encoding="utf-8"))
    if not isinstance(rows, list) or not rows:
        raise ValueError("Nominal Horizons summary is unavailable or empty")
    required = {
        "requested_name",
        "designation",
        "window",
        "minimum_range_state_jd_tdb",
        "sha256",
    }
    for row in rows:
        if not isinstance(row, dict) or not required.issubset(row):
            raise ValueError("Nominal summary row lacks A09 uncertainty linkage fields")
    return rows


def request_url(designation: str, epochs: list[float]) -> str:
    tlist = " ".join(f"'{epoch:.12f}'" for epoch in epochs)
    params = {
        "format": "json",
        "COMMAND": f"'{designation};'",
        "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'VECTORS'",
        "CENTER": "'500@399'",
        "TLIST": tlist,
        "TLIST_TYPE": "'JD'",
        "TIME_TYPE": "'TDB'",
        "REF_SYSTEM": "'ICRF'",
        "REF_PLANE": "'ECLIPTIC'",
        "OUT_UNITS": "'AU-D'",
        "VEC_TABLE": "'2x'",
        "VEC_CORR": "'NONE'",
        "CSV_FORMAT": "'YES'",
    }
    return HORIZONS_ENDPOINT + "?" + urllib.parse.urlencode(params)


def parse_uncertainty_rows(payload: dict[str, Any]) -> list[dict[str, float | str]]:
    result = str(payload["result"])
    body = result.split("$SOE", 1)[1].split("$EOE", 1)[0]
    parsed: list[dict[str, float | str]] = []
    for fields in csv.reader(io.StringIO(body)):
        fields = [field.strip() for field in fields]
        if len(fields) < 14 or not fields[0] or not fields[0][0].isdigit():
            continue
        try:
            values = [float(field) for field in fields[2:14]]
            jd = float(fields[0])
        except ValueError:
            continue
        if not all(math.isfinite(value) for value in [jd, *values]):
            raise ValueError("Non-finite Horizons uncertainty sample encountered")
        x, y, z, vx, vy, vz, xs, ys, zs, vxs, vys, vzs = values
        if min(xs, ys, zs, vxs, vys, vzs) < 0:
            raise ValueError("Negative formal state-component uncertainty encountered")
        parsed.append(
            {
                "jd_tdb": jd,
                "calendar": fields[1],
                "x_au": x,
                "y_au": y,
                "z_au": z,
                "vx_au_per_day": vx,
                "vy_au_per_day": vy,
                "vz_au_per_day": vz,
                "x_sigma_au": xs,
                "y_sigma_au": ys,
                "z_sigma_au": zs,
                "vx_sigma_au_per_day": vxs,
                "vy_sigma_au_per_day": vys,
                "vz_sigma_au_per_day": vzs,
                "position_sigma_rss_au": math.sqrt(xs * xs + ys * ys + zs * zs),
                "velocity_sigma_rss_au_per_day": math.sqrt(vxs * vxs + vys * vys + vzs * vzs),
            }
        )
    return parsed


def validate_payload(name: str, designation: str, payload: dict[str, Any], expected_rows: int) -> tuple[str, list[str]]:
    signature = payload.get("signature")
    if not isinstance(signature, dict) or not signature.get("version"):
        raise ValueError("Horizons signature/version is missing")
    if payload.get("error"):
        raise ValueError(f"Horizons error payload: {payload['error']}")
    result = payload.get("result")
    if not isinstance(result, str) or "$$SOE" not in result or "$$EOE" not in result:
        raise ValueError("Horizons result table markers are missing")
    if "Center body name: Earth (399)" not in result:
        raise ValueError("Horizons uncertainty response is not Earth-centred")
    if designation not in result:
        raise ValueError(f"Horizons response does not identify expected designation {designation}")
    rows = parse_uncertainty_rows(payload)
    if len(rows) != expected_rows:
        raise ValueError(f"Expected {expected_rows} uncertainty rows for {name}, got {len(rows)}")
    pre = result.split("$$SOE", 1)[0].splitlines()
    header_candidates = [line.strip() for line in pre if "JDTDB" in line and "," in line]
    return result, header_candidates[-3:]


def fetch(name: str, designation: str, epochs: list[float]) -> tuple[dict[str, Any], str, str, list[str]]:
    url = request_url(designation, epochs)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("Horizons payload is not a JSON object")
            _, headers = validate_payload(name, designation, payload, len(epochs))
            text = canonical_json(payload)
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            return payload, text, digest, headers
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                time.sleep(min(20, attempt * 3))
    raise RuntimeError(f"Failed to fetch uncertainty for {name}: {last_error}")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> bool:
    if not rows:
        return False
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0].keys()), extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return write_if_changed(path, buffer.getvalue())


def write_if_changed(path: Path, content: str) -> bool:
    previous = path.read_text(encoding="utf-8") if path.exists() else None
    if previous == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    nominal = load_nominal_rows()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    changed = False
    errors: list[str] = []
    objects: dict[str, Any] = {}
    summary_rows: list[dict[str, Any]] = []

    for index, (name, designation) in enumerate(OBJECTS):
        selected = [row for row in nominal if row["requested_name"] == name]
        selected.sort(key=lambda row: str(row["window"]))
        epochs = [float(row["minimum_range_state_jd_tdb"]) for row in selected]
        windows = [str(row["window"]) for row in selected]
        nominal_hashes = [str(row["sha256"]) for row in selected]
        try:
            payload, text, digest, headers = fetch(name, designation, epochs)
            raw_path = OUTPUT_DIR / f"{slugify(name)}.json"
            changed |= write_if_changed(raw_path, text)
            objects[slugify(name)] = {
                "requested_name": name,
                "designation": designation,
                "source_vector_table": "2x",
                "uncertainty_coordinate_system": "XYZ",
                "formal_uncertainty_sigma": 1,
                "requested_epochs_jd_tdb": epochs,
                "linked_windows": windows,
                "linked_nominal_payload_sha256": nominal_hashes,
                "row_count": len(epochs),
                "raw_path": raw_path.as_posix(),
                "sha256": digest,
                "captured_at": utc_now(),
                "header_probe": headers,
                "status": "captured_raw_uncertainty",
            }

            uncertainty_rows = parse_uncertainty_rows(payload)
            nominal_by_jd = {
                round(float(row["minimum_range_state_jd_tdb"]), 9): row
                for row in selected
            }
            for sample in uncertainty_rows:
                key = round(float(sample["jd_tdb"]), 9)
                nominal_row = nominal_by_jd.get(key)
                if nominal_row is None:
                    raise ValueError(f"No nominal state linkage for {name} uncertainty epoch {sample['jd_tdb']}")
                dx = float(sample["x_au"]) - float(nominal_row["minimum_range_x_au"])
                dy = float(sample["y_au"]) - float(nominal_row["minimum_range_y_au"])
                dz = float(sample["z_au"]) - float(nominal_row["minimum_range_z_au"])
                dvx = float(sample["vx_au_per_day"]) - float(nominal_row["minimum_range_vx_au_per_day"])
                dvy = float(sample["vy_au_per_day"]) - float(nominal_row["minimum_range_vy_au_per_day"])
                dvz = float(sample["vz_au_per_day"]) - float(nominal_row["minimum_range_vz_au_per_day"])
                summary_rows.append(
                    {
                        "requested_name": name,
                        "designation": designation,
                        "window": nominal_row["window"],
                        "state_jd_tdb": sample["jd_tdb"],
                        "calendar": sample["calendar"],
                        "x_sigma_au_1s": sample["x_sigma_au"],
                        "y_sigma_au_1s": sample["y_sigma_au"],
                        "z_sigma_au_1s": sample["z_sigma_au"],
                        "vx_sigma_au_per_day_1s": sample["vx_sigma_au_per_day"],
                        "vy_sigma_au_per_day_1s": sample["vy_sigma_au_per_day"],
                        "vz_sigma_au_per_day_1s": sample["vz_sigma_au_per_day"],
                        "position_component_sigma_rss_au": sample["position_sigma_rss_au"],
                        "velocity_component_sigma_rss_au_per_day": sample["velocity_sigma_rss_au_per_day"],
                        "nominal_position_delta_rss_au": math.sqrt(dx * dx + dy * dy + dz * dz),
                        "nominal_velocity_delta_rss_au_per_day": math.sqrt(dvx * dvx + dvy * dvy + dvz * dvz),
                        "nominal_payload_sha256": nominal_row["sha256"],
                        "uncertainty_payload_sha256": digest,
                        "source_vector_table": "2x",
                        "uncertainty_definition": "formal 1-sigma XYZ/VXYZ component uncertainty",
                        "claim_boundary": "Component formal uncertainty cross-check only; not a covariance matrix, confidence ellipsoid, impact probability or safety claim.",
                    }
                )
        except Exception as exc:
            errors.append(f"{name}: {exc}")

        if index < len(OBJECTS) - 1:
            time.sleep(REQUEST_DELAY_SECONDS)

    manifest = {
        "schema": "romer.jpl.horizons.critical-epoch-xyz-uncertainty.v0.1",
        "endpoint": HORIZONS_ENDPOINT,
        "source_nominal_summary": NOMINAL_SUMMARY.as_posix(),
        "objects": objects,
        "errors": errors,
        "interpretation_guardrails": [
            "Horizons VEC_TABLE=2x formal uncertainties are requested only at canonical A09 critical epochs; this is not a dense daily uncertainty sweep.",
            "The raw vector-table labels define X_s/Y_s/Z_s/VX_s/VY_s/VZ_s as formal 1-sigma component uncertainties.",
            "Horizons formal XYZ uncertainty is a propagated component-uncertainty cross-check and does not replace the full SBDB covariance matrix or its correlations.",
            "Horizons statistical uncertainty output is formal +/-3 sigma and can be optimistic far from the solution epoch or through close encounters; preserve JPL limitations.",
            "No impact probability, target selection, route feasibility, delta-v, capture or intervention claim follows from this source layer alone.",
        ],
    }
    summary_rows.sort(key=lambda row: (OBJECTS.index((row["requested_name"], row["designation"])), float(row["state_jd_tdb"])))
    changed |= write_if_changed(SUMMARY_JSON, json.dumps(summary_rows, ensure_ascii=False, indent=2, sort_keys=False) + "\n")
    changed |= write_csv(SUMMARY_CSV, summary_rows)
    changed |= write_if_changed(MANIFEST_JSON, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"captured": len(objects), "uncertainty_rows": len(summary_rows), "errors": errors, "changed": changed}, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
