# Bencont Demo

This repo’s **main purpose** is to show how to set up a project so coding agents stay interchangeable: shared skill folders, a thin `AGENTS.md`, and bootstrap prompts — not a product app.

The FastAPI + Pydantic AI Query API in this tree is a **side product**: a small app that happened to get built after the harness was in place. Treat it as an example of “what you might build next,” not as the point of the demo.

## What this demo teaches

1. **Agent-agnostic layout** — one canonical skill store (`.agents/skills/`), vendor symlinks (`.claude/skills/`, `.cursor/skills/`), and a short standing brief (`AGENTS.md` / `CLAUDE.md`).
2. **Bootstrap once** — install skills and wire the repo without stuffing install steps into `AGENTS.md`.
3. **(Optional side product)** — a teachable `POST /query` agent with a Bratislava weather tool, if you want something concrete to run after setup.

## Environment (`.env example`)

Copy the template and fill in secrets:

```bash
cp ".env example" .env
```

**Model provider (required to talk to a live Agent)** — you need credentials for **some** chat-model vendor. This repo’s `.env example` shows **Azure OpenAI** (`AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_VERSION`, `AZURE_OPENAI_DEPLOYMENT`) because that matched the original demo environment ([ADR-0001](docs/adr/0001-azure-openai.md)).

You can use **Azure OpenAI, OpenAI, Anthropic, or any other vendor Pydantic AI supports**. Put the vendor’s env vars in `.env`; a coding agent should **adapt the Agent wiring to whatever those settings imply** (don’t hard-require Azure if the env is clearly OpenAI-only, etc.).

**Logfire (optional)** — `LOGFIRE_API_KEY` (or `LOGFIRE_TOKEN`) enables tracing. Without it the app should still run; observability is nice-to-have, not a blocker.

| Variable | Required? | Role |
| --- | --- | --- |
| `AZURE_OPENAI_*` / `OPENAI_API_KEY` / other vendor keys | **One model stack** | Powers the Agent |
| `LOGFIRE_API_KEY` or `LOGFIRE_TOKEN` | Optional | Sends traces to Logfire |

## How to operate (sequence)

1. **Use the setup prompt** — paste [`example_prompt/SETUP-PROMPT.md`](example_prompt/SETUP-PROMPT.md) into a coding agent to install skills, create a thin `AGENTS.md`, and wire agent-agnostic folders/symlinks. For more detail on what that layout means and how `AGENTS.md` should stay small, read [`example_prompt/AGENT-AGNOSTIC-SETUP.md`](example_prompt/AGENT-AGNOSTIC-SETUP.md).
2. **Mimic `/grill-with-docs`** — run a grilling session the same way as in [`example_prompt/GRILL-WITH-DOCS-CONVERSATION.md`](example_prompt/GRILL-WITH-DOCS-CONVERSATION.md): one decision at a time, lock shared understanding, update `CONTEXT.md` / ADRs — don’t implement yet.

After that, continue with the Matt Pocock loop below (`setup-matt-pocock-skills` once per repo → `/to-tickets` → `/implement`, …).

## Example prompts

| Doc | Location | Role |
| --- | --- | --- |
| Setup prompt (paste to bootstrap skills) | [`example_prompt/SETUP-PROMPT.md`](example_prompt/SETUP-PROMPT.md) | Install skills + create thin `AGENTS.md` |
| Agent-agnostic setup (how the layout works) | [`example_prompt/AGENT-AGNOSTIC-SETUP.md`](example_prompt/AGENT-AGNOSTIC-SETUP.md) | Explain folders, symlinks, what belongs in `AGENTS.md` |
| Grill-with-docs conversation (essence) | [`example_prompt/GRILL-WITH-DOCS-CONVERSATION.md`](example_prompt/GRILL-WITH-DOCS-CONVERSATION.md) | Example design grill that shaped the side-product app |

## How we use Matt Pocock skills

Skills from [mattpocock/skills](https://github.com/mattpocock/skills) drive the engineering loop. Install them once into `.agents/skills/` (see setup prompts above). Then the **basic flow** is:

```text
setup-matt-pocock-skills   ← once per repo (tracker, triage labels, docs/agents/)
        ↓
grill-with-docs            ← stress-test the idea; update CONTEXT.md / ADRs
        ↓
to-spec                    ← optional: publish a spec to the issue tracker
        ↓
to-tickets                 ← break into tracer-bullet tickets with blockers
        ↓
implement                  ← build from tickets (often /tdd, then /code-review)
        ↓
handoff                    ← when another agent (or you later) continues
```

**What each step is for**

| Skill | When |
| --- | --- |
| `setup-matt-pocock-skills` | First time in the repo — without this, `/to-spec` / `/to-tickets` don’t know the tracker |
| `grill-with-docs` | Before coding — one decision at a time until shared understanding |
| `to-spec` | Conversation is clear enough to publish as a tracker spec |
| `to-tickets` | Spec/plan → small tickets with blocking edges (`ready-for-agent`, etc.) |
| `implement` | Pick tickets and build; close with review before commit |
| `handoff` | Session is done but work isn’t — compact context for the next agent |

In this demo’s side-product path we first ran **`/setup-matt-pocock-skills`** (once per repo), then **`/grill-with-docs` → `/to-tickets` → implement**. See [`example_prompt/GRILL-WITH-DOCS-CONVERSATION.md`](example_prompt/GRILL-WITH-DOCS-CONVERSATION.md) for the grill essence.

### `/to-tickets` → GitHub issues → `/implement`

`/to-tickets` turns the grilled plan into **tracer-bullet tickets on the GitHub project** ([`peter-zigo-kinit/demo-env`](https://github.com/peter-zigo-kinit/demo-env/issues)). Each ticket is an issue you can label `ready-for-agent`, pick up, and build with `/implement` (blockers stay visible as linked issues).

Closed issues from this demo’s side-product build:

| # | Ticket | Link |
| --- | --- | --- |
| 1 | Scaffold Query API contract | https://github.com/peter-zigo-kinit/demo-env/issues/1 |
| 2 | Wire Azure OpenAI Agent | https://github.com/peter-zigo-kinit/demo-env/issues/2 |
| 3 | Add Bratislava Weather Forecast Tool | https://github.com/peter-zigo-kinit/demo-env/issues/3 |
| 4 | Instrument with Logfire | https://github.com/peter-zigo-kinit/demo-env/issues/4 |
| 5 | HTTP seam tests for Query | https://github.com/peter-zigo-kinit/demo-env/issues/5 |

## Side-product app (optional)

Only needed if you want to run the Query API that came out of the grill session. Set up `.env` first (see [Environment](#environment-env-example) above).

```bash
uv sync --group dev
uv run bencont
```

```bash
curl -s http://127.0.0.1:8000/query \
  -H 'Content-Type: application/json' \
  -d '{"query":"Aka je dnesna teplota?"}'
```

```bash
uv run pytest
```
