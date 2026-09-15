# Worked examples and evidence

These examples distinguish public artifacts from an author's account of how work was coordinated. Public code can show what shipped; it cannot reconstruct every private agent interaction or establish a token-saving claim.

## 1. Publishing the original workflow reference

**Real work:** the first release of this repository, [commit 834c938](https://github.com/Esquetta/codex-delivery-workflow/commit/834c938a311ff5e2215f4561e528f992c8fd1029), published ten files: two starter roles, a routing skill, fictional packets, documentation, notices, and a validator.

**Sanitized author account:** a scoped authoring worker prepared the local package while the primary updated the public profile. The primary reviewed the package and requested explicit native role names and invalidation of review after any implementation change. An independent reviewer then inspected the final files before publication.

The primary ran the static validator and an in-memory negative check that changed the worker sandbox to the reviewer sandbox; the validator rejected the mismatch. This is a historical account of that run, not a new test result and not proof that the sample roles were installed.

**Publicly inspectable result:** the commit contains the final role names, two-pass review rules, license notices, and validation code. The private tool transcript and account configuration are intentionally not published. There is no claim that the commit alone proves which model or sandbox executed the authoring work.

**Lesson:** a small starter can be valid but still underrepresent an operational workflow. The current expansion adds the catalog and workflow relationships without claiming that more files mean better execution.

## 2. Archive preflight in Codex Plugin Doctor

**Real public change:** [PR #28](https://github.com/Esquetta/CodexPluginDoctor/pull/28) added bounded, no-extraction ZIP submission preflight and was merged as [6cf8c39](https://github.com/Esquetta/CodexPluginDoctor/commit/6cf8c39d25cabdcd0786a976168b5dc14653bd51).

The PR describes CLI/JSON/Action integration, ZIP64 and descriptor handling, path/type/CRC checks, resource budgets, privacy, and regression coverage. Its test plan reports a test run, build, release check, audit, and malformed-archive harness. Those are the PR author's recorded results; they were not rerun while writing this case study.

The [public review discussion](https://github.com/Esquetta/CodexPluginDoctor/pull/28#discussion_r3850599636) also raises a specific structural-validation concern. A review comment is a finding to investigate, not proof of a defect or a substitute for verifying the final implementation.

**How the current workflow would scope this class of change:** this is an illustrative routing analysis of a real change, not a claim that today's agent names or six-skill pack were used for that historical PR.

| Responsibility | Suggested owner | Required evidence |
| --- | --- | --- |
| No-extraction/offline contract, supported formats, report semantics | Primary | Approved scope and explicit invariants |
| Reader and preflight implementation | One backend/TypeScript owner | Actual diff and bounded parser behavior |
| Malformed archive regression cases | Same owner, or an independent test owner after interfaces settle | Reproducible fixtures and results |
| CLI/Action contract integration | Primary or scoped integration owner | Existing directory mode remains compatible |
| Standards and Spec review | Fresh reviewer | Safety and scope checked separately on a fixed result |
| Release | Primary within existing authorization | Package/release identity and independent read-back |

This example shows why a green build alone is insufficient: a parser can compile while missing structural or resource-bound checks. It also shows why a specialized test task needs settled interfaces before parallel implementation.

## Use the packets

The [order-submission task packet](../../examples/task-packet.md) and [review packet](../../examples/review-packet.md) remain **fictional templates**. Replace their scope and evidence with the real task; never present their sample verification statements as observed results.

No customer identities, credentials, private repository links, financial details, or private session logs are needed to explain these workflows.
