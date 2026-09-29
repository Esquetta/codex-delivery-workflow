# Implementer Prompt

Identify the host before dispatch. On Codex, select an available Terra/high domain
specialist and use `delivery_worker` with the starter pack; omit model and effort
overrides for its pinned role. On Claude Code, use a native `Agent` with an installed
normalized `subagent_type`, including `delivery-worker` with the starter pack. Do not
send Codex dispatch fields or copy Codex effort. Adapt this packet to applicable
repository instructions.

```md
## OBJECTIVE
[Exact task, observable outcome, and relevant architecture.]

## FILES AND OWNERSHIP
[Working directory, branch/worktree, exact files/modules, and concurrent work to preserve.]
Do not change files outside this scope or expand an interface without a primary decision.

## INTERFACES
[Signatures, schemas, behavior, dependencies, and compatibility to preserve.]

## CONSTRAINTS
[Settled decisions, repository instructions, exclusions, and existing authorization.]
Make the smallest change. Do not refactor adjacent code. Report material ambiguity before
dependent work. Do not request approval already supplied. Commit or write externally
only when separately authorized.

## VERIFICATION
[Exact commands, meaningful success/failure paths, and expected results.]
Use behavior-focused tests where they protect a meaningful regression. Self-review
scope, correctness, completeness, and evidence. Do not conceal failed checks or limits.

## RETURN
Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
- Actual files changed and behavior delivered
- Exact checks and observed results
- Self-review findings and decisions
- Missing context, residual risks, and incomplete work

If blocked, explain the evidence, attempts, and needed decision. Do not silently
redesign architecture or keep retrying without a new hypothesis.
```
