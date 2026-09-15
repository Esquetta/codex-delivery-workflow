---
name: dispatching-parallel-agents
description: Coordinate independent bounded work with non-overlapping ownership and primary integration.
---

# Dispatching Parallel Agents

Use parallelism only when tasks are independent. Several failures do not prove several
root causes: inspect shared dependencies first. Do not dispatch overlapping writes,
dependent tasks, or tests that compete for mutable services or ports. Sequence them or
isolate their resources.

## Before dispatch

For every task identify its exact files, settled interfaces, dependencies, shared
resources, constraints, and required evidence. Give every worker a self-contained
packet with objective, ownership, interfaces, constraints, verification, and return
format from [codex-delivery-workflow](../codex-delivery-workflow/SKILL.md). Preserve
worktrees and concurrent edits.

Select only runtime-available specialist roles; use the starter `delivery_worker` if
that is the installed option. Omit model and effort overrides for pinned Terra/high
roles. Respect the runtime slot limit, including the primary and descendants. Dispatch
in batches where needed, and retain useful primary work instead of creating workers
merely to wait. Do not duplicate investigation.

## Integrate

1. Read worker findings and inspect actual changes and verification evidence.
2. Check ownership, interfaces, and conflicting assumptions.
3. Run relevant targeted checks; broaden to integration checks only when the affected
   risk or repository requirements justify it.
4. Apply the selected route’s independent review requirement once to the appropriate
   fixed change set. Parallel execution does not require extra reviewers.
5. Accept only when results work together and remaining limits are explicit.

If workers reveal a shared cause, stop duplicate work and assign one owner. Send only
material context changes with a focused follow-up. Do not weaken assertions or increase
timeouts because tests fail. A worker report never authorizes integration or external
writes.
