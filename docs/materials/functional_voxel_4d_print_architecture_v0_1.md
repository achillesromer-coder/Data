# Functional-Voxel / 2D→3D→4D Adaptive Manufacturing Architecture v0.1

**Date:** 2026-10-06  
**State:** engineering analysis / digital scaffold  
**Parent:** PMX-MAT-001 / PMX-GRAPH-001 / BUILD-055  
**Reference vehicle:** Mark III  
**Evidence ceiling:** This document specifies an architecture and validation programme. It does not establish qualified alloys, hermetic/vacuum integrity, embedded-electronics survivability, pressure-vessel safety, flight readiness or autonomous build capability.

## 1. Core interpretation

The requested manufacturing system is best represented as a hierarchy:

1. **Concentrate / feedstock state** — each feed has measured composition, morphology, particle-size distribution, contamination, thermal/process limits and provenance.
2. **Functional voxel / bead state** — each deposited bead or region is a three-dimensional material volume with local composition and process history.
3. **Functional slice** — a nominal 2D layer contains many volumetric bead cross-sections, embedded traces, void boundaries and local treatment zones. It is therefore planned in 2D but is materially 3D inside the layer thickness.
4. **3D body** — slices and non-planar deposits are accumulated into a spatially functional structure.
5. **4D-M state** — intrinsic stimuli-responsive regions change material/shape state with time.
6. **4D-CPS state** — sensors, control logic and actuators change the object's state with time. This is a cyber-physical adaptive structure; it should not be conflated with strict materials-science 4D printing.
7. **Lifecycle state** — the body can be inspected, repaired, reconfigured, recovered and recycled.

A voxel/region is not defined only by composition. Use:

[
V(x,y,z,t)={\mathbf c,\ PSD,\phi,\rho,T,H,\sigma,\epsilon,k,\mu,F,E,\text{interfaces},\text{embedded IDs},\text{evidence}}
]

where:
- \(\mathbf c\) = composition vector,
- PSD = particle-size/morphology state,
- \(\phi\) = phase or microstructure descriptor,
- \(H\) = process/thermal history,
- \(F\) = function class,
- \(E\) = embedment/serviceability class.

The process command is:

[
u={\dot m_1...\dot m_n,P,v,T_{pre},T_{interpass},g,p,\mathbf q,\text{cooling},\text{field},\text{dwell}}
]

and local material state becomes:

[
V_{k+1}=mathcal F(V_k,u_k,\text{environment},\text{substrate},\text{history})
]

The post-mix equation remains the pre-process composition controller. It does not replace \(\mathcal F\).

## 2. Concentrate / functional feed families

These are candidate **feed families**, not authorised recipes.

| Feed family | Primary function | Candidate material classes | Preferred integration route | Main gate |
|---|---|---|---|---|
| F-STRUCT | load path / shell / hard point | qualified Al, Ti, Fe/Ni, Ni-base or other alloy families | DED/WAAM/PBF/extrusion depending scale | alloy/process qualification |
| F-COND | power/data conductor | Cu/Ag inks, Cu-rich metal feed, plated seed | low-temp direct write, aerosol/ink, plating, selected metal AM | ampacity, adhesion, thermal cycling |
| F-RETURN | electrical return/reference | conductive metal/ink plane | separate conductor layer or embedded bus | isolation and fault-current path |
| F-DIEL | electrical isolation | ceramic, glass/silica, ceramic-filled polymer, high-temp polymer | DIW/coating/lamination/insert | breakdown voltage and thermal compatibility |
| F-EMI | shield / field shaping | conductive shell, mesh, magnetic/absorptive material | printed layer, insert, coating | shielding effectiveness and field interaction |
| F-THERM-C | heat spreader | Cu, Al, graphite/carbon, AlN-class ceramic where compatible | insert, coating, DIW, structural deposition | CTE/interface and conductivity |
| F-THERM-I | thermal break | ceramic/polymer/aerogel-class insert | insert/separate low-temp deposition | compression, outgassing, environment |
| F-RESIST | heater / resistive sensing | NiCr-class, carbon-loaded inks/polymers | direct-write or thin functional layer | resistance stability and hot-spot control |
| F-MAG | magnetic / field path | Fe/Ni/Co-class; bonded hard-magnet feed where appropriate | specialised AM or insert | coercivity/permeability after process |
| F-SENSE | sensing | piezoresistive, RTD, strain, capacitive, optical channels | direct-write / insert | calibration and drift |
| F-SMART | intrinsic 4D response | SMP, SMA or other stimuli-responsive material | isolated insert or compatible low-temp print route | cycle life and trigger envelope |
| F-COMPLY | strain isolation / damping | elastomeric/viscoelastic or compliant lattice region | polymer print, insert, lattice design | vacuum/outgassing/temperature |
| F-SEAL | hermetic / environmental barrier | qualified seal coat, braze/weld closure, barrier layer | secondary closure/coating | leak rate / permeability |
| F-GETTER | vacuum maintenance | getter material | discrete insert / qualified deposition | activation and contamination |
| F-SUBSTRATE | local functional carrier | ceramic/polymer/metal substrate | print/insert | subsequent thermal budget |

