# AGENTS.md

This project demonstrates a **Pydantic AI harness** — how to structure agent work with shared skills, domain docs, and a repeatable engineering flow.

Prefer clarity and teachability over production hardening. After repo setup, follow `docs/agents/` when present.

## Agent skills

### Issue tracker

GitHub Issues on `peter-zigo-kinit/demo-env` (via `gh`). See `docs/agents/issue-tracker.md`.

### Triage labels

Default role labels: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: root `CONTEXT.md` + `docs/adr/`. See `docs/agents/domain.md`.
