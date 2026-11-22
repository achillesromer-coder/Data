import math
import unittest

from tools.functional_voxel_model import (
    FunctionalRegion,
    bead_volume_mm3,
    cavity_function,
    compatibility_allows_same_process,
    insert_thermal_budget_ok,
    line_energy_j_per_mm,
    slice_composition,
    diluted_composition,
    required_feed_composition_for_target,
)


class FunctionalVoxelModelTests(unittest.TestCase):
    def test_nominal_2d_bead_has_finite_3d_volume(self):
        self.assertTrue(math.isclose(bead_volume_mm3(10, 2, 0.5), 10.0))

    def test_line_energy_bookkeeping(self):
        self.assertTrue(math.isclose(line_energy_j_per_mm(1000, 10), 100.0))

    def test_vacuum_is_not_general_gas_damping(self):
        self.assertEqual(cavity_function("vacuum")["damping"], "NO_GENERAL_GAS_DAMPING")
        self.assertTrue(cavity_function("gas")["damping"].startswith("POTENTIAL"))

    def test_insert_thermal_budget(self):
        self.assertTrue(insert_thermal_budget_ok(150, 100, 20))
        self.assertFalse(insert_thermal_budget_ok(120, 110, 20))

    def test_only_A_is_same_process_ready(self):
        self.assertTrue(compatibility_allows_same_process("A"))
        for code in ["B", "C", "D", "X"]:
            self.assertFalse(compatibility_allows_same_process(code))

    def test_slice_bookkeeping(self):
        r1 = FunctionalRegion("s", "structure", {"Fe": 1}, "E4", "DIGITAL")
        r2 = FunctionalRegion("c", "conductor", {"Cu": 1}, "E1", "DIGITAL")
        out = slice_composition([r1, r2], {"s": 3, "c": 1})
        self.assertTrue(math.isclose(out["Fe"], 0.75))
        self.assertTrue(math.isclose(out["Cu"], 0.25))

    def test_substrate_dilution_composition(self):
        out = diluted_composition({"Ni": 1.0}, {"Fe": 1.0}, 0.2)
        self.assertTrue(math.isclose(out["Ni"], 0.8))
        self.assertTrue(math.isclose(out["Fe"], 0.2))

    def test_backsolve_feed_for_target_under_dilution(self):
        feed = required_feed_composition_for_target(
            {"Ni": 0.7, "Fe": 0.3},
            {"Fe": 1.0},
            0.2,
        )
        self.assertTrue(math.isclose(feed["Ni"], 0.875))
        self.assertTrue(math.isclose(feed["Fe"], 0.125))
        local = diluted_composition(feed, {"Fe": 1.0}, 0.2)
        self.assertTrue(math.isclose(local["Ni"], 0.7))
        self.assertTrue(math.isclose(local["Fe"], 0.3))

    def test_infeasible_target_under_dilution_is_rejected(self):
        with self.assertRaises(ValueError):
            required_feed_composition_for_target(
                {"Ni": 0.9, "Fe": 0.1},
                {"Fe": 1.0},
                0.2,
            )


if __name__ == "__main__":
    unittest.main()
