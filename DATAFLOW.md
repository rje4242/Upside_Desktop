# upside2-md Data Flow

## End-to-End Pipeline

```
PDB file
   │
   ▼  PDB_to_initial_structure.py
FASTA + backbone .npy + chain_breaks
   │
   ▼  upside_config.py  (+ advanced_config.py)
simulation.up  [HDF5 /input group]
   │
   ├─ (copy once per replica) ──►  replica_0.up  replica_1.up  ...
   │
   ▼  upside binary
simulation_N.up  [HDF5 /output group appended]
   │
   ▼  Python analysis tools
MDTraj / VTF / statistics
```

---

## Stage 1 — PDB → Initial Structure

**Script:** `py/PDB_to_initial_structure.py`

**Input:** `protein.pdb`

**Processing:**
1. Parse `ATOM` records; keep N, CA, C, O, CB atoms.
2. Detect chain breaks where Cα–Cα > 4 Å.
3. Compute backbone dihedrals φ, ψ, ω from N/CA/C positions.
4. Extract sidechain χ1, χ2 from heavy atom coordinates where available.

**Output files:**

| File | Format | Contents |
|---|---|---|
| `protein.fasta` | plain text | single-letter amino acid sequence |
| `protein.initial.npy` | NumPy array `[N_res, 3, 3]` | N / CA / C positions per residue |
| `protein.chi` | text table | χ1, χ2 angles per residue |
| `protein.chain_breaks` | text list | residue indices where chain breaks occur |

**Flags used in examples:**
- `--record-chain-breaks` — write `.chain_breaks` file
- `--disable-recentering` — keep original PDB coordinates

---

## Stage 2 — Initial Structure → Configuration File

**Script:** `py/upside_config.py`  
**Wrapper:** `run_upside.upside_config()` (calls the script as a subprocess)

**Input:**
- `protein.fasta`
- `protein.initial.npy` (optional; random chain built if absent)
- Parameter files from `parameters/`

**What the script does:**

```
1. Read FASTA → residue sequence
2. If initial_structure provided:
       load N/CA/C positions
   Else:
       sample φ, ψ, ω from Ramachandran prior
       build chain using transfer-and-build (TAB) matrices
3. Place all atoms:
       CB from N/CA/C geometry
       Virtual H (backbone NH) and O (carbonyl) positions
       Sidechain centroids from rotamer library
4. Assemble computational graph in HDF5:
       Write each force field term as a node group under /input/potential/
       Each group records: node class name, input node names (arguments attr),
       and all numerical parameters (indices, spline knots, etc.)
5. Write /input/pos  ← initial atomic coordinates [n_atom, 3, 1]
6. Write /input/fasta  ← sequence
7. Write /input/chain_first_residue  ← chain break indices (if multi-chain)
```

**Optional second pass — `advanced_config.py`:**

Opens the `.up` file in append mode and adds:
- Position constraints (`Const3D`) read from `.dat` files (e.g., `nail-xyz.dat`, `nail-y.dat`)
- Affine alignment constraints
- Extra surface or tension nodes

This is the mechanism used in curvature dynamics examples to nail specific atoms.

**Output:** `simulation.up` with `/input/` group fully populated.

---

## Stage 3 — Configuration → Replica Files

**Script:** example run scripts (`run.py`)

Before launching `upside`, the run script copies the base config to one file per replica:

```python
for j in range(n_rep):
    shutil.copyfile(config_base, h5_files[j])
```

Each replica starts from identical coordinates. Temperature differentiation happens at runtime via `--temperature T0,T1,...` passed to `upside`.

For **restart runs** (`continue_sim = True`), instead of copying the base config the script:
1. Opens each `.up` file in append mode.
2. Renames `/output` → `/output_previous_N` (preserving old trajectory).
3. Overwrites `/input/pos` with the last frame of the previous output.
4. Archives the log file with a timestamp suffix.

---

## Stage 4 — Simulation

**Binary:** `obj/upside`

