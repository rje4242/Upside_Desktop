# Upside Example Run Report - 2026-05-15 13:50 PDT

## Machine And Configuration

- Host: `nithin-MS-7B79`
- OS: Linux `5.15.0-179-generic` x86_64
- CPU: AMD Ryzen 5 2600 Six-Core Processor, 6 cores / 12 threads
- RAM: 62 GiB total, 57 GiB available at capture time
- Python: 3.11.9 from the repository `.venv` after `source source.sh`
- Key packages: `numpy==2.4.4`, `tables==3.11.1`, `h5py==3.16.0`, `matplotlib==3.10.9`, `scipy==1.17.1`, `mdtraj==1.11.1.post1`
- Dependency manifest: no `requirements.txt` is present; `.devcontainer/environment.yml` is the available manifest.
- Upside binary: `obj/upside`, 34,611,744 bytes, mtime `2026-05-14 16:43:59 -0700`, sha256 `41e26bba7fcd94187a1d8df0df492334d6962c33ce7aaf2786edc9b5d93f2e2b`
- Upside library: `obj/libupside.so`, 37,095,392 bytes, mtime `2026-05-14 16:46:18 -0700`, sha256 `34c811ec62b6dc2987bce9d4a9f980cf0739e330f071834008d7594d65b9f833`

## Scope

Requested scope was all local numbered Upside examples except `example/11.BigSystem`, using each script's default simulation duration. `example/00.AnalysisScripts` was not run standalone; it is an HXMS/HDX analysis toolkit used by HDX-style workflows.

Prior generated artifacts were archived before running:

- Archive: `example_run_archive_20260515_130302/`
- Archived contents: previous `example/15.SpatialTransformation/inputs`, `outputs`, and `results`

Run logs are under:

- `example_run_logs/20260515_130347/`

## Run Status

| Status | Example | Command | Elapsed | Log | Notes |
|---|---:|---|---:|---|---|
| PASS | 01 | `bash 0.run.sh` | 18.229 s | `example_run_logs/20260515_130347/01_01.GettingStarted_0.run.sh.log` | Generated input config and constant-temperature trajectory. |
| PASS | 01 | `bash 1.ana.sh` | 1.679 s | `example_run_logs/20260515_130347/02_01.GettingStarted_1.ana.sh.log` | Generated RMSD and VTF analysis outputs. |
| PASS | 02 | `python run.py` | 204.218 s | `example_run_logs/20260515_130347/03_02.ReplicaExchangeSimulation_run.py.log` | Generated 8 REMD replica `.up` outputs. |
| BLOCKED | 03 | `python 0.run.py` | >40 min before external stop | no completed per-command log | Created input config and 16 REMD output files, but the files had no `/output` group after interruption. |
| NOT RUN | 03 | `bash 1.traj_ana.sh` | n/a | n/a | Requires completed `03` simulation output. |
| NOT RUN | 03 | `python 2.mbar_meltingCurve_freeEnergy.py` | n/a | n/a | Requires completed `03` simulation output. |
| NOT RUN | 04-10, 12-13, 15 | planned workflows | n/a | n/a | Not reached because default-duration `03` blocked the sequential run. |
| EXCLUDED | 11 | all scripts | n/a | n/a | Excluded by request. |
| SKIPPED | 00 | standalone workflow | n/a | n/a | Analysis toolkit, not an independent numbered example run. |

## Artifact Verification

Generated layout followed the expected pattern for completed examples:

- `inputs/`: FASTA, initial coordinates, chain/chi files, and base config `.up`
- `outputs/<sim_id>/`: Upside run `.up` trajectory/config HDF5 files plus logs where scripts emit them
- `results/`: analysis products such as RMSD and VTF files

Observed artifacts:

- `example/01.GettingStarted/inputs/chig.up`
- `example/01.GettingStarted/outputs/simple_test/chig.run.up`
- `example/01.GettingStarted/results/chig_simple_test.rmsd`
- `example/01.GettingStarted/results/chig_simple_test.vtf`
- `example/02.ReplicaExchangeSimulation/inputs/chig.up`
- `example/02.ReplicaExchangeSimulation/outputs/REMD/chig.run.0.up` through `chig.run.7.up`
- `example/03.TrajectoryAnalysis/inputs/EHEE_rd2_0005.up`
- `example/03.TrajectoryAnalysis/outputs/REMD/EHEE_rd2_0005.run.0.up` through `.run.15.up`, but without `/output` after interruption

HDF5 checks:

- `01.GettingStarted`: `/input` and `/output` present; `/output/pos` has 20 frames; temperature range 0.8 to 0.8; potential range -1.139 to 133.439; kinetic range 0.013 to 1.462.
- `02.ReplicaExchangeSimulation`: `/input` and `/output` present for checked replica 0; `/output/pos` has 100 frames; temperature range 0.8 to 0.8 for replica 0; potential range -12.150 to 32.880; kinetic range 0.013 to 1.633.
- `03.TrajectoryAnalysis`: checked replica 0 has `/input` but no `/output`, consistent with an interrupted or incomplete run.

## Scientific Sanity Checks

The completed examples are functional smoke checks only. Default example durations are short relative to production molecular simulation needs and are not convergence evidence.

- `01.GettingStarted`: constant-temperature trajectory completed and analysis produced RMSD plus VTF outputs. Energies and temperatures were finite in the checked arrays.
- `02.ReplicaExchangeSimulation`: REMD run completed for 8 replicas. Checked replica output contains expected trajectory, potential, kinetic, temperature, and time arrays.
- `03.TrajectoryAnalysis`: not scientifically interpretable from this run because the simulation was interrupted before output groups were written.

## Visualization And Tooling

- Use VMD with generated `.vtf` files, for example `example/01.GettingStarted/results/chig_simple_test.vtf`.
- Use MDTraj through `py/mdtraj_upside.py` for notebook-based loading or conversion of completed `.up` trajectories.
- Use HDF5 viewers, PyTables, or `py/attr_overview.py` to inspect `.up` group and array structure.
- Use the example analysis scripts for RMSD, MBAR/free-energy, HDX/protection-state, pulling-force, and membrane plots once their upstream simulations complete.

## Performance Notes

- `01.GettingStarted` simulation plus analysis completed in about 20 seconds total.
- `02.ReplicaExchangeSimulation` completed in about 204 seconds.
- `03.TrajectoryAnalysis/0.run.py` blocked the sequential full-suite run for more than 40 minutes on this machine. It configured successfully and created 16 replica files, but the run did not complete before it was stopped.

## Failure And Next Steps

Primary blocker: runtime/performance in `example/03.TrajectoryAnalysis/0.run.py` at default settings: `duration = 200000`, `n_rep = 16`, `frame_interval = 100`.

Recommended next actions:

1. Re-run `03` alone under `time` or a scheduler and allow a longer wall-time window.
2. If the goal is regular validation rather than default-duration benchmarking, add a separate short-duration smoke-test mode instead of editing the default example scripts.
3. After `03` completes, run its `1.traj_ana.sh` and `2.mbar_meltingCurve_freeEnergy.py`, then continue the planned sequence from `04.HDX` onward.
4. For a full default-duration report, run the harness from `scripts/run_upside_examples.py` again after deciding an acceptable timeout policy for long examples.
