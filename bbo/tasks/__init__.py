"""Task packages and registries."""

from .registry import ALL_TASK_NAMES, SCIENTIFIC_TASK_REGISTRY, SYNTHETIC_PROBLEM_REGISTRY, TASK_FAMILIES, create_demo_task, create_task, get_synthetic_problem
from .scientific import HER_DATASET_FILENAME, HER_DATASET_SOURCE_URL, HER_FEATURES, HER_TASK_NAME, HerTask, HerTaskConfig, create_her_task
from .synthetic import BRANIN_DEFINITION, SPHERE_DEFINITION, SyntheticFunctionDefinition, SyntheticFunctionTask, SyntheticFunctionTaskConfig

__all__ = [
    "ALL_TASK_NAMES",
    "BRANIN_DEFINITION",
    "HER_DATASET_FILENAME",
    "HER_DATASET_SOURCE_URL",
    "HER_FEATURES",
    "HER_TASK_NAME",
    "HerTask",
    "HerTaskConfig",
    "SPHERE_DEFINITION",
    "SCIENTIFIC_TASK_REGISTRY",
    "SYNTHETIC_PROBLEM_REGISTRY",
    "TASK_FAMILIES",
    "SyntheticFunctionDefinition",
    "SyntheticFunctionTask",
    "SyntheticFunctionTaskConfig",
    "create_demo_task",
    "create_her_task",
    "create_task",
    "get_synthetic_problem",
]