**Invocation:**
```
upside --duration D --frame-interval F --temperature T0,T1,...  \
       --seed S [other flags]  replica_0.up  replica_1.up  ...
```

### Startup sequence

```
Parse CLI flags
For each .up file:
    Open HDF5, read /input/pos → positions
    Build DerivEngine from /input/potential graph
    Initialize OrnsteinUhlenbeck thermostat at target T
    Open /output group for writing
```

### Graph construction

The engine reads each node group from `/input/potential/`:
1. Reads the `arguments` attribute to find input nodes.
2. Instantiates the corresponding C++ class.
3. Connects nodes in dependency order.

This is done once at startup; the resulting DAG is fixed for the entire run.

### MD loop (per timestep)

```
┌──────────────────────────────────────────────────────────┐
│  (optional, at --monte-carlo-interval)                   │
│  Propose backbone pivot or jump move                     │
│  Compute ΔE; Metropolis accept/reject                    │
└──────────────────────────────────────────────────────────┘
                          │
┌──────────────────────────────────────────────────────────┐
│  Forward pass                                            │
│  → placement nodes reconstruct N,CA,C,O,CB,H from pos   │
│  → coord nodes compute distances, angles, dihedrals      │
│  → potential nodes compute scalar energies               │
│  → total E = Σ PotentialNode.potential                   │
└──────────────────────────────────────────────────────────┘
                          │
┌──────────────────────────────────────────────────────────┐
│  Backward pass                                           │
│  → sens arrays propagated from potentials → pos          │
│  → pos.sens = -∂E/∂x  (force on each atom)              │
└──────────────────────────────────────────────────────────┘
                          │
┌──────────────────────────────────────────────────────────┐
│  Velocity Verlet or multi-step Verlet                    │
│  p ← p + Δt · F    (half step)                          │
│  x ← x + Δt · p                                         │
│  [recompute F at new x]                                  │
│  p ← p + Δt · F    (half step)                          │
└──────────────────────────────────────────────────────────┘
                          │
┌──────────────────────────────────────────────────────────┐
│  Ornstein-Uhlenbeck thermostat                           │
│  p ← exp(-Δt/τ)·p + √(T·(1−exp(−2Δt/τ)))·ξ            │
└──────────────────────────────────────────────────────────┘
                          │
┌──────────────────────────────────────────────────────────┐
│  COM recentering                                         │
│  full XYZ (default) or XY only (--disable-z-recentering)│
└──────────────────────────────────────────────────────────┘
                          │
┌──────────────────────────────────────────────────────────┐
│  (optional, at --replica-interval)                       │
│  For each swap pair in current swap set:                 │
│    Compute Boltzmann factors for both replicas           │
│    Metropolis accept/reject coordinate exchange          │
└──────────────────────────────────────────────────────────┘
                          │
┌──────────────────────────────────────────────────────────┐
│  (optional, at --frame-interval)                         │
│  Append snapshot to /output/ datasets                    │
└──────────────────────────────────────────────────────────┘
```

### Curvature dynamics (membrane simulations)

When `--curvature-changer-interval` is set, an additional step runs:
1. Propose a random ΔZ shift to the curvature center node.
2. Evaluate membrane potential at new center.
3. Metropolis accept/reject (accepts if ΔE < 0 or by Boltzmann factor).

This is used in `08.MembraneSimulation/4–5` to let the membrane curvature equilibrate.

### Signal handling

`SIGTERM` or `SIGINT` sets a flag that causes the loop to exit cleanly after the current timestep, flushing all buffered output. This ensures partial runs are always readable.

---

## Stage 5 — Output

`upside` appends an `/output/` group to each `.up` file as the simulation runs, using chunked HDF5 datasets that grow by `frame_interval` steps.

### Core datasets (all runs)

