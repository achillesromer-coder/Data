# Post-Mix Composition Matrix — Materials / ISRU / Fleet Perpetuation v0.1

**Status:** engineering scaffold / evidence-governed implementation  
**Date:** 2026-10-06  
**Authority:** additive concept and deterministic mass-balance layer only. It does not promote RFS/EMFF performance, Solar Hull material compatibility, alloy qualification, celestial-resource rights, or flight readiness.

## 1. Canonical lens

The post-mix analogue is useful because it separates **stock concentrates** from a **bulk carrier** and meters each stream to create many outputs from a small feed library.

The engineering abstraction is:

- stock feed \(i\) has mass-flow \(\dot m_i\) and composition vector \(\mathbf c_i\);
- the carrier/diluent is simply another feed, usually with a simpler composition;
- total feed is \(\dot M=\sum_i \dot m_i\);
- linear pre-process composition is:

\[
\mathbf x_{feed}=\frac{\sum_i \dot m_i\mathbf c_i}{\sum_i\dot m_i}
\]

- a controlled machine should also enforce \(\dot M=\dot M_{target}\) where process stability depends on fixed total flow.

This is a **mass-balance model**, not a complete materials model.

## 2. Important correction to the beverage analogy

A typical post-mix system establishes water/soda flow and then adjusts syrup flow to the specified brix ratio. A common carbonated beverage setting is 5:1 water/soda to syrup, but product-specific ratios vary. Wunder-Bar and Cornelius documentation describe separate flow controls and brix calibration.

If one syrup stream is 1 unit and carrier is 5 units, syrup fraction is:

\[
1/(5+1)=1/6
\]

If two full syrup streams are opened while carrier remains 5 units, the output does **not** preserve the original ratio:

\[
2/(5+2)=2/7
\]

The mix is therefore more concentrate-rich. To preserve the original total concentrate fraction with both full concentrate streams, carrier must rise to 10 units. Alternatively, with carrier held at 5 units, the two concentrates must sum to 1 unit (for an equal blend: 0.5 + 0.5).

**Design consequence:** simultaneous-feed selection requires coordinated flow control. The controller must decide whether it is holding total output flow, carrier flow, concentrate fraction, or some other constrained property constant.

## 3. General material recipe model

Represent every qualified feedstock as a vector across relevant constituents:

\[
\mathbf c_i=[w_{Fe},w_{Ni},w_{Cu},w_{Bi},w_W,w_{Si},w_O,\ldots]
\]

with \(\sum_j w_{ij}=1\).

For \(n\) feeds and \(k\) constituents, define the feed matrix \(C\in\mathbb R^{k\times n}\), feed-rate vector \(\mathbf f\ge 0\), and desired target composition \(\mathbf x^*\).

A recipe engine solves or optimises:

\[
\min_{\mathbf f\ge 0}\;\lVert C\mathbf f-\mathbf x^*\dot M\rVert_W^2
\]

subject to:

- \(\mathbf 1^T\mathbf f=\dot M\);
- feeder minimum/maximum rates;
- incompatible feed-pair exclusions;
- thermal/process window;
- contamination limits;
- resource reserve / stewardship constraints;
- provenance and assay confidence thresholds.

The weighting matrix \(W\) can give tight control to critical constituents and looser tolerances to benign residuals.

## 4. Linear mix is only the first stage

Real alloy/process output is not determined by feed ratio alone. The actual state is a process-structure-property function:

\[
\mathbf y=f(\mathbf x_{feed},T(t),\nabla T,\dot T, P, atmosphere, melt-pool history, field history, residence time, geometry)
\]

and may include:

- preferential evaporation or oxidation;
- incomplete dissolution/homogenisation;
- segregation;
- brittle intermetallic formation;
- porosity;
- thermal-stress cracking;
- phase transformations;
- powder/wire feed lag;
- melt-pool dilution from substrate;
- magnetic/electric-field effects;
- vacuum and microgravity differences.

Therefore the mass-balance solver is an **input recipe calculator**. Material qualification still requires thermodynamic/kinetic modelling, coupons, microscopy/chemistry, mechanical testing and process-specific acceptance criteria.

## 5. Additive-manufacturing application

Multi-feed directed energy deposition (DED) is the nearest established engineering analogue. Literature already describes:

- multiple powder/wire feedstocks;
- in-situ alloying;
- discontinuous and continuous functionally graded materials;
- composition engineering;
- external-field-assisted DED.

The Römer implementation should therefore use the post-mix matrix as a **recipe and control layer above an appropriate manufacturing process**, not assume one print technology can process every constituent.

Candidate manufacturing routes by feed class:

| Feed / function | Candidate route | Key gate |
|---|---|---|
| compatible metallic powders/wires | multi-feed DED | phase compatibility, cracking, vaporisation, oxidation |
| high-reflectivity/high-conductivity metals | laser/e-beam DED with parameter qualification | coupling/stability |
| refractory additions | DED / powder metallurgy / pre-alloy feed | melt temperature, brittleness |
| ceramic / silica-rich phase | separate deposition, slurry/direct-ink, coating, composite route | thermal mismatch and interface |
| photovoltaic active layers | dedicated thin-film / semiconductor deposition | electronic quality; cannot be inferred from structural alloy recipe |
| surface coatings | electroplating, PVD/CVD, cold spray or other validated route | adhesion, porosity, environment |

