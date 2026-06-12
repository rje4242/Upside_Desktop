# Upside Expert Discussion Questions

These prompts identify scientific and product decisions that are not resolved
by the repository. Each can be discussed without first reading the
[technical FAQ](FAQ.md), while the linked evidence provides implementation and
workflow context.

## PDB Preparation and Representation

### 1. How should protonation states be represented?

Upside's PDB conversion recognizes generic amino-acid identities, including
ASP, GLU, and HIS, and writes N, CA, and C dynamical coordinates. It does not
document selectable charge states, histidine tautomers, or a target-specific
protonation workflow. This leaves uncertainty about systems whose
conformational behavior depends on ionization or tautomer choice. Because an
uncontrolled mapping could change interactions and invalidate comparisons,
what representation, parameter calibration, and validation protocol would you
recommend for incorporating target-specific protonation states and histidine
tautomers into Upside?

Evidence: [residue definitions](py/PDB_to_initial_structure.py#L14-L28);
[coordinate output](README.md#converting-a-pdb-file-to-upside-input).

### 2. What alternate-location preprocessing policy should be standard?

The converter delegates parsing to ProDy, exposes no altloc-selection option,
and can fail when duplicate selected CG or CD atoms remain. The repository does
not establish how the supported ProDy version chooses conformers or whether
that behavior is stable across environments. A reproducible policy matters
because different conformer choices can alter the starting backbone and
side-chain-derived inputs. How should alternate locations be selected,
reported, and tested before conversion, and which parts of that policy should
Upside enforce itself?

Evidence: [PDB parsing and atom collection](py/PDB_to_initial_structure.py#L76-L83);
[PDB parsing call](py/PDB_to_initial_structure.py#L125-L130).

### 3. How should modified tutorial structures be documented and validated?

The repository identifies several tutorial coordinates as extracted,
replicated, designed, or modeled structures, and the membrane tutorial's
`1rkl.pdb` contains dummy boundary records. It does not provide a complete
record-by-record and structural comparison against current authoritative RCSB
entries. That provenance matters for reproducibility and for separating
intentional scientific preparation from accidental drift. What comparison
procedure and provenance metadata should be adopted, and which tutorial
modifications should be retained, regenerated, or replaced?

Evidence: [PDB source table](example/pdb_sources.html);
[tutorial 1RKL](example/08.MembraneSimulation/pdb/1rkl.pdb).

## Output and Interoperability

### 4. What should the supported DCD and XTC export procedure be?

Upside documents VTF export and provides an MDTraj loader that joins restart
segments, constructs topology, applies chain metadata, converts angstroms to
nanometers, and can add pseudo-atoms. MDTraj can then write DCD or XTC, but the
repository has no dedicated, tested export workflow. Incorrect topology,
units, frame ordering, or reconstructed-atom semantics would silently corrupt
downstream analysis. What end-to-end export procedure, compatibility matrix,
and validation tests should be officially supported for DCD and XTC?

Evidence: [visualization instructions](README.md#simulation-analysis-and-visualization);
[Upside MDTraj loader](py/mdtraj_upside.py#L148-L224);
[restart handling](py/mdtraj_upside.py#L226-L263).

### 5. What PyMOL visualization workflow should be supported?

The documented visualization path uses VTF in VMD. A plausible PyMOL path is
to export a PDB topology and compatible trajectory through MDTraj, but this has
not been verified, and Upside's stored frames contain only N, CA, and C while
the loader can add inferred H, O, and CB atoms. The choice of displayed atoms
can affect whether a structure is interpreted as raw model output or derived
geometry. What PyMOL workflow should be supported for inspection, presentation,
and pocket analysis, and which reconstructed atoms and caveats should each mode
include?

Evidence: [Getting Started visualization](example/01.GettingStarted/readme.md);
[pseudo-atom reconstruction](py/mdtraj_upside.py#L103-L134).

### 6. Which full-atom reconstruction method is appropriate?

Upside samples a coarse-grained backbone and uses virtual rotamer
representations internally; full side-chain coordinates are not present in
`/output/pos`. The standard loader reconstructs H, O, and CB only, so
full-atom pocket geometry requires another reconstruction and usually
minimization. Different methods may impose side-chain packing that was not
sampled and can create or erase apparent cavities. Which reconstruction method,
ensemble protocol, and quality controls best preserve Upside's backbone
ensemble while avoiding misleading atomistic pocket claims?

Evidence: [trajectory reconstruction](py/mdtraj_upside.py#L34-L137);
[workflow reconstruction stage](CRYPTIC_POCKET_WORKFLOW.md#5-reconstruct-and-relax-selected-frames).

## Thermodynamics and Pocket Interpretation

### 7. How should natural units be calibrated?

Upside accepts temperature and reports potential and kinetic energies, but the
documentation warns that its temperature, time, and energy scales are natural
units rather than automatically physical units. The examples demonstrate
relative thermodynamic analysis, not a general calibration to kelvin,
kilocalories per mole, or physical time. Reporting physical values without a
validated mapping would overstate the model. Which observables, reference
systems, fitting strategy, and transferability tests should define a defensible
calibration of Upside temperatures and energies?

Evidence: [natural-unit warning](README.md#constant-temperature-simulation);
[MBAR example](example/03.TrajectoryAnalysis/2.mbar_meltingCurve_freeEnergy.py#L46-L118).

### 8. What would be required to estimate binding constants?

The repository supports protein conformational sampling and relative
statistics, but its PDB converter ignores general small-molecule ligands and it
does not implement an experimental Kd, Ka, or standard binding-free-energy
workflow. A binding calculation would need explicit partners, reversible
bound/unbound sampling, a standard state, and corrections for restraints,
confinement, symmetry, orientation, and binding modes. What explicit molecular
model, thermodynamic cycle, corrections, convergence criteria, and experimental
validation would be required before Upside-derived protein-protein or
ligand-binding constants could be reported?

Evidence: [ligand filtering](py/PDB_to_initial_structure.py#L47-L59);
[cavity option](py/advanced_config.py#L1103-L1113);
[Boresch et al., 2003](https://doi.org/10.1021/jp0217839).

### 9. Which observables should define local pocket opening?

The proposed cryptic-pocket workflow combines pocket volume, lining residues,
detector score, and spatial overlap, with controls for core CA RMSD, radius of
gyration, secondary structure, and native contacts. No single observable or
target-independent threshold is validated, and global expansion can mimic a
local opening. This distinction determines whether candidates represent useful
cryptic states or damaged protein structures. How should target-specific
collective variables and thresholds be selected and validated to distinguish
local pocket opening from unfolding, domain separation, or nonspecific
expansion?

Evidence: [fold filtering](CRYPTIC_POCKET_WORKFLOW.md#4-extract-filter-and-cluster-folded-frames);
[pocket detection](CRYPTIC_POCKET_WORKFLOW.md#6-detect-and-consolidate-pockets).

### 10. What protocol could support an equilibrium pocket probability?

The current workflow reports accepted-frame screening frequency and explicitly
does not treat it as an equilibrium opening probability. A defensible
probability would require a predeclared state classifier, consistent
reconstruction, equilibrium target-state samples, correct direct or MBAR
weights, and autocorrelation-aware uncertainty. The result could otherwise be
dominated by sampling design or correlated frames. What sampling, weighting,
state-definition, uncertainty, and sensitivity-analysis protocol would be
sufficient to report an equilibrium pocket-state probability?

Evidence: [candidate ranking](CRYPTIC_POCKET_WORKFLOW.md#7-rank-candidates);
[known limitations](CRYPTIC_POCKET_WORKFLOW.md#known-limitations-and-unresolved-calibration);
[MBAR weighting example](example/03.TrajectoryAnalysis/2.mbar_meltingCurve_freeEnergy.py#L75-L111).

### 11. How should convergence be diagnosed for pocket populations?

Replica exchange can improve barrier crossing and state mixing, but it does not
establish convergence, and temperature-stream adjacency cannot be interpreted
as a physical trajectory. Independent seeds may still produce different pocket
populations even when exchange diagnostics look acceptable. Since unreliable
populations undermine ranking and uncertainty estimates, what combination of
seed agreement, round trips, effective sample sizes, state transitions,
reweighting diagnostics, and stopping rules should be required before declaring
a pocket analysis converged?

Evidence: [replica-exchange semantics](README.md#replica-exchange-simulation);
[workflow limitations](CRYPTIC_POCKET_WORKFLOW.md#known-limitations-and-unresolved-calibration).

## Product Validation

### 12. What is the force field's credible operating domain?

The repository demonstrates folding, membrane, multichain, restraint, and HDX
workflows, but those examples do not establish accuracy across protein sizes,
folds, oligomeric states, or membrane classes. Upside's coarse-grained
representation also omits chemistry essential to some systems. Product
selection depends on knowing where conformational ensembles are reliable, not
only where simulations run. Across which target classes does the current force
field reproduce experimental ensembles, what evidence should define success,
and which classes should remain outside the claimed operating domain?

Evidence: [repository scientific concepts](REPOSITORY_REPORT.md#at-a-glance-core-scientific-concepts);
[example structures](example/pdb_sources.html);
[membrane example](example/08.MembraneSimulation/readme.md).

### 13. What benchmark would establish a credible operating domain?

The proposed validation workflow calls for blinded apo/holo targets, negative
controls, multiple seeds, compute-matched baselines, identical reconstruction,
and predeclared metrics. It does not settle the panel composition, competing
methods, or thresholds needed for a product claim. Those choices determine
whether apparent success generalizes beyond selected examples. Which benchmark
panel, negative controls, comparison methods, stratification variables,
preregistered thresholds, and failure rules would provide convincing evidence
of Upside's operating domain?

Evidence: [required controls](CRYPTIC_POCKET_WORKFLOW.md#required-controls);
[retrospective validation](CRYPTIC_POCKET_WORKFLOW.md#8-retrospective-validation);
[PocketMiner](https://pubmed.ncbi.nlm.nih.gov/36859488/).

### 14. Which experiments best test Upside-generated hypotheses?

The repository includes an HDX/HX-MS analysis path, while proposed deliverables
also include residue-level hypotheses, reconstructed structures, and predicted
perturbations that could be tested by labeling, cross-linking, FRET, or
construct design. These assays differ in speed, localization, cost, and ability
to distinguish the predicted state from generic destabilization. Which wet-lab
measurements, controls, and readouts would provide the fastest and most
discriminating validation of an Upside-generated conformational hypothesis?

Evidence: [HDX workflow](REPOSITORY_REPORT.md#L130-L133);
[candidate report](CRYPTIC_POCKET_WORKFLOW.md#candidate-table).

### 15. What prospective decision should an Upside result change?

The current materials propose ranked conformational candidates and
experimentally actionable residue hypotheses rather than affinity or kinetic
predictions. They do not identify a single prospective wet-lab decision with
defined performance requirements. Without such a decision, benchmark metrics
may not translate into practical value. Which concrete decision, such as assay
site selection, mutation choice, construct design, or follow-up prioritization,
should change because of an Upside result, and what accuracy, uncertainty,
turnaround time, and failure rate would make that change justified?

Evidence: [product-oriented deliverable](FAQ.md#29-what-would-make-upside-useful-to-a-wet-lab-group);
[candidate table](CRYPTIC_POCKET_WORKFLOW.md#candidate-table).
