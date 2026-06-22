# Cryptic Pocket Runbook

## Required Tools Summary

### OS and shell

- Linux or macOS.
- `bash` and standard Unix command-line tools.

### Build stack

- CMake.
- `make`.
- C++11 compiler.
- HDF5 C libraries with high-level interface support.
- Eigen 3.
- OpenMP support.

### Python

- Python 3.11 preferred.
- `venv` or `virtualenv`.
- `pip`.

### Python packages

- `numpy`
- `scipy`
- `tables`
- `h5py`
- `ProDy`
- `pandas`
- `matplotlib`
- `mdtraj`
- `pymbar`
- `scikit-learn`
- `jax`
- `colorcet`
- `pyhdx==0.4.3`
- `hdxms-datasets<0.2`

### Upside repository setup

- `install_python_env.sh`
- `install.sh`
- `source.sh`

### External cryptic-pocket tools

These are not included in this repository and must be installed, versioned, and
validated separately.

- PocketMiner, or an equivalent single-structure baseline cryptic-pocket
  predictor.
- All-atom reconstruction and side-chain packing tool.
- Molecular minimization engine.
- `fpocket`.
- `MDpocket`.

### Optional tools

- VMD for visualization.
- SLURM for cluster execution.

## What Each Tool Is Used For

- Linux/macOS, `bash`, and Unix tools: run the build, simulation, filtering,
  and file-management commands.
- CMake, `make`, C++11 compiler, HDF5, Eigen, and OpenMP: compile and run the
  Upside executable and shared library.
- Python 3.11, `venv`, and `pip`: create the repository Python environment.
- `numpy`, `scipy`, `tables`, and `h5py`: handle numerical arrays and HDF5
  Upside files.
- `ProDy`: read and prepare PDB structures.
- `pandas`, `matplotlib`, and `scikit-learn`: assemble tables, plots, and
  clustering or ranking features.
- `mdtraj`: load, filter, and analyze trajectories.
- `pymbar`: support optional REMD reweighting analysis.
- `jax`: support Python workflows that depend on accelerated array operations.
- `colorcet`, `pyhdx==0.4.3`, and `hdxms-datasets<0.2`: support optional HDX
  analysis workflows present in this repository.
- `install_python_env.sh`: create the repo-local `.venv` and install Python
  packages.
- `install.sh`: compile Upside.
- `source.sh`: set `UPSIDE_HOME`, activate `.venv`, and update `PATH` and
  `PYTHONPATH`.
- PocketMiner or equivalent: provide a fast baseline cryptic-pocket prior from
  the starting structure.
- Reconstruction and side-chain packing: convert accepted coarse-grained
  Upside frames to complete atomistic structures.
- Molecular minimization: relax reconstructed structures while checking that
  the sampled conformation is not erased.
- `fpocket`: detect pockets on individual atomistic structures.
- `MDpocket`: characterize pockets across an ensemble of atomistic structures.
- VMD: inspect structures and trajectories visually.
- SLURM: run larger REMD jobs on a cluster.

## Environment Setup

From the repository root:

```bash
./install_python_env.sh
./install.sh
source ./source.sh
```

Confirm the key commands and imports before starting a target:

```bash
which upside
python -c "import h5py, tables, mdtraj, pymbar, pandas, prody, sklearn, jax"
```

Record tool versions in the project log:

```bash
python --version
pip freeze > python_environment.freeze.txt
upside --help | head
```

For external tools, record the executable path, version, installation source,
and command-line settings. Do this for PocketMiner or its replacement, the
reconstruction tool, the minimization engine, `fpocket`, and `MDpocket`.

## PDB Preparation

Start from an apo structure for blind cryptic-pocket discovery. Keep any known
holo structure out of setup and ranking until retrospective evaluation is
frozen.

Before conversion:

- Select the biological assembly, model, and chains.
- Resolve alternate locations and inspect missing backbone atoms or residues.
- Decide how to handle termini, interfaces, disulfides, mutations, unresolved
  loops, cofactors, metals, glycans, lipids, ligands, and structured waters.
