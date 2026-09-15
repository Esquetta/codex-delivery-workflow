# Testing and debugging

Use this procedure for a defect, failing test, or unexpected behavior. Commands below
are illustrative; replace them with commands documented by the repository and record
the observed output.

1. **Reproduce.** Capture the trigger, inputs, environment, current behavior, expected
   behavior, and the smallest repeatable command or test. If the failure cannot be
   reproduced, say which evidence is missing instead of claiming a cause.
2. **Form a hypothesis.** Trace the relevant path and state one explanation that the
   available code, logs, or test output can confirm or reject. Group failures that may
   share a dependency before assigning separate investigations.
3. **Make the minimal fix.** Change only the owned code needed to test the hypothesis.
   Preserve public interfaces and concurrent work. Do not refactor nearby code during a
   diagnosis.
4. **Run a targeted regression.** Add or update a behavior-focused test where it
   protects a meaningful regression; run the smallest check that proves the reported
   path now works and relevant failure behavior remains correct.
5. **Broaden only when justified.** Run integration or full-suite checks when the
   affected interface, risk, or repository policy requires them. Record the exact
   command, result, and remaining limits.

```powershell
# Illustrative only. Replace with the repository's targeted check.
<test-command> <affected-test-or-filter>
```

Do not blindly retry a failing command, weaken assertions, expand timeouts, or call a
failure intermittent without new evidence. A repeated failure means the hypothesis,
test setup, dependency state, ownership, or scope needs investigation.

For a small, known issue, the primary can follow this procedure directly. A dedicated
debugger is useful only for an independent, bounded root-cause investigation with a
clear entry point and return evidence. A test specialist is useful only when test work
has independent file ownership and a settled interface; it is not a default extra
reviewer. Use the packet rules in
[codex-delivery-workflow](../../skills/codex-delivery-workflow/SKILL.md) and inspect
actual changes before accepting a worker report.

External TDD or debugging skills may provide additional process when installed, but this
pack has no hard dependency on them. Preserve repository contracts such as required
test commands, database migrations, environment variables, compatibility policies, and
integration gates. Passing a test proves only the exercised behavior; it does not prove
that every requirement is met. Use the fixed-point Standards and Spec review procedure
for material-risk or review-gated changes.