### Compatibility rule

Every adjacent pair gets a route code:

- **A** — same-process candidate after thermodynamic/process proof.
- **B** — graded transition candidate.
- **C** — requires discrete barrier or separate deposition process.
- **D** — insert/pick-place only.
- **X** — currently incompatible or unqualified.

No composition pair is promoted simply because both feeds can enter the same machine.

## 3. Heat × composition × particle state

For powder/ink/wire feeds, the design space must retain at least:

- \(d_{10},d_{50},d_{90}\), morphology, flowability and surface oxide;
- feedstock carrier/viscosity for inks or slurries;
- actual feed rate and its uncertainty;
- power/heat source state;
- traverse speed;
- line energy \(P/v\) as a bookkeeping variable, not a universal quality predictor;
- preheat and interpass temperature;
- local atmosphere, oxygen/moisture and pressure;
- cooling rate / dwell;
- local substrate composition and dilution depth;
- bead width/height and overlap;
- melt-pool or cure-zone temperature/area where measurable;
- phase/chemistry/microstructure result after deposition.

The experiment is therefore a response surface:

[
Y = f(\mathbf c,PSD,P/v,T_{pre},T_{interpass},g,p,\text{geometry},\text{history})
]

where \(Y\) includes chemistry, porosity, adhesion, conductivity, permeability, magnetic properties, dimensional error and mechanical properties as relevant.

## 4. Functional slice: “internal 3D inside one 2D layer”

A nominal layer \(L_k\) is a collection of deposited volumes, not a mathematically flat sheet:

[
L_k = igcup_j B_{kj}
]

Each bead/region \(B_{kj}\) has finite width, height, local composition, thermal gradient, interfaces and optional embedded objects.

A single functional slice may therefore contain:

- structural outer bead;
- internal lattice or rib;
- dielectric channel liner;
- conductive power/data trace;
- return/reference plane;
- EMI shield patch;
- thermal spreader;
- sensor trace;
- void/cavity wall;
- component pocket;
- closure land;
- local smart-material region;
- transition composition between two structural regions.

This is the correct abstraction for a “2D print” whose internal material state is already three-dimensional.

## 5. Layer accumulation and 4D behaviour

### 5.1 3D body

Stack or non-planarly deposit functional slices while carrying state forward:

[
S_{k+1}=mathcal G(S_k,L_k,\text{thermal history},\text{residual stress},\text{inspection})
]

### 5.2 4D-M — intrinsic material response

The material itself changes state in response to heat, electric/magnetic field, light, moisture/chemistry or other validated stimulus. Current literature supports shape-memory polymers/composites and other smart-material routes, but interface durability, cycle stability and standardisation remain major gates.

### 5.3 4D-CPS — cyber-physical response

The printed body contains sensors, buses, software-controlled actuators and local control. Examples:

