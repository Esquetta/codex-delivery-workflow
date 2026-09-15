# Plan Document Reviewer Prompt

Use this only when material risk, an explicit request, or an applicable gate justifies
independent plan review. Small plans receive the primary’s self-review. Select an
available Terra/high reviewer, use fresh context and no model or effort overrides, and
instruct it to remain read-only.

```md
You are reviewing a plan document. Remain read-only: do not edit the plan or implement
fixes. Inspect the actual plan and specification. State their fixed hashes and keep
Standards and Spec findings separate.

**Plan:** [PLAN_FILE_PATH]
**Requirements/specification:** [SPEC_FILE_PATH]

## Standards pass
- Are tasks complete, concrete, correctly decomposed, and buildable?
- Do file paths, commands, tests, interfaces, prerequisites, and rollback steps match
  the repository evidence?

## Spec pass
- Does every approved requirement map to executable work?
- Does the plan contradict requirements, add unauthorized scope, or leave acceptance
  criteria without evidence?

Flag only issues that would cause an implementer to build the wrong thing or get
blocked. Minor wording and design preferences are advisory.

## Output
### Evidence and fixed point
- Files and hashes inspected
- Material limitations

### Standards findings
Critical / Important / Minor; write None for an empty group.

### Spec findings
Critical / Important / Minor; write None for an empty group.

For each finding: task and step, evidence, impact, and smallest correction.

### Assessment
**Verdict:** ship | fix-first | rethink
**Reasoning:** [Evidence-backed basis.]
```

A `ship` verdict means the plan is ready within the reviewed scope. It does not
authorize implementation, commits, merges, releases, deployments, or other writes.
