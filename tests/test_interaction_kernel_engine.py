import math
import unittest

from tools.interaction_kernel_engine import (
    boltzmann_weights,
    canonical_participants,
    capability_check,
    compare_model_residuals,
    electrochemical_potential_j_mol,
    knudsen_number,
    many_body_total,
    peclet_number,
    reynolds_number,
)


class InteractionKernelTests(unittest.TestCase):
    def test_canonical_participant_order(self):
        self.assertEqual(canonical_participants(["b", "a", "c"]), ("a", "b", "c"))

    def test_many_body_keeps_nonadditive_triplet(self):
        total = many_body_total(
            {"a": 1.0, "b": 2.0, "c": 3.0},
            {("a", "b"): 0.5, ("b", "c"): 0.25},
            {("a", "b", "c"): -0.75},
        )
        self.assertTrue(math.isclose(total, 6.0))

    def test_boltzmann_lower_free_energy_is_more_probable(self):
        w = boltzmann_weights([0.0, 1e-21], 300.0)
        self.assertTrue(math.isclose(sum(w), 1.0))
        self.assertGreater(w[0], w[1])

    def test_electrochemical_potential_charge_term(self):
        neutral = electrochemical_potential_j_mol(0.0, 1.0, 0, 1.0, 298.15)
        charged = electrochemical_potential_j_mol(0.0, 1.0, 1, 1.0, 298.15)
        self.assertTrue(math.isclose(neutral, 0.0))
        self.assertGreater(charged, 96000.0)

    def test_dimensionless_scale_numbers(self):
        self.assertTrue(math.isclose(reynolds_number(1000, 1, 0.001, 0.001), 1000.0))
        self.assertTrue(math.isclose(peclet_number(1, 0.001, 1e-9), 1e6))
        self.assertTrue(math.isclose(knudsen_number(1e-7, 1e-4), 1e-3))

    def test_open_environment_allows_open_operation(self):
        env = {"sealed": False, "pressure_pa": 101325, "temperature_k": 298, "gases": ["air"]}
        req = {"sealed": False, "pressure_pa_min": 90000, "pressure_pa_max": 110000}
        self.assertTrue(capability_check(env, req)["allowed"])

    def test_open_environment_rejects_inert_sealed_operation(self):
        env = {"sealed": False, "pressure_pa": 101325, "temperature_k": 298, "gases": ["air"]}
        req = {"sealed": True, "required_gases": ["argon"]}
        out = capability_check(env, req)
        self.assertFalse(out["allowed"])
        self.assertIn("sealed_state", out["reasons"])
        self.assertIn("missing_gas:argon", out["reasons"])

    def test_candidate_model_is_not_promoted_by_name(self):
        out = compare_model_residuals([1, 2, 3], [1.0, 2.0, 3.0], [2.0, 3.0, 4.0])
        self.assertFalse(out["candidate_improves_rmse"])
        self.assertTrue(math.isclose(out["standard_rmse"], 0.0))


if __name__ == "__main__":
    unittest.main()
