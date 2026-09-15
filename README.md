# Codex Delivery Workflow

How I organize AI-assisted software development with a primary Codex session, specialist agents, explicit task ownership, and independent review.

This repository documents a real personal workflow and ships a portable version of its agent profiles and development skills. The first release contained only two starter roles. The expanded reference includes a **120-role specialist snapshot**, the **six-skill delivery workflow pack**, context and tool boundaries, and worked examples with stated evidence limits.

## Explore the system

| Question | Start here |
| --- | --- |
| What runs where, and what does each layer do? | [System architecture](docs/architecture/system.md) |
| How do planning, execution, tests, and review connect? | [Workflow map](docs/architecture/workflows.md) |
| Which specialist should own a task? | [Agent selection](docs/guides/agent-selection.md) and [machine-readable catalog](agents/catalog.json) |
| What context reaches an agent or another task? | [Context and handoffs](docs/architecture/context-and-handoffs.md) |
| How do I debug failures and verify changes? | [Testing and debugging](docs/guides/testing-and-debugging.md) |
| What happened in real work? | [Worked examples and evidence](docs/guides/worked-examples.md) |
| What should I install? | [Installation and compatibility](docs/guides/installation.md) |

## What is included

- **120 specialist profiles** in [agents/specialists](agents/specialists), captured from the source installation on 2026-09-15. All are configured for Terra / high. This is an inventory, not 120 simultaneously running agents.
- **Two separate starter roles:** [delivery_worker](agents/delivery_worker.toml) and [delivery_reviewer](agents/delivery_reviewer.toml). These were authored for the portable first release and are not counted in the 120-role snapshot.
- **Six skills:** [routing](skills/codex-delivery-workflow/SKILL.md), [planning](skills/writing-plans/SKILL.md), [execution](skills/executing-plans/SKILL.md), [delegated development](skills/subagent-driven-development/SKILL.md), [parallel work](skills/dispatching-parallel-agents/SKILL.md), and [review](skills/requesting-code-review/SKILL.md).
- [Task](examples/task-packet.md) and [review](examples/review-packet.md) packet examples.
- A standard-library [validator](scripts/validate.py) and [regression checks](tests/test_validate.py).

## Four routes, one accountable primary

| Route | Execution | Acceptance |
| --- | --- | --- |
| solo | Primary handles a small known-scope change. | Primary checks the actual result. |
| delegate | A selected specialist owns a bounded task while the primary does useful independent work. | Primary inspects changes and verification. |
| audit | Primary implements and verifies a material-risk change. | A fresh reviewer checks Standards and Spec separately. |
| full | Specialists implement scoped work; primary integrates and verifies it. | A fresh reviewer checks the fixed result. |

A new agent is not required for every phase. Shared-file work stays sequential unless it is genuinely isolated. Concurrency is limited by the running Codex environment and includes the primary. Missing context goes back to the owner; it is not a reason for blind retries.

The source setup prefers Astra / medium for the primary and Terra / high for specialists. These are configuration choices, not a guarantee of model availability or live routing. Preserve an explicitly selected primary model. A fresh reviewer provides context separation, not independent model training.

## Read before installing

Browse the catalog and select roles that match your work. The full catalog is not a recommended bulk installation. Existing skill names may collide with personal or plugin skills; the installation guide explains that boundary.

The repository does not contain personal account settings, credentials, local machine paths, private projects, session logs, or scheduled job-application instructions. It does not implement a new agent runtime or automatic cross-task context synchronization. Codex and connected tools perform execution.

Passing static validation does not prove that a particular host loaded a skill, used the configured model, enforced a sandbox, or ran an application correctly. We do not claim measured token savings or production reliability from the size of this catalog.

## Validate

Use Python 3.11 or newer from the repository root:

```sh
python -X utf8 scripts/validate.py
python -B -m unittest discover -s tests -v
```

Checks cover catalog/profile consistency, skill metadata, local and install-time links, required public documentation, and common accidental disclosure markers. The text scan is a guard against obvious mistakes, not a full secret scanner or security audit.

## Attribution

The specialist snapshot is locally adapted from [VoltAgent's awesome-codex-subagents](https://github.com/VoltAgent/awesome-codex-subagents). Routing and review draw on [Sol Advisor](https://github.com/DannyMac180/sol-advisor) and [Superpowers](https://github.com/obra/superpowers), alongside local workflow adaptations. The snapshot is not a claim that every file matches the latest upstream version. Copyright and MIT notices are retained in [NOTICE.md](NOTICE.md).
