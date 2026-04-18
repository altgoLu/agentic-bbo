from __future__ import annotations

from pathlib import Path

from bbo.core import ObjectiveDirection, TrialSuggestion
from bbo.run import run_single_experiment
from bbo.tasks import HER_FEATURES, create_her_task


def test_her_task_spec_and_sanity() -> None:
    task = create_her_task(max_evaluations=3, seed=19)
    report = task.sanity_check()

    assert report.ok
    assert task.spec.name == "her_demo"
    assert task.spec.primary_objective.name == "regret"
    assert task.spec.primary_objective.direction == ObjectiveDirection.MINIMIZE
    assert task.spec.search_space.names() == list(HER_FEATURES)
    assert report.metadata["row_count"] == 812
    assert report.metadata["column_count"] == 11

    result = task.evaluate(TrialSuggestion(config=task.spec.search_space.defaults()))
    assert result.success
    assert result.objectives["regret"] >= 0.0
    assert "predicted_target" in result.metrics


def test_her_demo_random_search_smoke(tmp_path: Path) -> None:
    summary = run_single_experiment(
        task_name="her_demo",
        algorithm_name="random_search",
        seed=5,
        max_evaluations=3,
        results_root=tmp_path,
        resume=False,
    )

    assert summary["trial_count"] == 3
    assert summary["best_primary_objective"] is not None
    assert Path(summary["results_jsonl"]).exists()
    assert len(summary["plot_paths"]) == 2
    for plot_path in summary["plot_paths"]:
        path = Path(plot_path)
        assert path.exists()
        assert path.stat().st_size > 0
