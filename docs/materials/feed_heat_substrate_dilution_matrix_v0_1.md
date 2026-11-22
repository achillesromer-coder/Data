# Feed × Heat × Particle × Substrate-Dilution Matrix v0.1

**Date:** 2026-10-06  
**Parent:** PMX-MAT-001 / FVX-MATRIX-001 / BUILD-056  
**State:** engineering design-space / qualification scaffold  
**Evidence ceiling:** candidate feed-process pairs and control equations only. No production material, weld, pressure boundary, embedded-electronics or flight qualification is implied.

## 1. Why the post-mix model needs a substrate term

For a cold liquid post-mix, the output composition is dominated by the metered input streams. In fusion additive manufacturing, the new bead can also remelt part of the existing substrate or prior layer. Define the local substrate dilution fraction:

\[
\lambda=\frac{m_{substrate,melted}}{m_{feed}+m_{substrate,melted}}
\]

Then the local fused composition is:

\[
\mathbf{x}_{local}=(1-\lambda)\mathbf{x}_{feed}+\lambda\mathbf{x}_{substrate}
\]

If the desired local composition is \(\mathbf{x}^{*}\), the feed composition required at an estimated dilution \(\lambda\) is:

\[
\mathbf{x}_{feed}^{*}
=
\frac{\mathbf{x}^{*}-\lambda\mathbf{x}_{substrate}}
{1-\lambda}
\]

A solution is feasible only when every resulting constituent fraction is non-negative and the requested feed can be formed from the qualified stock library.

**Consequence:** the printer cannot command a material recipe from nozzle fractions alone. It must carry substrate identity, estimated/observed dilution and uncertainty for each fusion region.

## 2. Control loop

For each functional bead or voxel:

1. bind target local composition and function;
2. bind current substrate/prior-layer composition and evidence state;
3. estimate a dilution interval, not a single universal constant;
4. back-solve the required feed composition;
5. reject an infeasible target rather than clipping silently;
6. solve qualified stock-feed rates for that composition;
7. execute inside the qualified heat/atmosphere/geometry window;
8. measure bead geometry and thermal/process state;
9. obtain chemistry/microstructure evidence at the coupon cadence required by the process;
10. update the dilution/process model and retain uncertainty.

This becomes:

\[
\text{target local state}
\rightarrow
\text{dilution compensation}
\rightarrow
\text{post-mix feed command}
\rightarrow
\text{thermal process}
\rightarrow
\text{measured state}
\rightarrow
\text{model update}
\]

## 3. Feed physical-state classes

### P-WIRE
Track:
- alloy/batch identity and certificate;
- wire diameter/tolerance;
- surface condition/cleanliness;
- feed-speed calibration;
- storage/moisture/contamination;
- actual mass deposition rate.

### P-POWDER
Per ISO/ASTM 52907 and related ASTM powder guidance, retain at minimum:
- documentation/traceability;
- representative sampling;
- particle-size distribution including d10/d50/d90 where applicable;
- chemistry;
- characteristic densities;
- morphology/sphericity;
- flowability;
- contamination;
- storage/reuse history.

Do **not** assign one universal powder-size range. The qualified PSD is machine/nozzle/process/material-specific.

### P-INK / P-SLURRY
Track:
- solids composition/loading;
- carrier/binder identity;
- viscosity/rheology versus temperature/shear;
- particle/agglomerate distribution;
- nozzle/line-width compatibility;
- cure/sinter process;
- shrinkage, adhesion and residual solvent/outgassing.

### P-FILAMENT / P-PELLET
Track:
- polymer/composite lot;
- fibre/filler state;
- moisture;
- diameter/pellet distribution;
- melt history;
- crystallinity/anneal state as applicable;
- emissions/outgassing qualification for enclosed or space use.

### P-INSERT
Track:
- component identity/revision;
- dimensions/coating/surface preparation;
- maximum subsequent process temperature;
- allowable atmosphere/pressure;
- test/service access;
- bonding/encapsulation method.