- local heater changes curvature/compliance;
- solenoid or field coil changes field state;
- valves alter gas-cell pressure;
- thermal routing changes with active control;
- smart-material insert is triggered on command;
- structural health sensing changes operating limits.

The real-time safety controller must be deterministic and local. Cognigrex/LightSpeed may plan, diagnose and optimise within bounded envelopes, but an LLM does not directly own safety-critical motion, laser/arc, pressure, high-current or thermal interlocks.

## 6. Embedded hardware and serviceability

NASA's printed-electronics work demonstrates conductive, insulating and ceramic direct-write materials, multiple print heads, printed sensors/RF devices and hybrid toolchains including pick-and-place and machining. The correct design is therefore **hybrid embedment**, not “print every semiconductor inside molten structural metal.”

Use embedment classes:

- **E0 — service bay:** conventional replaceable module.
- **E1 — conformal printed function:** trace, heater, antenna, strain/temperature sensor.
- **E2 — encapsulated passive:** passive component or robust sensor embedded behind a qualified barrier.
- **E3 — sealed functional insert:** component inserted during a build pause with defined access/test ports.
- **E4 — monolithic functional material:** function arises from the printed material/geometry itself.

High-failure-rate or high-value active electronics, connectors, valves, energy-storage cells and processors should default to E0/E3 until evidence supports deeper embedment.

## 7. “Neutral” functional layers

For Mark III use explicit classes rather than a generic neutral layer:

1. **power return/reference plane**;
2. **dielectric isolation layer**;
3. **EMI shield/ground plane**;
4. **magnetic flux-return/yoke region** where appropriate;
5. **thermal spreader**;
6. **thermal break**;
7. **chemical/diffusion barrier**;
8. **galvanic-isolation barrier**;
9. **strain/compliance layer**;
10. **hermetic/environmental barrier**.

Each has a different material and qualification requirement.

## 8. Internal cavities: gas, partial pressure and vacuum

### Gas/partial-pressure cells

Potential functions:
- pneumatic spring;
- squeeze/gas damping;
- acoustic attenuation;
- pressure-tunable joint response;
- thermal transport when gas is intentional.

Required controls:
- pressure boundary design;
- fill/evacuation port;
- leak test;
- gas compatibility;
- thermal expansion;
- pressure sensing where required;
- safe fail state.

### Vacuum / very-low-pressure cells

Potential functions:
- reduce convection;
- reduce gas drag and gas damping;
- thermal isolation;
- protect/process selected internal elements;
- provide low-pressure reference volume.

**Vacuum is not a general damping medium.** If damping is desired, a controlled gas/partial pressure, viscoelastic structure, frictional mechanism or other energy-dissipation mechanism is required.

Long-life sealed vacuum additionally requires permeability/outgassing control, leak-rate qualification and often a getter strategy.

### AM-specific cavity problems

- trapped powder or support material;
- inaccessible defects;
- inability to inspect internal welds;
- porosity/leakage;
- outgassing;
- inaccessible rework;
- differential thermal expansion.

Therefore cavities should include temporary evacuation/removal channels, inspection routes or staged closure whenever possible. Final sealing is a separate qualified operation.

## 9. Mark III solid-state compartmentalisation

The objective is not a completely non-serviceable monolith. It is an **integrated functional body** where the structure itself carries passive and distributed functions, leaving only life-limited/high-complexity devices as replaceable islands.

### Proposed zoning

**M3-Z01 structural backbone**
- primary shell/spine, hard points and three-appendage load transfer.

**M3-Z02 embedded power/data trunk**
- insulated power buses, return/reference conductors and data/fibre paths.

**M3-Z03 field-control regions**
- structural/thermal/magnetic support around RFS/EMFF/solenoid hardware.
- high-current windings remain serviceable until embedded-winding life and repairability are proven.

**M3-Z04 sensor skin**
- strain, thermal, field and damage-monitoring functions.

**M3-Z05 gas-damped joint cells**
- bounded pressure-tunable cells around appendage/joint regions, consistent with existing gas-compressed-joint lineage.

**M3-Z06 vacuum/low-pressure isolation cells**
- thermal/acoustic/process isolation; explicitly not relied on for gas damping.

