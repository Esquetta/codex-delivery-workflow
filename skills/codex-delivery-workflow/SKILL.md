---
name: codex-delivery-workflow
description: Route Codex delivery work through the smallest sufficient solo, delegate, audit, or full path with bounded ownership and evidence-based review.
---

# Codex Delivery Workflow

Use this portable pack to route delivery work. It describes a workflow; it does not
provide execution slots, synchronize all installed skills, prove model availability,
or guarantee a sandbox. Keep requirements, architecture, interfaces, scope decisions,
and final acceptance with the primary session.

Preserve a primary model the user selected. The included worker and reviewer profiles
are configured for Terra/high; verify exposed role metadata before dispatch. A role
file is configuration evidence only, not proof of discovery, routing, or enforcement.
If the selected role is unavailable or does not match its expected metadata, stop that
lane and report the mismatch. Do not silently substitute a model or attach overrides
to a pinned role.

## Choose a route

- `solo`: the primary plans, implements, verifies, and self-reviews a small,
  known-scope change.
- `delegate`: one specialist owns a bounded implementation or research packet; the
  primary does useful non-duplicate work and verifies the result.
- `audit`: the primary implements and verifies, then a fresh reviewer inspects a
  material-risk change, an explicitly requested review, or a repository review gate.
- `full`: a specialist implements a bounded area, the primary verifies it, then a
  fresh reviewer inspects the fixed result for broad or high-risk work.

Do not delegate merely to restate information already known to the primary. One helper
is usually enough. Use parallel workers only when file ownership and interfaces are
independent; preserve concurrent edits and respect the runtime concurrency limit,
including the primary and descendants. Do not encode a permanent slot count.

Use the included `delivery_worker` and `delivery_reviewer` profiles when this starter
pack is all that is installed. A broader role catalog may instead supply a selected
installed specialist such as `backend-developer`, `fullstack-developer`,
`react-specialist`, `code-mapper`, `debugger`, or `test-automator`, and a `reviewer`.
Select only a role available at runtime. A catalog snapshot is configuration, not
runtime proof.

## Optional full-pack helpers

When the full pack is installed, use `writing-plans` for multi-step design,
`executing-plans` for solo or tightly coupled execution,
`subagent-driven-development` for bounded specialist ownership,
`dispatching-parallel-agents` for independent work, and
`requesting-code-review` for fixed-point review. They are optional sibling skills, not
runtime requirements for this starter skill.

Optional external
worktree, brainstorming, TDD, debugging, or integration skills can be used when
installed and applicable; their absence does not block this pack. Apply their relevant
behavior here: inspect before changing, keep work isolated when required, reproduce
before another fix, write meaningful regression coverage for behavior changes, and
never invent a commit, push, merge, or deployment authorization.

## Worker packet

Every delegated prompt supplies a complete bounded packet:

```md
## OBJECTIVE
[Observable result, why it matters, and the relevant architecture.]

## FILES AND OWNERSHIP
[Exact files/modules or research sources; current branch/worktree; concurrent work to preserve.]

## INTERFACES
[Signatures, schemas, behavior, dependencies, compatibility, and constraints to retain.]

## CONSTRAINTS
[Repository instructions, settled decisions, exclusions, permissions, and existing authorization.]

## VERIFICATION
[Commands or inspection evidence, meaningful success and failure paths, expected results.]

## RETURN
Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
- Actual changes and behavior delivered
- Exact checks and observed results
- Decisions, missing context, residual risks, and incomplete work
```

The owner changes only assigned files, self-reviews, and reports actual evidence.
The primary inspects the actual diff and verification before accepting a claim.
For `NEEDS_CONTEXT`, give the same owner the missing facts with a focused follow-up;
do not restart an unchanged investigation. For `BLOCKED`, correct an incomplete packet,
split an oversized task, or ask the user only for a missing decision or authorization.
Do not blindly retry a failed fix or switch a pinned model.

## Independent review

For `audit` and `full`, after primary verification dispatch a fresh read-only reviewer
with `fork_turns: none` and no model or reasoning override. Give it the approved
requirements, exact changed scope, interfaces, constraints, verification evidence,
and a fixed base/head range or exact artifacts and hashes. The reviewer never fixes its
own findings. When installed, `requesting-code-review` supplies the review template.

One reviewer performs two separate evidence passes on the same fixed point:

1. **Standards:** correctness, security, compatibility, failure paths,
   maintainability, operational effects, and meaningful tests.
2. **Spec:** required behavior, contradictions, unauthorized additions, and evidence
   for acceptance claims.

The reviewer returns `ship`, `fix-first`, or `rethink`. Green tests do not prove Spec
fidelity, and a design preference is not a requirement. If a correction changes the
reviewed artifact, the owning implementer or primary fixes it, the primary re-verifies,
and a fresh reviewer checks the revised fixed point. Fresh context is independent
review context, not evidence of different model-family independence.

A review verdict never authorizes a commit, push, merge, release, deployment, or other
external write. Report permission or sandbox enforcement only when runtime evidence
establishes it. Installing this pack does not disable plugins or change global policy.

When a reviewer runs under a broader observed sandbox, continue only if hard isolation
is not required, its prompt forbids writes, and the primary compares exact before/after
artifact state. If isolation is unknown, required hard isolation is absent, or a
mutation occurs, stop the review lane and report it. Do not silently repair a mutation
under the same verdict.
