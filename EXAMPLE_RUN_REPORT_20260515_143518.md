# Upside Example Run Report - 20260515_143518

Date: 2026-05-15 14:35 America/Los_Angeles  
Repository: `/media/nithin/data2/nithin/codex_work/resilient_interface/Upside_Desktop`  
Requested examples: 04-10, 12-13, 15, default scripts and default simulation durations.

## Outcome

The run products that already existed in the requested example directories were archived first under:

`example_run_archive/20260515_143518/`

The requested suite was then started with per-command logging under:

`example_run_logs/20260515_143518/`

The suite did not complete. The first default command, `example/04.HDX: python 0.run.py`, launched a 16-replica REMD run of `200000` steps per replica. After roughly 4-5 minutes it had reached about `400 / 200000` steps, projecting to tens of hours for this command alone on this CPU before the remaining examples and analysis steps. I stopped the long-running process with `pkill -f 'obj/upside|python 0.run.py'` to preserve the machine and report the measured result instead of leaving an open multi-hour job.

## Machine Configuration

- OS/kernel: Linux `nithin-MS-7B79` `5.15.0-179-generic` x86_64
- CPU: AMD Ryzen 5 2600 Six-Core Processor, 6 cores / 12 threads
- RAM: 62 GiB total, about 57 GiB available at collection time
- Python: 3.11.9
- Key packages: `numpy==1.26.4`, `scipy==1.13.1`, `tables==3.10.1`, `h5py==3.11.0`, `matplotlib==3.9.2`, `mdtraj==1.11.0`
- `obj/upside`: 34,611,744 bytes, mtime `2026-05-14 16:43:59 -0700`, sha256 `41e26bba7fcd94187a1d8df0df492334d6962c33ce7aaf2786edc9b5d93f2e2b`
- `obj/libupside.so`: 37,095,392 bytes, mtime `2026-05-14 16:46:18 -0700`, sha256 `34c811ec62b6dc2987bce9d4a9f980cf0739e330f071834008d7594d65b9f833`

## Command Status

| Example | Command | Status | Log | Note |
|---|---:|---|---|---|
| 04.HDX | `python 0.run.py` | STOPPED | `example_run_logs/20260515_143518/example_04.HDX_python_0.run.py.log` | Started normally, reached about `400 / 200000` steps per replica, then stopped due projected runtime. |
| 04.HDX | `python 1.config.py` | SKIPPED | n/a | Requires completed HDX trajectories. |
| 04.HDX | `bash 2.traj_ana.sh` | SKIPPED | n/a | Requires completed config/run output. |
| 04.HDX | `bash 3.get_protaction_states.sh` | SKIPPED | n/a | Requires trajectory analysis output. |
| 04.HDX | `python 4.calc_HDX.py` | SKIPPED | n/a | Requires protection-state output. |
| 05.Advanced_config.py | `bash 0.run.sh` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 05.Advanced_config.py | `bash 1.ana.sh` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 06.PullingSimulation | `python 0.run.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 06.PullingSimulation | `python 1.get_force.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 07.MoreRestraints | `python 0.run.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 08.MembraneSimulation | `python 0.normal.run.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 08.MembraneSimulation | `python 1.channel.run.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 08.MembraneSimulation | `python 2.lateral_pressure.run.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 08.MembraneSimulation | `python 3.fixed_curvature.run.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 08.MembraneSimulation | `python 4.curvature_dynamics1.run.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 08.MembraneSimulation | `python 5.curvature_dynamics2.run.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 09.IsomerizationPRO | `python 0.run.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 09.IsomerizationPRO | `python recal_omega.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 09.IsomerizationPRO | `python recal_potential.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 09.IsomerizationPRO | `python plot_two_wall.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 10.SelfAvoidRandomWalk | `python run.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 12.MultistepIntegrator | `python 0.run.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 12.MultistepIntegrator | `bash 1.ana.sh` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 13.RestartSimulation | `python 0.run.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 13.RestartSimulation | `python 0.continue.py` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 15.SpatialTransformation | `bash 0.run.sh` | NOT RUN | n/a | Suite halted after first command runtime projection. |
| 15.SpatialTransformation | `bash 1.ana.sh` | NOT RUN | n/a | Suite halted after first command runtime projection. |

## HDF5 Verification

The partial HDX setup did generate readable HDF5 `.up` files.

- `example/04.HDX/inputs/EHEE_rd2_0005.up`
  - Top-level groups: `/input`
  - `/input/pos`: shape `(120, 3, 1)`, dtype `float32`
  - `/input/sequence`: shape `(40,)`, dtype `|S3`
  - Representative input potentials present under `/input/potential`, including `Angle`, `Distance3D`, `Spring_bond`, `hbond_energy`, `protein_hbond`, `rama_map_pot`, and `rotamer`.
- `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.0.up`
  - Readable as HDF5, but contains only `/input`; no `/output` group was appended before the interrupted run closed.
  - Missing `/output/pos`, `/output/time`, `/output/temperature`, `/output/potential`, and `/output/kinetic` because the command was stopped before a completed output trajectory was flushed.

No representative completed `.up` output could be verified for finite energy/temperature arrays in this run because no simulation command reached successful completion.

## Scientific Sanity

- The HDX run initialized normally, created 16 replica output files, and logged finite initial and early-step values.
- Representative log values were finite: initial potential energy around `-115.96`; early temperatures around `30.9` to `46.5`; early potentials were finite.
- The default examples are validation and illustration runs. Even if completed, they should not be treated as convergence proof without independent sampling and analysis criteria.

## File Structure And Data Flow

The observed HDX flow matches the expected Upside example structure:

1. PDB/static inputs remain under the example directory, for example `example/04.HDX/pdb/EHEE_rd2_0005.pdb`.
2. `python 0.run.py` generated `/inputs` artifacts including FASTA, chi, initial coordinates, and an HDF5 `.up` config.
3. Replica `.up` files were copied/generated under `outputs/REMD/`.
4. `obj/upside` was expected to append `/output` trajectory datasets such as `pos`, `time`, `temperature`, `potential`, and `kinetic`; this did not complete before interruption.
5. Downstream scripts would normally consume `/output` and write derived analysis outputs such as `results/`, VTF, RMSD, HDX tables, plots, or force/restart artifacts depending on the example.

## Visualization Guidance

- Use generated `.vtf` files in VMD when analysis scripts complete.
- Use `py/extract_vtf.py` to extract VTF trajectories from completed `.up` files.
- Use `py/attr_overview.py` or HDF5 viewers/PyTables to inspect `.up` dataset layout and attributes.
- Use MDTraj through `py/mdtraj_upside.py` where supported for trajectory-level inspection.
- Use example-specific plot outputs after the relevant analysis scripts complete, such as HDX plots/tables, pulling force data, isomerization potentials, and membrane-analysis artifacts.

## Performance Indication

- Only `04.HDX: python 0.run.py` ran long enough to measure.
- Observed progress: about `400 / 200000` steps after roughly 4-5 minutes for 16 replicas.
- Rough projection: tens of hours for the first HDX default command on this Ryzen 5 2600 CPU before downstream HDX analysis and the rest of examples 05-10, 12-13, and 15.
- The HDX command uses CPU-threaded replica exchange behavior across 16 replicas; on this 6-core/12-thread machine that is enough to saturate CPU for a long wall-clock run.

## Artifacts

- Archive: `example_run_archive/20260515_143518/`
- Logs: `example_run_logs/20260515_143518/`
- Partial HDX generated inputs and replica files remain in `example/04.HDX/inputs/` and `example/04.HDX/outputs/REMD/`.
