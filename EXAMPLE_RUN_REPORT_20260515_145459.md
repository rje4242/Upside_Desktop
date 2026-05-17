# Upside Example Run Report 20260515_145459

## Scope

Ran selected numbered examples with default scripts and durations. Excluded `00.AnalysisScripts`, `03.TrajectoryAnalysis`, and `11.BigSystem`.

- Repository: `/media/nithin/data2/nithin/codex_work/resilient_interface/Upside_Desktop`
- Log directory: `example_run_logs/20260515_145459`
- Archive directory: `example_run_archives/20260515_145459`
- Summary JSON: `example_run_logs/20260515_145459/summary.json`
- Status: `completed_with_failures`

## Archive

| Example | Directory | Files | Archived To |
|---|---:|---:|---|
| `01.GettingStarted` | `inputs` | 4 | `example_run_archives/20260515_145459/01.GettingStarted/inputs` |
| `01.GettingStarted` | `outputs` | 2 | `example_run_archives/20260515_145459/01.GettingStarted/outputs` |
| `01.GettingStarted` | `results` | 2 | `example_run_archives/20260515_145459/01.GettingStarted/results` |
| `02.ReplicaExchangeSimulation` | `inputs` | 4 | `example_run_archives/20260515_145459/02.ReplicaExchangeSimulation/inputs` |
| `02.ReplicaExchangeSimulation` | `outputs` | 8 | `example_run_archives/20260515_145459/02.ReplicaExchangeSimulation/outputs` |
| `04.HDX` | `inputs` | 4 | `example_run_archives/20260515_145459/04.HDX/inputs` |
| `04.HDX` | `outputs` | 16 | `example_run_archives/20260515_145459/04.HDX/outputs` |

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
Mem:            62Gi       7.8Gi       5.5Gi       248Mi        49Gi        54Gi
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
| 1 | `01.GettingStarted` | `bash 0.run.sh` | passed | 0 | 5.1s | `example_run_logs/20260515_145459/01_01.GettingStarted_0.run.sh.log` |  |
| 2 | `01.GettingStarted` | `bash 1.ana.sh` | passed | 0 | 0.5s | `example_run_logs/20260515_145459/02_01.GettingStarted_1.ana.sh.log` |  |
| 3 | `02.ReplicaExchangeSimulation` | `python run.py` | passed | 0 | 1m 13s | `example_run_logs/20260515_145459/03_02.ReplicaExchangeSimulation_run.py.log` |  |
| 4 | `04.HDX` | `python 0.run.py` | passed | 0 | 20h 25m 57s | `example_run_logs/20260515_145459/04_04.HDX_0.run.py.log` |  |
| 5 | `04.HDX` | `python 1.config.py` | passed | 0 | 2.4s | `example_run_logs/20260515_145459/05_04.HDX_1.config.py.log` |  |
| 6 | `04.HDX` | `bash 2.traj_ana.sh` | passed | 0 | 27.2s | `example_run_logs/20260515_145459/06_04.HDX_2.traj_ana.sh.log` |  |
| 7 | `04.HDX` | `bash 3.get_protaction_states.sh` | passed | 0 | 1m 22s | `example_run_logs/20260515_145459/07_04.HDX_3.get_protaction_states.sh.log` |  |
| 8 | `04.HDX` | `python 4.calc_HDX.py` | passed | 0 | 2m 35s | `example_run_logs/20260515_145459/08_04.HDX_4.calc_HDX.py.log` |  |
| 9 | `05.Advanced_config.py` | `bash 0.run.sh` | passed | 0 | 8.8s | `example_run_logs/20260515_145459/09_05.Advanced_config.py_0.run.sh.log` |  |
| 10 | `05.Advanced_config.py` | `bash 1.ana.sh` | passed | 0 | 0.7s | `example_run_logs/20260515_145459/10_05.Advanced_config.py_1.ana.sh.log` |  |
| 11 | `06.PullingSimulation` | `python 0.run.py` | passed | 0 | 2h 7m 56s | `example_run_logs/20260515_145459/11_06.PullingSimulation_0.run.py.log` |  |
| 12 | `06.PullingSimulation` | `python 1.get_force.py` | failed | 1 | 1.0s | `example_run_logs/20260515_145459/12_06.PullingSimulation_1.get_force.py.log` | Later commands in this example are skipped. |
| 13 | `07.MoreRestraints` | `python 0.run.py` | passed | 0 | 1m 6s | `example_run_logs/20260515_145459/13_07.MoreRestraints_0.run.py.log` |  |
| 14 | `08.MembraneSimulation` | `python 0.normal.run.py` | passed | 0 | 2h 7m 16s | `example_run_logs/20260515_145459/14_08.MembraneSimulation_0.normal.run.py.log` |  |
| 15 | `08.MembraneSimulation` | `python 1.channel.run.py` | passed | 0 | 3h 50m 59s | `example_run_logs/20260515_145459/15_08.MembraneSimulation_1.channel.run.py.log` |  |
| 16 | `08.MembraneSimulation` | `python 2.lateral_pressure.run.py` | passed | 0 | 3h 41m 56s | `example_run_logs/20260515_145459/16_08.MembraneSimulation_2.lateral_pressure.run.py.log` |  |
| 17 | `08.MembraneSimulation` | `python 3.fixed_curvature.run.py` | passed | 0 | 52m 39s | `example_run_logs/20260515_145459/17_08.MembraneSimulation_3.fixed_curvature.run.py.log` |  |
| 18 | `08.MembraneSimulation` | `python 4.curvature_dynamics1.run.py` | passed | 0 | 2h 45m 60s | `example_run_logs/20260515_145459/18_08.MembraneSimulation_4.curvature_dynamics1.run.py.log` |  |
| 19 | `08.MembraneSimulation` | `python 5.curvature_dynamics2.run.py` | passed | 0 | 2h 35m 17s | `example_run_logs/20260515_145459/19_08.MembraneSimulation_5.curvature_dynamics2.run.py.log` |  |
| 20 | `09.IsomerizationPRO` | `python 0.run.py` | passed | 0 | 14m 31s | `example_run_logs/20260515_145459/20_09.IsomerizationPRO_0.run.py.log` |  |
| 21 | `09.IsomerizationPRO` | `python recal_omega.py` | failed | 1 | 0.3s | `example_run_logs/20260515_145459/21_09.IsomerizationPRO_recal_omega.py.log` | Later commands in this example are skipped. |
| 22 | `09.IsomerizationPRO` | `python recal_potential.py` | skipped |  | 0.0s |  | Skipped because earlier command failed: python recal_omega.py |
| 23 | `09.IsomerizationPRO` | `python plot_two_wall.py` | skipped |  | 0.0s |  | Skipped because earlier command failed: python recal_omega.py |
| 24 | `10.SelfAvoidRandomWalk` | `python run.py` | passed | 0 | 19m 46s | `example_run_logs/20260515_145459/24_10.SelfAvoidRandomWalk_run.py.log` |  |
| 25 | `12.MultistepIntegrator` | `python 0.run.py` | passed | 0 | 32.7s | `example_run_logs/20260515_145459/25_12.MultistepIntegrator_0.run.py.log` |  |
| 26 | `12.MultistepIntegrator` | `bash 1.ana.sh` | failed | 1 | 0.6s | `example_run_logs/20260515_145459/26_12.MultistepIntegrator_1.ana.sh.log` | Later commands in this example are skipped. |
| 27 | `13.RestartSimulation` | `python 0.run.py` | passed | 0 | 12.7s | `example_run_logs/20260515_145459/27_13.RestartSimulation_0.run.py.log` |  |
| 28 | `13.RestartSimulation` | `python 0.continue.py` | passed | 0 | 5.2s | `example_run_logs/20260515_145459/28_13.RestartSimulation_0.continue.py.log` |  |
| 29 | `15.SpatialTransformation` | `bash 0.run.sh` | passed | 0 | 8.3s | `example_run_logs/20260515_145459/29_15.SpatialTransformation_0.run.sh.log` |  |
| 30 | `15.SpatialTransformation` | `bash 1.ana.sh` | passed | 0 | 0.3s | `example_run_logs/20260515_145459/30_15.SpatialTransformation_1.ana.sh.log` |  |

