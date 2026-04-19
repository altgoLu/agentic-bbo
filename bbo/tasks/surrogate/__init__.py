"""Surrogate-model tasks (database knob tuning via offline sklearn models)."""

from .catalog import SURROGATE_BENCHMARKS, SurrogateBenchmarkSpec
from .paths import (
    SYSBENCH_5_FEATURE_ORDER,
    bundled_knobs_top5_path,
    bundled_surrogate_sysbench5_path,
)
from .task import (
    SurrogateKnobTask,
    SurrogateKnobTaskConfig,
    create_surrogate_knob_task,
    create_sysbench5_surrogate_task,
)

__all__ = [
    "SURROGATE_BENCHMARKS",
    "SYSBENCH_5_FEATURE_ORDER",
    "SurrogateBenchmarkSpec",
    "SurrogateKnobTask",
    "SurrogateKnobTaskConfig",
    "bundled_knobs_top5_path",
    "bundled_surrogate_sysbench5_path",
    "create_surrogate_knob_task",
    "create_sysbench5_surrogate_task",
]
