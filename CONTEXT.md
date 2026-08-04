# Bancont Demo

A teachable Pydantic AI harness demo: FastAPI accepts a query, an agent may call tools, and the response is returned over HTTP.

## Language

**Query**:
A natural-language request sent to the demo API that the agent answers in one independent turn (no conversation history across requests).
_Avoid_: Prompt, chat message, question (as API vocabulary)

**Agent**:
The Pydantic AI agent that interprets a Query and may call tools before answering.
_Avoid_: Bot, assistant, LLM (as the product noun)

**Weather Forecast Tool**:
A tool the Agent can call to obtain a live near-term weather forecast for Bratislava only (location fixed; today / next 24 hours).
_Avoid_: Weather API (as the agent-facing concept), get_weather

**Answer**:
The Agent's final natural-language reply to a Query after any tool use.
_Avoid_: Response text, completion, output (as the field name)

**Tool Call**:
A record that the Agent invoked a named tool with arguments (and optionally a short result summary), returned alongside the Answer for teachability.
_Avoid_: Function call, tool use (as API vocabulary)