## Artifacts

### 01.GettingStarted

- `example/01.GettingStarted/inputs`: 4 files, 1588434 bytes
- `example/01.GettingStarted/outputs`: 2 files, 1648369 bytes
- `example/01.GettingStarted/results`: 2 files, 21923 bytes
- Notable file counts: `{".log": 2, ".npy": 1, ".rmsd": 1, ".up": 2, ".vtf": 1}`

### 02.ReplicaExchangeSimulation

- `example/02.ReplicaExchangeSimulation/inputs`: 4 files, 1588498 bytes
- `example/02.ReplicaExchangeSimulation/outputs`: 8 files, 13632100 bytes
- Notable file counts: `{".log": 1, ".npy": 1, ".up": 9}`

### 04.HDX

- `example/04.HDX/inputs`: 5 files, 6345237 bytes
- `example/04.HDX/outputs`: 16 files, 131090212 bytes
- `example/04.HDX/results`: 113 files, 136647680 bytes
- Notable file counts: `{".npy": 97, ".up": 18, ".vtf": 16}`

### 05.Advanced_config.py

- `example/05.Advanced_config.py/inputs`: 4 files, 1606154 bytes
- `example/05.Advanced_config.py/outputs`: 2 files, 1666068 bytes
- `example/05.Advanced_config.py/results`: 2 files, 21896 bytes
- Notable file counts: `{".log": 1, ".npy": 1, ".rmsd": 1, ".up": 2, ".vtf": 1}`

