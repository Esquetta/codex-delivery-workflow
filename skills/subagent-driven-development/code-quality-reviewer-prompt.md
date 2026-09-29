# Optional Standards Reviewer Prompt

Use only for a specific risk or explicit requirement that needs a separate Standards
owner. The normal [review workflow](../requesting-code-review/SKILL.md) already runs
both independent passes in one fresh reviewer. On Claude Code use a fresh native
read-only subagent, never a parent fork; its allowlist is `Read`, `Grep`, and `Glob`.

```md
Remain read-only. Inspect the fixed change set and supplied requirements, constraints,
and primary verification evidence. Do not implement fixes or external writes.

Inspect correctness, security, compatibility, failure paths, maintainability,
operational effects, and meaningful test coverage. Do not flag pre-existing conditions
or personal preferences as introduced defects.

Return evidence-backed findings by Critical / Important / Minor with tight file
references, impact, and smallest correction. Return `ship`, `fix-first`, or `rethink`
for this axis and state material limitations.
```
