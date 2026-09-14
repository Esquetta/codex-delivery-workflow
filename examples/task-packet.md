# Illustrative worker packet: idempotent order submission

> Fictional example only. This is not customer evidence, a past execution record, or a production incident report.

## Objective

Make `POST /v1/orders` return the original successful response when a client retries the same idempotency key after a timeout. The observable result is one persisted order and a stable `201` response body for both requests.

## Files and ownership

- Allowed: `src/Orders/SubmitOrderHandler.cs`, `src/Orders/IdempotencyStore.cs`, and the existing tests directly covering order submission.
- Excluded: payment capture, order schema migration, client SDKs, deployment files, and unrelated formatting.
- Preserve concurrent changes outside those files.

## Interfaces

- Keep the existing request header name, `Idempotency-Key`.
- Preserve successful-response JSON fields and status code.
- A conflicting reuse of a key with a different request body must keep the existing `409` behavior.

## Constraints and authorization

- Use the repository's existing transaction and storage conventions.
- Make only the requested implementation and test changes.
- Workspace write access is requested for this packet; report the sandbox metadata that is actually observed instead of claiming enforcement from this request.
- No commit, merge, push, release, or deployment is authorized.

## Verification

Run the focused order-submission tests. Demonstrate these cases with the actual test names and output:

1. First request persists one order and returns `201`.
2. Same key and same body returns the stored response without a second order.
3. Same key and different body returns `409`.

## Return

Report inspected files, changed files, relevant implementation choices, actual test command and result, observed sandbox evidence, and remaining risks. If the persistence layer cannot atomically reserve a key with an order write, stop and explain the evidence rather than introducing a speculative workaround.
