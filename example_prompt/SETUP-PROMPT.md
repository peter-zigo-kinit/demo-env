# Setup prompt

Paste into a coding agent in an empty (or new) repo:

---

This project is for demo purposes.
It should be coding agent agnostic. Create AGENTS.md.

Purpose of this project will demonstrate a pydantic AI harness.

Skills should be installed to a common folder `.agents/skills`.

Install https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md

Also this:
`npx skills@latest add mattpocock/skills`

Only main flow:

- grill-with-docs — Grilling session that also builds your project's domain model, sharpening terminology and updating CONTEXT.md and ADRs inline.
- triage — Move issues through a state machine of triage roles.
- improve-codebase-architecture — Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
- setup-matt-pocock-skills — Configure this repo for the engineering skills (issue tracker, triage labels, domain doc layout). Run once per repo before using the other engineering skills.
- to-spec — Turn the current conversation into a spec and publish it to the issue tracker. No interview — just synthesizes what you've already discussed.
- to-tickets — Break any plan, spec, or conversation into a set of tracer-bullet tickets, each declaring its blocking edges — written as text in a local file, or as native blocking links on a real tracker.
- implement — Build the work described by a spec or set of tickets, driving /tdd at pre-agreed seams and closing out with /code-review before committing.
- wayfinder — Plan a huge chunk of work, more than one agent session can hold, as a shared map of investigation tickets on the issue tracker — resolve them one at a time until the way to the destination is clear.
- handoff — Compact the current conversation into a handoff document so another agent can continue the work.

Keep AGENTS.md small — just that this is a pydantic AI harness demo. Don't put the skill list or install instructions in there; install is one-time. Follow the aihero AGENTS.md idea: progressive disclosure, skills carry the workflows.

Also create `.claude/skills` and `.cursor/skills` — but those should just be symlinks to the skills in `.agents/skills`.
CLAUDE.md should be a symlink to AGENTS.md.