- Record anything that Upside will not model directly.

Convert the selected chains:

```bash
python "$UPSIDE_HOME/py/PDB_to_initial_structure.py" \
  input.pdb target_apo \
  --chains=A \
  --record-chain-breaks
```

Expected outputs include:

- `target_apo.fasta`
- `target_apo.initial.npy`
- `target_apo.chi`
- `target_apo.chain_breaks`, when chain breaks are recorded

Do not use `--allow-unexpected-chain-breaks` just to bypass missing residues.
If the polymer connectivity is wrong, downstream sampling and pocket calls are
not interpretable.

Run the external baseline tools on the prepared starting structure before
simulation:

```bash
# External: command depends on the installed predictor.
pocketminer_or_equivalent input.pdb > baseline_cryptic_prior.txt

# External: fpocket is not included in this repository.
fpocket -f input.pdb
```

Save baseline pocket lining residues, volumes, detector scores, and settings.
Use the same detector settings later on reconstructed simulation frames.

## Upside Config and REMD Run

Create one Upside configuration per replica. The exact options should follow
the force field and example configuration used for the target, but this is the
typical shape:

```bash
for i in 0 1 2 3 4 5 6 7; do
  python "$UPSIDE_HOME/py/upside_config.py" \
    --output "remd_${i}.up" \
    --fasta target_apo.fasta \
    --initial-structure target_apo.initial.npy \
    --hbond-energy "$UPSIDE_HOME/parameters/ff_2.1/hbond.h5" \
    --dynamic-rotamer-1body \
    --rotamer-placement "$UPSIDE_HOME/parameters/ff_2.1/sidechain.h5" \
    --rotamer-interaction "$UPSIDE_HOME/parameters/ff_2.1/sidechain.h5" \
    --environment-potential "$UPSIDE_HOME/parameters/ff_2.1/environment.h5" \
    --bb-environment-potential "$UPSIDE_HOME/parameters/ff_2.1/bb_env.dat" \
    --rama-library "$UPSIDE_HOME/parameters/common/rama.dat" \
    --rama-sheet-mixing-energy "$UPSIDE_HOME/parameters/ff_2.1/sheet" \
    --reference-state-rama "$UPSIDE_HOME/parameters/common/rama_reference.pkl"
done
```

Run a CPU REMD pilot. Treat these values as starting points, not a validated
cryptic-pocket protocol:

```bash
upside \
  --duration 20000 \
  --frame-interval 100 \
  --temperature 0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94 \
  --swap-set 0-1,2-3,4-5,6-7 \
  --swap-set 1-2,3-4,5-6 \
  --replica-interval 20 \
  --monte-carlo-interval 5 \
  --seed "$RANDOM" \
  remd_0.up remd_1.up remd_2.up remd_3.up \
  remd_4.up remd_5.up remd_6.up remd_7.up
```

Upside duration, frame interval, replica interval, and temperature are in
Upside natural units, not picoseconds. REMD output files are organized by
temperature state after swaps, so do not treat adjacent frames in a state file
as a continuous physical trajectory.

For SLURM, request one task and one CPU per replica as a starting point:

```bash
sbatch --ntasks 1 --cpus-per-task 8 run_remd.sh
```

## Folded-Frame Extraction and Filtering

Load Upside trajectories with `mdtraj_upside.py`:

```python
import sys
sys.path.append("py")
import mdtraj_upside as mu

traj = mu.load_upside_traj("remd_0.up")
```

Filter frames before pocket detection. Keep at least:

- seed, temperature state, frame index, and restart segment;
- core CA RMSD to the prepared apo reference;
- radius of gyration relative to the starting structure;
- native-contact or secondary-structure retention;
- flags for chain separation, global unfolding, or severe backbone distortion.

As a first diagnostic only, inspect frames within about 2-4 A core CA RMSD and
within about 10% of the starting radius of gyration. These are not universal
acceptance thresholds. Set final thresholds from the apo control, the pilot
run, and target-specific structural behavior.

