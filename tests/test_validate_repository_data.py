from __future__ import annotations

import csv
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "scripts" / "validate_repository_data.py"
SPEC = importlib.util.spec_from_file_location("validate_repository_data", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class RepositoryDataValidationTests(unittest.TestCase):
    def test_declared_json_hash_is_line_ending_independent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "payload.json"
            payload = {"b": [2, 3], "a": 1}
            canonical = json.dumps(
                payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ) + "\n"
            path.write_text(canonical.replace("\n", "\r\n"), encoding="utf-8")

            expected = validator.hashlib.sha256(canonical.encode("utf-8")).hexdigest()

            self.assertEqual(validator.declared_sha256(path), expected)

    def test_current_repository_contract_passes(self) -> None:
        stats, errors = validator.validate_repository()

        self.assertEqual(errors, [])
        self.assertEqual(stats["handoff_lanes"], 4)

    def test_duplicate_summary_identity_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = REPOSITORY_ROOT / "data" / "jpl" / "sbdb" / "latest"
            lane = root / "data" / "jpl" / "sbdb" / "latest"
            shutil.copytree(source, lane)
            contract = root / "schemas" / "jpl_normalized_handoff_contract.json"
            contract.parent.mkdir(parents=True)
            shutil.copy2(
                REPOSITORY_ROOT / "schemas" / "jpl_normalized_handoff_contract.json",
                contract,
            )

            summary_path = lane / "summary.json"
            rows = json.loads(summary_path.read_text(encoding="utf-8"))
            rows.append(dict(rows[0]))
            summary_path.write_text(json.dumps(rows), encoding="utf-8")

            csv_path = lane / "summary.csv"
            with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
                csv_rows = list(csv.DictReader(handle))
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(csv_rows[0]))
                writer.writeheader()
                writer.writerows(csv_rows + [dict(csv_rows[0])])

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "DATA_ROOT", root / "data"),
                patch.object(validator, "CONTRACT_PATH", contract),
            ):
                _, errors = validator.validate_repository()

            self.assertTrue(
                any("Summary identity duplicated" in error for error in errors), errors
            )
            self.assertTrue(
                any("object-count mismatch" in error for error in errors), errors
            )

    def test_json_csv_value_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = REPOSITORY_ROOT / "data" / "jpl" / "sbdb" / "latest"
            lane = root / "data" / "jpl" / "sbdb" / "latest"
            shutil.copytree(source, lane)
            contract = root / "schemas" / "jpl_normalized_handoff_contract.json"
            contract.parent.mkdir(parents=True)
            shutil.copy2(
                REPOSITORY_ROOT / "schemas" / "jpl_normalized_handoff_contract.json",
                contract,
            )

            csv_path = lane / "summary.csv"
            with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            rows[0]["orbit_invariant_status"] = "NOT_CHECKED"
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)

            with (
                patch.object(validator, "ROOT", root),
                patch.object(validator, "DATA_ROOT", root / "data"),
                patch.object(validator, "CONTRACT_PATH", contract),
            ):
                _, errors = validator.validate_repository()

            self.assertTrue(
                any("JSON/CSV value mismatch" in error for error in errors), errors
            )


if __name__ == "__main__":
    unittest.main()
