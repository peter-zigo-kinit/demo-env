# Bencont Demo

Teachable FastAPI + Pydantic AI harness: `POST /query` accepts a Query, the Agent may call the Bratislava Weather Forecast Tool, and the Answer (plus Tool Calls) is returned over HTTP.

## Setup

```bash
cp ".env example" .env   # fill in secrets
uv sync --group dev
```

## Run

```bash
uv run bancont
# or: uv run uvicorn bancont.app:app --reload
```

```bash
curl -s http://127.0.0.1:8000/query \
  -H 'Content-Type: application/json' \
  -d '{"query":"What is the capital of Slovakia?"}'
```

## Tests

```bash
uv run pytest
```

HTTP seam tests use `TestModel` and a fake forecast — no live Azure or Open-Meteo.