Cluster retained frames by core CA RMSD or local candidate-site features. Pick
representatives from populated folded clusters, not only the largest apparent
pockets.

## Reconstruction and Minimization

Upside frames are coarse-grained and should not be scored directly as
atomistic cavities.

For every accepted representative and for the starting apo control:

1. Reconstruct full backbone and side-chain atoms with one documented external
   reconstruction tool and version.
2. Restore required cofactors, metals, disulfides, protonation choices, and
   membrane context with a documented mapping procedure.
3. Run restrained local minimization with an external minimization engine.
4. Measure reconstruction and minimization changes, including backbone RMSD and
   clash or stereochemistry checks.
5. Reject frames whose pocket depends on unresolved clashes, broken chemistry,
   missing required context, or large minimization-induced backbone drift.

Example command placeholders:

```bash
# External: replace with the selected reconstruction/packing tool.
reconstruct_all_atom accepted_frame.pdb -o accepted_frame_rebuilt.pdb

# External: replace with the selected minimization engine.
minimize_structure accepted_frame_rebuilt.pdb -o accepted_frame_minimized.pdb
```

Use the same reconstruction and minimization procedure for the apo control and
all simulation-derived structures.

## Pocket Detection

Run the same detector versions and settings on:

- the original prepared apo input;
- the reconstructed/minimized apo control;
- every accepted reconstructed/minimized cluster representative;
- additional accepted frames if estimating screening frequency;
- the holo structure only after blind candidate ranking is frozen.

Example `fpocket` command:

```bash
fpocket -f accepted_frame_minimized.pdb
```

Example `MDpocket` placeholder:

```bash
MDpocket --trajectory accepted_frames.xtc --topology accepted_frame_minimized.pdb
```

Map pockets across frames by lining-residue overlap and, when coordinates are
comparable, pocket-center distance or volume overlap. Keep raw per-frame
detector outputs so merges and splits can be revisited.

## Candidate Ranking and Report Outputs

Rank consolidated pockets using separate reported components rather than a
single opaque score:

- Apo novelty: absent or weaker in the starting apo control.
- Reproducibility: present across independent seeds, temperature states, or
  populated folded clusters.
- Pocket quality: volume and detector score after reconstruction and
  minimization.
- Folded-cluster support: found in structurally intact clusters rather than
  unfolded outliers.
- Orthogonal agreement: overlap with PocketMiner or equivalent residues.
- Robustness: survives reasonable reconstruction, minimization, and detector
  setting perturbations.

Report screening frequency as:

```text
accepted frames containing the site / accepted frames evaluated
```

Stratify by seed, temperature state, and folded cluster. Do not call this an
opening probability, physical population, dwell time, or kinetic rate.

Produce a candidate table with these fields:

| Field | Required content |
| --- | --- |
| Pocket ID | Stable site identifier |
| Lining residues | Chain-aware residue identifiers |
| Representative | Structure file, seed, state, frame, and cluster |
| Apo baseline | Presence, volume, and score in starting apo control |
| Volume | Representative value and distribution |
| Druggability score | Detector name, version, settings, and score |
| Screening frequency | Overall and stratified counts/denominators |
| Seed and temperature support | Independent seeds and states containing the site |
| Cluster support | Folded clusters and cluster populations |
| Baseline predictor agreement | Overlap with PocketMiner or equivalent residues |
| Holo overlap | Hidden until retrospective ranking is frozen |
| Quality flags | Reconstruction, minimization, integrity, and merge/split concerns |

Archive the following with each run:

- prepared input PDB and conversion command;
- Upside config commands and `.up` files;
- Upside run command, seed, duration, frame interval, temperature ladder, and
  swap sets;
- filtering thresholds and rejected-frame counts;
- cluster assignments and representative structures;
- reconstruction and minimization commands;
- pocket detector commands and raw outputs;
- final ranked candidate table and summary plots.
