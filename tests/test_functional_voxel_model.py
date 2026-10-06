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


if __name__ == "__main__":
    unittest.main()
