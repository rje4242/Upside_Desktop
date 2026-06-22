# Cryptic Pocket Runbook

## Required Tools Summary

### Cryptic-pocket workflow tools

These tools are not included in this repository and must be installed,
version-pinned, and validated separately before use.

- [PocketMiner web interface](https://pocketminer.azurewebsites.net/) or
  [PocketMiner code](https://github.com/Mickdub/gvp/tree/pocket_pred): fast
  baseline cryptic-pocket prior from the starting structure.
- Reconstruction and side-chain packing options, selected as a documented
  integration choice: [MODELLER](https://www.salilab.org/modeller/),
  [PDBFixer](https://github.com/openmm/pdbfixer), or PULCHRA/SCWRL-style tools
  if they have been locally validated for the target workflow.
- Molecular minimization options, selected as a documented integration choice:
  [OpenMM](https://openmm.org/) or [OpenMM GitHub](https://github.com/openmm/openmm),
  or another MD/minimization engine such as GROMACS or AMBER if already used by
  the lab.
- [fpocket and mdpocket](https://github.com/Discngine/fpocket): `fpocket`
  detects pockets on individual atomistic structures; `mdpocket` characterizes
  pockets across atomistic ensembles.
- [VMD](https://www.ks.uiuc.edu/Research/vmd/): visual inspection of structures
  and trajectories.

Reconstruction and minimization tools are selectable integration choices, not
repo-integrated defaults. Pin versions, record command-line settings, and apply
the same reconstruction and minimization procedure to apo controls and sampled
frames.

### Supporting infrastructure

#### OS and shell

- Linux or macOS.
- `bash` and standard Unix command-line tools.

#### Build stack

- CMake.
- `make`.
- C++11 compiler.
- HDF5 C libraries with high-level interface support.
- Eigen 3.
- OpenMP support.

#### Python

- Python 3.11 preferred.
- `venv` or `virtualenv`.
- `pip`.

#### Python packages

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

#### Upside repository setup

- `install_python_env.sh`
- `install.sh`
- `source.sh`

#### Optional infrastructure

- SLURM for cluster execution.

## What Each Tool Is Used For

| Tool | Install/source link | Required? | Used for |
| --- | --- | --- | --- |
| PocketMiner | [Web interface](https://pocketminer.azurewebsites.net/) / [code](https://github.com/Mickdub/gvp/tree/pocket_pred) | Recommended baseline | Provide a fast baseline cryptic-pocket prior from the starting structure. |
| Reconstruction and side-chain packing | [MODELLER](https://www.salilab.org/modeller/), [PDBFixer](https://github.com/openmm/pdbfixer), or locally validated PULCHRA/SCWRL-style tools | Required for atomistic pocket detection on Upside frames | Convert accepted coarse-grained Upside frames to complete atomistic structures. |
| Molecular minimization | [OpenMM](https://openmm.org/) / [GitHub](https://github.com/openmm/openmm), or a documented lab-standard engine such as GROMACS or AMBER | Required after reconstruction | Relax reconstructed structures while checking that the sampled conformation is not erased. |
| `fpocket` | [fpocket repository](https://github.com/Discngine/fpocket) | Required for per-frame pocket calls | Detect pockets on individual atomistic structures. |
| `mdpocket` | [fpocket repository](https://github.com/Discngine/fpocket) | Required for ensemble pocket characterization | Characterize pockets across an ensemble of atomistic structures. |
| VMD | [VMD](https://www.ks.uiuc.edu/Research/vmd/) | Optional | Inspect structures and trajectories visually. |
| Linux/macOS, `bash`, Unix tools | OS package manager | Required | Run build, simulation, filtering, and file-management commands. |
| CMake, `make`, C++11 compiler, HDF5, Eigen, OpenMP | OS package manager or HPC module stack | Required | Compile and run the Upside executable and shared library. |
| Python 3.11, `venv`, `pip` | [Python](https://www.python.org/) or OS package manager | Required | Create and manage the repository Python environment. |
| Python packages | `install_python_env.sh` / `requirements.txt` in this repository | Required for repo workflows | Handle arrays, HDF5 files, PDB preparation, trajectories, tables, plots, clustering, optional REMD reweighting, accelerated array operations, and optional HDX analysis. |
| Upside setup scripts | `install_python_env.sh`, `install.sh`, `source.sh` in this repository | Required | Create the repo-local `.venv`, compile Upside, set `UPSIDE_HOME`, activate `.venv`, and update `PATH` and `PYTHONPATH`. |
| SLURM | Cluster module or site scheduler documentation | Optional | Run larger REMD jobs on a cluster. |

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
