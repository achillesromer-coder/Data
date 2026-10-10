"""Interaction-kernel utilities for the Raphael/standard fabrication compiler.

This module is deliberately model-agnostic. It composes interaction contributions,
computes a few established dimensionless/equilibrium bookkeeping quantities, and
checks environment envelopes. It does not replace CFD, FEA, chemistry, plasma,
semiconductor, or electrochemical solvers.
"""
from __future__ import annotations

from math import exp, log
from typing import Dict, Iterable, Mapping, Sequence, Tuple

R_GAS = 8.31446261815324
FARADAY = 96485.33212
BOLTZMANN = 1.380649e-23


def canonical_participants(ids: Iterable[str]) -> Tuple[str, ...]:
    vals = tuple(sorted(str(x) for x in ids))
    if not vals:
        raise ValueError("interaction requires at least one participant")
    if len(set(vals)) != len(vals):
        raise ValueError("participant IDs must be unique within an interaction term")
    return vals


def many_body_total(
    one_body: Mapping[str, float],
    pair_terms: Mapping[Tuple[str, str], float] | None = None,
    higher_terms: Mapping[Tuple[str, ...], float] | None = None,
) -> float:
    """Sum one-, two-, and higher-body contributions.

    Numerical contributions must already have a common physical meaning/unit.
    This function is bookkeeping, not a universal interaction law.
    """
    total = sum(float(v) for v in one_body.values())
    seen = set()
    for table in (pair_terms or {}, higher_terms or {}):
        for participants, contribution in table.items():
            key = canonical_participants(participants)
            if len(key) < 2:
                raise ValueError("pair/higher interaction must contain >=2 participants")
            if key in seen:
                raise ValueError(f"duplicate interaction term for {key}")
            seen.add(key)
            total += float(contribution)
    return total


def boltzmann_weights(delta_g_j_per_particle: Sequence[float], temperature_k: float) -> Tuple[float, ...]:
    """Normalized equilibrium weights for per-particle free-energy differences."""
    if temperature_k <= 0:
        raise ValueError("temperature_k must be positive")
    if not delta_g_j_per_particle:
        raise ValueError("at least one state is required")
    beta = 1.0 / (BOLTZMANN * temperature_k)
    scaled = [-float(g) * beta for g in delta_g_j_per_particle]
    m = max(scaled)
    weights = [exp(x - m) for x in scaled]
    z = sum(weights)
    return tuple(w / z for w in weights)


def electrochemical_potential_j_mol(
    mu0_j_mol: float,
    activity: float,
    charge_number: float,
    electric_potential_v: float,
    temperature_k: float,
) -> float:
    """Ideal-activity electrochemical-potential bookkeeping."""
    if activity <= 0:
        raise ValueError("activity must be positive")
    if temperature_k <= 0:
        raise ValueError("temperature_k must be positive")
    return (
        float(mu0_j_mol)
        + R_GAS * temperature_k * log(activity)
        + float(charge_number) * FARADAY * float(electric_potential_v)
    )


def reynolds_number(rho: float, velocity: float, length: float, dynamic_viscosity: float) -> float:
    if dynamic_viscosity <= 0 or rho < 0 or length < 0:
        raise ValueError("invalid Reynolds inputs")
    return rho * velocity * length / dynamic_viscosity


def peclet_number(velocity: float, length: float, diffusivity: float) -> float:
    if diffusivity <= 0 or length < 0:
        raise ValueError("invalid Peclet inputs")
    return velocity * length / diffusivity


def capillary_number(dynamic_viscosity: float, velocity: float, surface_tension: float) -> float:
    if surface_tension <= 0 or dynamic_viscosity < 0:
        raise ValueError("invalid Capillary inputs")
    return dynamic_viscosity * velocity / surface_tension


def weber_number(rho: float, velocity: float, length: float, surface_tension: float) -> float:
    if surface_tension <= 0 or rho < 0 or length < 0:
        raise ValueError("invalid Weber inputs")
    return rho * velocity * velocity * length / surface_tension


def knudsen_number(mean_free_path_m: float, characteristic_length_m: float) -> float:
    if mean_free_path_m < 0 or characteristic_length_m <= 0:
        raise ValueError("invalid Knudsen inputs")
    return mean_free_path_m / characteristic_length_m


def capability_check(
    environment: Mapping[str, object],
    requirement: Mapping[str, object],
) -> Dict[str, object]:
    """Evaluate a simple environment requirement contract.

    Supported requirement keys:
      sealed: bool
      pressure_pa_min / pressure_pa_max
      required_gases: iterable of gas names
      forbidden_gases: iterable of gas names
      temperature_k_min / temperature_k_max
    """
    reasons = []
    if "sealed" in requirement and bool(environment.get("sealed", False)) != bool(requirement["sealed"]):
        reasons.append("sealed_state")

    pressure = environment.get("pressure_pa")
    if "pressure_pa_min" in requirement:
        if pressure is None or float(pressure) < float(requirement["pressure_pa_min"]):
            reasons.append("pressure_below_min")
    if "pressure_pa_max" in requirement:
        if pressure is None or float(pressure) > float(requirement["pressure_pa_max"]):
            reasons.append("pressure_above_max")

    temperature = environment.get("temperature_k")
    if "temperature_k_min" in requirement:
        if temperature is None or float(temperature) < float(requirement["temperature_k_min"]):
            reasons.append("temperature_below_min")
    if "temperature_k_max" in requirement:
        if temperature is None or float(temperature) > float(requirement["temperature_k_max"]):
            reasons.append("temperature_above_max")

    gases = {str(x) for x in environment.get("gases", [])}
    for gas in requirement.get("required_gases", []):
        if str(gas) not in gases:
            reasons.append(f"missing_gas:{gas}")
    for gas in requirement.get("forbidden_gases", []):
        if str(gas) in gases:
            reasons.append(f"forbidden_gas:{gas}")

    return {"allowed": not reasons, "reasons": tuple(reasons)}


def compare_model_residuals(
    observations: Sequence[float],
    standard_predictions: Sequence[float],
    candidate_predictions: Sequence[float],
) -> Dict[str, float | bool]:
    """Compare RMSE of a candidate/hypothesis model to a standard baseline."""
    if not observations or len(observations) != len(standard_predictions) or len(observations) != len(candidate_predictions):
        raise ValueError("observation and prediction vectors must be non-empty and equal length")

    def rmse(pred: Sequence[float]) -> float:
        return (
            sum((float(y) - float(p)) ** 2 for y, p in zip(observations, pred))
            / len(observations)
        ) ** 0.5

    std = rmse(standard_predictions)
    cand = rmse(candidate_predictions)
    return {
        "standard_rmse": std,
        "candidate_rmse": cand,
        "candidate_improves_rmse": cand < std,
        "rmse_delta": cand - std,
    }
