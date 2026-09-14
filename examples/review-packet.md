# Illustrative review packet: idempotent order submission

> Fictional example only. Replace every placeholder with the real repository evidence before use.

## Review boundary

- Base: `<base-sha-or-artifact-hash>`
- Head: `<head-sha-or-artifact-hash>`
- Scope: `src/Orders/SubmitOrderHandler.cs`, `src/Orders/IdempotencyStore.cs`, and focused order-submission tests.
- Fixed-point check: compare the supplied range or artifact hashes again before accepting a verdict.

## Approved requirements

- A retry with the same `Idempotency-Key` and same body returns the original `201` response without creating another order.
- A conflicting reuse with a different body keeps the current `409` response.
- Payment capture, schema migration, client SDK changes, and deployment changes are out of scope.

## Primary evidence supplied

- The primary inspected the changed files and ran the focused order-submission tests.
- The test evidence covers first submission, equivalent retry, and conflicting reuse.
- This evidence is illustrative; do not report it as observed until real commands and outputs are supplied.

## Reviewer instructions

Remain read-only. Inspect only the stated fixed point and evidence. Report the actual observed sandbox metadata separately from this read-only request.

### Standards pass

Check correctness under retry, transaction and concurrency behavior, error handling, compatibility, security of stored request data, and whether tests exercise the intended failure paths.

### Spec pass

Independently check each approved requirement and confirm there is no payment, migration, SDK, deployment, or other unauthorized scope.

## Required response

State the reviewed fixed point and limitations. Separate Standards findings from Spec findings, grouping each by Critical, Important, and Minor. Every finding needs evidence, impact, and the smallest remediation. End with `ship`, `fix-first`, or `rethink`.

Do not edit files or implement fixes. If the owner makes any implementation change, invalidate this verdict and request a fresh reviewer after primary re-verification. The verdict does not authorize commit, merge, push, release, or deployment.
