---
name: executing-plans
description: Execute a reviewed implementation plan with explicit checkpoints and verification.
---

# Executing Plans

Use this skill when a written implementation plan is already approved for execution.
Read it critically before changing files. Preserve existing authorization: an approved
implementation plan does not require asking again, but it also does not authorize a
commit, push, merge, release, or deployment.

## Review the plan

1. Read the plan and map each task to its files, interfaces, and verification.
2. Inspect the current branch or workspace and preserve unrelated changes.
3. Raise a material gap before dependent work begins: an unknown requirement,
   contradictory interface, missing permission, or verification that cannot establish
   the requested result. Do not guess.
4. If the plan is executable, track the tasks with available tooling and proceed.

For Git work, use an isolated worktree when repository policy or the user requires it.
If an external worktree helper is installed, it is optional; otherwise inspect the
current branch and do not start on `main` or `master` without existing user consent.

## Execute and verify

For each task, make the smallest change that satisfies its acceptance criteria, then
run the stated targeted verification. Keep interfaces and concurrent work intact.
Use behavior-focused regression tests where a change can regress meaningful behavior;
do not add a test solely to mirror a low-impact implementation detail.

Reproduce a failure before changing code when a bug report is available. Form a
testable hypothesis, apply one minimal fix, and use the relevant regression check.
Do not repeat the same failed fix or broaden timeouts without new evidence.

Use `solo` execution for tightly coupled work. For useful bounded delegation, use
[subagent-driven-development](../subagent-driven-development/SKILL.md); for independent
tasks, use [dispatching-parallel-agents](../dispatching-parallel-agents/SKILL.md).
Follow the selected route's host-native dispatch and review requirement rather than
creating reviewers per task.

## Finish

Confirm that the executed work meets the plan, relevant checks pass, and remaining
limitations are explicit. For material-risk or review-gated work, obtain the fixed-point
review described in [requesting-code-review](../requesting-code-review/SKILL.md).
When integration is in scope, prepare the verified result for the user’s separately
authorized integration action. Otherwise report the changed files and evidence without
inventing a branch, commit, PR, or deployment workflow.
