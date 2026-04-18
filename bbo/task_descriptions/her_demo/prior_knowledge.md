# Domain Prior Knowledge

The ten inputs correspond to catalyst additives, dyes, surfactants, salts, and related composition controls included in the tutorial HER dataset:

- `AcidRed871_0gL`, `MethyleneB_250mgL`, and `RhodamineB1_0gL` are dye-like additives.
- `L-Cysteine-50gL` can act as a sulfur-containing additive.
- `NaCl-3M` and `NaOH-1M` change the ionic or alkaline environment.
- `P10-MIX1` is the primary catalyst-composition control in this dataset.
- `PVP-1wt`, `SDS-1wt`, and `Sodiumsilicate-1wt` act as stabilizing or interfacial additives.

For this smoke benchmark, treat these notes as weak priors only.
The benchmark does not claim mechanistic causality beyond what is encoded in the tutorial data and the fitted random-forest oracle.
