from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPOSITORY_ROOT / "scripts" / "validate_intersol_contracts.py"
SPEC = importlib.util.spec_from_file_location("validate_intersol_contracts", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class InterSolContractValidationTests(unittest.TestCase):
    def test_current_intersol_contracts_pass(self) -> None:
        self.assertEqual(validator.validate_intersol_contracts(), [])

    def test_assembly_identity_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            facility = Path(temp_dir) / "facility"
            web4 = Path(temp_dir) / "web4"
            schemas = Path(temp_dir) / "schemas"
            facility.mkdir(parents=True)
            web4.mkdir(parents=True)
            schemas.mkdir(parents=True)

            for source in validator.FACILITY.glob("*.json"):
                (facility / source.name).write_bytes(source.read_bytes())
            for source in validator.WEB4.glob("*.json"):
                (web4 / source.name).write_bytes(source.read_bytes())
            for source in validator.SCHEMAS.glob("*.json"):
                (schemas / source.name).write_bytes(source.read_bytes())

            matrix_path = facility / "intersol_facility_finalization_matrix_v0_1.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            matrix["assemblies"][0]["id"] = "IFM-999"
            matrix_path.write_text(json.dumps(matrix), encoding="utf-8")

            with (
                patch.object(validator, "ROOT", Path(temp_dir)),
                patch.object(validator, "FACILITY", facility),
                patch.object(validator, "WEB4", web4),
                patch.object(validator, "SCHEMAS", schemas),
            ):
                errors = validator.validate_intersol_contracts()

            self.assertTrue(any("assembly" in error for error in errors), errors)

    def test_economic_enablement_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            facility = Path(temp_dir) / "facility"
            web4 = Path(temp_dir) / "web4"
            schemas = Path(temp_dir) / "schemas"
            facility.mkdir(parents=True)
            web4.mkdir(parents=True)
            schemas.mkdir(parents=True)

            for source in validator.FACILITY.glob("*.json"):
                (facility / source.name).write_bytes(source.read_bytes())
            for source in validator.WEB4.glob("*.json"):
                (web4 / source.name).write_bytes(source.read_bytes())
            for source in validator.SCHEMAS.glob("*.json"):
                (schemas / source.name).write_bytes(source.read_bytes())

            coin_path = web4 / "infrastructure_coin_provenance_map_v0_1.json"
            coin = json.loads(coin_path.read_text(encoding="utf-8"))
            coin["object_mappings"][0]["economic"] = "ENABLED"
            coin_path.write_text(json.dumps(coin), encoding="utf-8")

            with (
                patch.object(validator, "ROOT", Path(temp_dir)),
                patch.object(validator, "FACILITY", facility),
                patch.object(validator, "WEB4", web4),
                patch.object(validator, "SCHEMAS", schemas),
            ):
                errors = validator.validate_intersol_contracts()

            self.assertTrue(any("economic hold" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
