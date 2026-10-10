import math
import unittest

from tools.material_postmix_solver import (
    blend,
    concentrate_fraction,
    required_carrier_rate,
    scaled_concentrate_rates_for_fixed_carrier,
)


class PostMixSolverTests(unittest.TestCase):
    def test_single_five_to_one(self):
        self.assertTrue(math.isclose(concentrate_fraction(5.0, {"A": 1.0}), 1.0 / 6.0))

    def test_two_full_concentrates_without_compensation_get_stronger(self):
        self.assertTrue(math.isclose(concentrate_fraction(5.0, {"A": 1.0, "B": 1.0}), 2.0 / 7.0))

    def test_carrier_compensation_preserves_fraction(self):
        self.assertEqual(required_carrier_rate(2.0, 5.0), 10.0)
        self.assertTrue(math.isclose(concentrate_fraction(10.0, {"A": 1.0, "B": 1.0}), 1.0 / 6.0))

    def test_fixed_carrier_scales_selected_concentrates(self):
        scaled = scaled_concentrate_rates_for_fixed_carrier(5.0, 5.0, {"A": 1.0, "B": 1.0})
        self.assertEqual(scaled, {"A": 0.5, "B": 0.5})
        self.assertTrue(math.isclose(concentrate_fraction(5.0, scaled), 1.0 / 6.0))

    def test_material_blend_is_mass_conserving(self):
        result = blend(
            {"cu_stock": 3.0, "bi_stock": 1.0},
            {
                "cu_stock": {"Cu": 1.0},
                "bi_stock": {"Bi": 1.0},
            },
        )
        self.assertEqual(result.total_rate, 4.0)
        self.assertTrue(math.isclose(result.composition["Cu"], 0.75))
        self.assertTrue(math.isclose(result.composition["Bi"], 0.25))
        self.assertTrue(math.isclose(sum(result.composition.values()), 1.0))


if __name__ == "__main__":
    unittest.main()