## 6. Solar Hull application

For Solar Hull, the matrix becomes a **layer/gradient recipe graph**.

Do **not** simply co-melt Cu, Bi, Si/SiO2, W or other candidate constituents because they appear in the same conceptual stack. Each layer must first be classified by function and process compatibility.

Proposed digital structure:

1. **Structural/substrate layer** — qualified base alloy or composite.
2. **Thermal / conductive transition layer** — composition can be graded where metallurgy supports it.
3. **Shielding / refractory additions** — bounded local composition or discrete layer.
4. **PV-compatible interface** — separate qualification.
5. **PV active layer** — semiconductor-specific process.
6. **Protective / environmental layer** — radiation, erosion, charging and thermal-cycle qualification.

The post-mix matrix can vary composition spatially:

\[
\mathbf x^*=\mathbf x^*(x,y,z,t)
\]

so a print/deposition path may create gradual interfaces rather than abrupt material boundaries. That maps directly to functionally graded manufacturing.

## 7. ISRU and mined-body processing loop

The same matrix should begin **before** printing, at resource processing.

### 7.1 Characterise

- remote sensing and prior source data;
- local spectroscopy / assay;
- particle-size distribution;
- magnetic susceptibility / conductivity;
- volatile content;
- mineral/metal phases;
- contamination and uncertainty.

### 7.2 Fragment / classify

Create controlled size classes before high-selectivity processing. Dust/fines, coarse fragments and metal-rich inclusions should not be forced through one mechanism.

### 7.3 Beneficiate

Established analogue mechanisms include magnetic and electrostatic separation. NASA has demonstrated/advanced regolith beneficiation architectures using magnetic separation and electrostatic sieving.

RFS and EMFF are entered here only as **R&D candidate modules**:

- RFS candidate role: frequency-dependent liberation/sorting/selectivity.
- EMFF candidate role: field-dependent collection/routing/containment of responsive particles.
- promotion requires measured selectivity, throughput, power, contamination, particle-size and failure-state evidence.

### 7.4 Extract / refine

Depending on resource body and target products:

- thermal processing;
- reduction;
- molten-regolith / molten-oxide electrolysis where applicable;
- vacuum volatilisation/distillation for suitable species;
- electromagnetic or electrostatic handling;
- slag/by-product separation;
- recycling and secondary recovery.

NASA's current lunar technology portfolio provides an established analogue for extracting oxygen and metals from regolith and producing useful downstream material streams.

### 7.5 Assay and qualify stock bins

Every concentrate becomes a **qualified stock concentrate** with:

- batch ID;
- origin/body/site;
- elemental/mineral composition;
- uncertainty;
- particle-size distribution;
- moisture/volatile state;
- contamination limits;
- process history;
- custody/provenance;
- acceptable downstream processes.

This is the direct analogue of labelled post-mix concentrate — but with full material passport and uncertainty.

### 7.6 Recipe / alloy / feedstock synthesis

Qualified bins are blended according to target alloy or composite recipes. The controller uses measured composition, not nominal source labels.

Closed-loop control should reconcile:

**assay → recipe → feeder command → in-process sensing → coupon/part verification → recipe correction**.

### 7.7 Manufacture

Use the selected process to produce:

- structural parts;
- repair stock;
- wiring/conductors where material quality permits;
- pressure/non-pressure hardware subject to qualification;
- shielding;
- tools;
- fixtures;
- replacement mining hardware;
- local infrastructure;
- expansion hardware for Cognigrex/LightSpeed compute and operations.

### 7.8 Recover and recycle

Scrap, failed builds and retired parts re-enter the material graph as characterised secondary feedstocks. This is essential to fleet perpetuation because it reduces the need for continuous virgin extraction.

## 8. Matrix graph / digital twin

Model the system as a directed graph:

**resource node → assay → size class → beneficiation → concentrate bin → refining → qualified feedstock → recipe → manufacturing process → part → service → recovery/recycle**

Each edge carries:

- mass flow;
- elemental/mineral composition vector;
- energy demand;
- uncertainty;
- loss/yield;
- process duration;
- contamination risk;
- provenance;
- readiness/evidence state;
- owner/approval gate.

Each node exposes failure modes and alternate routing.

This is more useful than a single fixed BOM because it lets the fleet ask: *what can we make from what we actually have, at this location, with this process capability and these stewardship constraints?*

## 9. Enterprise-level application

Römer's long-horizon operational scope becomes a **distributed interplanetary industrial coordination layer**, not merely a mining/logistics chain:

