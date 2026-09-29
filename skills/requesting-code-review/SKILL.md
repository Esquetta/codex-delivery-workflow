---
name: requesting-code-review
description: Review a fixed change against requirements and repository standards with separate Standards and Spec evidence passes.
---

# Requesting Code Review

Review a fixed change boundary through two independent evidence passes. A trivial
change can be checked by the primary; use a fresh reviewer for material risk, an
explicit review request, or an applicable repository gate. Identify the host before
selecting a reviewer. On Codex, select the available Terra/high `delivery_reviewer` in
the starter pack or a runtime-available `reviewer`, use fresh context (`fork_turns:
none`), and attach no model or effort overrides to a pinned role. On Claude Code, use
a fresh native `Agent` with `subagent_type` `delivery-reviewer` or a normalized
`reviewer`; do not fork the parent conversation and do not send Codex dispatch fields.
The Claude aliases are account-available runtime names, not fixed model IDs or a claim
of equivalent model behavior.

## Fix the review boundary

Use an explicit fixed point:

```powershell
# Illustrative commands: replace refs with this repository's review range.
git rev-parse <base-ref>
git rev-parse HEAD
git diff --stat <base-sha>..<head-sha>
```

For uncommitted work, capture the exact diff and file hashes. For non-Git work, capture
the changed files and hashes or supplied before/after artifacts. Recheck the fixed point
before acceptance: any change invalidates the verdict. Do not require a commit just to
review. If no fixed point exists, review only supplied evidence and state that limit.

## Two independent passes

### Standards

Inspect correctness, security, authorization and data-loss risks, repository
conventions, compatibility, error handling, maintainability, operational effects, and
tests that exercise real behavior and relevant failure paths.

### Spec

Inspect the same boundary for every approved requirement, contradictions, unauthorized
scope, and evidence for acceptance claims. Green tests do not prove Spec fidelity; a
design preference is not a Spec violation.

## Request and act

Use [code-reviewer.md](code-reviewer.md) as the read-only reviewer prompt. Supply what
was implemented, approved requirements, fixed range or artifacts, interfaces,
constraints, and primary verification evidence. Do not send the parent’s intended
verdict. The reviewer returns `ship`, `fix-first`, or `rethink` with evidence.

Fix Critical findings before proceeding. Fix Important findings before merge unless the
requirement owner accepts the risk. Minor findings are advisory. The reviewer never
implements fixes. After a correction, the owner re-verifies and a fresh reviewer checks
the revised fixed point.

Review never authorizes commit, merge, push, comments, labels, releases, deployments,
or other external writes. Completion requires an explicit boundary or limitation,
separate Standards and Spec findings, evidence and impact for every finding, calibrated
severity, and a verdict that accounts for blocking findings on either axis.
