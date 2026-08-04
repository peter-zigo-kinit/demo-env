"""HTTP seam tests for POST /query.

Seam under test: POST /query (not Agent internals).
Uses Pydantic AI TestModel and a fake Bratislava forecast — no live Azure or Open-Meteo.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from pydantic_ai.models.test import TestModel

from bancont.agent import agent
from bancont.app import app
from bancont.deps import AppDeps, set_deps


FAKE_FORECAST = (
    "Bratislava next 24h: mostly clear, 18–24°C, light breeze, "
    "low rain chance (~10%)."
)


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    set_deps(AppDeps(forecast_fetcher=lambda: FAKE_FORECAST))
    monkeypatch.setenv("LOGFIRE_SEND_TO_LOGFIRE", "false")
    with TestClient(app) as test_client:
        yield test_client
    set_deps(AppDeps())


def test_query_returns_answer_and_tool_calls_shape(client: TestClient) -> None:
    with agent.override(model=TestModel(call_tools=[])):
        response = client.post("/query", json={"query": "What is 2 + 2?"})

    assert response.status_code == 200
    body = response.json()
    assert "answer" in body
    assert isinstance(body["answer"], str)
    assert body["answer"]
    assert "tool_calls" in body
    assert isinstance(body["tool_calls"], list)


def test_weather_query_includes_tool_call_and_coherent_answer(
    client: TestClient,
) -> None:
    with agent.override(model=TestModel()):
        response = client.post(
            "/query",
            json={"query": "What is the weather forecast for Bratislava today?"},
        )

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["answer"], str)
    assert body["answer"]

    tool_calls = body["tool_calls"]
    assert len(tool_calls) >= 1
    names = {tc["tool_name"] for tc in tool_calls}
    assert "weather_forecast" in names

    weather_call = next(tc for tc in tool_calls if tc["tool_name"] == "weather_forecast")
    assert "args" in weather_call
    assert weather_call["result_summary"] == FAKE_FORECAST
    # TestModel folds tool results into the Answer text — require forecast content there too.
    assert "Bratislava" in body["answer"]
    assert "18–24°C" in body["answer"] or "18-24" in body["answer"]