### 06.PullingSimulation

- `example/06.PullingSimulation/inputs`: 4 files, 13105078 bytes
- `example/06.PullingSimulation/outputs`: 8 files, 116021180 bytes
- Notable file counts: `{".dat": 2, ".npy": 1, ".up": 9}`

### 07.MoreRestraints

- `example/07.MoreRestraints/inputs`: 4 files, 5069923 bytes
- `example/07.MoreRestraints/outputs`: 2 files, 5205958 bytes
- Notable file counts: `{".dat": 5, ".log": 1, ".npy": 1, ".up": 2}`

### 08.MembraneSimulation

- `example/08.MembraneSimulation/inputs`: 18 files, 23008696 bytes
- `example/08.MembraneSimulation/outputs`: 36 files, 439595708 bytes
- Notable file counts: `{".dat": 3, ".npy": 4, ".up": 40}`

### 09.IsomerizationPRO

- `example/09.IsomerizationPRO/inputs`: 4 files, 12563063 bytes
- `example/09.IsomerizationPRO/outputs`: 2 files, 13929918 bytes
- Notable file counts: `{".dat": 1, ".log": 1, ".npy": 1, ".up": 2}`

### 10.SelfAvoidRandomWalk

- `example/10.SelfAvoidRandomWalk/inputs`: 4 files, 4133940 bytes
- `example/10.SelfAvoidRandomWalk/outputs`: 8 files, 43171431 bytes
- Notable file counts: `{".npy": 1, ".up": 9}`

### 12.MultistepIntegrator

- `example/12.MultistepIntegrator/inputs`: 5 files, 2626154 bytes
- `example/12.MultistepIntegrator/outputs`: 2 files, 2744572 bytes
- `example/12.MultistepIntegrator/results`: 1 files, 59 bytes
- Notable file counts: `{".log": 1, ".npy": 1, ".rmsd": 1, ".up": 2}`

### 13.RestartSimulation

- `example/13.RestartSimulation/inputs`: 4 files, 1591322 bytes
- `example/13.RestartSimulation/outputs`: 1 files, 3533636 bytes
- Notable file counts: `{".npy": 1, ".up": 2}`

### 15.SpatialTransformation

- `example/15.SpatialTransformation/inputs`: 4 files, 1588498 bytes
- `example/15.SpatialTransformation/outputs`: 2 files, 1647947 bytes
- `example/15.SpatialTransformation/results`: 2 files, 22125 bytes
- Notable file counts: `{".log": 1, ".npy": 1, ".rmsd": 1, ".up": 2, ".vtf": 1}`

