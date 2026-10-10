"""Reference digital-state utilities for functional-voxel manufacturing.

These functions are bookkeeping/architecture helpers only. They do not predict
microstructure, weld quality, pressure-vessel integrity, smart-material response,
or flight qualification.
"""
from dataclasses import dataclass
from typing import Dict, Iterable, Mapping


def normalize(comp: Mapping[str, float]) -> Dict[str, float]:
    if not comp:
        raise ValueError("composition cannot be empty")
    if any(float(v) < 0 for v in comp.values()):
        raise ValueError("composition values must be non-negative")
    s = float(sum(comp.values()))
    if s <= 0:
        raise ValueError("composition total must be positive")
    return {k: float(v) / s for k, v in comp.items()}


def line_energy_j_per_mm(power_w: float, speed_mm_s: float) -> float:
    """Bookkeeping line energy P/v; not a universal AM quality predictor."""
    if power_w < 0:
        raise ValueError("power must be non-negative")
    if speed_mm_s <= 0:
        raise ValueError("speed must be positive")
    return power_w / speed_mm_s


def bead_volume_mm3(length_mm: float, width_mm: float, height_mm: float, shape_factor: float = 1.0) -> float:
    """Approximate finite bead volume used to prove a nominal 2D path is volumetric."""
    for n, v in {"length": length_mm, "width": width_mm, "height": height_mm, "shape_factor": shape_factor}.items():
        if v <= 0:
            raise ValueError(f"{n} must be positive")
    return length_mm * width_mm * height_mm * shape_factor


def cavity_function(mode: str) -> Dict[str, str]:
    m = mode.strip().upper()
    table = {
        "GAS": {
            "damping": "POTENTIAL_GAS_DAMPING_REQUIRES_MODEL_TEST",
            "thermal": "GAS_CONDUCTION_PRESENT",
        },
        "LOW_PRESSURE": {
            "damping": "REDUCED_GAS_DAMPING_RELATIVE_TO_DENSE_GAS",
            "thermal": "REDUCED_CONVECTION_CONDUCTION_CONTEXT_DEPENDENT",
        },
        "VACUUM": {
            "damping": "NO_GENERAL_GAS_DAMPING",
            "thermal": "CONVECTION_SUPPRESSED_RADIATION_AND_SOLID_CONDUCTION_REMAIN",
        },
    }
    if m not in table:
        raise ValueError(f"unsupported cavity mode: {mode}")
    return table[m]


def insert_thermal_budget_ok(
    insert_max_temp_c: float,
    predicted_process_peak_c: float,
    safety_margin_c: float = 0.0,
) -> bool:
    """True only when subsequent processing remains below allowed insert temperature."""
    if safety_margin_c < 0:
        raise ValueError("safety margin must be non-negative")
    return predicted_process_peak_c + safety_margin_c <= insert_max_temp_c


def compatibility_allows_same_process(code: str) -> bool:
    """Only A allows an already-qualified same-process route; B still requires transition proof."""
    c = code.strip().upper()
    if c not in {"A", "B", "C", "D", "X"}:
        raise ValueError("compatibility code must be A/B/C/D/X")
    return c == "A"


@dataclass(frozen=True)
class FunctionalRegion:
    region_id: str
    function_class: str
    composition: Dict[str, float]
    embedment_class: str
    evidence_state: str

    def normalized(self) -> "FunctionalRegion":
        return FunctionalRegion(
            self.region_id,
            self.function_class,
            normalize(self.composition),
            self.embedment_class,
            self.evidence_state,
        )


def slice_composition(regions: Iterable[FunctionalRegion], volumes_mm3: Mapping[str, float]) -> Dict[str, float]:
    """Volume-weighted composition approximation for digital bookkeeping only.

    This assumes equal constituent density basis and is deliberately not a
    metallurgical mixing model. Use mass-based assay for real recipe control.
    """
    total_v = 0.0
    weighted: Dict[str, float] = {}
    for region in regions:
        if region.region_id not in volumes_mm3:
            raise ValueError(f"missing volume for {region.region_id}")
        v = float(volumes_mm3[region.region_id])
        if v <= 0:
            raise ValueError("region volume must be positive")
        comp = normalize(region.composition)
        total_v += v
        for k, x in comp.items():
            weighted[k] = weighted.get(k, 0.0) + v * x
    if total_v <= 0:
        raise ValueError("slice volume must be positive")
    return {k: val / total_v for k, val in sorted(weighted.items())}


def diluted_composition(
    feed_composition: Mapping[str, float],
    substrate_composition: Mapping[str, float],
    substrate_fraction: float,
) -> Dict[str, float]:
    """Local mass composition after mixing feed with a melted substrate fraction.

    substrate_fraction is lambda = m_substrate_melted / (m_feed + m_substrate_melted).
    This is composition bookkeeping only; lambda must come from a process model or
    measurement and is not a universal DED/weld constant.
    """
    lam = float(substrate_fraction)
    if not 0.0 <= lam < 1.0:
        raise ValueError("substrate_fraction must be in [0, 1)")
    feed = normalize(feed_composition)
    sub = normalize(substrate_composition)
    keys = set(feed) | set(sub)
    return {
        k: (1.0 - lam) * feed.get(k, 0.0) + lam * sub.get(k, 0.0)
        for k in sorted(keys)
    }


def required_feed_composition_for_target(
    target_composition: Mapping[str, float],
    substrate_composition: Mapping[str, float],
    substrate_fraction: float,
    *,
    tol: float = 1e-12,
) -> Dict[str, float]:
    """Back-solve feed composition required to reach a target after dilution.

    Raises ValueError if the target is infeasible at the specified substrate
    dilution because one or more required feed fractions would be negative.
    """
    lam = float(substrate_fraction)
    if not 0.0 <= lam < 1.0:
        raise ValueError("substrate_fraction must be in [0, 1)")
    target = normalize(target_composition)
    sub = normalize(substrate_composition)
    keys = set(target) | set(sub)
    raw: Dict[str, float] = {}
    for k in sorted(keys):
        value = (target.get(k, 0.0) - lam * sub.get(k, 0.0)) / (1.0 - lam)
        if value < -tol:
            raise ValueError(
                f"target composition is infeasible at substrate_fraction={lam}: "
                f"required feed fraction for {k} is negative"
            )
        raw[k] = 0.0 if abs(value) <= tol else value
    return normalize(raw)
