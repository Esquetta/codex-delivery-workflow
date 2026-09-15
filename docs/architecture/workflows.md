# Delivery workflow architecture

This pack describes a delivery decision flow for a primary Codex session. The primary
keeps requirements, architecture, scope, integration judgment, and acceptance. Workers
own only bounded tasks; reviewers inspect a fixed result and do not fix it.

```mermaid
flowchart TD
    A[Requirements and constraints] --> B[Map code paths, interfaces, and current workspace]
    B --> C{Known scope and risk?}
    C -->|Small, tightly coupled| D[Solo execution]
    C -->|Multi-step work| E[Write implementation plan]
    E --> F{Ownership independent?}
    F -->|No| G[Execute plan sequentially]
    F -->|Yes| H[Dispatch bounded owners]
    D --> I[Targeted verification]
    G --> I
    H --> J[Primary inspects changes and integrates]
    J --> I
    I --> K{Material risk, requested review, or repository gate?}
    K -->|No| L[Prepare verified result]
    K -->|Yes| M[Fresh reviewer: Standards and Spec]
    M --> N{ship?}
    N -->|fix-first or rethink| O[Owner corrects; primary re-verifies]
    O --> M
    N -->|ship| L
    L --> P{Integration separately authorized?}
    P -->|Yes| Q[Commit, merge, push, release, or deploy as authorized]
    P -->|No| R[Report evidence and remaining limits]
```

| Decision or stage | Included skill | Responsibility |
|---|---|---|
| Route selection and packet contract | [codex-delivery-workflow](../../skills/codex-delivery-workflow/SKILL.md) | Select solo, delegate, audit, or full; keep scope and acceptance with the primary. |
| Multi-step design | [writing-plans](../../skills/writing-plans/SKILL.md) | Make file ownership, interfaces, commands, and acceptance checks executable. |
| Tightly coupled execution | [executing-plans](../../skills/executing-plans/SKILL.md) | Execute the approved plan with targeted evidence. |
| Specialist ownership | [subagent-driven-development](../../skills/subagent-driven-development/SKILL.md) | Send a complete bounded packet and inspect the returned diff and tests. |
| Independent concurrency | [dispatching-parallel-agents](../../skills/dispatching-parallel-agents/SKILL.md) | Run only ownership-independent work and integrate it deliberately. |
| Fixed-point review | [requesting-code-review](../../skills/requesting-code-review/SKILL.md) | Keep Standards and Spec as separate passes and return a clear verdict. |

The starter pack names `delivery_worker` and `delivery_reviewer`. A broader installed
catalog can select a runtime-available specialist such as `code-mapper` for a bounded
execution map, `backend-developer` or `fullstack-developer` for implementation,
`react-specialist` or `angular-architect` for UI work, `debugger` for a bounded
root-cause investigation, and `test-automator` only for independent test ownership.
Do not select a role merely because it appears in a catalog. A saved profile or catalog
snapshot is configuration, not proof that the role is available, routed, or running.

Installing sibling folders does not guarantee global synchronization with local skills,
plugins, configuration, or a role catalog. Runtime availability, model metadata,
permissions, and isolation must be checked in the active environment. The workflow
never overrides higher-priority instructions or grants integration authority.

Attribution for exported workflow sources is retained in the repository
[NOTICE](../../NOTICE.md).