**M3-Z07 energy-absorption lattice**
- crush/compliant lattice and replaceable impact zones.

**M3-Z08 thermal highways**
- heat-spreading paths connected to radiative/active thermal-control surfaces.

**M3-Z09 EMI / field-return layers**
- shielding, reference and field-containment functions kept distinct from power return.

**M3-Z10 service islands**
- CPU/control electronics, valves, high-value sensors, connectors and replaceable power devices.

**M3-Z11 interlock hard points**
- preserve the current three-appendage and Mark III↔Mark III cooperative-interlock authority; exact production geometry remains open.

**M3-Z12 manufacturing/service channels**
- powder removal, evacuation/fill, wiring/fibre pull, inspection and repair access.

## 10. Energy cycling / absorption map

Keep energy domains explicit.

| Input / disturbance | Printed/integrated response | Possible recovery | Boundary |
|---|---|---|---|
| structural impact | crush lattice, compliant zone, gas-damped cell | usually dissipative | do not assume recoverable energy |
| vibration | viscoelastic/compliant path, gas damping | specialised transduction only if separately designed | vacuum reduces gas damping |
| thermal load | spreader, thermal break, radiator path, phase-change insert | TE only with validated ΔT/system | heat routing ≠ energy generation |
| RF/EMI | shield/absorber/field-return path | normally dissipative/reflective | must not interfere with EMFF |
| solar flux | Solar Hull/PV surface | electrical generation if qualified | structural material alone not photovoltaic |
| electrical transient | local capacitance/Free Flow candidate subsystem | bounded electrical storage | independent electrochemistry/safety gate |

## 11. Adaptive 3–5-agent manufacturing cell

The user's “3–5 post-mix printers around a central node” is technically well aligned with cooperative robotic additive manufacturing.

**Recommended motion architecture:** six-axis industrial robot per deposition/manipulation agent, plus a 1–2 axis central positioner. Four degrees of freedom is a useful minimum for constrained paths, but is not sufficient for arbitrary nozzle orientation around a complex closed body.

### Central node / seed datum

Functions:
- common metrology frame;
- part support and thermal datum;
- rotary/tilt positioner;
- temporary utilities;
- build-state identity;
- optional future integration as a serviceable vehicle spine, but not assumed.

### Five-role maximum cell

**R1 — structural deposition**
- WAAM/DED/large-scale extrusion; high heat.

**R2 — graded/multi-feed functional deposition**
- multi-hopper/wire or multiplexed extrusion.

**R3 — electronics/dielectric/ceramic direct write**
- conductive, insulating and sensing paths at lower thermal budget.

**R4 — insertion / subtractive / closure**
- pick-and-place, drilling/milling, ports, connectors, seal-prep.

**R5 — inspection / repair / coating**
- machine vision, profilometry, thermography, NDE, local repair or protective layer.

A 3-agent cell can combine R2/R3 and R4/R5 roles.

ORNL's MedUSA demonstrates three robotic arms with welders in collaborative WAAM; ORNL also publishes multi-agent motion-control and common-frame calibration methods. This validates the architecture class, not this specific machine.

## 12. Environment control

Use nested environments rather than one universal chamber.

**Macro enclosure**
- personnel safety;
- fume/extraction;
- controlled humidity/O2 where needed;
- thermal stability.

**Local process shroud**
- inert shielding gas;
- local O2 control;
- local cooling/heating.

**Thermal field**
- preheat;
- induction/resistance/laser local treatment;
- interpass dwell and active cooling.

**Special process cell**
- vacuum or low-pressure process only where required.
- a full macro-scale vacuum enclosure is not a default for terrestrial multi-robot builds.

**Experimental field bias**
- magnetic/electric field during deposition only under separately instrumented R&D protocols.

## 13. Sensor / feedback stack

Fast inner loops:
- robot pose and force/torque;
- feeder rate;
- arc/laser current/power;
- melt-pool/cure-zone size and temperature;
- bead height/width;
- layer surface profile.

