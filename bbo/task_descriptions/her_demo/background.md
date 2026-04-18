# Background

`her_demo` models catalyst-composition optimization for photocatalytic hydrogen evolution reaction (HER) in water-splitting experiments.
The task is based on the HER case study in *Efficient and Principled Scientific Discovery through Bayesian Optimization: A Tutorial* and uses the tutorial repository's virtual HER dataset as a lightweight benchmark proxy.

The benchmark objective is not to execute a real chemistry workflow.
Instead, it exposes a reproducible mock oracle trained on the tutorial data so optimizers can interact with a scientifically motivated search space through the standard ask/evaluate/tell protocol.
