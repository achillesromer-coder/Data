#!/usr/bin/env python3
"""Capture an actuator-independent Apophis 2029 Earth close-encounter baseline.

Adaptive source capture:
1) coarse 1-hour table-3 vectors over 2029-Apr-12..15,
2) 5-minute refinement around the coarse range minimum,
3) 30-second refinement around the 5-minute minimum,
4) one table-2x formal XYZ/VXYZ uncertainty sample at the final nominal epoch.

This does not model an intervention, impact probability, keyholes, capture or mission merit.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

HORIZONS_ENDPOINT = "https://ssd.jpl.nasa.gov/api/horizons.api"
DESIGNATION = "99942"
NAME = "Apophis"
OUTPUT_DIR = Path("data/jpl/horizons/events/apophis-2029")
SBDB_APOPHIS = Path("data/jpl/sbdb/latest/apophis.json")
MANIFEST_JSON = OUTPUT_DIR / "manifest.json"
EVENT_JSON = OUTPUT_DIR / "event.json"
USER_AGENT = "Romer-Industries-Cognigrex-Apophis-2029/1.0"
TIMEOUT_SECONDS = 90
MAX_RETRIES = 5


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def base_params(vec_table: str) -> dict[str, str]:
    return {
        "format": "json",
        "COMMAND": f"'{DESIGNATION};'",
        "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'",
        "EPHEM_TYPE": "'VECTORS'",
        "CENTER": "'500@399'",
        "TIME_TYPE": "'TDB'",
        "REF_SYSTEM": "'ICRF'",
        "REF_PLANE": "'ECLIPTIC'",
        "OUT_UNITS": "'AU-D'",
        "VEC_TABLE": f"'{vec_table}'",
        "VEC_CORR": "'NONE'",
        "CSV_FORMAT": "'YES'",
    }


def request(params: dict[str, str]) -> tuple[dict[str, Any], str, str]:
    url = HORIZONS_ENDPOINT + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    last_error: Exception | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
                payload = json.loads(response.read().decode("utf-8"))
            if not isinstance(payload, dict) or payload.get("error"):
                raise ValueError(f"Horizons error: {payload.get('error') if isinstance(payload, dict) else 'invalid payload'}")
            result = payload.get("result")
            if not isinstance(result, str) or "$$SOE" not in result or "$$EOE" not in result:
                raise ValueError("Horizons ephemeris markers missing")
            if "Center body name: Earth (399)" not in result or DESIGNATION not in result:
                raise ValueError("Horizons target/center identity check failed")
            text = canonical_json(payload)
            return payload, text, hashlib.sha256(text.encode("utf-8")).hexdigest()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                time.sleep(min(20, attempt * 3))
    raise RuntimeError(f"Horizons request failed: {last_error}")


def parse_table3(payload: dict[str, Any]) -> list[dict[str, float | str]]:
    body = payload["result"].split("$$SOE", 1)[1].split("$$EOE", 1)[0]
    out: list[dict[str, float | str]] = []
    for fields in csv.reader(io.StringIO(body)):
        fields = [field.strip() for field in fields]
        if len(fields) < 11 or not fields[0] or not fields[0][0].isdigit():
            continue
        jd = float(fields[0])
        x, y, z, vx, vy, vz, lt, rg, rr = [float(value) for value in fields[2:11]]
        vals = [jd, x, y, z, vx, vy, vz, lt, rg, rr]
        if not all(math.isfinite(value) for value in vals):
            raise ValueError("Non-finite table-3 value")
        rnorm = math.sqrt(x*x + y*y + z*z)
        speed = math.sqrt(vx*vx + vy*vy + vz*vz)
        radial = (x*vx + y*vy + z*vz) / rnorm
        transverse = math.sqrt(max(0.0, speed*speed - radial*radial))
        if not math.isclose(rnorm, rg, rel_tol=1e-11, abs_tol=1e-12):
            raise ValueError("table-3 |r| != RG")
        if not math.isclose(radial, rr, rel_tol=1e-9, abs_tol=1e-12):
            raise ValueError("table-3 radial derivative != RR")
        out.append({
            "jd_tdb": jd, "calendar": fields[1],
            "x_au": x, "y_au": y, "z_au": z,
            "vx_au_per_day": vx, "vy_au_per_day": vy, "vz_au_per_day": vz,
            "light_time_days": lt, "range_au": rg, "range_rate_au_per_day": rr,
            "speed_au_per_day": speed, "radial_au_per_day": radial,
            "transverse_au_per_day": transverse,
        })
    if not out:
        raise ValueError("No table-3 rows parsed")
    return out


def parse_table2x(payload: dict[str, Any]) -> list[dict[str, float | str]]:
    body = payload["result"].split("$$SOE", 1)[1].split("$$EOE", 1)[0]
    out: list[dict[str, float | str]] = []
    for fields in csv.reader(io.StringIO(body)):
        fields = [field.strip() for field in fields]
        if len(fields) < 14 or not fields[0] or not fields[0][0].isdigit():
            continue
        jd = float(fields[0])
        vals = [float(value) for value in fields[2:14]]
        if not all(math.isfinite(value) for value in [jd, *vals]):
            raise ValueError("Non-finite table-2x value")
        x, y, z, vx, vy, vz, sx, sy, sz, svx, svy, svz = vals
        out.append({
            "jd_tdb": jd, "calendar": fields[1],
            "x_au": x, "y_au": y, "z_au": z,
            "vx_au_per_day": vx, "vy_au_per_day": vy, "vz_au_per_day": vz,
            "x_sigma_au_1s": sx, "y_sigma_au_1s": sy, "z_sigma_au_1s": sz,
            "vx_sigma_au_per_day_1s": svx, "vy_sigma_au_per_day_1s": svy, "vz_sigma_au_per_day_1s": svz,
        })
    if not out:
        raise ValueError("No table-2x rows parsed")
    return out


def parse_calendar(label: str) -> datetime:
    clean = label.replace("A.D.", "").strip()
    return datetime.strptime(clean, "%Y-%b-%d %H:%M:%S.%f")


def calendar_span(center_label: str, half_span: timedelta) -> tuple[str, str]:
    center = parse_calendar(center_label)
    start = center - half_span
    stop = center + half_span
    return start.strftime("%Y-%m-%d %H:%M:%S"), stop.strftime("%Y-%m-%d %H:%M:%S")


def tlist(center_jd: float, half_span_seconds: int, step_seconds: int) -> str:
    values = []
    for offset in range(-half_span_seconds, half_span_seconds + 1, step_seconds):
        values.append(f"'{center_jd + offset / 86400.0:.12f}'")
    return " ".join(values)


def load_sbdb_close_approach() -> tuple[dict[str, Any], str]:
    payload = json.loads(SBDB_APOPHIS.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Apophis SBDB payload is not an object")
    matches = [
        row for row in payload.get("ca_data", [])
        if isinstance(row, dict)
        and row.get("body") == "Earth"
        and str(row.get("cd", "")).startswith("2029-Apr-13")
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected one Apophis 2029 Earth close-approach row, got {len(matches)}")
    text = canonical_json(payload)
    return matches[0], hashlib.sha256(text.encode("utf-8")).hexdigest()


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    coarse_params = base_params("3")
    coarse_params.update({
        "START_TIME": "'2029-04-12'",
        "STOP_TIME": "'2029-04-15'",
        "STEP_SIZE": "'1 h'",
    })
    coarse_payload, coarse_text, coarse_sha = request(coarse_params)
    coarse = parse_table3(coarse_payload)
    coarse_min = min(coarse, key=lambda row: float(row["range_au"]))

    refine5_params = base_params("3")
    refine5_start, refine5_stop = calendar_span(str(coarse_min["calendar"]), timedelta(hours=3))
    refine5_params.update({
        "START_TIME": f"'{refine5_start}'",
        "STOP_TIME": f"'{refine5_stop}'",
        "STEP_SIZE": "'5 m'",
    })
    refine5_payload, refine5_text, refine5_sha = request(refine5_params)
    refine5 = parse_table3(refine5_payload)
    refine5_min = min(refine5, key=lambda row: float(row["range_au"]))

    refine30_params = base_params("3")
    refine30_params.update({"TLIST": tlist(float(refine5_min["jd_tdb"]), 5*60, 30), "TLIST_TYPE": "'JD'"})
    refine30_payload, refine30_text, refine30_sha = request(refine30_params)
    refine30 = parse_table3(refine30_payload)
    final_min = min(refine30, key=lambda row: float(row["range_au"]))

    unc_params = base_params("2x")
    unc_params.update({"TLIST": f"'{float(final_min['jd_tdb']):.12f}'", "TLIST_TYPE": "'JD'"})
    unc_payload, unc_text, unc_sha = request(unc_params)
    unc_rows = parse_table2x(unc_payload)
    if len(unc_rows) != 1:
        raise ValueError(f"Expected one uncertainty row, got {len(unc_rows)}")
    unc = unc_rows[0]

    sbdb_ca, sbdb_sha = load_sbdb_close_approach()

    dp = math.sqrt(
        (float(final_min["x_au"])-float(unc["x_au"]))**2
        + (float(final_min["y_au"])-float(unc["y_au"]))**2
        + (float(final_min["z_au"])-float(unc["z_au"]))**2
    )
    dv = math.sqrt(
        (float(final_min["vx_au_per_day"])-float(unc["vx_au_per_day"]))**2
        + (float(final_min["vy_au_per_day"])-float(unc["vy_au_per_day"]))**2
        + (float(final_min["vz_au_per_day"])-float(unc["vz_au_per_day"]))**2
    )

    write(OUTPUT_DIR / "coarse_1h.json", coarse_text)
    write(OUTPUT_DIR / "refine_5m.json", refine5_text)
    write(OUTPUT_DIR / "refine_30s.json", refine30_text)
    write(OUTPUT_DIR / "uncertainty_2x.json", unc_text)

    interpolated_zero_rr_jd = float(final_min["jd_tdb"]) - float(final_min["range_rate_au_per_day"]) * (30.0 / 86400.0) / (
        float(refine30[min(range(len(refine30)), key=lambda i: abs(float(refine30[i]["jd_tdb"]) - float(final_min["jd_tdb"]) - 30.0/86400.0))]["range_rate_au_per_day"])
        - float(final_min["range_rate_au_per_day"])
    )
    sbdb_jd = float(sbdb_ca["jd"])
    sbdb_dist_au = float(sbdb_ca["dist"])

    summary = {
        "schema": "romer.jpl.horizons.apophis-2029-no-intervention.v0.2",
        "target": NAME,
        "designation": DESIGNATION,
        "center": "Earth (399), geocentric 500@399",
        "frame": "ICRF axes / ecliptic J2000 reference plane as requested",
        "units": "AU-D",
        "baseline_type": "NO-INTERVENTION NOMINAL SOURCE BASELINE",
        "coarse_minimum": coarse_min,
        "refine_5m_minimum": refine5_min,
        "refine_30s_minimum": final_min,
        "formal_state_uncertainty_1s": unc,
        "sbdb_close_approach_crosscheck": {
            "body": sbdb_ca["body"],
            "calendar_tdb": sbdb_ca["cd"],
            "jd_tdb": sbdb_jd,
            "nominal_distance_au": sbdb_dist_au,
            "distance_min_3sigma_au": float(sbdb_ca["dist_min"]),
            "distance_max_3sigma_au": float(sbdb_ca["dist_max"]),
            "time_uncertainty_3sigma_minutes": float(sbdb_ca["sigma_t"]),
            "time_uncertainty_formatted": sbdb_ca["sigma_tf"],
            "bplane_semimajor_1sigma_km": float(sbdb_ca["unc_major"]),
            "bplane_semiminor_1sigma_km": float(sbdb_ca["unc_minor"]),
            "bplane_major_axis_angle_deg": float(sbdb_ca["unc_angle"]),
            "relative_velocity_km_s": float(sbdb_ca["v_rel"]),
            "hyperbolic_excess_velocity_km_s": float(sbdb_ca["v_inf"]),
            "orbit_ref": sbdb_ca["orbit_ref"],
            "sbdb_payload_sha256": sbdb_sha,
            "interpolated_zero_rr_time_delta_seconds": (interpolated_zero_rr_jd - sbdb_jd) * 86400.0,
            "interpolated_range_delta_km": (
                float(final_min["range_au"]) - sbdb_dist_au
            ) * 149597870.7,
            "interpretation": "SBDB direct close-approach product is authoritative for nominal TCA, 3-sigma distance/time bounds and 1-sigma B-plane ellipse. Horizons table-3 refinement is retained as an independent state/zero-RR cross-check.",
        },
        "table3_vs_2x_position_delta_au": dp,
        "table3_vs_2x_velocity_delta_au_per_day": dv,
        "source_hashes": {
            "coarse_1h": coarse_sha,
            "refine_5m": refine5_sha,
            "refine_30s": refine30_sha,
            "uncertainty_2x": unc_sha,
        },
        "claim_boundary": (
            "This is a nominal no-intervention source baseline and formal component-uncertainty cross-check. "
            "It is not an impact probability, B-plane/keyhole analysis, intervention recommendation, capture state, or safety certification."
        ),
    }
    summary_text = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=False) + "\n"
    write(EVENT_JSON, summary_text)
    event_sha = hashlib.sha256(summary_text.encode("utf-8")).hexdigest()

    manifest = {
        "schema": "romer.jpl.horizons.apophis-2029-event-capture.v0.2",
        "captured_at": utc_now(),
        "event_sha256": event_sha,
        "source_receipts": [
            {"raw_path": (OUTPUT_DIR / "coarse_1h.json").as_posix(), "sha256": coarse_sha},
            {"raw_path": (OUTPUT_DIR / "refine_5m.json").as_posix(), "sha256": refine5_sha},
            {"raw_path": (OUTPUT_DIR / "refine_30s.json").as_posix(), "sha256": refine30_sha},
            {"raw_path": (OUTPUT_DIR / "uncertainty_2x.json").as_posix(), "sha256": unc_sha},
            {"raw_path": SBDB_APOPHIS.as_posix(), "sha256": sbdb_sha}
        ],
        "adaptive_levels": [
            {"name": "coarse", "step": "1 hour", "span": "2029-04-12..2029-04-15"},
            {"name": "refine", "step": "5 minutes", "span": "+/-3 hours around coarse minimum"},
            {"name": "final", "step": "30 seconds", "span": "+/-10 minutes around 5-minute minimum"},
            {"name": "uncertainty", "table": "2x", "epochs": 1, "definition": "formal 1-sigma XYZ/VXYZ component uncertainty"},
        ],
        "guardrails": [
            "No intervention is applied.",
            "Range minima are source-sampled/refined nominal geometry, not impact probabilities.",
            "Formal 1-sigma vector components do not replace full SBDB covariance.",
            "The SBDB close-approach record is used directly for 3-sigma TCA/distance bounds and 1-sigma B-plane ellipse parameters; do not re-derive those from the reduced event sample.",
            "Any hypothetical deflection analysis must start from and preserve the validated no-intervention baseline as the control.",
        ],
    }
    write(MANIFEST_JSON, json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"final_jd_tdb": final_min["jd_tdb"], "final_range_au": final_min["range_au"], "event_sha256": event_sha}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
