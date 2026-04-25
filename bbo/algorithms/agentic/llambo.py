"""Compatibility shim for ``bbo.algorithms.agentic.llambo``."""

from __future__ import annotations

from ..llm_based import llambo as _llambo
from ..llm_based.llambo import *  # noqa: F403

urllib_error = _llambo.urllib_error
urllib_request = _llambo.urllib_request

__all__ = list(_llambo.__all__)
