---
name: codex-delivery-workflow
description: "Route Codex delivery work through the smallest sufficient solo, delegate, audit, or full path with bounded ownership and evidence-based review."
---

# Codex Delivery Workflow

Use this portable reference to choose a delivery route. Native Codex performs the work; this skill does not provide distributed execution, memory synchronization, model availability, or a runtime sandbox guarantee.

Keep requirements, architecture, scope decisions, and final acceptance with the primary session. Prefer the smallest sufficient route:

- `solo`: primary plans, implements, verifies, and self-reviews a small known-scope change.
- `delegate`: a worker owns one bounded implementation or research packet; primary performs useful non-duplicate work and verifies the result.
- `audit`: primary implements and verifies, then a fresh reviewer examines a material-risk change or requested independent review.
- `full`: a worker implements a bounded area, primary verifies, then a fresh reviewer reviews the fixed result for broad or high-risk work.

Do not delegate merely to restate work already known to the primary. Give each delegate exact ownership, preserve concurrent work, and respect runtime concurrency including the primary. Do not encode a permanent slot count. Do not use per-spawn model or reasoning overrides for the supplied pinned roles.

## Native role invocation

Dispatch `delivery_worker` for a bounded `delegate` or `full` packet. After primary verification, dispatch `delivery_reviewer` for `audit` or `full` with `fork_turns: none` and no model or reasoning override. This supplies fresh reviewer context.

Before dispatch, verify exposed role availability and that its metadata matches Terra/high. The role TOML is configuration evidence only; it does not prove discovery or runtime routing. If either role is unavailable or conflicts with the expected metadata, stop that lane and report the mismatch rather than silently substituting another role.

## Delegate packet

Every worker packet must state:

- **Objective:** observable result and why it matters.
- **Files and ownership:** allowed files, modules, or research sources; exclusions and concurrent work to preserve.
- **Interfaces:** behavior, compatibility, signatures, schemas, or contracts to retain.
- **Constraints:** repository instructions, settled choices, permissions, and existing authorization.
- **Verification:** concrete checks and success criteria.
- **Return:** findings, actual changes, actual verification, decisions, incomplete work, and residual risk.

Distinguish a requested sandbox or permission from metadata actually observed at runtime. Configuration saved on disk is static evidence; it does not prove discovery, routing, or enforcement. Do not claim that installing this skill disables other plugins or skills.

## Independent review

For `audit` and `full`, provide a fresh read-only reviewer a fixed base/head range or exact artifacts and hashes, the approved requirements, changed scope, preserved interfaces, constraints, and primary verification evidence. The reviewer must inspect read-only and must never implement fixes.

Require two separate passes in one review:

1. **Standards:** correctness, safety, compatibility, maintainability, operational impact, and meaningful verification.
2. **Spec:** approved requirements, prohibited behavior, unauthorized scope, and acceptance evidence.

The reviewer returns `ship`, `fix-first`, or `rethink` with evidence and an explicit fixed-point limitation if needed. A review verdict never authorizes a commit, merge, push, release, or deployment.

If an implementation change follows review, the owner fixes it, the primary re-verifies it, and a new reviewer checks the revised fixed point. Fresh context is useful independence, but it is not evidence of different model-family independence. Report sandbox isolation only when runtime metadata establishes it.

The supplied worker recommends `gpt-5.6-terra` / `high` with `workspace-write`; the reviewer recommends `gpt-5.6-terra` / `high` with `read-only`. Preserve an explicitly selected primary model. A personal source preference may be `gpt-6-astra` / `medium`, subject to current account and runtime availability.
