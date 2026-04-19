"""Smoke tests for ``bbo.run`` CLI helpers (no plotting)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from bbo.run import run_single_experiment


@pytest.mark.unit
def test_run_single_experiment_writes_jsonl_and_summary(tmp_path: Path) -> None:
    summary = run_single_experiment(
        task_name="branin_demo",
        algorithm_name="random_search",
        seed=3,
        max_evaluations=10,
        results_root=tmp_path,
        resume=False,
    )
    results_jsonl = Path(summary["results_jsonl"])
    assert results_jsonl.exists()
    assert results_jsonl.stat().st_size > 0
    summary_path = results_jsonl.parent / "summary.json"
    assert summary_path.exists()
    data = json.loads(summary_path.read_text(encoding="utf-8"))
    assert data["trial_count"] == 10
    assert "plot_paths" not in data and "plot_paths" not in summary
