flowchart TD
    A[Input protein structure<br/>Apo preferred for blind discovery] --> B[Prepare + audit input<br/>Assembly, chains, missing residues,<br/>cofactors, metals, membrane context]
    B --> C[Convert to Upside input<br/>PDB_to_initial_structure.py<br/>standard amino acids only]
    C --> D[Baseline controls<br/>PocketMiner on apo<br/>fpocket/MDpocket on apo<br/>reconstruction/minimization control]

    D --> E[Upside stressed sampling<br/>Pilot REMD ladder<br/>multiple seeds<br/>folded-state stress, not unfolding]
    E --> F{Sampling acceptable?}
    F -- No --> G[Recalibrate<br/>temperature range, duration,<br/>frame interval, fold filters]
    G --> E
    F -- Yes --> H[Production Upside REMD<br/>save seed, state, frame,<br/>restart history, config]

    H --> I[Extract frames<br/>Use Upside trajectory tools<br/>analyze state ensembles only<br/>no kinetic rates from REMD adjacency]
    I --> J[Filter folded frames<br/>core CA RMSD<br/>radius of gyration<br/>native contacts<br/>secondary structure<br/>chain integrity]
    J --> K[Cluster intact frames<br/>core CA RMSD or pocket-region features<br/>choose representatives from populated clusters]

    K --> L[Atomistic reconstruction<br/>full backbone + side chains<br/>restore cofactors/metals/context]
    L --> M[Restrained local minimization<br/>same protocol for apo control<br/>reject clashes or large backbone drift]

    M --> N[Pocket detection<br/>fpocket per structure<br/>MDpocket across ensemble]
    N --> O[Consolidate sites<br/>merge by lining-residue overlap<br/>pocket center / volume overlap<br/>manual audit of splits/merges]

    O --> P[Rank cryptic-pocket candidates<br/>apo novelty<br/>reproducibility<br/>pocket quality<br/>folded-cluster support<br/>PocketMiner agreement<br/>robustness]

    P --> Q[Candidate table<br/>Pocket ID<br/>lining residues<br/>representative structure<br/>volume + score<br/>screening frequency<br/>seed/state/cluster support<br/>quality flags]

    Q --> R[Retrospective validation<br/>freeze ranks first<br/>then reveal holo structure]
    R --> S{Known holo pocket recovered<br/>in top candidates?}
    S -- Yes --> T[Workflow passes benchmark<br/>Use prospectively as candidate generator]
    S -- No --> U[Diagnose failure<br/>sampling too short<br/>opening only unfolded<br/>reconstruction closes pocket<br/>detector misses site<br/>false positives dominate]

    classDef input fill:#0b1220,stroke:#60a5fa,color:#e5e7eb
    classDef sim fill:#111827,stroke:#a78bfa,color:#e5e7eb
    classDef filter fill:#172554,stroke:#38bdf8,color:#e5e7eb
    classDef rank fill:#312e81,stroke:#c4b5fd,color:#e5e7eb
    classDef validate fill:#064e3b,stroke:#34d399,color:#e5e7eb
    classDef fail fill:#7f1d1d,stroke:#f87171,color:#fee2e2

    class A,B,C,D input
    class E,F,G,H sim
    class I,J,K,L,M,N,O filter
    class P,Q rank
    class R,S,T validate
    class U fail