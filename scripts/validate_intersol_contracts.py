#!/usr/bin/env python3
"""Validate cross-file invariants in the InterSol control manifests."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FACILITY = ROOT / "data" / "intersol" / "facility"
WEB4 = ROOT / "data" / "intersol" / "web4"
SCHEMAS = ROOT / "schemas"


def load(path: Path, errors: list[str]) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"Unreadable contract: {path.relative_to(ROOT).as_posix()}: {exc}")
        return {}
    if not isinstance(payload, dict):
        errors.append(f"Contract is not an object: {path.relative_to(ROOT).as_posix()}")
        return {}
    return payload


def expected_ids(prefix: str, count: int) -> list[str]:
    return [f"{prefix}-{index:03d}" for index in range(1, count + 1)]


def require_equal(errors: list[str], label: str, actual: Any, expected: Any) -> None:
    if actual != expected:
        errors.append(f"{label}: expected={expected!r} actual={actual!r}")


def require_unique(errors: list[str], label: str, values: list[Any]) -> None:
    if len(values) != len(set(values)):
        errors.append(f"{label}: duplicate values present")


def parse_id_range(value: Any) -> tuple[str, int] | None:
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"([A-Z]+)-001\.\.\1-(\d{3})", value)
    if not match:
        return None
    return match.group(1), int(match.group(2))


def validate_intersol_contracts() -> list[str]:
    errors: list[str] = []

    progression = load(FACILITY / "cognigrex_progression_rules_v0_1.json", errors)
    rules = progression.get("rules", [])
    require_equal(errors, "progression rule count", len(rules), progression.get("canonical_rule_count"))
    require_equal(
        errors,
        "progression rule sequence",
        [row.get("id") for row in rules if isinstance(row, dict)],
        expected_ids("CPR", 12),
    )

    bod = load(FACILITY / "intersol_facility_bod_seed_v0_1.json", errors)
    finalization = load(FACILITY / "intersol_facility_finalization_matrix_v0_1.json", errors)
    bod_ids = [row.get("assembly_id") for row in bod.get("assemblies", []) if isinstance(row, dict)]
    matrix_ids = [row.get("id") for row in finalization.get("assemblies", []) if isinstance(row, dict)]
    require_equal(errors, "BOD assembly sequence", bod_ids, expected_ids("IFM", 18))
    require_equal(errors, "finalization assembly sequence", matrix_ids, expected_ids("IFM", 18))
    require_equal(errors, "BOD/finalization assembly identity parity", bod_ids, matrix_ids)
    require_equal(
        errors,
        "BOD/finalization operating-state parity",
        bod.get("shared_operational_states"),
        finalization.get("global_operating_states"),
    )

    space_program = load(FACILITY / "intersol_space_program_v0_1.json", errors)
    grouped_space_ids = [
        item
        for values in space_program.get("programme_groups", {}).values()
        if isinstance(values, list)
        for item in values
    ]
    require_equal(errors, "space-program ID sequence", sorted(grouped_space_ids), expected_ids("ISP", 48))
    require_equal(errors, "space-program row count", len(grouped_space_ids), space_program.get("row_count"))
    require_unique(errors, "space-program IDs", grouped_space_ids)

    human_factors = load(FACILITY / "intersol_human_factors_safety_v0_1.json", errors)
    hfs_ids = list(human_factors.get("priority_controls", {}).values())
    require_equal(errors, "human-factors control sequence", sorted(hfs_ids), expected_ids("HFS", 25))
    require_equal(errors, "human-factors control count", len(hfs_ids), human_factors.get("control_count"))
    require_unique(errors, "human-factors control IDs", hfs_ids)

    for filename, list_field in (
        ("intersol_hazard_trigger_matrix_v0_1.json", "families"),
        ("intersol_missing_inputs_queue_v0_1.json", "priority_order"),
        ("intersol_post_occupancy_learning_v0_1.json", "domains"),
        ("intersol_site_block_planning_v0_1.json", "coverage"),
    ):
        payload = load(FACILITY / filename, errors)
        values = payload.get(list_field, [])
        require_equal(errors, f"{filename} record count", len(values), payload.get("record_count"))
        require_unique(errors, f"{filename} {list_field}", values)

    missing_inputs = load(FACILITY / "intersol_missing_inputs_queue_v0_1.json", errors)
    dependency_ids = [str(value).split(" ", 1)[0] for value in missing_inputs.get("priority_order", [])]
    require_equal(
        errors,
        "missing-input reach-map identities",
        sorted(missing_inputs.get("cross_system_reach", {})),
        sorted(dependency_ids),
    )

    implementation = load(FACILITY / "intersol_longitudinal_implementation_states_v0_1.json", errors)
    phase_and_state_count = len(implementation.get("phases", [])) + len(implementation.get("operational_states", []))
    require_equal(errors, "implementation phase/state count", phase_and_state_count, implementation.get("state_count"))

    for filename in (
        "intersol_commissioning_acceptance_v0_1.json",
        "intersol_hazard_trigger_matrix_v0_1.json",
        "intersol_requirements_traceability_v0_1.json",
        "intersol_room_input_requirements_v0_1.json",
    ):
        payload = load(FACILITY / filename, errors)
        parsed = parse_id_range(payload.get("key_ids"))
        if parsed is None:
            errors.append(f"{filename} key_ids: invalid declared range")
        else:
            require_equal(errors, f"{filename} key range count", parsed[1], payload.get("record_count"))

    readiness = load(FACILITY / "intersol_readiness_scorecard_v0_1.json", errors)
    expected_control_rows = sum((18, 48, 25, 18, 30, 20, 17, 20, 24, 25, 18, 25, 24))
    require_equal(
        errors,
        "readiness principal control-row arithmetic",
        readiness.get("observed_metrics", {}).get("principal_current_control_rows"),
        expected_control_rows,
    )
    require_equal(
        errors,
        "readiness economic-layer hold",
        readiness.get("observed_metrics", {}).get("economic_token_layers_enabled"),
        0,
    )

    receipt_schema = load(SCHEMAS / "intersol_multiobjective_optimization_receipt_fields.json", errors)
    receipt_fields = receipt_schema.get("fields", [])
    field_names = [row.get("name") for row in receipt_fields if isinstance(row, dict)]
    require_unique(errors, "optimization receipt field names", field_names)
    if not receipt_fields or not all(row.get("required") is True for row in receipt_fields if isinstance(row, dict)):
        errors.append("optimization receipt fields: every declared field must remain required")

    coin = load(WEB4 / "infrastructure_coin_provenance_map_v0_1.json", errors)
    require_equal(errors, "COIN operating default", coin.get("operating_default"), "COIN_FIRST_NON_MONETARY")
    economic_states = [row.get("economic") for row in coin.get("object_mappings", []) if isinstance(row, dict)]
    if not economic_states or any(not str(state).startswith("DISABLED") for state in economic_states):
        errors.append("COIN economic hold: every object mapping must remain disabled")

    publish = load(FACILITY / "intersol_publish_handoff_v0_1.json", errors)
    require_equal(errors, "publication hold", publish.get("first_publish", {}).get("state"), "PREP_NOT_RELEASED")
    require_equal(errors, "BOD economic hold", bod.get("economic_state"), "DISABLED")

    return errors


def main() -> int:
    errors = validate_intersol_contracts()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"InterSol contract validation failed with {len(errors)} error(s).")
        return 1
    print("InterSol cross-file contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
