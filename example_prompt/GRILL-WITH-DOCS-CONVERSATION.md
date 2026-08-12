# Example: `/grill-with-docs` conversation

Condensed from a real grilling session that shaped the **side-product** FastAPI + Pydantic AI demo in this repo. Use it as a pattern for how `/grill-with-docs` walks decisions one at a time, records domain language, and stops before implementation.

Not a full transcript — only the essence: prompts, forks, choices, and the locked shared understanding.

## Starting prompt

```text
/grill-with-docs

I would create basic demo with pydantic ai 2.0,
I will fast api server, with simple query endpoint
```

## How the session ran

One question at a time. Each turn: short options + a **recommended** answer. User replies with a choice (or a short override). No app code until shared understanding is confirmed.

## Decisions (essence)

| # | Question | User choice |
| --- | --- | --- |
| Q1 | What should a successful query demonstrate — thin hello-world, harness slice, or richer (tools/RAG/Code Mode)? | **Tools already in v1** — add a weather forecast tool (tool calling), not a no-tool hello-world |
| Q2 | Fake forecast vs live provider? | **Real** provider |
| Q3 | Which weather API? | **Open-Meteo** (no weather API key) |
| Q4 | Which model provider? | **Azure OpenAI** (keys/endpoint like `.env example`) |
| Q5 | Azure deployment name? | **`gpt-5.6-luna`** (via env, e.g. `AZURE_OPENAI_DEPLOYMENT`) |
| Q6 | What does `POST /query` return? | **`{ answer, tool_calls }`** (teachable tool-calling) |
| Q7 | Logfire in v1? | **Yes** — instrument FastAPI + Pydantic AI |
| Q8 | Single-turn or multi-turn? | **Single-turn** — each Query independent |
| Q9 | How does the weather tool pick a place? | Clarified as **Bratislava only** (fixed city for the demo) |
| Q10 | Forecast window? | **Today / next 24h** |
| Q11 | Auth on `/query`? | **None** for v1 |
| Q12 | Packaging? | **`uv` + `pyproject.toml`** |
| Q13 | Out of scope for v1? | Agree: no Code Mode/harness extras, streaming, multi-turn, auth, multi-city weather, RAG/DB |

## Representative Q&A (condensed)

**Assistant (Q1):** Is this a thin agent-behind-HTTP hello-world, or a teachable harness slice? Recommended: harness slice *without* tools yet.

**User:** Yes, add weather forecast — tool calling.

**Assistant (Q2–Q3):** Fake vs real forecast? → Real → Open-Meteo recommended.

**User:** Real. Open-Meteo.

**Assistant (Q4):** Model provider? `.env` had Logfire only; recommended OpenAI.

**User:** Azure — same structure as `.env example`.

**Assistant (Q5–Q6):** Deployment name? Response shape `{ answer }` vs `{ answer, tool_calls }`?

**User:** `gpt-5.6-luna`. Return `{ answer, tool_calls }`.

**Assistant (Q8–Q9):** Single-turn? Place name geocoding for any city vs fixed location?

**User:** Single-turn. Bratislava → **Bratislava only** (not “any city, Bratislava as example”).

**Assistant (Q10–Q13):** 7-day vs 24h? Auth? uv? Lock out-of-scope list?

**User:** 24h. No auth. uv. Accept the boundary.

## Locked shared understanding

| Piece | Decision |
| --- | --- |
| Shape | FastAPI + Pydantic AI agent — thin teachable slice (not full harness) |
| Endpoint | Stateless `POST /query`, no auth |
| Contract | Request `{ "query": "..." }` → `{ "answer", "tool_calls" }` |
| Model | Azure OpenAI, deployment `gpt-5.6-luna` |
| Tool | Weather Forecast Tool — **Bratislava only**, **next 24h**, **Open-Meteo** |
| Observability | Logfire on FastAPI + agent |
| Packaging | `uv` + `pyproject.toml` |
| Out of scope | Harness extras (Code Mode, etc.), streaming, multi-turn, auth, multi-city weather, RAG/DB |

After “yes,” the session recorded:

- `CONTEXT.md` — glossary (Query, Agent, Weather Forecast Tool, Answer, Tool Call)
- `docs/adr/0001-azure-openai.md` — Azure OpenAI decision

Implementation waited for a later step (`/to-tickets`, `/implement`, etc.).

## Why keep this example

- Shows **grill-with-docs** style: decisions only, one at a time, recommendation + options.
- Shows how a vague “FastAPI + Pydantic AI demo” becomes a crisp v1 boundary.
- Reminds that in *this* repo the app is a **side product**; the primary demo is agent-agnostic project setup (see [`SETUP-PROMPT.md`](./SETUP-PROMPT.md) and [`AGENT-AGNOSTIC-SETUP.md`](./AGENT-AGNOSTIC-SETUP.md)).

## Paste-ready opener (reuse)

```text
/grill-with-docs

I want a basic Pydantic AI demo: FastAPI with a simple query endpoint.
Ask one decision at a time. Don't implement until we lock shared understanding.
Prefer teachability over production hardening.
```
