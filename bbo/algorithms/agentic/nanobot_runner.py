"""Nanobot CLI runner with compatibility patches for BBO agent calls."""

from __future__ import annotations

import os


def _patch_strip_max_tokens() -> None:
    """Strip legacy ``max_tokens`` for compatible endpoints that reject it."""

    try:
        from nanobot.providers import openai_compat_provider as provider_module  # type: ignore

        original = provider_module.OpenAICompatProvider._build_kwargs

        def patched(
            self,
            messages,
            tools,
            model,
            max_tokens,
            temperature,
            reasoning_effort,
            tool_choice,
        ):
            kwargs = original(
                self,
                messages,
                tools,
                model,
                max_tokens,
                temperature,
                reasoning_effort,
                tool_choice,
            )
            kwargs.pop("max_tokens", None)
            return kwargs

        provider_module.OpenAICompatProvider._build_kwargs = patched
    except Exception:
        pass


def _patch_log_llm() -> None:
    """Write nanobot's final message snapshot when a log directory is provided."""

    import contextvars
    import json
    import time
    from datetime import datetime, timezone
    from pathlib import Path

    log_root = Path(os.environ["BBO_NANOBOT_LOG_DIR"])
    session_key_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
        "bbo_nanobot_session_key",
        default=None,
    )

    def iso_now() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="milliseconds")

    def filename_ts() -> str:
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%dT%H-%M-%S-") + f"{now.microsecond // 1000:03d}Z"

    def write_agent_end(session_key: str, messages: list, duration_s: float, usage: dict, success: bool) -> None:
        session_dir = log_root / session_key
        try:
            session_dir.mkdir(parents=True, exist_ok=True)
            (session_dir / f"{filename_ts()}_agent-end.json").write_text(
                json.dumps(
                    {
                        "stage": "agent_end",
                        "timestamp": iso_now(),
                        "sessionKey": session_key,
                        "success": success,
                        "durationMs": round(duration_s * 1000, 1),
                        "messageCount": len(messages),
                        "messages": messages,
                        "usage": usage,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )
        except Exception:
            pass

    try:
        from nanobot.agent import loop as loop_module  # type: ignore

        original_process = loop_module.AgentLoop._process_message
        original_run = loop_module.AgentLoop._run_agent_loop

        async def patched_process(self, msg, session_key=None, **kwargs):
            key = session_key or msg.session_key
            token = session_key_var.set(key)
            try:
                return await original_process(self, msg, session_key=session_key, **kwargs)
            finally:
                session_key_var.reset(token)

        async def patched_run_agent_loop(self, initial_messages, **kwargs):
            start = time.monotonic()
            result = await original_run(self, initial_messages, **kwargs)
            final_content = result[0]
            messages = result[2]
            session_key = session_key_var.get()
            if session_key:
                write_agent_end(
                    session_key=session_key,
                    messages=messages,
                    duration_s=time.monotonic() - start,
                    usage=dict(getattr(self, "_last_usage", {})),
                    success=final_content is not None,
                )
            return result

        loop_module.AgentLoop._process_message = patched_process
        loop_module.AgentLoop._run_agent_loop = patched_run_agent_loop
    except Exception:
        pass


if os.environ.get("BBO_NANOBOT_NO_MAX_TOKENS") == "1":
    _patch_strip_max_tokens()

if os.environ.get("BBO_NANOBOT_LOG_DIR"):
    _patch_log_llm()


from nanobot.cli.commands import app  # noqa: E402  # type: ignore

app()
