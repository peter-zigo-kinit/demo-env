# Agent-agnostic coding setup

How this Pydantic AI harness is laid out, where skills come from, and how to keep `AGENTS.md` honest.

## Idea

One **canonical** skill store. Every coding agent (Cursor, Claude Code, Codex, …) either reads that store directly or reaches it through **symlinks**. One **minimal** project brief (`AGENTS.md`) that any harness can load. No duplicated skill copies, no vendor-locked install story in the brief.

```text
.agents/skills/          ← source of truth (installed once)
.claude/skills/*         ← symlinks → ../../.agents/skills/*
.cursor/skills/*         ← symlinks → ../../.agents/skills/*
AGENTS.md                ← tiny standing brief (always loaded)
CLAUDE.md                ← symlink → AGENTS.md
skills-lock.json         ← lockfile from `npx skills`
```

## Where skills come from

| Source | Package | What’s installed here |
| --- | --- | --- |
| [anthropics/skills](https://github.com/anthropics/skills) | `npx skills add anthropics/skills` | `skill-creator` |
| [mattpocock/skills](https://github.com/mattpocock/skills) | `npx skills add mattpocock/skills` | Main engineering flow only |

**Main flow skills in this harness:**

| Skill | Role |
| --- | --- |
| `setup-matt-pocock-skills` | Once per repo: issue tracker, triage labels, domain doc layout → writes `docs/agents/` and a short block into `AGENTS.md` / `CLAUDE.md` |
| `grill-with-docs` | Grill a plan while updating `CONTEXT.md` / ADRs |
| `triage` | Move issues through triage roles |
| `improve-codebase-architecture` | Deepening opportunities → HTML report → grill |
| `to-spec` | Conversation → spec on the issue tracker |
| `to-tickets` | Plan/spec → tracer-bullet tickets with blockers |
| `implement` | Build from spec/tickets (may call `/tdd`, `/code-review`) |
| `wayfinder` | Large work as investigation tickets |
| `handoff` | Compact session for another agent |

Supporting skills (`grilling`, `domain-modeling`, `tdd`, `code-review`, `codebase-design`) are **not** vendored by default. Install into `.agents/skills/` only when a main-flow skill needs them, then refresh vendor symlinks.

Install is a **one-time** repo bootstrap (see `SETUP-PROMPT.md`). Do not put install steps in `AGENTS.md`.

## How to handle AGENTS.md

Guidance: [AGENTS.md (AI Hero dictionary)](https://www.aihero.dev/ai-coding-dictionary/agents-md) and [A Complete Guide To AGENTS.md](https://www.aihero.dev/a-complete-guide-to-agents-md).

**Rules of thumb:**

1. **Always-loaded cost** — everything in `AGENTS.md` is paid on every turn. Keep it small.
2. **Only undiscoverable + globally relevant** — project one-liner, hard constraints, non-obvious commands. Not file trees, not style guides, not skill catalogs.
3. **Progressive disclosure** — workflows live in `.agents/skills/*/SKILL.md`. Domain/tracker config lives in `docs/agents/` after `setup-matt-pocock-skills`. Point; don’t paste.
4. **Don’t auto-generate a fat brief** — catalogs go stale and dilute attention.

**Belongs in AGENTS.md**

- What this repo is (Pydantic AI harness demo).
- Demo posture (teachability over production hardening).
- After setup: follow `docs/agents/` when present.
- Later, the short `## Agent skills` pointers that `setup-matt-pocock-skills` adds (issue tracker / triage / domain).

**Does not belong in AGENTS.md**

- Full skill tables or “suggested order” of skills.
- Where skills are installed or how to `npx skills add …`.
- “How agents should load skills” tutorials.
- Long conventions that should be a skill or `docs/*.md`.

`CLAUDE.md` is a symlink to `AGENTS.md` so Claude Code and AGENTS.md-aware tools share one brief.

## How agnostic coding-agent setup works

1. **Canonical store** — `.agents/skills/` is the only place skill *content* lives. Edit there; never edit through a symlink as if it were a separate copy.
2. **Vendor adapters** — `.claude/skills/` and `.cursor/skills/` exist only so each product discovers skills in its native path. Same for any future agent: add another symlink tree, don’t fork the skills.
3. **CLI quirks** — `npx skills` may install under `.agents/skills` or another agent path depending on flags. After install, normalize to `.agents/skills/`, then recreate symlinks.
4. **Refresh symlinks after adding a skill** — point `.claude/skills/<name>` and `.cursor/skills/<name>` at `../../.agents/skills/<name>`.
5. **Once-per-repo engineering config** — run `setup-matt-pocock-skills` when you’re ready to choose issue tracker and domain layout. That is separate from skill install.

## Related files

- Reusable bootstrap prompt: [`SETUP-PROMPT.md`](./SETUP-PROMPT.md)
- Lockfile: `/skills-lock.json`
- Standing brief: `/AGENTS.md`
