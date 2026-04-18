"""Task registries and convenience constructors."""

from __future__ import annotations

from ..core import Task
from .scientific import HER_TASK_NAME, create_her_task
from .synthetic import BRANIN_DEFINITION, SPHERE_DEFINITION, SyntheticFunctionDefinition, SyntheticFunctionTask, SyntheticFunctionTaskConfig


SYNTHETIC_PROBLEM_REGISTRY: dict[str, SyntheticFunctionDefinition] = {
    BRANIN_DEFINITION.key: BRANIN_DEFINITION,
    SPHERE_DEFINITION.key: SPHERE_DEFINITION,
}
SCIENTIFIC_TASK_REGISTRY: dict[str, str] = {
    HER_TASK_NAME: "HER random-forest demo task",
}
TASK_REGISTRY: dict[str, str] = {
    **{name: "synthetic" for name in SYNTHETIC_PROBLEM_REGISTRY},
    **{name: "scientific" for name in SCIENTIFIC_TASK_REGISTRY},
}
ALL_TASK_NAMES: tuple[str, ...] = tuple(sorted(TASK_REGISTRY))

TASK_FAMILIES: dict[str, tuple[str, ...]] = {
    "scientific": tuple(sorted(SCIENTIFIC_TASK_REGISTRY)),
    "synthetic": tuple(sorted(SYNTHETIC_PROBLEM_REGISTRY)),
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
) -> Task:
    if problem in SYNTHETIC_PROBLEM_REGISTRY:
        config = SyntheticFunctionTaskConfig(
            problem=problem,
            max_evaluations=max_evaluations,
            seed=seed,
            noise_std=noise_std,
        )
        return SyntheticFunctionTask(config=config, definition=get_synthetic_problem(problem))
    if problem == HER_TASK_NAME:
        return create_her_task(max_evaluations=max_evaluations, seed=seed)
    available = ", ".join(ALL_TASK_NAMES)
    raise ValueError(f"Unknown task `{problem}`. Available: {available}")


def create_task(
    name: str,
    *,
    max_evaluations: int | None = None,
    seed: int = 0,
    noise_std: float = 0.0,
) -> Task:
    return create_demo_task(
        problem=name,
        max_evaluations=max_evaluations,
        seed=seed,
        noise_std=noise_std,
    )


def get_scientific_task(name: str) -> str:
    if name not in SCIENTIFIC_TASK_REGISTRY:
        available = ", ".join(sorted(SCIENTIFIC_TASK_REGISTRY))
        raise ValueError(f"Unknown scientific task `{name}`. Available: {available}")
    return SCIENTIFIC_TASK_REGISTRY[name]


__all__ = [
    "ALL_TASK_NAMES",
    "SCIENTIFIC_TASK_REGISTRY",
    "SYNTHETIC_PROBLEM_REGISTRY",
    "TASK_FAMILIES",
    "create_demo_task",
    "create_task",
    "get_scientific_task",
    "get_synthetic_problem",
]
