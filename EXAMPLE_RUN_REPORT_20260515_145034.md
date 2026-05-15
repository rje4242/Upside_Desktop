# Upside Example Run Report 20260515_145034

## Scope

Ran selected numbered examples with default scripts and durations. Excluded `00.AnalysisScripts`, `03.TrajectoryAnalysis`, and `11.BigSystem`.

- Repository: `/media/nithin/data2/nithin/codex_work/resilient_interface/Upside_Desktop`
- Log directory: `example_run_logs/20260515_145034`
- Archive directory: `example_run_archives/20260515_145034`
- Summary JSON: `example_run_logs/20260515_145034/summary.json`
- Status: `completed`

## Archive

No pre-existing generated `inputs/`, `outputs/`, or `results/` directories were found for the selected examples.

## Machine Snapshot

- Platform: `Linux-5.15.0-179-generic-x86_64-with-glibc2.35`
- Python executable used by runner: `/media/nithin/data2/anaconda3/bin/python3`
- `obj/upside`: `{"path": "obj/upside", "exists": true, "size_bytes": 34611744, "mtime": "2026-05-14T16:43:59", "sha256": "41e26bba7fcd94187a1d8df0df492334d6962c33ce7aaf2786edc9b5d93f2e2b"}`
- `obj/libupside.so`: `{"path": "obj/libupside.so", "exists": true, "size_bytes": 37095392, "mtime": "2026-05-14T16:46:18", "sha256": "34c811ec62b6dc2987bce9d4a9f980cf0739e330f071834008d7594d65b9f833"}`

### OS
```
Linux nithin-MS-7B79 5.15.0-179-generic #189-Ubuntu SMP Tue May 5 18:20:56 UTC 2026 x86_64 x86_64 x86_64 GNU/Linux
```
### CPU
```
Architecture:                            x86_64
CPU op-mode(s):                          32-bit, 64-bit
Address sizes:                           43 bits physical, 48 bits virtual
Byte Order:                              Little Endian
CPU(s):                                  12
On-line CPU(s) list:                     0-11
Vendor ID:                               AuthenticAMD
Model name:                              AMD Ryzen 5 2600 Six-Core Processor
CPU family:                              23
Model:                                   8
Thread(s) per core:                      2
Core(s) per socket:                      6
Socket(s):                               1
Stepping:                                2
Frequency boost:                         enabled
CPU max MHz:                             3400.0000
CPU min MHz:                             1550.0000
BogoMIPS:                                6799.11
Flags:                                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx mmxext fxsr_opt pdpe1gb rdtscp lm constant_tsc rep_good nopl nonstop_tsc cpuid extd_apicid aperfmperf rapl pni pclmulqdq monitor ssse3 fma cx16 sse4_1 sse4_2 movbe popcnt aes xsave avx f16c rdrand lahf_lm cmp_legacy svm extapic cr8_legacy abm sse4a misalignsse 3dnowprefetch osvw skinit wdt tce topoext perfctr_core perfctr_nb bpext perfctr_llc mwaitx cpb hw_pstate ssbd ibpb vmmcall fsgsbase bmi1 avx2 smep bmi2 rdseed adx smap clflushopt sha_ni xsaveopt xsavec xgetbv1 clzero xsaveerptr arat npt lbrv svm_lock nrip_save tsc_scale vmcb_clean flushbyasid decodeassists pausefilter pfthreshold avic v_vmsave_vmload vgif overflow_recov succor smca sme sev sev_es ibpb_exit_to_user
Virtualization:                          AMD-V
L1d cache:                               192 KiB (6 instances)
L1i cache:                               384 KiB (6 instances)
L2 cache:                                3 MiB (6 instances)
L3 cache:                                16 MiB (2 instances)
NUMA node(s):                            1
```
### Memory
```
total        used        free      shared  buff/cache   available
Mem:            62Gi       4.6Gi        27Gi        88Mi        31Gi        57Gi
Swap:          2.0Gi          0B       2.0Gi
```
### Python Packages
```
Python 3.11.9
numpy==2.4.4
tables==3.11.1
h5py==3.16.0
matplotlib==3.10.9
scipy==1.17.1
mdtraj==1.11.1.post1
```

