# Cryptic-Pocket Discovery with Upside on a CPU Workstation

## Scope and status

This note proposes a screening workflow:

> protein structure -> baseline pocket prediction -> Upside REMD sampling ->
> folded-state frame filtering and clustering -> atomistic reconstruction ->
> pocket scoring -> ranked cryptic-pocket candidates

Upside provides the structure preparation, coarse-grained simulation, replica
exchange, restart, and trajectory-analysis components demonstrated in this
repository. PocketMiner, all-atom reconstruction, minimization, and
`fpocket`/`MDpocket` are proposed external integrations. The complete workflow
has not been validated in this repository, and Upside should not be treated as
an established cryptic-pocket discovery engine without the retrospective
benchmark described below.

The objective is candidate generation, not an estimate of physical opening
kinetics or equilibrium pocket populations.

## Evidence labels

Use these labels in results and decisions:

- **Repository-demonstrated**: directly supported by this repository's README,
  scripts, or examples.
- **External-method evidence**: supported by the cited literature or an
  external tool's documented purpose, but not integrated here.
- **Workflow proposal**: a defensible operating recommendation that still
  requires target-specific calibration.
- **Unresolved**: a choice or threshold that must be established by a
  benchmark.

## 1. Prepare and audit the input

Start from an apo structure when the intended test is blind cryptic-site
discovery. Keep any known holo structure out of simulation setup and ranking;
use it only for retrospective evaluation.

Before conversion:

1. Select the biologically relevant assembly, model, and chains. A crystallographic
   asymmetric unit is not automatically the biological assembly.
2. Resolve alternate locations and inspect missing backbone atoms or residues.
   Model missing segments only when biologically justified, and record the
   modeling method and uncertainty.
3. Decide whether interfaces, termini, disulfides, engineered mutations, and
   unresolved loops are part of the biological system being tested.
4. Record cofactors, metals, glycans, lipids, ligands, and structured waters.
   `PDB_to_initial_structure.py` recognizes standard amino acids and converts
   MSE to MET; other residue types are ignored. Therefore, retention of a
   cofactor in the input PDB does not imply that Upside models it.
5. For membrane proteins, use a membrane-aware Upside configuration and verify
   orientation and membrane thickness. The repository has dedicated membrane
   and membrane-pulling examples, but membrane setup is not automatic.

Convert the selected protein chains with:

```bash
python "$UPSIDE_HOME/py/PDB_to_initial_structure.py" \
    input.pdb input_basename \
    --chains=A \
    --record-chain-breaks
```

The converter writes `input_basename.fasta`,
`input_basename.initial.npy`, `input_basename.chi`, and, when applicable,
`input_basename.chain_breaks`. It removes residues lacking a complete N/CA/C
backbone and fails on unexpected chain breaks unless the dangerous
`--allow-unexpected-chain-breaks` override is supplied. Do not use that
override merely to bypass missing residues: the resulting polymer connectivity
may be invalid. These behaviors are repository-demonstrated in
`README.md`, `py/PDB_to_initial_structure.py`, and
`example/01.GettingStarted`.

Run an input control through the later reconstruction and pocket-scoring stages
before simulation. This separates pockets introduced by conversion,
reconstruction, minimization, or the detector from pockets opened during
sampling.

## 2. Establish a cheap baseline

