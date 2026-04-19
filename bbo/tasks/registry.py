"""Task registries and convenience constructors."""

from __future__ import annotations

from pathlib import Path

from .surrogate import (
    SURROGATE_BENCHMARKS,
    SurrogateKnobTask,
    create_surrogate_knob_task,
    create_sysbench5_surrogate_task,
)
from .synthetic import BRANIN_DEFINITION, SPHERE_DEFINITION, SyntheticFunctionDefinition, SyntheticFunctionTask, SyntheticFunctionTaskConfig


SYNTHETIC_PROBLEM_REGISTRY: dict[str, SyntheticFunctionDefinition] = {
    BRANIN_DEFINITION.key: BRANIN_DEFINITION,
    SPHERE_DEFINITION.key: SPHERE_DEFINITION,
}

SURROGATE_TASK_IDS: tuple[str, ...] = tuple(sorted(SURROGATE_BENCHMARKS))

TASK_FAMILIES: dict[str, tuple[str, ...]] = {
    "synthetic": tuple(sorted(SYNTHETIC_PROBLEM_REGISTRY)),
    "surrogate": SURROGATE_TASK_IDS,
}


def get_synthetic_problem(name: str) -> SyntheticFunctionDefinition:
    if name not in SYNTHETIC_PROBLEM_REGISTRY:
        available = ", ".join(sorted(SYNTHETIC_PROBLEM_REGISTRY))
        raise ValueError(f"Unknown synthetic problem `{name}`. Available: {available}")
    return SYNTHETIC_PROBLEM_REGISTRY[name]


def create_demo_task(
    problem: str = "branin_demo",
    *,
    max_evaluations: int | None = None,
    seed: int = 0,
    noise_std: float = 0.0,
) -> SyntheticFunctionTask:
    config = SyntheticFunctionTaskConfig(
        problem=problem,
        max_evaluations=max_evaluations,
        seed=seed,
        noise_std=noise_std,
    )
    return SyntheticFunctionTask(config=config, definition=get_synthetic_problem(problem))


def create_surrogate_task(
    name: str = "knob_surrogate_sysbench_5",
    *,
    max_evaluations: int | None = None,
    seed: int = 0,
    surrogate_path: str | Path | None = None,
    knobs_json_path: str | Path | None = None,
) -> SurrogateKnobTask:
    """Construct a surrogate knob task by id (see ``SURROGATE_BENCHMARKS``)."""
    if name not in SURROGATE_BENCHMARKS:
        available = ", ".join(SURROGATE_TASK_IDS)
        raise ValueError(f"Unknown surrogate task `{name}`. Available: {available}")
    return create_surrogate_knob_task(
        name,
        max_evaluations=max_evaluations,
        seed=seed,
        surrogate_path=surrogate_path,
        knobs_json_path=knobs_json_path,
    )


__all__ = [
    "SURROGATE_BENCHMARKS",
    "SURROGATE_TASK_IDS",
    "SYNTHETIC_PROBLEM_REGISTRY",
    "TASK_FAMILIES",
    "SurrogateKnobTask",
    "create_demo_task",
    "create_surrogate_knob_task",
    "create_surrogate_task",
    "create_sysbench5_surrogate_task",
    "get_synthetic_problem",
]
