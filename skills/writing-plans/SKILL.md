---
name: writing-plans
description: Write implementation-ready plans for approved multi-step work before code changes begin.
---

# Writing Plans

Write an implementation plan when requirements are clear enough to define a
multi-step change but code work has not begun. A plan must let a capable developer who
does not know the repository implement and verify the work without filling in missing
design decisions. It is not authorization to implement, integrate, or publish.

For public repositories, do not create a default `docs/superpowers/` archive. Put a
user-approved private working plan in the location they specify, or return it directly
for review. Do not auto-commit a plan.

## Map before drafting

Read the request, repository instructions, relevant code paths, tests, and current
workspace state. Record the outcome, affected users, architecture, interfaces,
compatibility constraints, test strategy, and files that each task owns. Keep primary
architecture and scope decisions with the primary session. If independent subsystems
need incompatible designs, split the plan before implementation.

## Plan format

Start with:

```md
# [Feature] Implementation Plan

**Goal:** [One observable result.]

**Architecture:** [The selected approach and preserved interfaces.]

**Prerequisites:** [Permissions, environment, migrations, or setup required.]
```

Then give each task exact files and bite-sized steps:

```md
### Task N: [Component]

**Files:**
- Modify: `path/to/file`
- Test: `path/to/test`

- [ ] **Step 1: Establish the regression or acceptance check**
  Run: `project-specific command`
  Expected: [Observed failure or current behavior.]

- [ ] **Step 2: Make the minimal implementation change**
  [Exact behavior, interface, and code-level direction needed.]

- [ ] **Step 3: Verify the result**
  Run: `project-specific command`
  Expected: [Pass condition and relevant outcome.]
```

Name exact paths, commands, expected outcomes, behavior, signatures, and migration or
rollback steps when they matter. Include test code or a concrete test case when the
task changes behavior. Do not leave `TODO`, `TBD`, “add validation,” “handle edge
cases,” “write tests,” or references to undefined future work.

## Self-review and handoff

Check each requirement has a task; check later names and interfaces match earlier
definitions; scan for placeholders; and verify paths and commands against the
repository. Use a fresh independent plan review only for material risk, an explicit
request, or an applicable gate; see [plan-document-reviewer-prompt.md](plan-document-reviewer-prompt.md).

If implementation is already authorized, hand off to
[executing-plans](../executing-plans/SKILL.md),
[subagent-driven-development](../subagent-driven-development/SKILL.md), or
[dispatching-parallel-agents](../dispatching-parallel-agents/SKILL.md) according to
ownership and dependencies. Do not request the same approval again. If the request was
planning only, return the complete plan and wait for implementation authorization.
