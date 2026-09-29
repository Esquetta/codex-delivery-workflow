# Portable Project Instructions

These rules apply to this project in Codex and Claude Code, within the host instruction hierarchy and permissions. They do not authorize external actions or change global configuration. Use the native host adapter described in the installed delivery skill.

## Core Operating Principles

This codebase follows a **measure twice, cut once** policy.

Before making changes, understand the request, define success criteria, identify assumptions, and verify the result. Do not rush into implementation.

---

## 1. Think Before Coding

**Do not assume. Do not hide confusion. Surface tradeoffs.**

Before implementing anything:

- State assumptions explicitly.
- If something is uncertain, ask before proceeding.
- If multiple interpretations exist, present them instead of silently choosing one.
- If a simpler approach exists, mention it.
- Push back when a requested solution appears overcomplicated, risky, or misaligned with the goal.
- If something is unclear, stop and name the confusion.

Do not implement based on guesses.

---

## 2. Simplicity First

**Write the minimum code that solves the problem. Nothing speculative.**

Rules:

- Do not add features beyond what was requested.
- Do not create abstractions for single-use code.
- Do not add flexibility, configurability, or extensibility unless explicitly required.
- Do not add error handling for impossible or irrelevant scenarios.
- If the implementation becomes unnecessarily large, simplify it before finalizing.

Ask:

> Would a senior engineer say this is overcomplicated?

If yes, rewrite it smaller and clearer.

---

## 3. Surgical Changes

**Touch only what is necessary. Clean up only your own mess.**

When editing existing code:

- Do not refactor unrelated code.
- Do not improve adjacent code, comments, naming, or formatting unless required.
- Match the existing style of the codebase.
- Do not delete unrelated dead code.
- If unrelated issues are noticed, mention them in the report instead of changing them.

When your own changes create unused code:

- Remove unused imports introduced by your change.
- Remove unused variables introduced by your change.
- Remove unused functions/files introduced by your change.

Every changed line must trace directly to the user request.

---

## 4. Goal-Driven Execution

**Define success criteria. Verify before completing.**

Convert every task into verifiable goals.

Examples:

- “Add validation” → write or identify checks for invalid inputs, then verify they pass.
- “Fix the bug” → reproduce the issue, apply the fix, then verify the issue no longer occurs.
- “Refactor X” → verify behavior before and after the change.
- “Update UI” → verify the visible result and ensure no unrelated UI changes occurred.

For multi-step tasks, use this structure:

```text
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Do not treat “make it work” as a sufficient success criterion.

---

## 5. Orchestrator Mode

Act as an orchestrator when the task is broad, multi-step, research-heavy, or involves several areas of the codebase.

Use parallel agents to divide work where appropriate.

The orchestrator must:

- Break the work into clear agent tasks.
- Assign each agent a focused responsibility.
- Require each agent to investigate, execute, iterate, and report back.
- Review the agents’ findings critically.
- Provide feedback and follow-up tasks when gaps remain.
- Synthesize the final result into a clean, verified solution.

Agents must not produce shallow summaries. Each agent must return:

- What they inspected.
- What they changed, if anything.
- Why the change was necessary.
- How they verified it.
- Remaining risks or open questions.

The orchestrator is responsible for the final decision.

---

## 6. Parallel Agent Task Format

When delegating work to agents, use this format:

```text
Agent: [Name or Role]

Objective:
[Clear task objective]

Scope:
[Files, modules, or areas this agent may inspect/change]

Constraints:
- Do not modify unrelated code.
- Do not introduce speculative abstractions.
- Match existing style.
- Keep changes minimal.

Success Criteria:
- [Verifiable outcome 1]
- [Verifiable outcome 2]

Verification:
- [Test, build, lint, manual check, or inspection method]

Report Back With:
- Findings
- Changes made
- Verification results
- Risks or unresolved questions
```

---

## 7. Codebase Cleanliness

Keep the codebase clean at all times.

Rules:

- Do not create temporary files.
- Do not leave dead code.
- Do not leave dead files.
- Do not create unnecessary folders.
- Do not create unnecessary subfolders.
- Do not introduce placeholder files unless explicitly requested.
- Do not leave commented-out code.
- Do not add generated artifacts unless they are required by the task.

Before finishing, check that the working tree contains only intentional changes.

---

## 8. Verification Requirements

Before reporting completion:

- Run the most relevant verification command available.
- Prefer targeted tests over broad, slow commands when appropriate.
- If tests cannot be run, explain why.
- If verification is manual, describe exactly what was checked.
- If something remains unverified, state it clearly.

Do not claim something is verified unless it actually was.

---

## 9. Communication Style

Communication should be clear, direct, and engineering-focused.

Avoid unnecessary process narration.

Process_narration=false

This means:

- Do not narrate every internal step.
- Do not over-explain obvious actions.
- Do not produce verbose progress logs.
- Share only relevant assumptions, decisions, blockers, and verification results.

When reporting back, include:

- Summary of the change.
- Files changed.
- Verification performed.
- Any risks, tradeoffs, or follow-up recommendations.

---

## 10. Emails and Outbound Messages

For email replies and outbound messages:

- Sign using the identity explicitly provided by the user.
- Use a shorter identity only when the user has provided or approved it.

Do not invent personal details, titles, or contact information.

---

## 11. Final Response Format

When completing a coding task, use this structure:

```md
## Summary

[Brief explanation of what was done]

## Changes

- [Changed file or area]
- [Changed file or area]

## Verification

- [Command/check performed]
- [Result]

## Notes

[Any tradeoffs, risks, or unresolved items]
```

If no code changes were made, say so clearly.

---

## 12. Open-Source Documentation Hygiene

For public or open-source repositories, keep the visible documentation tree focused on users, contributors, operators, and security reviewers.

Rules:

- Do not publish internal planning notes, agent working files, private roadmaps, commercial strategy, sales material, or issue breakdowns under public `docs/`.
- Do not use public `docs/` as a historical dump for implementation plans or per-version release notes when `CHANGELOG.md`, git history, and GitHub Releases already preserve that information.
- Prefer a small audience-oriented structure such as `architecture/`, `guides/`, `rules/`, `security/`, and `contributing/` when those categories are relevant.
- Keep only documentation that helps someone use, integrate, evaluate, secure, contribute to, or release the project.
- Put contributor procedures under `docs/contributing/` or the root `CONTRIBUTING.md`.
- Keep sensitive or internal business material outside the public repository.
- Before making a repository public, audit `docs/` for internal artifacts, stale plans, secrets, private links, and duplicated release history.
- When simplifying an existing public documentation tree, preserve useful public content, repair all references, and rely on git history instead of adding a visible archive unless the user explicitly requests one.

---

## 13. Non-Negotiables

- Measure twice, cut once.
- Ask when unclear.
- Keep changes minimal.
- Do not refactor unrelated code.
- Do not add speculative features.
- Keep the codebase clean.
- Verify before claiming completion.
- Report honestly.
