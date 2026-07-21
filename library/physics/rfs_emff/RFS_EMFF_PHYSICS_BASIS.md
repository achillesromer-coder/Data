# RFS / EMFF physics basis and evidence gate

Status: controlled internal; systematic lanes 1–7 initiated 2026-07-21.

## Canonical routing

- This file is the overarching physics and applicability surface for Cognigrex/Data.
- Specialised parameters, run records, measurements and accepted results belong in the RFS & EMFF Twin and, for coil/field detail, the Free Flow Solenoid Stack Twin.
- Neo routes accepted result packets to CORE and the owning Twins.
- Raphael Equations remain independent personal IP and may be referenced as a source lens; they are not silently merged into this library.
- N^3 / GeoMatrices remains a separate package boundary.
- MPL means Maximum Probable Loss and is routed separately to `https://romer.industries/MPL` and its functional code source.

## Retained empirical analogue observation

The owner reports that magnetic and cymatic board tests moved metal particles through the remainder of the medium along a desired, traceable push/pull path. No numeric parameters, raw logs, apparatus identifier, timestamp, sample composition, field map, drive frequency, amplitude or uncertainty were recorded.

Evidence state: `OBSERVED_QUALITATIVE`.

This observation must not be translated into extraction rate, enrichment, purity, force, optimal frequency, throughput, efficiency or equipment-safety claims.

## Accepted first-order relations

The following relations are allowed for screening when units and applicability are explicit:

1. Angular frequency: `omega = 2*pi*f`.
2. Sinusoidal acceleration amplitude: `a_peak = (2*pi*f)^2 * A`.
3. Spherical-equivalent particle volume and mass: `V = 4*pi*r^3/3`, `m = rho*V`.
4. Inertial-force screening: `F = m*a`.
5. Long-solenoid field screening: `B ~= mu0*mu_r*(N/l)*I`.
6. Linear-susceptibility force screening: `F ~= (chi*V/(2*mu0))*grad(B^2)`.
7. Stokes drag, only for Newtonian low-Re flow: `F_drag = 6*pi*eta*r*v`.
8. Skin depth for a homogeneous conductor under harmonic excitation: `delta = sqrt(2/(omega*mu*sigma))`.

Each calculation must carry its assumptions, units, uncertainty, falsification condition and evidence status. Skin depth or conductivity alone does not establish a material-specific separation resonance.

## Applicability and falsification controls

- Board geometry, support points and modal boundary conditions must be recorded.
- Field-driven translation requires a gradient; a uniform field may orient a neutral magnetic object without producing the claimed translation.
- Ferromagnetic materials require measured magnetisation behaviour when linear susceptibility is not valid.
- Stokes drag is rejected for dry granular or high-Re conditions unless an appropriate model is substituted.
- Airflow, electrostatics, vibration coupling, friction, cohesion, convection and operator disturbance are alternative causes to control.
- Predicted direction, reversal, threshold and velocity must be compared against tracked motion and controls.

## Promotion doctrine

A model result is eligible for controlled canon when either:

- empirical verification passes; or
- mathematical proof and an independent reasoning review both pass.

Physical capability language remains controlled until empirical evidence is instrumented, raw logs are attached, controls pass and at least two repeat runs are recorded. Rejected, conflicting and superseded values remain in the reconciliation register.

## Legacy model quarantine

The existing LightSpeed legacy RFS theory contains unsourced material resonance frequencies, an unsupported statement that an extraction-energy relation is empirical, assumed extraction efficiency/rate, an unsourced equipment-safety threshold and downstream ROI/value outputs. These remain historical source material, not validated canon. The safe validator must not emit those claims.
