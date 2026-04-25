"""Compatibility shim for ``bbo.algorithms.agentic.opro``."""

from __future__ import annotations

from ..llm_based import opro as _opro
from ..llm_based.opro import *  # noqa: F403

urllib_error = _opro.urllib_error
urllib_request = _opro.urllib_request

__all__ = list(_opro.__all__)
