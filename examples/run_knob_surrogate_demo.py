"""Run a baseline optimizer on a surrogate knob task (offline sklearn RF)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from bbo.algorithms import create_algorithm
from bbo.core import ExperimentConfig, Experimenter, JsonlMetricLogger
from bbo.tasks import SURROGATE_TASK_IDS, create_surrogate_task

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS_ROOT = PROJECT_ROOT / "runs" / "demo"


def main() -> None:
    parser = argparse.ArgumentParser(description="Knob surrogate benchmark demo.")
    parser.add_argument(
        "--task",
        default="knob_surrogate_sysbench_all",
        choices=sorted(SURROGATE_TASK_IDS),
        help="Surrogate task id (default: sysbench_5; large models e.g. *_20 need a complete .joblib).",
    )
    parser.add_argument(
        "--algorithm",
        default="random_search",
        choices=("random_search", "pycma"),
        help="Baseline optimizer.",
    )
    parser.add_argument("--max-evaluations", type=int, default=60)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--sigma-fraction", type=float, default=0.18)
    parser.add_argument("--popsize", type=int, default=6)
    args = parser.parse_args()

    task = create_surrogate_task(args.task, max_evaluations=args.max_evaluations, seed=args.seed)
    algo_kwargs: dict = {}
    if args.algorithm == "pycma":
        algo_kwargs = {"sigma_fraction": args.sigma_fraction, "popsize": args.popsize}
    algorithm = create_algorithm(args.algorithm, **algo_kwargs)

    run_dir = DEFAULT_RESULTS_ROOT / args.task / args.algorithm / f"seed_{args.seed}"
    run_dir.mkdir(parents=True, exist_ok=True)
    results_jsonl = run_dir / "trials.jsonl"

    logger = JsonlMetricLogger(results_jsonl)
    experiment = Experimenter(
        task=task,
        algorithm=algorithm,
        logger_backend=logger,
        config=ExperimentConfig(seed=args.seed, resume=False, fail_fast_on_sanity=True),
    )
    summary = experiment.run()
    out = {
        "task_name": summary.task_name,
        "n_completed": summary.n_completed,
        "best_primary_objective": summary.best_primary_objective,
        "results_jsonl": str(results_jsonl),
    }
    (run_dir / "summary.json").write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
