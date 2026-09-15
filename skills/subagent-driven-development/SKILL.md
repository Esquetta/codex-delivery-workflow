---
name: subagent-driven-development
description: Execute approved plan work with scoped specialists, parent verification, and risk-based independent review.
---

# Subagent-Driven Development

Use this skill when delegation reduces useful primary work. Agent availability alone
does not justify delegation. Keep small or tightly coupled work in
[executing-plans](../executing-plans/SKILL.md). This workflow does not grant commits,
pushes, merges, releases, deployments, or external writes.

## Prepare

Read the approved plan once and extract the exact task, settled architecture,
interfaces, file ownership, constraints, and verification. Inspect current workspace
state and preserve unrelated changes. Resolve a material question before dependent work
starts; do not reopen settled design or request approval already supplied.

Choose an installed Terra/high domain specialist. In the starter pack, use
`delivery_worker`; in a wider installed catalog, select a runtime-available role that
matches the task. Omit model and effort overrides for pinned roles. Give the worker the
complete [implementer prompt](implementer-prompt.md), with enough context to act safely.
Prefer fresh bounded context, but include relevant history when the task depends on it.

## Execute

The worker changes only its owned files, runs relevant checks, self-reviews, and reports
actual evidence. The primary inspects the diff and verification, resolves gaps, and
checks integration. Worker self-review does not replace a selected independent review.

Use parallel execution only with independent ownership and settled interfaces under
[dispatching-parallel-agents](../dispatching-parallel-agents/SKILL.md). Shared-file,
dependent, or unresolved-interface tasks stay sequential.

Handle worker results precisely:

- `DONE`: inspect its evidence before accepting it.
- `DONE_WITH_CONCERNS`: resolve correctness, scope, and failed-check concerns.
- `NEEDS_CONTEXT`: send missing facts to the same owner with a focused follow-up.
- `BLOCKED`: identify the cause, repair the packet or task boundary, and ask the user
  only for a missing decision or permission.

Do not blindly repeat failed fixes. A selected debugger can own a bounded root-cause
investigation when new evidence justifies the changed route.

## Review and finish

For an `audit` or `full` route, after primary verification use one fresh reviewer and
[requesting-code-review](../requesting-code-review/SKILL.md) on a fixed change boundary.
One reviewer normally runs both Standards and Spec passes. The optional separate
[Spec reviewer](spec-reviewer-prompt.md) and
[Standards reviewer](code-quality-reviewer-prompt.md) help only when a specific risk
or explicit requirement warrants split ownership; they do not automatically add agents.

A reviewer does not fix findings. The primary or original owner applies a correction,
re-verifies it, and obtains a fresh review of the changed result. Complete only when
scope, acceptance criteria, relevant checks, integration, and any required review pass.
