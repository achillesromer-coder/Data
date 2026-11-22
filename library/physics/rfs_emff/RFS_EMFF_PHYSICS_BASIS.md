# RFS / EMFF physics basis and evidence gate

Status: **historical controlled reference**, initiated 2026-07-21 and reconciled to current canon 2026-08-28.

## Canonical routing

This file retains conservative first-order physics/evidence controls as a Git reference. It is **not** the live task/status master.

- Current reviewed authority is the federated Achilles P.A / ACR3 / owning Type 1 Systems RFS/EMFF and related specialist surfaces.
- Specialised parameters, run records, measurements and accepted results belong in the owning RFS/EMFF evidence/Twin family and, for coil/field detail, the owning Free Flow Solenoid family.
- Neo/LightSpeed route accepted result packets to the owning canon under Achilles governance.
- Raphael Equations remain separately governed source/model lineage and are not silently merged into this library.
- N^3 / GeoMatrices remains a separate model/package boundary.
- Romer-MPL is the Maximum Probable Loss toolchain; GMAT/mission models, MPL risk/loss methodology and RFS/EMFF physics remain distinct model authorities even when LightSpeed/Cognigrex integrates their outputs.

## Retained qualitative analogue observation

Historical owner-reported observation: magnetic and cymatic board tests moved metal particles through the remainder of a medium along a desired, traceable push/pull path. The historical observation did not include sufficient numeric parameters, raw logs, apparatus identity, sample composition, calibrated field map, drive frequency/amplitude or uncertainty to support quantitative performance claims.

Evidence state: `OBSERVED_QUALITATIVE`.

Do not convert that observation into extraction rate, enrichment, purity, force, optimal frequency, throughput, energy efficiency or equipment-safety claims.

## First-order screening relations

The following relations are usable only with explicit units, assumptions and applicability bounds:

1. Angular frequency: `omega = 2*pi*f`.
2. Sinusoidal acceleration amplitude: `a_peak = (2*pi*f)^2 * A`.
3. Spherical-equivalent particle volume and mass: `V = 4*pi*r^3/3`, `m = rho*V`.
4. Inertial-force screening: `F = m*a`.
5. Long-solenoid field screening: `B ~= mu0*mu_r*(N/l)*I`.
6. Linear-susceptibility force screening: `F ~= (chi*V/(2*mu0))*grad(B^2)`.
7. Stokes drag only for Newtonian low-Re flow: `F_drag = 6*pi*eta*r*v`.
8. Skin depth for a homogeneous conductor under harmonic excitation: `delta = sqrt(2/(omega*mu*sigma))`.

Every calculation should carry configuration, assumptions, units, uncertainty/evidence state and a falsification condition. Skin depth, conductivity or a numerical sweep alone does not establish a material-specific separation resonance.

## Applicability and falsification controls

- Record board geometry, supports and modal boundary conditions.
- Field-driven translation requires a gradient; a uniform field can orient a magnetic object without establishing the claimed translation mechanism.
- Use measured magnetisation behaviour where linear susceptibility is not valid.
- Do not apply Stokes drag to dry granular/high-Re regimes without a justified replacement model.
- Control alternative causes such as airflow, electrostatics, vibration coupling, friction, cohesion, convection and operator disturbance.
- Compare predicted direction/reversal/threshold/velocity against tracked motion, controls and uncertainty-bearing measurements.
- Preserve calibrated instrument identity, reference frame, probe orientation and raw immutable receipts for field-map claims.

## Promotion doctrine

A successful equation check, simulation, CI run or software validator can support **model integrity**, but cannot by itself establish physical capability.

Physical capability or safety language requires the applicable source-bound acceptance criteria, calibrated instrumented empirical measurements, immutable raw receipts, controls/repeats, uncertainty treatment and independent engineering/safety/publication gates. Rejected, conflicting and superseded values remain visible in ACR3/owning evidence registers.

## Legacy model quarantine

Legacy RFS material may contain unsourced resonance values, assumed efficiencies/rates, unsupported safety thresholds or downstream ROI/value calculations. Retain such material as historical lineage where useful; do not promote it into validated canon without the required source, model and empirical proof chain.
