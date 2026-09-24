#!/usr/bin/env python3
"""Capture JPL Small-Body Mission Design Mode-Q options for the six first-loop bodies.

The capture is source-first and adaptive. It records pre-computed ballistic mission options,
checks whether the mission-design orbit solution matches the current orbit solution, and
derives compact non-authoritative screening metrics. It does not select a target or claim
mission feasibility. Mode-M recomputation is intentionally deferred unless Q data are stale
or absent.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ENDPOINT = "https://ssd-api.jpl.nasa.gov/mdesign.api"
OBJECTS: tuple[tuple[str, str], ...] = (
    ("Apophis", "99942"),
    ("Castalia", "4769"),
    ("Toutatis", "4179"),
    ("Anteros", "1943"),
    ("Apollo", "1862"),
    ("Eros", "433"),
)
OUTPUT_DIR = Path("data/jpl/mdesign/latest")
REPORT_JSON = OUTPUT_DIR / "report.json"
MANIFEST_JSON = OUTPUT_DIR / "manifest.json"
USER_AGENT = "Romer-Industries-Cognigrex-JPL-Mission-Design/1.0"
TIMEOUT_SECONDS = 90
MAX_RETRIES = 5
REQUEST_DELAY_SECONDS = 1.5
MJD_EPOCH = datetime(1858, 11, 17, tzinfo=timezone.utc)
CURRENT_LAUNCH_START = datetime(2027, 1, 1, tzinfo=timezone.utc)
CURRENT_LAUNCH_STOP = datetime(2032, 12, 31, 23, 59, 59, tzinfo=timezone.utc)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slugify(value: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-") or "object"


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def request_mode_q(name: str) -> tuple[dict[str, Any], str, str]:
    params = {"sstr": name}
    url = ENDPOINT + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("Mission-design payload is not an object")
            sig = payload.get("signature")
            if not isinstance(sig, dict) or not sig.get("version"):
                raise ValueError("Mission-design signature/version missing")
            if payload.get("error") or payload.get("message") and not payload.get("selectedMissions"):
                raise ValueError(str(payload.get("error") or payload.get("message")))
            text = canonical_json(payload)
            return payload, text, hashlib.sha256(text.encode("utf-8")).hexdigest()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                time.sleep(min(20, attempt * 3))
    raise RuntimeError(f"Mode-Q fetch failed for {name}: {last_error}")


def mjd_to_datetime(value: float) -> datetime:
    return MJD_EPOCH + timedelta(days=value)


def finite(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def normalize(name: str, designation: str, payload: dict[str, Any], raw_sha: str) -> dict[str, Any]:
    obj = payload.get("object") if isinstance(payload.get("object"), dict) else {}
    fields = payload.get("fields") if isinstance(payload.get("fields"), list) else []
    missions = payload.get("selectedMissions") if isinstance(payload.get("selectedMissions"), list) else []
    index = {str(field): i for i, field in enumerate(fields)}

    required = {"MJD0", "MJDf", "vinf_dep", "vinf_arr"}
    if missions and not required.issubset(index):
        raise ValueError(f"{name}: Mode-Q fields missing {sorted(required - set(index))}")

    parsed: list[dict[str, Any]] = []
    for row in missions:
        if not isinstance(row, list):
            continue
        try:
            mjd0 = finite(row[index["MJD0"]])
            mjdf = finite(row[index["MJDf"]])
            vinf_dep = finite(row[index["vinf_dep"]])
            vinf_arr = finite(row[index["vinf_arr"]])
        except (IndexError, KeyError):
            continue
        if None in (mjd0, mjdf, vinf_dep, vinf_arr):
            continue
        dep = mjd_to_datetime(float(mjd0))
        arr = mjd_to_datetime(float(mjdf))
        tof = float(mjdf) - float(mjd0)
        rec = {
            "MJD0": float(mjd0),
            "MJDf": float(mjdf),
            "departure_date": dep.date().isoformat(),
            "arrival_date": arr.date().isoformat(),
            "tof_days": tof,
            "vinf_dep_km_s": float(vinf_dep),
            "vinf_arr_km_s": float(vinf_arr),
            "endpoint_vinf_sum_proxy_km_s": float(vinf_dep) + float(vinf_arr),
        }
        for optional in ("phase_ang", "earth_dist", "elong_arr", "decl_dep", "approach_ang"):
            if optional in index and index[optional] < len(row):
                rec[optional] = finite(row[index[optional]])
        parsed.append(rec)

    current = [
        rec for rec in parsed
        if CURRENT_LAUNCH_START <= mjd_to_datetime(rec["MJD0"]) <= CURRENT_LAUNCH_STOP
    ]

    def min_by(rows: list[dict[str, Any]], key: str) -> dict[str, Any] | None:
        return min(rows, key=lambda item: float(item[key])) if rows else None

    orbit_id = str(obj.get("orbit_id")) if obj.get("orbit_id") is not None else None
    md_orbit_id = str(obj.get("md_orbit_id")) if obj.get("md_orbit_id") is not None else None
    orbit_match = bool(orbit_id and md_orbit_id and orbit_id == md_orbit_id)

    return {
        "requested_name": name,
        "designation": designation,
        "object": obj,
        "signature": payload.get("signature"),
        "mission_count": len(parsed),
        "current_window_count_2027_2032": len(current),
        "orbit_id": orbit_id,
        "md_orbit_id": md_orbit_id,
        "orbit_match": orbit_match,
        "computed_on": obj.get("computed_on"),
        "mode_q_fields": fields,
        "min_departure_vinf_all": min_by(parsed, "vinf_dep_km_s"),
        "min_arrival_vinf_all": min_by(parsed, "vinf_arr_km_s"),
        "min_endpoint_vinf_sum_all": min_by(parsed, "endpoint_vinf_sum_proxy_km_s"),
        "min_tof_all": min_by(parsed, "tof_days"),
        "min_departure_vinf_2027_2032": min_by(current, "vinf_dep_km_s"),
        "min_arrival_vinf_2027_2032": min_by(current, "vinf_arr_km_s"),
        "min_endpoint_vinf_sum_2027_2032": min_by(current, "endpoint_vinf_sum_proxy_km_s"),
        "min_tof_2027_2032": min_by(current, "tof_days"),
        "raw_payload_sha256": raw_sha,
        "mode_m_recompute_gate": (
            "REQUIRED" if not orbit_match or len(current) == 0 else "NOT_REQUIRED_FOR_INITIAL_SCREEN"
        ),
        "claim_boundary": (
            "JPL pre-computed ballistic mission options and derived screening metrics only; "
            "not target selection, total system delta-V, launch-vehicle feasibility, capture feasibility, "
            "mining feasibility or mission approval."
        ),
    }


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report: list[dict[str, Any]] = []
    objects: dict[str, Any] = {}
    errors: list[str] = []

    for idx, (name, designation) in enumerate(OBJECTS):
        try:
            payload, raw_text, raw_sha = request_mode_q(name)
            raw_path = OUTPUT_DIR / f"{slugify(name)}.json"
            write(raw_path, raw_text)
            rec = normalize(name, designation, payload, raw_sha)
            report.append(rec)
            objects[slugify(name)] = {
                "requested_name": name,
                "designation": designation,
                "raw_path": raw_path.as_posix(),
                "sha256": raw_sha,
                "signature_version": (payload.get("signature") or {}).get("version"),
                "orbit_id": rec["orbit_id"],
                "md_orbit_id": rec["md_orbit_id"],
                "orbit_match": rec["orbit_match"],
                "mission_count": rec["mission_count"],
                "current_window_count_2027_2032": rec["current_window_count_2027_2032"],
                "mode_m_recompute_gate": rec["mode_m_recompute_gate"],
                "status": "captured",
            }
        except Exception as exc:
            errors.append(f"{name}: {exc}")
        if idx < len(OBJECTS) - 1:
            time.sleep(REQUEST_DELAY_SECONDS)

    report.sort(key=lambda rec: [name for name, _ in OBJECTS].index(rec["requested_name"]))
    report_text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    report_sha = hashlib.sha256(report_text.encode("utf-8")).hexdigest()
    write(REPORT_JSON, report_text)

    manifest = {
        "schema": "romer.jpl.mdesign.priority-mode-q.v0.1",
        "endpoint": ENDPOINT,
        "captured_at": utc_now(),
        "objects": objects,
        "report_receipt": {"path": REPORT_JSON.as_posix(), "sha256": report_sha},
        "errors": errors,
        "adaptive_policy": (
            "Mode-Q first. Run Mode-M only for bodies with stale/mismatched md_orbit_id, "
            "no current-window options, or a later mission-design question requiring a fresh launch/TOF grid."
        ),
        "claim_boundary": (
            "Mission-design source capture and screening only; no final target ranking or mission feasibility claim."
        ),
    }
    write(MANIFEST_JSON, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "captured": len(report),
        "errors": errors,
        "mode_m_required": [r["requested_name"] for r in report if r["mode_m_recompute_gate"] == "REQUIRED"],
    }, indent=2))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
