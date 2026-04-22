"""Hook database HTTP tasks into ``bbo.tasks.registry`` / ``python -m bbo.run`` without editing ``run.py``."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ...core import Task
from .specs import HTTP_DATABASE_TASK_IDS, is_database_task_id
from .task import create_http_database_task

DATABASE_TASK_FAMILY = "database"
DATABASE_TASK_NAMES: frozenset[str] = frozenset(HTTP_DATABASE_TASK_IDS)


def database_registry_entries() -> dict[str, str]:
    """task_id -> family label for ``TASK_REGISTRY``."""
    return {name: DATABASE_TASK_FAMILY for name in HTTP_DATABASE_TASK_IDS}


def create_database_task_for_registry(
    name: str,
    *,
    max_evaluations: int | None = None,
    seed: int = 0,
    noise_std: float = 0.0,
    **kwargs: Any,
) -> Task:
    """
    Dispatch from ``create_demo_task`` / ``create_task`` when ``name`` is a database HTTP task.

    ``noise_std`` is ignored (synthetic-only). Optional ``kwargs`` may include
    ``knobs_json_path`` if callers pass it through ``create_task(**kwargs)``.
    """
    _ = noise_std
    if not is_database_task_id(name):
        known = ", ".join(HTTP_DATABASE_TASK_IDS)
        raise ValueError(f"Unknown database task `{name}`. Known: {known}")
    knobs = kwargs.get("knobs_json_path")
    return create_http_database_task(
        name,
        max_evaluations=max_evaluations,
        seed=seed,
        base_url=kwargs.get("http_eval_base_url"),
        knobs_json_path=Path(knobs) if knobs is not None else None,
        request_timeout_sec=kwargs.get("http_eval_timeout_sec"),
        skip_health_check=bool(kwargs.get("http_skip_health_check", False)),
    )


__all__ = [
    "DATABASE_TASK_FAMILY",
    "DATABASE_TASK_NAMES",
    "create_database_task_for_registry",
    "database_registry_entries",
]
