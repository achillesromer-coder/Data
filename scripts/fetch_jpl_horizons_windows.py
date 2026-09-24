#!/usr/bin/env python3
"""Capture JPL Horizons Earth-relative state vectors and comparison windows for M1-M3 candidates.

This runner intentionally does not calculate launch suitability, delta-v, route feasibility,
mining feasibility, or a target score. It captures and validates public Horizons geometric
state vectors plus light-time/range/range-rate context, then summarizes three approved
month-wide comparison windows. Statistical state uncertainty/covariance is a separate gate.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import statistics
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timezone
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
WINDOWS: tuple[tuple[str, date, date], ...] = (
    ("June 2027", date(2027, 6, 1), date(2027, 7, 1)),
    ("January 2028", date(2028, 1, 1), date(2028, 2, 1)),
    ("August 2028", date(2028, 8, 1), date(2028, 9, 1)),
)
QUERY_START = "2027-06-01"
QUERY_STOP = "2028-09-01"
OUTPUT_DIR = Path("data/jpl/horizons/latest")
SUMMARY_JSON = OUTPUT_DIR / "summary.json"
SUMMARY_CSV = OUTPUT_DIR / "summary.csv"
MANIFEST_JSON = OUTPUT_DIR / "manifest.json"
USER_AGENT = "Romer-Industries-Cognigrex-Horizons-Capture/1.0"
TIMEOUT_SECONDS = 75
MAX_RETRIES = 5
REQUEST_DELAY_SECONDS = 2.0
MIN_WINDOW_SAMPLES = 28
DATE_RE = re.compile(r"(?P<date>\d{4}-[A-Za-z]{3}-\d{2})")


@dataclass(frozen=True)
class FetchResult:
    requested_name: str
    designation: str
    payload: dict[str, Any]
    canonical_json: str
    sha256: str


@dataclass(frozen=True)
class VectorSample:
    calendar_date: date
    calendar_label: str
    julian_date_tdb: float
    x_au: float
    y_au: float
    z_au: float
    vx_au_per_day: float
    vy_au_per_day: float
    vz_au_per_day: float
    light_time_days: float
    range_au: float
    range_rate_au_per_day: float

    @property
    def speed_au_per_day(self) -> float:
        return (self.vx_au_per_day**2 + self.vy_au_per_day**2 + self.vz_au_per_day**2) ** 0.5


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "object"


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def result_from_payload(name: str, designation: str, payload: dict[str, Any]) -> FetchResult:
    signature = payload.get("signature")
    if not isinstance(signature, dict) or not signature.get("version"):
        raise ValueError("Horizons signature/version is missing")
    if payload.get("error"):
        raise ValueError(f"Horizons error payload: {payload['error']}")
    result = payload.get("result")
    if not isinstance(result, str) or "$$SOE" not in result or "$$EOE" not in result:
        raise ValueError("Horizons result table markers are missing")
    if "Center body name: Earth (399)" not in result:
        raise ValueError("Horizons response is not Earth-centred")
    if designation not in result:
        raise ValueError(f"Horizons response does not identify expected designation {designation}")
    text = canonical_json(payload)
    return FetchResult(
        requested_name=name,
        designation=designation,
        payload=payload,
        canonical_json=text,
        sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
    )


def request_url(designation: str) -> str:
    params = {
        "format": "json",
        "COMMAND": f"'{designation};'",
        "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'VECTORS'",
        "CENTER": "'500@399'",
        "START_TIME": f"'{QUERY_START}'",
        "STOP_TIME": f"'{QUERY_STOP}'",
        "STEP_SIZE": "'1 d'",
        "TIME_TYPE": "'TDB'",
        "OUT_UNITS": "'AU-D'",
        "REF_SYSTEM": "'ICRF'",
        "REF_PLANE": "'ECLIPTIC'",
        "VEC_TABLE": "'3'",
        "VEC_CORR": "'NONE'",
        "CSV_FORMAT": "'YES'",
        "VEC_LABELS": "'YES'",
    }
    return f"{HORIZONS_ENDPOINT}?{urllib.parse.urlencode(params)}"


def fetch_object(name: str, designation: str) -> FetchResult:
    url = request_url(designation)
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
            return result_from_payload(name, designation, payload)
        except (
            urllib.error.URLError,
            urllib.error.HTTPError,
            TimeoutError,
            ValueError,
            json.JSONDecodeError,
        ) as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                time.sleep(min(25, attempt * 4))
    raise RuntimeError(f"Failed to fetch Horizons data for {name}: {last_error}")


def cached_object(name: str, designation: str) -> FetchResult | None:
    path = OUTPUT_DIR / f"{slugify(name)}.json"
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            return None
        return result_from_payload(name, designation, payload)
    except (OSError, ValueError, json.JSONDecodeError):
        return None


def parse_float(value: str) -> float:
    return float(value.strip().replace("D", "E"))


def parse_samples(payload: dict[str, Any]) -> list[VectorSample]:
    result = str(payload["result"])
    table = result.split("$$SOE", 1)[1].split("$$EOE", 1)[0]
    samples: list[VectorSample] = []
    for parsed in csv.reader(io.StringIO(table)):
        fields = [field.strip() for field in parsed if field.strip()]
        if len(fields) < 11:
            continue
        match = DATE_RE.search(fields[1])
        if not match:
            continue
        try:
            sample_date = datetime.strptime(match.group("date"), "%Y-%b-%d").date()
            julian_date = parse_float(fields[0])
            x_au = parse_float(fields[2])
            y_au = parse_float(fields[3])
            z_au = parse_float(fields[4])
            vx_au_per_day = parse_float(fields[5])
            vy_au_per_day = parse_float(fields[6])
            vz_au_per_day = parse_float(fields[7])
            light_time_days = parse_float(fields[8])
            range_au = parse_float(fields[9])
            range_rate = parse_float(fields[10])
        except (ValueError, IndexError):
            continue
        if range_au <= 0:
            raise ValueError(f"Non-positive Horizons range encountered: {range_au}")
        samples.append(
            VectorSample(
                calendar_date=sample_date,
                calendar_label=fields[1],
                julian_date_tdb=julian_date,
                x_au=x_au,
                y_au=y_au,
                z_au=z_au,
                vx_au_per_day=vx_au_per_day,
                vy_au_per_day=vy_au_per_day,
                vz_au_per_day=vz_au_per_day,
                light_time_days=light_time_days,
                range_au=range_au,
                range_rate_au_per_day=range_rate,
            )
        )
    if len(samples) < 400:
        raise ValueError(f"Expected at least 400 daily samples across full span; received {len(samples)}")
    if samples != sorted(samples, key=lambda sample: sample.julian_date_tdb):
        raise ValueError("Horizons samples are not chronologically ordered")
    return samples


def summarize_window(
    name: str,
    designation: str,
    label: str,
    start: date,
    stop: date,
    samples: list[VectorSample],
    signature: dict[str, Any],
    sha256: str,
    captured_at: str,
    refresh_status: str,
    refresh_error: str | None,
) -> dict[str, Any]:
    selected = [sample for sample in samples if start <= sample.calendar_date < stop]
    if len(selected) < MIN_WINDOW_SAMPLES:
        raise ValueError(
            f"{name} {label}: expected at least {MIN_WINDOW_SAMPLES} daily samples; received {len(selected)}"
        )
    nearest = min(selected, key=lambda sample: sample.range_au)
    farthest = max(selected, key=lambda sample: sample.range_au)
    return {
        "requested_name": name,
        "designation": designation,
        "window": label,
        "window_start": start.isoformat(),
        "window_stop_exclusive": stop.isoformat(),
        "sample_count": len(selected),
        "first_sample_date": selected[0].calendar_date.isoformat(),
        "last_sample_date": selected[-1].calendar_date.isoformat(),
        "minimum_earth_relative_range_au": nearest.range_au,
        "minimum_range_date": nearest.calendar_date.isoformat(),
        "maximum_earth_relative_range_au": farthest.range_au,
        "maximum_range_date": farthest.calendar_date.isoformat(),
        "mean_earth_relative_range_au": statistics.fmean(sample.range_au for sample in selected),
        "median_earth_relative_range_au": statistics.median(sample.range_au for sample in selected),
        "start_range_au": selected[0].range_au,
        "end_range_au": selected[-1].range_au,
        "range_change_au": selected[-1].range_au - selected[0].range_au,
        "minimum_range_rate_au_per_day": min(sample.range_rate_au_per_day for sample in selected),
        "maximum_range_rate_au_per_day": max(sample.range_rate_au_per_day for sample in selected),
        "mean_range_rate_au_per_day": statistics.fmean(sample.range_rate_au_per_day for sample in selected),
        "minimum_range_state_jd_tdb": nearest.julian_date_tdb,
        "minimum_range_x_au": nearest.x_au,
        "minimum_range_y_au": nearest.y_au,
        "minimum_range_z_au": nearest.z_au,
        "minimum_range_vx_au_per_day": nearest.vx_au_per_day,
        "minimum_range_vy_au_per_day": nearest.vy_au_per_day,
        "minimum_range_vz_au_per_day": nearest.vz_au_per_day,
        "minimum_range_speed_au_per_day": nearest.speed_au_per_day,
        "start_x_au": selected[0].x_au,
        "start_y_au": selected[0].y_au,
        "start_z_au": selected[0].z_au,
        "start_vx_au_per_day": selected[0].vx_au_per_day,
        "start_vy_au_per_day": selected[0].vy_au_per_day,
        "start_vz_au_per_day": selected[0].vz_au_per_day,
        "end_x_au": selected[-1].x_au,
        "end_y_au": selected[-1].y_au,
        "end_z_au": selected[-1].z_au,
        "end_vx_au_per_day": selected[-1].vx_au_per_day,
        "end_vy_au_per_day": selected[-1].vy_au_per_day,
        "end_vz_au_per_day": selected[-1].vz_au_per_day,
        "state_vector_available": True,
        "state_uncertainty_available": False,
        "source_center": "Earth (399), geocentric 500@399",
        "source_ephemeris_type": "VECTORS",
        "source_vector_table": 3,
        "source_units": "AU-D",
        "source_step": "1 day",
        "source_reference_system": "ICRF",
        "source_reference_plane": "ECLIPTIC",
        "signature_source": signature.get("source"),
        "signature_version": signature.get("version"),
        "source_url": request_url(designation),
        "sha256": sha256,
        "captured_at": captured_at,
        "refresh_status": refresh_status,
        "last_refresh_error": refresh_error,
        "interpretation_limit": "Geocentric geometric state vectors plus Earth-relative range/time comparison; not launch, delta-v, route, mining or target feasibility. Statistical state uncertainty/covariance is not attached in this lane.",
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
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    return write_if_changed(path, buffer.getvalue())


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    previous_manifest = load_json(MANIFEST_JSON)
    rows: list[dict[str, Any]] = []
    manifest_objects: dict[str, Any] = {}
    errors: list[str] = []
    changed = False

    for index, (name, designation) in enumerate(OBJECTS):
        refresh_status = "CAPTURED_CURRENT"
        refresh_error: str | None = None
        try:
            result = fetch_object(name, designation)
            raw_path = OUTPUT_DIR / f"{slugify(name)}.json"
            changed |= write_if_changed(raw_path, result.canonical_json)
        except Exception as exc:
            refresh_error = str(exc)
            errors.append(refresh_error)
            result = cached_object(name, designation)
            refresh_status = "RETAINED_VALIDATED_CACHE"
            if result is None:
                errors.append(f"No valid cached Horizons payload available for {name}")
                continue

        try:
            samples = parse_samples(result.payload)
            signature = result.payload["signature"]
            previous = previous_manifest.get("objects", {}).get(slugify(name), {})
            captured_at = (
                previous.get("captured_at")
                if previous.get("sha256") == result.sha256
                else utc_now()
            )
            object_rows = [
                summarize_window(
                    name,
                    designation,
                    label,
                    start,
                    stop,
                    samples,
                    signature,
                    result.sha256,
                    captured_at,
                    refresh_status,
                    refresh_error,
                )
                for label, start, stop in WINDOWS
            ]
        except (ValueError, KeyError) as exc:
            errors.append(f"{name}: {exc}")
            continue

        rows.extend(object_rows)
        slug = slugify(name)
        manifest_objects[slug] = {
            "requested_name": name,
            "designation": designation,
            "sha256": result.sha256,
            "captured_at": captured_at,
            "raw_path": (OUTPUT_DIR / f"{slug}.json").as_posix(),
            "source_url": request_url(designation),
            "signature_version": signature.get("version"),
            "full_span_sample_count": len(samples),
            "window_sample_counts": {
                row["window"]: row["sample_count"] for row in object_rows
            },
            "refresh_status": refresh_status,
            "last_refresh_error": refresh_error,
            "status": "captured" if refresh_status == "CAPTURED_CURRENT" else "retained_validated_cache",
        }

        if index < len(OBJECTS) - 1:
            time.sleep(REQUEST_DELAY_SECONDS)

    if not rows:
        print("No current or cached Horizons rows survived validation", file=sys.stderr)
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    object_order = {name: index for index, (name, _) in enumerate(OBJECTS)}
    window_order = {label: index for index, (label, _, _) in enumerate(WINDOWS)}
    rows.sort(key=lambda row: (object_order[row["requested_name"]], window_order[row["window"]]))

    manifest = {
        "schema": "romer.jpl.horizons.comparative-windows.v1",
        "endpoint": HORIZONS_ENDPOINT,
        "query_span": {"start": QUERY_START, "stop": QUERY_STOP, "step": "1 day"},
        "windows": [
            {"label": label, "start": start.isoformat(), "stop_exclusive": stop.isoformat()}
            for label, start, stop in WINDOWS
        ],
        "objects": manifest_objects,
        "errors": errors,
        "validation": [
            "JSON signature/version required.",
            "Earth (399) centre required.",
            "Expected small-body designation required in result header.",
            "At least 400 ordered daily samples required across the full query span.",
            f"At least {MIN_WINDOW_SAMPLES} samples required per month-wide comparison window.",
            "All ranges must be positive.",
            "Each parsed table-3 sample must contain finite XYZ position and XYZ velocity components.",
            "Vector table 3 is geometric state + light-time/range/range-rate; statistical state uncertainty/covariance is a separate acquisition gate.",
            "Transient upstream failures may use only cached raw payloads that pass all validations.",
        ],
        "interpretation_limit": "Geocentric geometric state vectors plus Earth-relative range/time comparison; not launch, delta-v, route, mining or target feasibility. Statistical state uncertainty/covariance is not attached in this lane.",
        "operating_state": {
            "current_hardware": ["Mark III", "Mark V"],
            "mark_iv": "Post-mission successor/next model of Mark III; not current input",
            "capacity_basis": "Active Mark III/capture-capable units x 1 m3",
        },
    }

    changed |= write_if_changed(
        SUMMARY_JSON, json.dumps(rows, ensure_ascii=False, indent=2) + "\n"
    )
    changed |= write_csv(SUMMARY_CSV, rows)
    changed |= write_if_changed(
        MANIFEST_JSON, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )

    print(json.dumps({"available_window_rows": len(rows), "errors": errors, "changed": changed}, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
