# Background

This benchmark optimizes a **surrogate model** of database throughput under Sysbench-style workloads.
The original data and training pipeline come from the KnobsTuningEA research codebase; this repository **re-implements** only the evaluation path (joblib RF + knob decoding) so runs do not require that checkout.

The optimizer proposes normalized knob coordinates in `[0, 1]^d`; the task decodes them to physical MySQL knob values and returns the surrogate's predicted objective (higher is better).
