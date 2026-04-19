# Surrogate assets

If `joblib.load` fails with **`EOF` / `reading array data`**, the file on disk is **incomplete** (partial copy, or Git LFS not pulled). Replace it with the full file from KnobsTuningEA.

Each `*.joblib` is a **serialized sklearn surrogate** (RF, etc.) trained in KnobsTuningEA: it maps normalized knob vectors → predicted metric (throughput or latency). Names indicate workload: **Sysbench/MySQL** (`RF_SYSBENCH_*`, `SYSBENCH_all`), **JOB** (`RF_JOB_*`, `JOB_all`), **PostgreSQL** (`pg_5`, `pg_20`). Matching `knobs_*.json` in this folder defines the search space.

Large `*.joblib` checkpoints from KnobsTuningEA are **not** committed. Copy them from:

`KnobsTuningEA/autotune/tuning_benchmark/surrogate/`

into **`bbo/tasks/surrogate/assets/`** using the filenames below (or set the env override).

## Joblib files ↔ benchmark `task_id`

| Copy this file | `task_id` | Env override (optional) |
|----------------|-----------|-------------------------|
| `RF_SYSBENCH_5knob.joblib` | `knob_surrogate_sysbench_5` | `AGENTIC_BBO_SYSBENCH5_SURROGATE` |
| `SYSBENCH_all.joblib` | `knob_surrogate_sysbench_all` | `AGENTIC_BBO_SYSBENCH_ALL_SURROGATE` |
| `RF_JOB_5knob.joblib` | `knob_surrogate_job_5` | `AGENTIC_BBO_JOB5_SURROGATE` |
| `JOB_all.joblib` | `knob_surrogate_job_all` | `AGENTIC_BBO_JOB_ALL_SURROGATE` |
| `pg_5.joblib` | `knob_surrogate_pg_5` | `AGENTIC_BBO_PG5_SURROGATE` |
| `pg_20.joblib` | `knob_surrogate_pg_20` | `AGENTIC_BBO_PG20_SURROGATE` |

Sysbench 5 also accepts a tiny placeholder from `python -m bbo.tasks.surrogate.build_placeholder_surrogate` (`sysbench_5knob_surrogate.joblib`).

## Bundled knobs JSON

Subset files are under this folder (generated from KnobsTuningEA knob specs). Full list: `bbo/tasks/surrogate/catalog.py` → `default_knobs_json_filename` per benchmark.

## Tests / demo

```bash
uv sync --extra dev --extra surrogate
uv run pytest tests/test_surrogate_task_smoke.py tests/test_surrogate_knob_space.py -v
uv run python examples/run_knob_surrogate_demo.py
```

Use `create_surrogate_task("<task_id>")` from `bbo.tasks`.