| Dataset | Shape | Contents |
|---|---|---|
| `pos` | `[n_frame, n_atom, 3]` | atomic coordinates per frame |
| `potential` | `[n_frame]` | total potential energy |
| `kinetic` | `[n_frame]` | kinetic energy per atom |
| `time` | `[n_frame]` | simulation time at each frame |
| `temperature` | `[n_frame, n_replica]` | thermostat temperature |

### Conditional datasets

| Condition | Dataset | Contents |
|---|---|---|
| `--log-level detailed` | `hbond_*` | per-H-bond occupancy |
| `--log-level detailed` | `environment_*` | per-residue burial fraction |
| `--log-level extensive` | `rotamer_state_*` | selected rotamer index |
| `--monte-carlo-interval > 0` | `pivot_stats`, `jump_stats` | MC acceptance statistics |
| `--replica-interval > 0` | `replica_index` | `[n_frame, n_replica]` T-slot assignment |
| `--replica-interval > 0` | `replica_cumulative_swaps` | `[n_frame, n_pair, 2]` success/attempt |
| `--record-momentum` | `mom` | `[n_frame, n_atom, 3]` momentum |

### Output rate

```
n_frames = floor(duration / frame_interval)
```

Each frame records one snapshot regardless of the inner timestep count.

---

## Stage 6 — Analysis

### Loading trajectories

```python
import mdtraj_upside as mu

traj = mu.load('outputs/run/protein.run.0.up')
# traj is an MDTraj Trajectory object
```

`mdtraj_upside.py` reads `/output/pos` and reconstructs full heavy-atom coordinates from the coarse-grained representation using the same placement logic as the engine.

### Extracting energetics

```python
import tables as tb
import numpy as np

with tb.open_file('protein.run.0.up') as f:
    potential = f.root.output.potential[:]   # [n_frame]
    time      = f.root.output.time[:]        # [n_frame]
```

### Replica exchange analysis

```python
with tb.open_file('protein.run.0.up') as f:
    replica_index = f.root.output.replica_index[:]
    # replica_index[frame, T_slot] = which physical replica is at that temperature
```

### VMD visualization

```
python py/extract_vtf.py outputs/run/protein.run.0.up protein.vtf
# Open protein.vtf in VMD
```

### Restart / continuation

```python
import generate_restart_config as gr
gr.generate('protein.run.0.up', 'protein_restart.up', frame=-1)
# Creates new .up with /input/pos set to the last frame
```

---

## Data Formats Reference

| Extension | Format | Tool that writes it | Tool that reads it |
|---|---|---|---|
| `.pdb` | PDB text | external | `PDB_to_initial_structure.py` |
| `.fasta` | plain text | `PDB_to_initial_structure.py` | `upside_config.py` |
| `.initial.npy` | NumPy binary | `PDB_to_initial_structure.py` | `upside_config.py` |
| `.chain_breaks` | text list | `PDB_to_initial_structure.py` | `upside_config.py` |
| `.up` | HDF5 | `upside_config.py` (input), `upside` (output) | `upside`, analysis scripts |
| `.h5` (parameters) | HDF5 | parameter estimation scripts | `upside_config.py` |
| `.dat` (parameters) | text table | manual / estimation scripts | `upside_config.py`, `advanced_config.py` |
| `.vtf` | VMD text | `extract_vtf.py` | VMD |
| `.log` | text | `upside` / sbatch | human / monitoring |

---

## Internal Data Layout in C++

All per-atom arrays use the `VecArray` type, which is a 2D view into aligned memory:

```
VecArray  shape: [n_elem, width]
VecArray3 shape: [n_elem, 3]   ← positions, forces, momenta
```

Positions and momenta are stored in `[n_atom, 3, 1]` layout in HDF5 (the trailing 1 is a historical artifact for single-system runs).

The `DerivEngine` levels array ensures nodes are evaluated in topological order: all inputs to a node are computed before the node itself runs.

Parameter arrays (spline knots, residue type indices, etc.) are read once from HDF5 into CPU memory at startup and never change during a run, except when `--set-param` is used for developer parameter perturbation.