Medium loops:
- thermal field;
- electrical continuity/resistance;
- atmosphere/O2/moisture;
- cavity pressure/leak checks;
- spectroscopy/optical emission where calibrated.

Slow/qualification loops:
- dimensional scan;
- CT/ultrasonic/other NDE;
- chemistry;
- microscopy;
- mechanical/electrical/magnetic testing.

NIST has demonstrated feedback control using melt-pool measurement and layer-thickness/powder-spread state; this is the established control precedent for adaptive setpoint correction.

## 14. Control hierarchy

[
	ext{CGX build intent}
ightarrow
	ext{functional voxel compiler}
ightarrow
	ext{recipe solver}
ightarrow
	ext{thermal/process scheduler}
ightarrow
	ext{multi-robot task allocator}
ightarrow
	ext{collision/motion planner}
ightarrow
	ext{deterministic local controllers}
ightarrow
	ext{sensors}
ightarrow
	ext{state estimator}
ightarrow
	ext{bounded correction / pause / repair}
]

Each correction must preserve:
- hard safety envelope;
- material process window;
- robot collision envelope;
- embedded-component thermal budget;
- cavity/pressure boundary state;
- evidence/provenance record.

## 15. Initial experimental ladder

**FV-L0 — digital state model**
- composition + PSD + thermal/process/environment state;
- functional voxel and slice schema.

**FV-L1 — cold multi-feed placement**
- inert coloured/granular/viscous feeds;
- verify spatial concentration and feeder response.

**FV-L2 — thermal single-material bead control**
- map line energy, preheat/interpass state, bead geometry and feedback.

**FV-L3 — compatible multi-feed gradient coupon**
- chemistry/microstructure and interface verification.

**FV-L4 — dielectric + conductor + sensor coupon**
- continuity, insulation, adhesion, thermal cycle.

**FV-L5 — pause/insert/encapsulate coupon**
- embedded sensor/passive plus service/test port.

**FV-L6 — gas/low-pressure cell coupon**
- leak rate, pressure cycling, damping/thermal function separately measured.

**FV-L7 — adaptive/4D coupon**
- intrinsic smart material or sensor-controller-actuator state change.

**FV-L8 — multi-agent coordinated object**
- 3 robots minimum, one coordinate frame, dynamic task assignment, collision-safe repair.

**FV-L9 — Mark III representative subassembly**
- one appendage/joint/body-sector representative article; no mission claim.

## 16. Immediate programme objects

- INV-021 Functional Voxel / 2D→3D→4D Print Architecture.
- INV-022 Hybrid Embedded Hardware and Printed Electronics Body.
- INV-023 Mark III Integrated Functional Body / Solid-State Compartmentalisation.
- INV-024 Multi-Agent Adaptive Post-Mix Manufacturing Cell.
- BUILD-056 Functional-Voxel + Mark III representative build programme.
- new Type-1 Römer surface: 21_Functional_Voxel_MarkIII_v0_1.
- frontier handoff to Type 1 Systems / Mark-series material-process-test owner.

## 17. External evidence anchors

- NASA Goddard 3D Printing of Electronics Laboratory: conductive, insulating, ceramic and custom inks; multiple heads; curved-surface circuits/sensors.
- NASA NTRS 20240004627 ODME: DIW, FFF, micro-mill, pick-and-place, EHD and electrodeposition tools for on-demand electronics.
- NASA TechPort 89568: five ink/material classes for conductor, resistor, capacitor, semiconductor and insulator with rotating injectors.
- NASA TechPort 154855: shape-conformable printed sodium-ion batteries with embedded thermal/electronic/load-management features.
- NIST 2025: real-time melt-pool and powder-layer feedback control.
- NIST AM monitoring programme: layer/melt-pool metrology linked to part quality.
- ORNL MedUSA: three collaborative robotic WAAM arms.
- ORNL Multi-Agent Motion Control and multi-robot calibration.
- 2025/2026 4D-printing reviews: stimuli-responsive materials are credible but interface durability, cycle life, scale and standards remain open industrialisation challenges.