Run PocketMiner on the starting apo structure before simulation. PocketMiner
predicts residue-level cryptic-pocket propensity from a single structure
([Meller et al., 2023](https://pubmed.ncbi.nlm.nih.gov/36859488/)).

Use this result to:

- define regions for reporting and focused analysis;
- prioritize reconstruction and pocket scoring if CPU time is limited;
- compare independently predicted residues with simulation-derived pocket
  linings.

Do not call a PocketMiner prediction simulation evidence, and do not discard
all sites outside its predictions. It is a fast prior, not a hard spatial
restraint or proof that a pocket opens.

Also run the selected pocket detector on the starting apo structure. Save each
baseline pocket's lining residues, volume, and score using the same settings
that will be applied to reconstructed simulation frames.

## 3. Pilot the Upside sampling regime

Use `example/02.ReplicaExchangeSimulation` as the primary template. Replica
exchange is preferred here because the repository describes strong
temperature-dependence of equilibration and uses REMD to locate a melting
transition. Upside parallelizes replicas with OpenMP on one machine.

The following is a **CPU-oriented starting assumption**, not a validated
protocol:

| Setting | Pilot starting point | Purpose |
| --- | --- | --- |
| Replicas | 8 | Fits a typical 8-core workstation |
| Temperature range | 0.80-0.94 | Matches example 02; recalibrate per protein |
| Ladder | quadratic spacing as in example 02 | Denser spacing at the low end |
| Duration | 5,000-20,000 Upside units | Short ladder and stability pilot |
| Frame interval | 50-100 Upside units | Limits storage while retaining screening frames |
| Exchange interval | 10-20 Upside units | Matches repository examples/README scale |
| Seeds | 2 initially, 3 or more after triage | Tests reproducibility |

Upside temperature, duration, and frame interval are in natural units. Duration
must not be interpreted as picoseconds, and the repository warns that mapping
to experimental folding time may be conformation-dependent. Wall-clock cost
should be measured on the target workstation with a short run, then the
production duration should be scaled from observed throughput.

Pilot acceptance criteria should be set before production:

- neighboring replicas exchange often enough to permit temperature traversal;
- low-temperature ensembles retain the native or near-native fold;
- at least some intermediate-temperature frames show local rearrangement
  without global unfolding;
- RMSD, radius of gyration, secondary structure, and contact integrity are
  stable enough to define a folded-state analysis region.

If the initial ladder is entirely folded, raise the upper end cautiously. If
the lower states lose the fold, lower or narrow the ladder. The numerical
thresholds are unresolved and must be calibrated for protein size, topology,
and the selected force field.

Run multiple independent seeds where affordable. A local opening observed in
one correlated segment of one state trajectory is weaker evidence than an
opening reproduced across seeds and folded conformational clusters.

### Why pulling and arbitrary restraints are not the default

`example/05.Advanced_config.py`, `example/06.PullingSimulation`, and
`example/07.MoreRestraints` demonstrate restraint, wall, and pulling
capabilities. These are appropriate for a specific mechanical or structural
hypothesis, but they can create or stabilize nonphysical cavities. Use them
only as labeled hypothesis-driven follow-ups, with unrestrained controls; do
not mix their pocket frequencies with unbiased-screening results.

### Continuing runs

Longer sampling can be split into restartable segments. `example/13.RestartSimulation`
demonstrates recording momentum and restarting with the final configuration
and momentum. Preserve each command line, configuration, seed, force-field
version, and restart history.

## 4. Extract, filter, and cluster folded frames

Upside output is coarse-grained. `mdtraj_upside.py` can load `.up` trajectories
as MDTraj trajectories and add H, O, and CB pseudo-atoms for analysis and
visualization:

```python
import sys
sys.path.append("py")
import mdtraj_upside as mu

traj = mu.load_upside_traj("simulation.up")
```

`example/03.TrajectoryAnalysis` and `py/get_info_from_upside_traj.py`
demonstrate extraction of CA RMSD, radius of gyration, potential energy,
hydrogen-bond count, and temperature. `py/mdtraj_upside.py` also supplies
CA-RMSD and clustering helpers.

Important: replica-exchange files are stored by thermodynamic state, not by a
continuous physical replica. After swaps, consecutive frames in a
temperature-state file may come from different replicas and the trajectory is
discontinuous. Analyze each state as an ensemble. Do not infer opening or
closing rates, dwell times, or transition paths from adjacency in these files.

Apply structural-integrity filters before pocket analysis. Calibrate thresholds
from the apo control and low-temperature pilot rather than using universal
numbers. A practical filter records:

- core CA RMSD to the prepared apo reference, excluding genuinely disordered
  tails when justified;
- radius of gyration relative to the starting structure;
- retained secondary structure and native-contact fraction;
- absence of chain separation, severe backbone distortion, or global
  unfolding;
- temperature state, seed, frame index, and restart segment.

As an initial diagnostic only, inspect frames within roughly 2-4 A core CA RMSD
and within roughly 10% of the starting radius of gyration. These are not
acceptance thresholds; compact proteins, flexible multidomain proteins, and
membrane proteins require different criteria.

Cluster the retained frames using core CA RMSD or a feature set focused on
candidate regions, while keeping global integrity metrics. Choose
representatives from populated clusters and preserve cluster weights. Avoid
selecting only extreme maximum-volume frames, which enriches reconstruction
artifacts and globally damaged structures.

## 5. Reconstruct and relax selected frames

The coordinates loaded from Upside are not complete atomistic structures.
Before atomistic pocket detection:

1. Reconstruct full backbone and side-chain atoms for each selected frame with
   one documented reconstruction tool and version.
2. Restore required cofactors, metals, disulfides, protonation choices, and
   membrane context using an explicit mapping procedure.
3. Resolve clashes and perform restrained local minimization, initially
   restraining backbone heavy atoms so that relaxation does not erase the
   sampled conformation.
4. Apply the identical reconstruction/minimization procedure to the starting
   apo control.
5. Reject structures with unresolved clashes, broken stereochemistry, failed
   cofactor geometry, or large minimization-induced backbone changes.

The reconstruction package, force field, solvent model, restraint strength,
and minimization convergence criteria are unresolved integration choices.
Coarse-grained openings may close after side-chain packing or minimization.
That closure is a negative or uncertain result, not a reason to score the
unrelaxed coarse-grained geometry as an atomistic pocket.

## 6. Detect and consolidate pockets

Use open-source `fpocket` for per-structure detection and `MDpocket` for
ensemble-level pocket characterization as the default proposed stage. This
integration is not present in the repository. Recent reviews describe the
broader computational cryptic-site landscape and the role of conformational
sampling and pocket detection
([Bemelmans et al., 2025](https://pubmed.ncbi.nlm.nih.gov/39778412/);
[Gasparikova et al., 2025](https://pubmed.ncbi.nlm.nih.gov/40799497/)).
MD-based work also supports combining conformational dynamics with pocket
characterization, while not validating this particular Upside workflow
([Qu et al., 2025](https://pubmed.ncbi.nlm.nih.gov/40875922/)).

Run one pinned detector version and one parameter set on:

- the prepared/reconstructed starting apo control;
- every accepted cluster representative;
- additional frames sampled across each accepted cluster if frequency is to be
  estimated;
- the known holo structure only after blind ranking is frozen.

Map pockets across frames by overlap of lining residues and, where coordinates
are comparable, pocket-center proximity or volume overlap. Manually audit
ambiguous merges and splits. Keep raw per-frame detector output so that site
consolidation can be revised without rerunning reconstruction.

## 7. Rank candidates

Rank consolidated sites using separately reported components rather than a
single opaque score:

1. **Apo novelty**: absent or substantially smaller/weaker in the starting apo
   control.
2. **Reproducibility**: opens in independent seeds, temperature states, or
   independently populated folded clusters.
3. **Pocket quality**: volume and detector druggability score after
   reconstruction and minimization.
4. **Folded-cluster support**: occurrence in structurally intact, populated
   clusters rather than only unfolded outliers.
5. **Orthogonal agreement**: overlap with PocketMiner residues or, during
   retrospective validation only, a known holo pocket.
6. **Robustness**: survives reasonable reconstruction, minimization, and
   detector-parameter perturbations.

Do not compare raw frame counts across temperatures as if they were unbiased
physical probabilities. Sampling is correlated, REMD state trajectories are
discontinuous, and frame-selection and clustering alter weights. Report
screening frequency as:

> accepted frames containing the site / accepted frames evaluated

stratified by seed, temperature state, and folded cluster. Call it a screening
frequency, not an opening probability or kinetic rate.

### Candidate table

Produce one row per consolidated site:

| Field | Required content |
| --- | --- |
| Pocket ID | Stable site identifier |
| Lining residues | Chain-aware residue identifiers |
| Representative | Reconstructed structure file, seed, state, frame, cluster |
| Apo baseline | Presence, volume, and score in starting apo control |
| Volume | Representative value and distribution across supporting frames |
| Druggability score | Detector name/version and score distribution |
| Screening frequency | Overall and stratified counts/denominators |
| Seed/temperature support | Independent seeds and states containing the site |
| Cluster support | Folded clusters and cluster populations |
| PocketMiner agreement | Overlapping predicted residues |
| Holo overlap | Hidden until retrospective ranking is frozen |
| Evidence classification | Repository-demonstrated, external-method, proposed, unresolved |
| Quality flags | Reconstruction, minimization, integrity, merge/split concerns |

## 8. Retrospective validation

Before prospective use, benchmark one protein with experimentally determined
apo and holo structures and a known cryptic pocket.

For a broader one-year proof of concept with frozen biological answer keys,
target-specific success criteria, and force-positive controls, use
[`SCIENCE_DRIVEN_POC_PLAN.md`](SCIENCE_DRIVEN_POC_PLAN.md). That companion
plan treats KRAS G12C, PI3K-alpha, MYC, talin-vinculin, and latent TGF-beta1
as explicit recovery tests rather than generic pocket-discovery examples.

### Blind protocol

1. Prepare only the apo structure and record the known holo structure with the
   evaluator, not the analyst making ranking choices.
2. Run the apo input control, PocketMiner baseline, REMD, folded-frame
   filtering, clustering, reconstruction, minimization, detection, and ranking.
3. Freeze all candidate identities, ranks, thresholds, and exclusions.
4. Reveal the holo structure and define the experimental pocket by ligand
   contacts and/or a documented pocket-volume procedure.
5. Measure residue overlap, center distance, and rank of the best-matching
   predicted site.

### Required controls

- Pocket detector on the original and reconstructed/minimized apo structure.
- Pocket detector on the holo structure with ligand removed.
- Structural-integrity distributions for all retained and rejected Upside
  frames.
- At least two independent simulation seeds.
- Pocket results before and after minimization.
- A no-simulation baseline using PocketMiner and apo `fpocket`.

### Success criterion

The known holo pocket is recovered among the leading predeclared candidates,
with meaningful lining-residue or spatial overlap, in locally rearranged but
globally folded conformations. Recovery only from severely expanded,
chain-separated, or globally unfolded frames is failure.

Predeclare what "leading" and "meaningful overlap" mean for the benchmark
(for example, top 3 or top 5 and a residue-overlap threshold). Do not choose
these cutoffs after seeing the holo result.

### Interpreting failure

- **No opening in intact frames**: sampling may be too short or the ladder may
  not visit the relevant local transition.
- **Opening only in unfolded frames**: the sampling regime is not selective
  for a cryptic pocket.
- **Opening disappears after reconstruction**: coarse-grained geometry or
  side-chain packing likely produced an artifact.
- **Reconstructed opening exists but detector misses it**: pocket definition or
  detector sensitivity may be the limiting factor.
- **Stable false-positive pockets dominate**: the force field, reconstruction,
  detector scoring, or ranking weights may be biased.
- **Seeds disagree**: sampling is insufficient for a reproducible candidate.

## Known limitations and unresolved calibration

- Upside is not established here as a validated cryptic-pocket discovery
  engine.
- Upside's coarse-grained representation does not directly provide
  atomistically scoreable cavities.
- Side-chain reconstruction and minimization can close apparent openings or
  create new ones.
- Ligands, cofactors, metals, glycans, and membrane context require explicit
  handling outside the basic PDB conversion.
- REMD temperature-state trajectories are discontinuous across swaps.
- Screening frequencies are not equilibrium probabilities or physical
  opening/closing kinetics.
- Temperature range, duration, number of seeds, fold filters, clustering,
  reconstruction method, minimization protocol, detector settings, and ranking
  thresholds require benchmark calibration.

## Repository evidence map

- `README.md`: PDB conversion, chain-break warning, natural units, constant
  temperature and REMD commands, temperature-state output semantics, OpenMP,
  VTF export, and MDTraj loading.
- `example/01.GettingStarted`: PDB conversion, configuration, simulation, and
  trajectory conversion.
- `example/02.ReplicaExchangeSimulation`: 8-replica quadratic temperature
  ladder, swap sets, exchange interval, and restart pattern.
- `example/03.TrajectoryAnalysis`: MDTraj/HDF5 analysis and extraction of RMSD,
  radius of gyration, energy, hydrogen bonds, and temperature.
- `example/05.Advanced_config.py`: restraint-group configuration.
- `example/06.PullingSimulation`: hypothesis-driven membrane pulling.
- `example/07.MoreRestraints`: wall, spring, and positional restraint options.
- `example/13.RestartSimulation`: continuation with recorded momentum.
- `py/PDB_to_initial_structure.py`: chain/model selection, standard-residue
  handling, complete-backbone filtering, chain-break detection, and outputs.
- `py/mdtraj_upside.py`: Upside trajectory loading, CA RMSD, and clustering
  utilities.

## External references

1. Meller A, et al. Predicting locations of cryptic pockets from single protein
   structures using the PocketMiner graph neural network. *Nature
   Communications*. 2023. [PubMed 36859488](https://pubmed.ncbi.nlm.nih.gov/36859488/).
2. Bemelmans MP, et al. Computational advances in discovering cryptic pockets
   for drug discovery. *Current Opinion in Structural Biology*. 2025.
   [PubMed 39778412](https://pubmed.ncbi.nlm.nih.gov/39778412/).
3. Gasparikova D, et al. Recent computational advances in the identification
   of cryptic binding sites for drug discovery. *Bioinformatics Advances*.
   2025. [PubMed 40799497](https://pubmed.ncbi.nlm.nih.gov/40799497/).
4. Qu T, et al. Identification of Protein Cryptic Sites via Conformational
   Dynamics Capturing and Water-Based Pocket Characterization in Molecular
   Dynamics Simulations. *Journal of Chemical Theory and Computation*. 2025.
   [PubMed 40875922](https://pubmed.ncbi.nlm.nih.gov/40875922/).
5. `fpocket`/`MDpocket` project:
   [Discngine/fpocket](https://github.com/Discngine/fpocket).