## 4. Heat/process classes

These are scheduling classes, not universal temperatures.

- **HT-0 — cold/no-fusion:** feeder calibration, placement, metrology, mechanical insertion.
- **HT-L — low-temperature functional:** inks, adhesives, coatings, selected direct-write and curing/sintering processes within an exact material thermal budget.
- **HT-P — polymer/composite:** extrusion/consolidation and any anneal; exact material/process window required.
- **HT-C — ceramic/glass:** slurry/direct-write/other route plus material-specific cure/sinter or secondary processing.
- **HT-M — metal fusion:** DED/WAAM/PBF or equivalent melt process; melt pool, substrate dilution and HAZ dominate.
- **HT-POST — local/global post-process:** stress relief, heat treatment, sinter, HIP or other separately controlled operation.

The build compiler should order operations by **future thermal budget**. A common logical sequence is high-heat structural work first, then machining/cleaning, then lower-temperature functional layers, then vulnerable inserts, then closure/sealing/coatings. Exact order is process-specific and can be changed only with a verified thermal-survival route.

## 5. Candidate feed library — staged, not production-selected

### LIB-00 — benign control feeds
Purpose: prove post-mix spatial metering without thermal or metallurgical ambiguity.

Use non-reactive, safely handled, visually or instrumentally distinguishable beads/granules/pastes selected for the actual feeder. Their chemistry is irrelevant to the first control proof; mass/volume conservation, cross-contamination, switching lag and spatial placement are the metrics.

### LIB-10 — 316L reference structural family
UNS S31603 / 316L is a useful **reference AM material family**, not a Mark III material selection. ASTM has a current PBF specification for S31603 and active DED guidance exists for metals generally.

Reference wrought chemistry from ATI includes Cr 16–18 wt%, Ni 10–14%, Mo 2–3%, C <=0.03%, with Fe balance and other controlled elements. Actual AM batch chemistry and powder/wire state must come from the exact certificate and assay.

Use:
- single-material thermal/bead calibration;
- substrate dilution experiments;
- dimensional/NDE/control development.

Do not use the reference chemistry as a substitute for the actual feed certificate.

### LIB-11 — Alloy 625 reference high-Ni family
UNS N06625 / Alloy 625 is a Ni-Cr-Mo-Nb family used here as a **research comparator**, not a Mark III selection. Exact batch chemistry comes from its material certificate.

Use:
- independent single-material process calibration;
- dissimilar-alloy transition research after both single-material windows are known.

### LIB-12 — 316L ↔ 625 challenge pair
This pair is deliberately useful because it disproves the assumption that a smoother gradient is always better. A 2026 WAAM review reports detrimental intermediate phases such as delta/Laves/MC phases in some graded compositions and notes cases where direct compositional interfaces performed better than smooth gradients.

Therefore:
- classify the pair as **B-RESEARCH**, not production-compatible;
- test direct-interface and bounded-gradient variants separately;
- measure actual chemistry, dilution, microstructure, cracking, residual stress and corrosion/mechanical response;
- do not select the gradient merely because the recipe solver can generate it.

### LIB-20 — conductive functional family
Candidates include qualified Cu/Ag-based inks or compatible metal/plating routes for buses, antennas, heaters and sensor traces.

Default architectural rule:
- treat this as a separate low-temperature/specialist process from the structural fusion path until a specific cross-process interface is qualified;
- do not assume bulk-copper structural co-melting with the shell alloy.

### LIB-21 — dielectric / ceramic functional family
Candidates include alumina/silica/glass/other qualified ceramic or ceramic-filled formulations.

Uses:
- electrical isolation;
- sensor substrates;
- local thermal isolation or conductive ceramic functions where demonstrated.

Default route is C/D: separate deposition, barrier, substrate or insert unless same-process compatibility is established.

