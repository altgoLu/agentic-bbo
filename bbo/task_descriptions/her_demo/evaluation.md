# Evaluation

- Dataset: bundled copy of `examples/HER/HER_virtual_data.csv` from `zwyu-ai/BO-Tutorial-for-Sci`
- Preprocessing: replace `Target` with `Target.max() - Target`
- Oracle: `RandomForestRegressor(n_estimators=100, random_state=<seed>)`
- Primary objective: `regret` with direction `minimize`
- Smoke budget: 3 random-search evaluations for the required demo command
- Standard outputs: append-only JSONL history, run summary JSON, and generic trace/distribution plots
