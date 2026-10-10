"""Deterministic reference utilities for the Post-Mix Composition Matrix.

Authority ceiling:
- mass-balance / feed-control arithmetic only;
- does not predict alloy phases, mechanical properties, process qualification,
  RFS/EMFF performance, or flight readiness.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping


@dataclass(frozen=True)
class BlendResult:
    total_rate: float
    composition: Dict[str, float]


def _require_nonnegative(name: str, value: float) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def normalize_composition(comp: Mapping[str, float], *, tol: float = 1e-9) -> Dict[str, float]:
    if not comp:
        raise ValueError("composition must not be empty")
    for key, value in comp.items():
        _require_nonnegative(key, float(value))
    total = float(sum(comp.values()))
    if total <= tol:
        raise ValueError("composition total must be positive")
    return {k: float(v) / total for k, v in comp.items()}


def blend(
    feed_rates: Mapping[str, float],
    feed_compositions: Mapping[str, Mapping[str, float]],
) -> BlendResult:
    """Return linear pre-process blend composition from measured feed rates."""
    if set(feed_rates) != set(feed_compositions):
        missing_comp = set(feed_rates) - set(feed_compositions)
        missing_rate = set(feed_compositions) - set(feed_rates)
        raise ValueError(f"feed keys differ; missing compositions={missing_comp}, missing rates={missing_rate}")

    total_rate = 0.0
    weighted: Dict[str, float] = {}
    for feed, rate_raw in feed_rates.items():
        rate = float(rate_raw)
        _require_nonnegative(feed, rate)
        comp = normalize_composition(feed_compositions[feed])
        total_rate += rate
        for constituent, fraction in comp.items():
            weighted[constituent] = weighted.get(constituent, 0.0) + rate * fraction

    if total_rate <= 0:
        raise ValueError("total feed rate must be positive")

    return BlendResult(
        total_rate=total_rate,
        composition={k: v / total_rate for k, v in sorted(weighted.items())},
    )


def required_carrier_rate(concentrate_total_rate: float, carrier_to_concentrate_ratio: float) -> float:
    """Carrier needed when all selected concentrate streams retain their individual rates."""
    _require_nonnegative("concentrate_total_rate", concentrate_total_rate)
    _require_nonnegative("carrier_to_concentrate_ratio", carrier_to_concentrate_ratio)
    return concentrate_total_rate * carrier_to_concentrate_ratio


def scaled_concentrate_rates_for_fixed_carrier(
    carrier_rate: float,
    carrier_to_concentrate_ratio: float,
    requested_concentrate_rates: Mapping[str, float],
) -> Dict[str, float]:
    """Scale selected concentrates proportionally so the aggregate ratio is preserved."""
    _require_nonnegative("carrier_rate", carrier_rate)
    if carrier_to_concentrate_ratio <= 0:
        raise ValueError("carrier_to_concentrate_ratio must be > 0")
    requested_total = float(sum(requested_concentrate_rates.values()))
    if requested_total <= 0:
        raise ValueError("requested concentrate total must be positive")
    allowed_total = carrier_rate / carrier_to_concentrate_ratio
    scale = allowed_total / requested_total
    out: Dict[str, float] = {}
    for name, rate_raw in requested_concentrate_rates.items():
        rate = float(rate_raw)
        _require_nonnegative(name, rate)
        out[name] = rate * scale
    return out


def concentrate_fraction(carrier_rate: float, concentrate_rates: Mapping[str, float]) -> float:
    """Aggregate concentrate fraction of the pre-process stream."""
    _require_nonnegative("carrier_rate", carrier_rate)
    c = float(sum(concentrate_rates.values()))
    for name, rate in concentrate_rates.items():
        _require_nonnegative(name, float(rate))
    total = carrier_rate + c
    if total <= 0:
        raise ValueError("total flow must be positive")
    return c / total


if __name__ == "__main__":
    one = concentrate_fraction(5.0, {"A": 1.0})
    two_uncompensated = concentrate_fraction(5.0, {"A": 1.0, "B": 1.0})
    two_carrier_comp = concentrate_fraction(10.0, {"A": 1.0, "B": 1.0})
    two_scaled = scaled_concentrate_rates_for_fixed_carrier(5.0, 5.0, {"A": 1.0, "B": 1.0})
    print({
        "single_5_to_1": one,
        "two_full_fixed_carrier": two_uncompensated,
        "two_full_carrier_compensated": two_carrier_comp,
        "two_scaled_fixed_carrier": two_scaled,
    })
