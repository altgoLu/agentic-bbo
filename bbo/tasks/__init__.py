"""Task packages and registries."""

from .registry import (
    SURROGATE_BENCHMARKS,
    SURROGATE_TASK_IDS,
    SYNTHETIC_PROBLEM_REGISTRY,
    TASK_FAMILIES,
    SurrogateKnobTask,
    create_demo_task,
    create_surrogate_knob_task,
    create_surrogate_task,
    create_sysbench5_surrogate_task,
    get_synthetic_problem,
)
from .synthetic import BRANIN_DEFINITION, SPHERE_DEFINITION, SyntheticFunctionDefinition, SyntheticFunctionTask, SyntheticFunctionTaskConfig

__all__ = [
    "BRANIN_DEFINITION",
    "SPHERE_DEFINITION",
    "SURROGATE_BENCHMARKS",
    "SURROGATE_TASK_IDS",
    "SYNTHETIC_PROBLEM_REGISTRY",
    "TASK_FAMILIES",
    "SurrogateKnobTask",
    "SyntheticFunctionDefinition",
    "SyntheticFunctionTask",
    "SyntheticFunctionTaskConfig",
    "create_demo_task",
    "create_surrogate_knob_task",
    "create_surrogate_task",
    "create_sysbench5_surrogate_task",
    "get_synthetic_problem",
]
