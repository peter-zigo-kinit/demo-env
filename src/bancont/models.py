"""API request/response models using domain vocabulary from CONTEXT.md."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(description="Natural-language Query for the Agent")


class ToolCall(BaseModel):
    """A record that the Agent invoked a named tool."""

    tool_name: str
    args: dict[str, Any] = Field(default_factory=dict)
    result_summary: str | None = None


class QueryResponse(BaseModel):
    answer: str
    tool_calls: list[ToolCall] = Field(default_factory=list)
