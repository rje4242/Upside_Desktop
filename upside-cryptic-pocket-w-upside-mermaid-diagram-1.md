flowchart TD
    A["Input protein<br/>Prefer apo PDB for blind discovery"] --> B{"Audit input"}
    B --> B1["Choose biological assembly + chains"]
    B --> B2["Check missing residues, chain breaks,<br/>cofactors, metals, membrane context"]
    B1 --> C
    B2 --> C

    C["Prepare Upside input<br/>PDB_to_initial_structure.py<br/>standard amino acids only"] --> D["Apo control<br/>Run reconstruction + pocket scoring<br/>before simulation"]

    C --> E["Cheap baseline<br/>PocketMiner + fpocket on starting apo"]
    E --> F["Define candidate regions<br/>Do not discard other sites"]

    F --> G{"Pilot stressed Upside sampling<br/>REMD temperature ladder<br/>multiple seeds"}
    G -->|Fold unfolds globally| G1["Recalibrate ladder<br/>lower or narrow temperature range"]
    G1 --> G

    G -->|Fold intact + local rearrangement| H["Production Upside REMD<br/>temperature-stressed ensemble<br/>unrestrained default"]

    H --> I["Extract frames<br/>RMSD, radius of gyration,<br/>energy, H-bonds, temperature"]
    I --> J{"Folded-state filter"}
    J -->|Reject| J1["Discard global unfolding,<br/>chain separation, severe distortion"]
    J -->|Accept| K["Cluster accepted frames<br/>core CA RMSD or region features"]

    K --> L["Select cluster representatives<br/>keep seed, state, frame,<br/>cluster weight"]
    L --> M["Atomistic reconstruction<br/>restore backbone, side chains,<br/>cofactors, protonation, membrane context"]
    M --> N["Restrained local minimization<br/>same pipeline for apo control"]

    N --> O{"Quality gate"}
    O -->|Fails| O1["Reject artifacts<br/>clashes, bad geometry,<br/>large minimization drift"]
    O -->|Passes| P["Pocket detection<br/>fpocket per structure<br/>MDpocket across ensemble"]

    P --> Q["Consolidate pockets<br/>merge by lining residues,<br/>center proximity, volume overlap"]
    Q --> R["Rank candidate cryptic pockets"]

    R --> R1["Apo novelty"]
    R --> R2["Seed / temperature reproducibility"]
    R --> R3["Pocket volume + druggability"]
    R --> R4["Folded-cluster support"]
    R --> R5["PocketMiner agreement"]
    R --> R6["Robustness to reconstruction,<br/>minimization, detector settings"]

    R1 --> S["Candidate table<br/>Pocket ID, lining residues,<br/>representative structure,<br/>volume, score, frequency,<br/>evidence class, quality flags"]
    R2 --> S
    R3 --> S
    R4 --> S
    R5 --> S
    R6 --> S

    S --> T{"Retrospective validation"}
    T --> T1["Freeze ranking before holo reveal"]
    T1 --> T2["Reveal holo structure<br/>ligand removed for pocket detection"]
    T2 --> T3["Measure residue overlap,<br/>center distance, rank"]

    T3 -->|Recovered in top candidates| U["Validated workflow candidate<br/>Proceed to prospective use"]
    T3 -->|Missed or artifact-only| V["Diagnose failure<br/>sampling, reconstruction,<br/>detector, ranking, or fold filter"]
    V --> G