## Commands

| # | Example | Command | Status | Return | Elapsed | Log | Notes |
|---:|---|---|---|---:|---:|---|---|

## Artifacts

### 01.GettingStarted

- `example/01.GettingStarted/inputs`: 4 files, 1588434 bytes
- `example/01.GettingStarted/outputs`: 2 files, 1648764 bytes
- `example/01.GettingStarted/results`: 2 files, 21856 bytes
- Notable file counts: `{".log": 2, ".npy": 1, ".rmsd": 1, ".up": 2, ".vtf": 1}`

### 02.ReplicaExchangeSimulation

- `example/02.ReplicaExchangeSimulation/inputs`: 4 files, 1588498 bytes
- `example/02.ReplicaExchangeSimulation/outputs`: 8 files, 13632100 bytes
- Notable file counts: `{".log": 1, ".npy": 1, ".up": 9}`

### 04.HDX

- `example/04.HDX/inputs`: 4 files, 3164550 bytes
- `example/04.HDX/outputs`: 16 files, 50709820 bytes
- Notable file counts: `{".npy": 1, ".up": 17}`

### 05.Advanced_config.py

- No generated `inputs/`, `outputs/`, or `results/` directory was present.

### 06.PullingSimulation

- No generated `inputs/`, `outputs/`, or `results/` directory was present.
- Notable file counts: `{".dat": 2}`

### 07.MoreRestraints

- No generated `inputs/`, `outputs/`, or `results/` directory was present.
- Notable file counts: `{".dat": 5}`

### 08.MembraneSimulation

- No generated `inputs/`, `outputs/`, or `results/` directory was present.
- Notable file counts: `{".dat": 3}`

### 09.IsomerizationPRO

- No generated `inputs/`, `outputs/`, or `results/` directory was present.
- Notable file counts: `{".dat": 1}`

### 10.SelfAvoidRandomWalk

- No generated `inputs/`, `outputs/`, or `results/` directory was present.

### 12.MultistepIntegrator

- No generated `inputs/`, `outputs/`, or `results/` directory was present.

### 13.RestartSimulation

- No generated `inputs/`, `outputs/`, or `results/` directory was present.

### 15.SpatialTransformation

- No generated `inputs/`, `outputs/`, or `results/` directory was present.

## Data-Flow Verification

HDF5 inspection return code: `1`.

| File | /input | /output | Interesting Datasets | Numeric Check |
|---|---:|---:|---|---|

## Scientific Sanity Notes

- Energy, temperature, position, and time-like arrays in representative `.up` files are checked for finite numeric values when PyTables can read them.
- REMD examples should produce multiple replica `.up` files under `outputs/REMD`; inspect logs and HDF5 temperatures for exchange workflow health.
- HDX should produce configured REMD analysis outputs, protection-state files, and final HDX calculations after the four analysis stages complete.
- Pulling examples should produce force data from `1.get_force.py`; plot or inspect the generated `.dat` files for force-extension behavior.
- Membrane examples are independent six-script variants; compare generated `.up` files and logs by numbered membrane mode.
- Restart simulation should contain both initial and continued trajectory artifacts; check continuity in output time arrays.
- Isomerization and multistep-integrator workflows rely on their recalculation/analysis products in addition to raw `.up` trajectories.

## Visualization Guidance

- Open `.vtf` files in VMD where analysis scripts generated them.
- Use `py/extract_vtf.py` for trajectory extraction, `py/mdtraj_upside.py` for MDTraj-based inspection, and `py/attr_overview.py` for HDF5 attribute browsing.
- Use PyTables, HDFView, or another HDF5 viewer to inspect `/input`, `/output`, position, time, temperature, potential, and kinetic datasets.
- Review example-specific `.png`, `.pdf`, `.dat`, `.rmsd`, and table outputs for workflow-specific plots and summaries.

## Performance

- Total measured command wall time: 0.0s.
- Completed commands: 0 / 0.
- Failed or interrupted commands: 0.


Elapsed times are machine-specific and include setup, simulation, analysis, and Python startup overhead. For coarse throughput, inspect each command log for progress lines and compare elapsed time against generated frame counts in the corresponding `.up` files.