### LIB-22 — resistive / sensor family
Candidates include qualified NiCr-class, carbon-loaded, RTD, piezoresistive, capacitive and optical/fibre functions.

Use after structural thermal work where possible.

### LIB-30 — high-temperature polymer/composite family
PEEK, PEKK/PAEK and PEI-class systems are candidate service/insulation/compliant/substrate materials, not default internal spaceflight materials. NASA work confirms their relevance to space AM but also identifies interlayer-adhesion and high-temperature-printing limitations. Vacuum/environment use additionally requires exact-process outgassing and thermal-cycle evidence.

NASA's outgassing database uses ASTM E595-style TML/CVCM testing for candidate spacecraft materials. The exact printed formulation, additives and process history matter.

### LIB-31 — smart material family
SMP/SMA/other stimuli-responsive material remains isolated from the structural process until trigger range, cycling, creep/fatigue, thermal compatibility and fail-safe behaviour are established.

### LIB-40 — seals / barriers / getter inserts
Hermetic barriers, closure materials and getters are treated as controlled process/insert families. They are not blended casually into structural feed.

## 6. Substrate/transition classes

- **S0 SAME:** same qualified feed and substrate family. Dilution still measured for process control.
- **S1 RELATED:** metallurgically related pair with existing evidence; compatibility still exact-process dependent.
- **S2 RESEARCH-FGM:** dissimilar fusion pair requiring mapped composition/process/phase response.
- **S3 BARRIER:** functions separated by a diffusion/electrical/thermal barrier or intermediate qualified layer.
- **S4 INSERT:** no intentional fusion mix; functional insert/pocket/interface.
- **SX HOLD:** target combination presently incompatible, infeasible or unsupported.

## 7. A/B/C/D/X route and dilution are separate dimensions

A material pair may be:
- A for one deposition process and C for another;
- A at one heat input and X at another;
- B as a narrow transition sequence but infeasible under high substrate dilution;
- C/D when an electronic or polymer function cannot survive the subsequent structural thermal budget.

Therefore the compatibility key is:

\[
K = K(feed_A,feed_B,substrate,process,thermal\ history,environment,geometry)
\]

not simply \(K(material_A,material_B)\).

## 8. 2D slice scheduling

Each functional slice contains regions with different process classes. The compiler must solve a partial order:

1. deposit/fuse the highest-temperature structural regions;
2. allow required cooling/stress-control state;
3. machine/clean/expose pockets and service channels;
4. deposit medium/low-temperature dielectric and conductor functions;
5. place vulnerable components/inserts;
6. electrically/thermally test before burial;
7. close local barriers/cavities;
8. perform leak/electrical/NDE verification;
9. add final environmental/EMI/protective layers.

A later operation is prohibited when its predicted local temperature or contamination state exceeds the embedded region's remaining budget.

## 9. Multi-robot implication

The 3–5-agent cell should allocate tasks by:
- process thermal class;
- contamination class;
- feed family;
- orientation/access;
- local thermal keep-out;
- active cavity state;
- component thermal budget;
- collision envelope;
- current evidence gate.

This means R1/R2 can continue high-heat structural/graded work in one zone while R3 performs low-temperature function deposition only in a thermally isolated and schedule-safe zone, and R5 verifies the result before R4 closes it.

No concurrent operation is allowed merely because robots are physically separated; the part-level thermal/field/vibration state must also be compatible.

## 10. First evidence sequence

1. cold feed switching and lag/cross-contamination;
2. single-material structural bead and substrate-dilution estimation;
3. same-material layer-on-layer remelt repeatability;
4. compatible or deliberately challenging dissimilar pair coupon;
5. dielectric/conductor stack on a thermally characterised substrate;
6. embedded insert with future-thermal-budget proof;
7. gas/low-pressure/vacuum closure and leak/outgassing test;
8. multi-agent sequencing with common state model.

This is the shortest path from post-mix analogy to a credible multifunctional Mark III manufacturing architecture.
