"""Pydantic AI Agent backed by Azure OpenAI (ADR-0001)."""

from __future__ import annotations

import json
import os
import warnings

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ToolCallPart, ToolReturnPart
from pydantic_ai.models import Model
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.test import TestModel
from pydantic_ai.providers.azure import AzureProvider

from bancont.deps import AppDeps, get_deps
from bancont.models import ToolCall

load_dotenv()


def _build_model() -> Model:
    """Build Azure OpenAI model from env; TestModel only when Azure env is unset (CI/import)."""
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-5.6-luna")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION") or os.getenv("OPENAI_API_VERSION")

    if not endpoint or not api_key:
        warnings.warn(
            "AZURE_OPENAI_ENDPOINT / AZURE_OPENAI_API_KEY unset; using TestModel. "
            "Set Azure env vars for a live Agent (ADR-0001).",
            stacklevel=2,
        )
        return TestModel()

    return OpenAIChatModel(
        deployment,
        provider=AzureProvider(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        ),
    )


agent: Agent[AppDeps, str] = Agent(
    _build_model(),
    name="bancont_agent",
    deps_type=AppDeps,
    instructions=(
        "You answer each Query in a single turn. "
        "For Bratislava weather (today or next 24 hours), call the weather_forecast tool. "
        "For other topics, answer directly without tools. Be concise."
    ),
)


@agent.tool
def weather_forecast(ctx: RunContext[AppDeps]) -> str:
    """Get the live today / next-24h weather forecast for Bratislava (location is fixed)."""
    return ctx.deps.forecast_fetcher()


def _tool_args(raw_args: object) -> dict:
    if isinstance(raw_args, dict):
        return raw_args
    if isinstance(raw_args, str):
        try:
            parsed = json.loads(raw_args)
            return parsed if isinstance(parsed, dict) else {"raw": raw_args}
        except json.JSONDecodeError:
            return {"raw": raw_args}
    return {}


def _tool_calls_from_messages(messages: list) -> list[ToolCall]:
    summaries: dict[str, str] = {}
    for message in messages:
        for part in message.parts:
            if isinstance(part, ToolReturnPart):
                content = part.content
                summaries[part.tool_call_id] = (
                    content if isinstance(content, str) else str(content)
                )

    tool_calls: list[ToolCall] = []
    for message in messages:
        for part in message.parts:
            if isinstance(part, ToolCallPart):
                tool_calls.append(
                    ToolCall(
                        tool_name=part.tool_name,
                        args=_tool_args(part.args),
                        result_summary=summaries.get(part.tool_call_id),
                    )
                )
    return tool_calls


async def run_query(query: str, deps: AppDeps | None = None) -> tuple[str, list[ToolCall]]:
    """Run a single-turn Query; return Answer text and Tool Call records from messages."""
    result = await agent.run(query, deps=deps or get_deps())
    return result.output, _tool_calls_from_messages(result.all_messages())
