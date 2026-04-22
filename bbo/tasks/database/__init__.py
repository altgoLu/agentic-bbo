"""HTTP-backed MariaDB/sysbench evaluation tasks (Docker API)."""

from __future__ import annotations

from .specs import (
    HTTP_DATABASE_TASK_IDS,
    HttpDatabaseTaskSpec,
    SYSBENCH_TEST_BY_WORKLOAD,
    DATABASE_TASK_SPECS,
    by_task_id,
    is_database_task_id,
)
from .task import (
    HttpDatabaseKnobTask,
    HttpDatabaseKnobTaskConfig,
    create_http_database_sysbench5_task,
    create_http_database_task,
)
from .cli_support import DATABASE_TASK_NAMES, DATABASE_TASK_FAMILY, database_registry_entries

__all__ = [
    "DATABASE_TASK_FAMILY",
    "DATABASE_TASK_NAMES",
    "DATABASE_TASK_SPECS",
    "HTTP_DATABASE_TASK_IDS",
    "HttpDatabaseKnobTask",
    "HttpDatabaseKnobTaskConfig",
    "HttpDatabaseTaskSpec",
    "SYSBENCH_TEST_BY_WORKLOAD",
    "by_task_id",
    "create_http_database_sysbench5_task",
    "create_http_database_task",
    "database_registry_entries",
    "is_database_task_id",
]