## Data-Flow Verification

HDF5 inspection return code: `0`.

| File | /input | /output | Interesting Datasets | Numeric Check |
|---|---:|---:|---|---|
| `example/01.GettingStarted/inputs/chig.up` | True | False | 123 matched | non-finite values present |
| `example/01.GettingStarted/outputs/simple_test/chig.run.up` | True | True | 134 matched | non-finite values present |
| `example/02.ReplicaExchangeSimulation/inputs/chig.up` | True | False | 123 matched | non-finite values present |
| `example/02.ReplicaExchangeSimulation/outputs/REMD/chig.run.0.up` | True | True | 134 matched | non-finite values present |
| `example/02.ReplicaExchangeSimulation/outputs/REMD/chig.run.1.up` | True | True | 134 matched | non-finite values present |
| `example/02.ReplicaExchangeSimulation/outputs/REMD/chig.run.2.up` | True | True | 134 matched | non-finite values present |
| `example/02.ReplicaExchangeSimulation/outputs/REMD/chig.run.3.up` | True | True | 134 matched | non-finite values present |
| `example/02.ReplicaExchangeSimulation/outputs/REMD/chig.run.4.up` | True | True | 134 matched | non-finite values present |
| `example/02.ReplicaExchangeSimulation/outputs/REMD/chig.run.5.up` | True | True | 134 matched | non-finite values present |
| `example/02.ReplicaExchangeSimulation/outputs/REMD/chig.run.6.up` | True | True | 134 matched | non-finite values present |
| `example/02.ReplicaExchangeSimulation/outputs/REMD/chig.run.7.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/inputs/EHEE_rd2_0005-HDX.up` | True | False | 130 matched | non-finite values present |
| `example/04.HDX/inputs/EHEE_rd2_0005.up` | True | False | 123 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.0.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.1.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.10.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.11.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.12.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.13.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.14.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.15.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.2.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.3.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.4.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.5.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.6.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.7.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.8.up` | True | True | 134 matched | non-finite values present |
| `example/04.HDX/outputs/REMD/EHEE_rd2_0005.run.9.up` | True | True | 134 matched | non-finite values present |
| `example/05.Advanced_config.py/inputs/chig.up` | True | False | 127 matched | non-finite values present |
| `example/05.Advanced_config.py/outputs/simple_test/chig.run.up` | True | True | 138 matched | non-finite values present |
| `example/06.PullingSimulation/inputs/1qhj.up` | True | False | 143 matched | non-finite values present |
| `example/06.PullingSimulation/outputs/pulling_test/1qhj.run.0.up` | True | True | 156 matched | non-finite values present |
| `example/06.PullingSimulation/outputs/pulling_test/1qhj.run.1.up` | True | True | 156 matched | non-finite values present |
| `example/06.PullingSimulation/outputs/pulling_test/1qhj.run.2.up` | True | True | 156 matched | non-finite values present |
| `example/06.PullingSimulation/outputs/pulling_test/1qhj.run.3.up` | True | True | 156 matched | non-finite values present |
| `example/06.PullingSimulation/outputs/pulling_test/1qhj.run.4.up` | True | True | 156 matched | non-finite values present |
| `example/06.PullingSimulation/outputs/pulling_test/1qhj.run.5.up` | True | True | 156 matched | non-finite values present |
| `example/06.PullingSimulation/outputs/pulling_test/1qhj.run.6.up` | True | True | 156 matched | non-finite values present |
| `example/06.PullingSimulation/outputs/pulling_test/1qhj.run.7.up` | True | True | 156 matched | non-finite values present |
| `example/07.MoreRestraints/inputs/1UBQ.up` | True | False | 130 matched | non-finite values present |
| `example/07.MoreRestraints/outputs/simple_test/1UBQ.run.up` | True | True | 141 matched | non-finite values present |
| `example/08.MembraneSimulation/inputs/1qhj.up` | True | False | 146 matched | non-finite values present |
| `example/08.MembraneSimulation/inputs/1rkl.up` | True | False | 136 matched | non-finite values present |
| `example/08.MembraneSimulation/inputs/three_1rkl_a.up` | True | False | 140 matched | non-finite values present |
| `example/08.MembraneSimulation/inputs/three_1rkl_b.up` | True | False | 140 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/channel_test/1qhj.run.0.up` | True | True | 155 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/channel_test/1qhj.run.1.up` | True | True | 155 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/channel_test/1qhj.run.2.up` | True | True | 155 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/channel_test/1qhj.run.3.up` | True | True | 155 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/channel_test/1qhj.run.4.up` | True | True | 155 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/channel_test/1qhj.run.5.up` | True | True | 155 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/channel_test/1qhj.run.6.up` | True | True | 155 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/channel_test/1qhj.run.7.up` | True | True | 155 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/curv_dy1/three_1rkl_a.run.0.up` | True | True | 151 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/curv_dy1/three_1rkl_a.run.1.up` | True | True | 151 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/curv_dy1/three_1rkl_a.run.2.up` | True | True | 151 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/curv_dy1/three_1rkl_a.run.3.up` | True | True | 151 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/curv_dy2/three_1rkl_b.run.0.up` | True | True | 151 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/curv_dy2/three_1rkl_b.run.1.up` | True | True | 151 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/curv_dy2/three_1rkl_b.run.2.up` | True | True | 151 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/curv_dy2/three_1rkl_b.run.3.up` | True | True | 151 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/fixed_curv/1rkl.run.0.up` | True | True | 147 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/fixed_curv/1rkl.run.1.up` | True | True | 147 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/fixed_curv/1rkl.run.2.up` | True | True | 147 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/fixed_curv/1rkl.run.3.up` | True | True | 147 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/lateral_test/1qhj.run.0.up` | True | True | 157 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/lateral_test/1qhj.run.1.up` | True | True | 157 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/lateral_test/1qhj.run.2.up` | True | True | 157 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/lateral_test/1qhj.run.3.up` | True | True | 157 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/lateral_test/1qhj.run.4.up` | True | True | 157 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/lateral_test/1qhj.run.5.up` | True | True | 157 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/lateral_test/1qhj.run.6.up` | True | True | 157 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/lateral_test/1qhj.run.7.up` | True | True | 157 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/memb_test/1qhj.run.0.up` | True | True | 147 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/memb_test/1qhj.run.1.up` | True | True | 147 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/memb_test/1qhj.run.2.up` | True | True | 147 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/memb_test/1qhj.run.3.up` | True | True | 147 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/memb_test/1qhj.run.4.up` | True | True | 147 matched | non-finite values present |
| `example/08.MembraneSimulation/outputs/memb_test/1qhj.run.5.up` | True | True | 147 matched | non-finite values present |

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

- Total measured command wall time: 39h 10m 19s.
- Completed commands: 25 / 30.
- Failed or interrupted commands: 3.

| Example | Command | Elapsed | Status |
|---|---|---:|---|
| `04.HDX` | `python 0.run.py` | 20h 25m 57s | passed |
| `08.MembraneSimulation` | `python 1.channel.run.py` | 3h 50m 59s | passed |
| `08.MembraneSimulation` | `python 2.lateral_pressure.run.py` | 3h 41m 56s | passed |
| `08.MembraneSimulation` | `python 4.curvature_dynamics1.run.py` | 2h 45m 60s | passed |
| `08.MembraneSimulation` | `python 5.curvature_dynamics2.run.py` | 2h 35m 17s | passed |
| `06.PullingSimulation` | `python 0.run.py` | 2h 7m 56s | passed |
| `08.MembraneSimulation` | `python 0.normal.run.py` | 2h 7m 16s | passed |
| `08.MembraneSimulation` | `python 3.fixed_curvature.run.py` | 52m 39s | passed |

Elapsed times are machine-specific and include setup, simulation, analysis, and Python startup overhead. For coarse throughput, inspect each command log for progress lines and compare elapsed time against generated frame counts in the corresponding `.up` files.
