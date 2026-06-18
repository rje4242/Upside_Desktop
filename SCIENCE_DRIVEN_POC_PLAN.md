# Science-Driven PoC Plan With Answer-Key Definitions

## Summary

This proof of concept starts from experimentally known or strongly
precedent-backed biological answers, then tests whether the workflow can
rediscover or extend them. The schedule is organized around target-specific
mechanisms rather than a generic simulation pipeline.

The realistic single-person scope is:

- **Weeks 1-8:** answer-key definition, structure curation, and baseline
  controls.
- **Weeks 9-24:** computational recovery of the strongest answer keys.
- **Weeks 25-40:** expansion to harder oncology and interface targets.
- **Weeks 41-52:** robustness, falsification, and an experiment-ready
  validation package.

Wet-lab force validation is a follow-on unless an established
force-spectroscopy platform is already available.

## Answer-Key Definitions

### 1. KRAS G12C: Switch-II Cryptic Pocket

| Field | Definition |
| --- | --- |
| Known answer | The switch-II pocket exploited by covalent KRAS G12C inhibitors including sotorasib and adagrasib. |
| Why it is a good answer key | It is the clearest positive control for a hidden or allosteric cancer pocket that became druggable. |
| Site definition | KRAS G12C pocket adjacent to switch-II; include local geometry around Cys12 and switch-II residues, with H95/Y96 treated as important specificity-sensitive residues. |
| Success criterion | Blind-ranked top 3-5 candidate overlaps the known switch-II pocket in folded KRAS conformations. |
| Failure criterion | Pocket appears only in globally unfolded or nonspecifically expanded structures. |
| Evidence | [PubMed 39283696](https://pubmed.ncbi.nlm.nih.gov/39283696/), [PubMed 40391409](https://pubmed.ncbi.nlm.nih.gov/40391409/) |

### 2. PI3K-alpha / PIK3CA: RLY-2608 / Zovegalisib-Class Allosteric State

| Field | Definition |
| --- | --- |
| Known answer | An allosteric, mutant-selective PI3K-alpha inhibitory mechanism distinct from ordinary ATP-site recovery. |
| Why it is a good answer key | It tests whether the workflow can find a disease-relevant conformational or allosteric state, not just a visible orthosteric pocket. |
| Site/state definition | Allosteric state coupled to oncogenic or secondary resistance PIK3CA mutations; exclude ATP-site-only hits from success. |
| Success criterion | Predicted state/site gives a plausible structural explanation for mutant selectivity or resistance escape. |
| Failure criterion | Workflow only rediscovers the ATP pocket or generic kinase clefts. |
| Evidence | [PubMed 37916958](https://pubmed.ncbi.nlm.nih.gov/37916958/), [PubMed 40829787](https://pubmed.ncbi.nlm.nih.gov/40829787/) |

### 3. MYC / OMO-103: Interaction-Surface Disruption

| Field | Definition |
| --- | --- |
| Known answer | OMO-103 targets MYC biology through a miniprotein strategy rather than a conventional small-molecule cryptic pocket. |
| Why it is useful | It forces the workflow to distinguish pocket discovery from interface-state discovery. |
| Site/state definition | MYC/MAX or MYC interaction-surface region compatible with miniprotein disruption. |
| Success criterion | Ranked hypothesis maps to a known or plausible MYC interaction surface. |
| Failure criterion | Only nonspecific hydrophobic patches are identified. |
| Evidence | [PubMed 38321218](https://pubmed.ncbi.nlm.nih.gov/38321218/) |

### 4. Talin-Vinculin: Force-Exposed Vinculin-Binding Sites

| Field | Definition |
| --- | --- |
| Known answer | Talin mechanical stretching exposes vinculin-binding sites. |
| Why it is the best force positive control | Force-dependent exposure has strong single-molecule and cellular precedent. |
| Site/state definition | Talin rod helix-bundle opening that exposes vinculin-binding helices. |
| Success criterion | Pulling exposes the expected vinculin-binding region in a direction-specific way, absent or reduced in sham/wrong-direction controls. |
| Failure criterion | Exposure requires complete unfolding or appears equally in control pulls. |
| Evidence | [PubMed 34463480](https://pubmed.ncbi.nlm.nih.gov/34463480/), [PubMed 31897422](https://pubmed.ncbi.nlm.nih.gov/31897422/), [PubMed 22205879](https://pubmed.ncbi.nlm.nih.gov/22205879/) |

### 5. Latent TGF-beta1: Force-Sensitized Activation

| Field | Definition |
| --- | --- |
| Known answer | Integrin/ECM-applied force can activate latent TGF-beta by mechanically perturbing the latent complex. |
| Why it matters for fibrous cancers | TGF-beta activation is tightly linked to fibrotic matrix, stiffness, invasion, and tumor microenvironment remodeling. |
| Site/state definition | Force-dependent opening or destabilization of the latent LAP/TGF-beta cage under biologically relevant integrin-to-matrix pulling geometry. |
| Success criterion | Directional force exposes an activation-compatible state before nonspecific rupture. |
| Failure criterion | Only total disruption or non-directional unfolding is observed. |
| Evidence | [PubMed 25332161](https://pubmed.ncbi.nlm.nih.gov/25332161/), [PubMed 22169532](https://pubmed.ncbi.nlm.nih.gov/22169532/), [PubMed 18342983](https://pubmed.ncbi.nlm.nih.gov/18342983/) |

## Secondary Prospective Answers

### FAK / PTK2 Autoinhibition

- **Mechanistic hypothesis:** focal-adhesion force shifts FERM-kinase
  autoinhibited states.
- **Use:** only after talin/TGF-beta controls succeed.
- **Readouts:** FRET between FERM and kinase domains, phosphorylation, and
  stiffness-dependent inhibitor sensitivity.
- **Evidence tier:** plausible mechanotransduction target, weaker direct
  force-pocket precedent.

### DDR1 / Collagen-Rich Matrix Signaling

- **Mechanistic hypothesis:** collagen-rich fibrotic matrix stabilizes receptor
  states that expose regulatory or druggable regions.
- **Use:** exploratory year-2 target.
- **Readouts:** collagen-dependent receptor phosphorylation, HDX-MS/FRET, and
  matrix-stiffness response.
- **Evidence tier:** fibrotic cancer relevance is strong; direct force-opened
  pocket evidence is weaker.

## Precedent-Based Timeline

### Weeks 1-8: Answer-Key Lock

- Curate structures, constructs, mutations, known-positive residues, and
  withheld labels.
- Define exact success/failure rules for KRAS, PI3K-alpha, MYC, talin, and
  latent TGF-beta.
- Run static baselines: apo pocket detection, reconstructed apo controls, known
  holo/interface controls, and PocketMiner-style priors.
- Output: frozen answer-key table and baseline report.

### Weeks 9-16: Strongest Computational Positives

- Run KRAS G12C unrestrained sampling and folded-frame filtering.
- Run one force-positive control: talin or latent TGF-beta.
- Reconstruct representative frames and rank candidates blind.
- Gate: continue only if KRAS or the force-positive control shows a specific,
  non-unfolding signal.

### Weeks 17-24: Second Force Control and KRAS Robustness

- Add the second force-positive control.
- Add KRAS seed replication and reconstruction/minimization sensitivity checks.
- Compare simulation-derived candidates against no-simulation baselines.
- Output: first validated computational recovery package.

### Weeks 25-32: PI3K-alpha and MYC

- Add PI3K-alpha allosteric-state analysis.
- Add MYC interface-state analysis.
- Keep their success definitions distinct: PI3K is allosteric-state recovery;
  MYC is interface recovery.
- Output: expanded oncology answer-key benchmark.

### Weeks 33-40: Falsification and Prioritization

- Run parameter sensitivity and detector robustness checks.
- Classify failures as sampling miss, reconstruction artifact, detector miss,
  global unfolding, or weak biology.
- Select no more than three candidates for experimental follow-up.

### Weeks 41-52: Experiment-Ready Validation Package

Produce assay cards for top candidates:

- KRAS: HDX-MS, fragment/covalent probe, or biochemical stabilization around
  switch-II.
- Talin: force-extension plus vinculin-binding assay.
- Latent TGF-beta: force/FRET or activation reporter.
- PI3K-alpha: mutant-selective allosteric-state assay.
- MYC: interaction disruption or miniprotein-competition assay.

FAK and DDR1 remain follow-on targets unless core answer keys pass.

## Key Constraints

- UPSIDE screening frequency is not an equilibrium opening probability.
- REMD state trajectories are ensembles, not continuous kinetic paths.
- Pulling simulations are hypothesis-driven perturbations, not unbiased pocket
  discovery.
- AI can rank or enrich hypotheses but cannot replace missing structural
  evidence.
- Quantum methods may refine energetics after a site exists, but do not solve
  rare conformational discovery.

## Acceptance Criteria

- KRAS switch-II pocket recovered in top 3-5 blind candidates.
- PI3K-alpha result is allosteric/mutant-selective, not ATP-site-only.
- MYC result maps to an interaction surface, not a generic patch.
- Talin and TGF-beta force states are direction-specific and control-sensitive.
- At least three final candidates have residue-level predictions and feasible
  experimental readouts.
