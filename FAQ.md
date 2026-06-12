# Upside Technical FAQ

This FAQ summarizes behavior demonstrated by this repository. It distinguishes
implemented behavior from proposed workflows and scientific interpretation.

## PDB Input

### 1. What PDB preparation does Upside require?

Provide a parseable PDB containing the intended protein model and chains.
Residues used by Upside must have complete N, CA, and C backbone atoms, valid
chain labels, and no unexplained polymer breaks. Select particular models or
chains with `--model` and `--chains`; use `--record-chain-breaks` for
multichain systems.

The converter produces a FASTA sequence, N/CA/C coordinates, side-chain chi
angles, and optional chain-break metadata. Coordinates are recentered unless
`--disable-recentering` is supplied.

Evidence: [README](README.md#converting-a-pdb-file-to-upside-input);
[PDB converter](py/PDB_to_initial_structure.py#L104-L150).

### 2. Are missing loops allowed?

Not by default. Residues lacking N, CA, or C are removed, and an internal gap
normally becomes an unexpected chain break that stops conversion.
`--allow-unexpected-chain-breaks` suppresses that failure, but the converter
labels the option dangerous because the resulting polymer connectivity may be
invalid. Missing segments should therefore be modeled or represented as
intentional chain breaks rather than silently bypassed.

Evidence: [PDB converter](py/PDB_to_initial_structure.py#L149-L190);
[README](README.md#converting-a-pdb-file-to-upside-input).

### 3. Are nonstandard residues allowed?

The converter explicitly maps MSE to MET. Other unrecognized residue names are
ignored rather than parameterized. Cis-proline is represented internally as
`CPR`.

Evidence: [PDB converter](py/PDB_to_initial_structure.py#L14-L24);
[residue filtering](py/PDB_to_initial_structure.py#L47-L59).

### 4. How are ligands handled?

General small-molecule ligands are ignored by the PDB converter because
unrecognized residue types are skipped. The repository provides no general
ligand parameterization workflow. Receptor/ligand options elsewhere in the code
can refer to groups of protein chains and should not be interpreted as support
for arbitrary chemical compounds.

Evidence: [residue filtering](py/PDB_to_initial_structure.py#L47-L59);
[cryptic-pocket limitations](CRYPTIC_POCKET_WORKFLOW.md#known-limitations-and-unresolved-calibration).

### 5. Are waters retained?

No. HOH is not a recognized protein residue and is ignored during conversion.

Evidence: [residue filtering](py/PDB_to_initial_structure.py#L47-L59).

### 6. How should protonation states be handled?

The input workflow has no documented selectable protonation variants or
histidine-tautomer controls. It recognizes generic residue types such as ASP,
GLU, and HIS, while the generated dynamical coordinates contain only N, CA, and
C. The repository does not provide a validated protocol for mapping
target-specific protonation choices into Upside.

Evidence: [residue definitions](py/PDB_to_initial_structure.py#L14-L28);
[coordinate output](README.md#converting-a-pdb-file-to-upside-input).

### 7. Are multiple chains supported?

Yes. All chains are parsed by default, or a subset can be selected with
`--chains`. `--record-chain-breaks` records boundaries for later configuration,
and the release notes state that multiple chains are handled automatically.

Evidence: [PDB converter options](py/PDB_to_initial_structure.py#L104-L130);
[release notes](Release_note#L14-L17).

### 8. Are alternate locations supported?

Upside exposes no altloc-selection option and delegates PDB parsing to ProDy.
Duplicate selected CG or CD atoms can make conversion fail. Resolve alternate
locations to a single conformer before conversion. The exact default ProDy
selection policy has not been established from this repository.

Evidence: [PDB parsing and atom collection](py/PDB_to_initial_structure.py#L76-L83);
[PDB parsing call](py/PDB_to_initial_structure.py#L125-L130).

### 9. Are membrane proteins supported?

Yes, through an implicit membrane force field. Membrane context is not inferred
from the PDB: users must supply membrane parameters and thickness. Channel,
lateral-pressure, and curvature modes have additional configuration
requirements.

Evidence: [membrane example](example/08.MembraneSimulation/readme.md);
[membrane options](py/upside_config.py#L2216-L2235);
[release notes](Release_note#L6-L9).

### 10. Which tutorial PDBs differ from their PDB.org originals?

The repository explicitly identifies these derived structures:

- `2qke_mon.pdb`: a monomer extracted from 2QKE.
- `three_1rkl_a.pdb` and `three_1rkl_b.pdb`: constructed from three copies of
  1RKL.
- `EHEE_rd2_0005.pdb`: a de novo Rosetta-designed structure without an RCSB
  entry.
- `fs_wtseq.pdb`: a MODELLER homology model without an RCSB entry.

`chig.pdb` is associated with 1UAO, and the tutorial `1rkl.pdb` includes many
dummy membrane-boundary records. The repository does not establish a complete
record-by-record comparison of every tutorial file with the current RCSB
download.

Evidence: [PDB source table](example/pdb_sources.html);
[tutorial 1RKL](example/08.MembraneSimulation/pdb/1rkl.pdb).

## Simulation Output

### 11. What is inside a `.up` HDF5 file?

A typical combined configuration and trajectory contains:

- `/input/sequence` and `/input/pos`;
- `/input/potential/*`, containing the force-field computation graph and
  embedded parameters;
- configuration arguments, command invocations, and optional chain metadata;
- `/output`, containing trajectory frames and logged observables;
- `/output_previous_N`, containing earlier output segments after restarts;
- optional target, sampler, momentum, restraint, or feature-specific data.

Exact datasets depend on configuration and logging level.

Evidence: [configuration writer](py/upside_config.py#L2256-L2373);
[output logger](src/main.cpp#L719-L748);
[inspection instructions](README.md#simulation-analysis-and-visualization).

### 12. Which arrays represent coordinates?

- `/input/pos`: initial coordinates, normally shaped
  `(3 * residues, 3, 1)`.
- `/output/pos`: recorded trajectory coordinates, with logger shape
  `(frames, 1, 3 * residues, 3)`.
- `/output_previous_N/pos`: preceding restart segments.
- `/target/pos`: optional target coordinates.

The stored particles are N, CA, and C for each residue, in that order.
Coordinates are stored in angstroms; the MDTraj loader converts them to
nanometers.

Evidence: [engine coordinate logger](src/main.cpp#L738-L745);
[trajectory logger](src/main.cpp#L807-L819);
[MDTraj loader](py/mdtraj_upside.py#L1-L16).

### 13. Which arrays represent energies?

The core time series are `/output/potential` and `/output/kinetic`. Depending on
enabled features and logging level, output can also include component
quantities such as Ramachandran, rotamer, HMM, wall, or contact energies.
Arrays under `/input/potential` are model parameters and graph data, not
trajectory energy series.

Evidence: [core energy logging](src/main.cpp#L822-L831);
[analysis reader](py/get_info_from_upside_traj.py#L59-L80);
[rotamer logging](src/rotamer.cpp#L709-L730).

### 14. Which arrays represent temperature or replica state?

`/output/temperature` records the thermodynamic temperature associated with
each frame. Replica-exchange runs additionally log `/output/replica_index` and
the possible `/output/replica_swap_partner` values. Restarted segments can hold
the same arrays under `/output_previous_N`.

Replica-exchange files are organized by temperature or Hamiltonian state, not
as continuous physical-replica trajectories.

Evidence: [replica logging](src/main.cpp#L210-L225);
[temperature logging](src/main.cpp#L889-L895);
[REMD output semantics](README.md#replica-exchange-simulation).

### 15. Is the trajectory physically interpretable directly?

It is interpretable as an Upside coarse-grained backbone ensemble, not as an
ordinary all-atom trajectory. Stored frames omit explicit side-chain heavy
atoms, carbonyl oxygen, amide hydrogen, solvent, ions, and lipids. In addition,
adjacent frames in a replica-exchange temperature stream can come from
different physical replicas, so they must not be used to infer transition paths
or dwell times.

Evidence: [trajectory reconstruction](py/mdtraj_upside.py#L34-L137);
[REMD warning](CRYPTIC_POCKET_WORKFLOW.md#L182-L186).

### 16. How should `.up` trajectories be converted for DCD or XTC use?

The repository's documented native conversion is VTF:

```bash
python py/extract_vtf.py simulation.up simulation.vtf
```

Alternatively, load the trajectory with `mdtraj_upside`, which handles restart
segments, topology, chain metadata, unit conversion, and optional pseudo-atoms.
The resulting MDTraj object can use MDTraj's format writers:

```python
import sys
sys.path.append("py")
import mdtraj_upside as mu

traj = mu.load_upside_traj("simulation.up")
traj[0].save_pdb("simulation.pdb")
traj.save_dcd("simulation.dcd")
traj.save_xtc("simulation.xtc")
```

The repository does not include a dedicated or tested DCD/XTC conversion
script, so this route requires validation against the installed MDTraj version.

Evidence: [visualization instructions](README.md#simulation-analysis-and-visualization);
[Upside loader](py/mdtraj_upside.py#L148-L224).

### 17. What output should be visualized in PyMOL versus VMD?

The documented VMD workflow uses the generated VTF trajectory. The repository
does not provide a verified PyMOL-specific trajectory procedure. A conventional
PyMOL route would use an exported PDB topology with a compatible trajectory,
but that workflow remains to be validated.

Evidence: [visualization instructions](README.md#simulation-analysis-and-visualization);
[Getting Started](example/01.GettingStarted/readme.md).

### 18. Are side-chain positions explicit, reconstructed, or approximated?

Full side-chain coordinates are not stored in `/output/pos`. Upside uses
rotamer-based virtual side-chain representations internally. The standard
MDTraj visualization loader reconstructs only CB, except for glycine, and also
adds geometrically inferred H and O atoms. Atoms beyond CB are not generated by
that loader. These visualization atoms are derived approximations, not an
all-atom trajectory.

Evidence: [pseudo-atom reconstruction](py/mdtraj_upside.py#L103-L134);
[rotamer logging and model](src/rotamer.cpp#L709-L730).

## Thermodynamics

### 19. Can Upside estimate Kd, Ka, delta G, or only relative statistics?

The repository demonstrates model energies, equilibrium conformational
statistics, temperature-dependent observables, and relative free-energy
profiles along chosen coordinates. It does not demonstrate an experimental
ligand-binding Kd, Ka, or standard binding free energy.

For two defined conformational states, equilibrium populations can provide a
model-relative conformational free-energy difference,
`delta G = -kT ln(P_B/P_A)`. This is not automatically a ligand-binding free
energy or an experimentally calibrated value.

Evidence: [MBAR example](example/03.TrajectoryAnalysis/2.mbar_meltingCurve_freeEnergy.py#L46-L118);
[ligand handling](py/PDB_to_initial_structure.py#L47-L59).

### 20. What assumptions would be required to estimate a binding constant?

Such a calculation is not implemented or validated here. It would require
explicit bound and unbound definitions, reversible equilibrium sampling, an
appropriate model for every binding partner, a defined concentration and
standard state, and corrections for confinement, restraints, symmetry,
orientation, and binding modes. It would also require convergence tests and
physical calibration of the model's thermodynamic units.

The repository's finite-concentration cavity option does not by itself provide
these corrections. Also, `ka` and `kb` variables in the HX scripts are chemical
exchange-rate terms, not association constants.

Evidence: [cavity option](py/advanced_config.py#L1103-L1113);
[Boresch et al., 2003](https://doi.org/10.1021/jp0217839).

### 21. Is replica exchange required?

No. Upside supports constant-temperature simulation. Replica exchange is a
sampling strategy and is recommended in the repository for folding studies
because equilibration is strongly temperature-dependent. It may improve
barrier crossing but does not establish convergence by itself.

Evidence: [constant-temperature simulation](README.md#constant-temperature-simulation);
[replica exchange](README.md#replica-exchange-simulation);
[pocket sampling recommendation](CRYPTIC_POCKET_WORKFLOW.md#3-pilot-the-upside-sampling-regime).

### 22. What is the recommended observable for pocket opening?

No single pocket-opening observable is validated in this repository. The
proposed workflow uses a predeclared local pocket-state definition based on
reconstructed and minimized structures, including pocket volume, lining
residues, detector score, and spatial overlap. It accompanies this with global
fold-integrity controls such as core CA RMSD, radius of gyration, secondary
structure, and native contacts.

Global RMSD, energy, radius of gyration, or maximum cavity volume alone is not a
sufficient pocket-opening definition.

Evidence: [fold filtering](CRYPTIC_POCKET_WORKFLOW.md#4-extract-filter-and-cluster-folded-frames);
[pocket detection](CRYPTIC_POCKET_WORKFLOW.md#6-detect-and-consolidate-pockets).

### 23. How should pocket-state probability be estimated?

The repository does not validate equilibrium pocket probabilities. A defensible
future estimate would require a classifier fixed before outcome inspection,
consistent reconstruction and detection, target-state equilibrium samples,
appropriate direct or MBAR weights, autocorrelation-aware uncertainty, and
agreement across independent seeds and analysis choices.

The current proposed workflow reports accepted-frame screening frequency,
stratified by seed, temperature, and folded cluster. It explicitly warns that
this is not an opening probability or kinetic rate.

Evidence: [candidate ranking](CRYPTIC_POCKET_WORKFLOW.md#7-rank-candidates);
[known limitations](CRYPTIC_POCKET_WORKFLOW.md#known-limitations-and-unresolved-calibration);
[MBAR weighting example](example/03.TrajectoryAnalysis/2.mbar_meltingCurve_freeEnergy.py#L75-L111).

### 24. What scientific claims would be unsafe?

Unsupported claims include:

- deriving experimental Kd, Ka, or standard binding free energy from raw
  energies or frame counts;
- treating potential-energy differences as free-energy differences;
- reporting physical energy or time units without calibration;
- calling screening frequency an equilibrium population;
- inferring kinetics or pathways from replica-exchange frame adjacency;
- treating coarse-grained or pseudo-atom coordinates as atomistic geometry;
- accepting openings that occur only in globally damaged structures or vanish
  after reconstruction;
- combining biased and unbiased runs into one population estimate;
- claiming convergence from one seed, visual inspection, replica mixing, or
  MBAR output alone;
- claiming validated cryptic-pocket prediction without blinded benchmarking and
  controls.

Evidence: [natural-unit warning](README.md#constant-temperature-simulation);
[workflow limitations](CRYPTIC_POCKET_WORKFLOW.md#known-limitations-and-unresolved-calibration).

## Product Fit

The answers in this section are evidence-based recommendations, not validated
performance claims.

### 25. What target class is the best-supported fit for Upside?

The most defensible starting class is small or moderate-sized, well-folded
protein domains whose question is dominated by backbone conformational
sampling. Prefer standard amino-acid systems with high-quality structures,
known comparison states, and no essential omitted chemistry. Soluble proteins
are the simplest initial targets; membrane proteins are supported but require
additional setup and validation.

Evidence: [repository scientific concepts](REPOSITORY_REPORT.md#at-a-glance-core-scientific-concepts);
[example structures](example/pdb_sources.html);
[Jumper et al.](https://arxiv.org/abs/1610.07277).

### 26. What target classes should be avoided initially?

Poor initial product targets include:

- ligand-affinity problems requiring explicit ligand energetics;
- metal-, cofactor-, glycan-, nucleic-acid-, lipid-, ion-, or water-dependent
  mechanisms;
- chemistry dominated by protonation changes, covalent reactions, or
  post-translational modifications;
- highly disordered proteins without independent validation;
- uncertain assemblies, large missing segments, or highly flexible
  multidomain complexes;
- atomistic pocket-design problems controlled by detailed side-chain packing
  and structured water.

Evidence: [converter limitations](py/PDB_to_initial_structure.py#L47-L59);
[workflow limitations](CRYPTIC_POCKET_WORKFLOW.md#known-limitations-and-unresolved-calibration).

### 27. What is the smallest credible demonstration?

For engineering, reproduce `example/01.GettingStarted`: convert Chignolin, run a
trajectory, inspect the `.up` file, and visualize the result. This demonstrates
installation and data flow, not scientific validity.

For scientific credibility, use one blinded retrospective apo/holo case with a
known local conformational change. Predeclare the analysis, run at least two
independent seeds, reject globally damaged frames, reconstruct and minimize
candidates, compare against a static baseline, and reveal the holo result only
after rankings are frozen.

Evidence: [Getting Started](example/01.GettingStarted/readme.md);
[blind validation protocol](CRYPTIC_POCKET_WORKFLOW.md#8-retrospective-validation).

### 28. What benchmark would persuade a skeptical computational chemist?

A persuasive benchmark should use a preregistered panel of apo/holo targets and
negative controls, blind analysis, multiple independent seeds, compute-matched
baselines, identical atomistic reconstruction for controls and predictions, and
predeclared metrics. Relevant metrics include top-k recovery, lining-residue
overlap, pocket-center distance, false-positive rate, fold integrity,
reproducibility, compute cost, and sensitivity to analysis choices.

Recovery only from unfolded structures, or only before atomistic
reconstruction, should count as failure.

Evidence: [required controls and success criteria](CRYPTIC_POCKET_WORKFLOW.md#required-controls);
[PocketMiner](https://pubmed.ncbi.nlm.nih.gov/36859488/).

### 29. What would make Upside useful to a wet-lab group?

The deliverable should be an experimentally actionable hypothesis rather than a
raw trajectory: a short ranked residue list, reconstructed representative
structures, confidence across seeds, predicted perturbations, assay-compatible
readouts, and negative controls. Potential readouts include HDX-MS peptides,
cysteine-labeling sites, cross-link pairs, FRET-label pairs, or construct
boundaries.

HDX/HX-MS is the repository's strongest demonstrated bridge to experimental
data and is a more defensible initial offering than ligand-affinity prediction.

Evidence: [HDX workflow](REPOSITORY_REPORT.md#L130-L133);
[candidate report](CRYPTIC_POCKET_WORKFLOW.md#candidate-table).

### 30. What is the fastest way to avoid fooling ourselves?

Run a falsification-oriented blinded pilot before expanding the product:

1. Select one known apo/holo case and one negative control.
2. Freeze thresholds and success criteria before revealing holo results.
3. Run a static baseline.
4. Use at least two independent seeds.
5. Reject globally unfolded or chain-separated openings.
6. Require candidates to survive reconstruction and minimization.
7. Report failures and disagreements.
8. Describe results as screening candidates, not affinities, kinetics, or
   equilibrium probabilities.
9. Stop if Upside does not reproducibly outperform the static baseline.

Evidence: [retrospective validation](CRYPTIC_POCKET_WORKFLOW.md#8-retrospective-validation);
[failure interpretation](CRYPTIC_POCKET_WORKFLOW.md#interpreting-failure).

## External References

1. Jumper JM, Freed KF, Sosnick TR. *Rapid calculation of side chain packing and
   free energy with applications to protein molecular dynamics.*
   [arXiv:1610.07277](https://arxiv.org/abs/1610.07277).
2. Shirts MR, Chodera JD. *Statistically optimal analysis of samples from
   multiple equilibrium states.*
   [J Chem Phys. 2008](https://doi.org/10.1063/1.2978177).
3. Boresch S, Tettinger F, Leitgeb M, Karplus M. *Absolute binding free
   energies: a quantitative approach for their calculation.*
   [J Phys Chem B. 2003](https://doi.org/10.1021/jp0217839).
4. Meller A, et al. *Predicting locations of cryptic pockets from single protein
   structures using the PocketMiner graph neural network.*
   [Nature Communications. 2023](https://pubmed.ncbi.nlm.nih.gov/36859488/).