- prospecting and resource characterisation;
- resource extraction and beneficiation;
- material refining;
- feedstock qualification;
- adaptive alloy/composite synthesis;
- additive/subtractive manufacturing;
- repair/remanufacture;
- infrastructure construction;
- energy and utility provisioning;
- fleet replacement and growth;
- local compute/communications;
- scientific laboratories;
- ecological/planetary stewardship;
- trade and shared-service interfaces.

The system should optimise for **capability sufficiency**, not maximum extraction.

A useful objective set is:

\[
\min (M_{import}, E, waste, irreversible\_extraction, risk, monopoly\_concentration)
\]

while maximising:

\[
availability, repairability, recyclability, interoperability, local\_autonomy, shared\_benefit
\]

subject to safety and stewardship hard constraints.

## 10. Anti-"Buy n Large" governance

Fleet perpetuation must not be allowed to collapse into closed vertical monopoly. Mandatory design principles:

1. **Separation of authority:** IP custody, operations, assurance, resource stewardship and public-interest review are distinct roles.
2. **Interoperable material passports:** recipe and provenance formats must be exportable and inspectable.
3. **No forced single-vendor dependency:** interfaces should support qualified third-party tools, vehicles, habitats and manufacturers.
4. **Distributed capacity:** stations/nodes must retain safe local operation when disconnected from central Römer/Cognigrex services.
5. **Resource stewardship budgets:** extraction ceilings, preserve/no-touch zones and recycling-first policy are first-class constraints.
6. **Interspecial egalitarian gate:** where biological/ecological systems may be affected, welfare and habitat constraints are non-tradeable optimisation limits.
7. **Planetary-protection gate:** contamination and irreversible environmental alteration are separately reviewed.
8. **Benefit-sharing:** commercial gain cannot be the sole optimisation target; science, safety, resilience and shared infrastructure are explicit outputs.
9. **Auditability:** recipe, extraction, yield, waste, rejected builds and externalities are logged.
10. **Right to exit / fork:** data and control schemas must avoid permanent lock-in.
11. **No unsupported sovereignty:** internal registries do not create territorial, celestial-resource or regulatory rights.
12. **Human/independent override:** high-consequence extraction, biological impact and irreversible deployment require an accountable review path.

## 11. Immediate implementation objects

- `INV-018`: Post-Mix Composition Matrix / Variable Feedstock Synthesis.
- `INV-019`: RFS/EMFF-Assisted ISRU Beneficiation and Qualified Feedstock Loop.
- `INV-020`: Distributed Fleet Perpetuation Manufacturing Loop.
- new Type-1 workbook surface: `20_PostMix_Material_Matrix_v0_1`.
- machine-readable matrix JSON.
- deterministic mass-balance reference solver.
- source/evidence rows binding post-mix hardware, multi-material DED and NASA ISRU analogues.
- next-build item for physical/digital test design.

## 12. Minimum validation ladder

**L0 — arithmetic:** mass conservation and ratio tests pass.  
**L1 — simulation:** recipe/feeder controller and uncertainty propagation.  
**L2 — bench feeding:** multiple inert/benign feeds with measured commanded vs actual flow.  
**L3 — material coupons:** established feedstocks and controlled composition gradients.  
**L4 — post-process characterisation:** chemistry, microscopy, porosity, phase and mechanical tests.  
**L5 — environmental:** vacuum/thermal/microgravity-relevant tests where required.  
**L6 — ISRU analogue:** beneficiated natural/simulant feed with assay and recycle loop.  
**L7 — mission-qualified:** only after independent engineering/safety review and evidence-defined acceptance.

RFS/EMFF cannot skip this ladder.

## 13. Evidence anchors

- Wunder-Bar Mark 4 Post-Mix manual: flow regulators; common 5:1 syrup-to-soda/water calibration; product-specific ratio variation.
- Cornelius post-mix documentation: independent water/syrup flow calibration and brix control.
- Feenstra et al., 2021, *Critical review of the state of the art in multi-material fabrication via directed energy deposition*, DOI 10.1016/j.cossms.2021.100924.
- Shang et al., 2026, *Directed energy deposition additive manufacturing: Microstructure and composition engineering for high-performing metallic materials*, DOI 10.1016/j.addma.2026.105240.
- NASA, *Overview: In-Situ Resource Utilization*.
- NASA TechPort project 158644, *Parabolic Flight Testing of Regolith Beneficiation for Lunar ISRU*.
- NASA NTRS 20250010678, *In-Situ Resource Utilization with Advanced Manufacturing*.
- NASA Lunar Surface Technology: molten regolith electrolysis and integrated regolith-to-product demonstrations.

## 14. Evidence ceiling

The post-mix mass-balance analogy and multi-feed AM / ISRU analogues are technically grounded.

The following remain **Römer hypotheses / R&D** unless separately evidenced:

- useful RFS selectivity and throughput;
- useful EMFF selectivity/routing efficiency for mined-body material streams;
- direct production of flight-qualified Solar Hull material from locally derived feedstock;
- closed-loop autonomous asteroid-to-alloy-to-flight-hardware operation;
- economic, legal or resource-right viability of a self-perpetuating interplanetary enterprise.

These are implementation targets, not present capabilities.
