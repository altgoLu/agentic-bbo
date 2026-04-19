# Environment Setup

Install optional surrogate dependencies:

```bash
uv sync --extra dev --extra surrogate
```

Generate the small default `sysbench_5knob_surrogate.joblib` next to the bundled knobs JSON (required once per clone unless you copy a `.joblib` yourself):

```bash
uv run python -m bbo.tasks.surrogate.build_placeholder_surrogate
```

To use a **full** RF checkpoint (e.g. copied from KnobsTuningEA):

**Option A — copy into assets (no env var):**

```text
cp <KnobsTuningEA>/autotune/tuning_benchmark/surrogate/RF_SYSBENCH_5knob.joblib \
   <agentic-bbo>/bbo/tasks/surrogate/assets/RF_SYSBENCH_5knob.joblib
```

**Option B — any path:**

```bash
export AGENTIC_BBO_SYSBENCH5_SURROGATE=/absolute/path/to/RF_SYSBENCH_5knob.joblib
```

See also `bbo/tasks/surrogate/assets/README.md`.

No MySQL instance or live Sysbench run is required; evaluation is surrogate-only.
