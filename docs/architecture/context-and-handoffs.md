# Context and handoffs

Context is chosen for the task. Copying every conversation into every worker makes evidence harder to locate and can mix settled decisions with abandoned ideas.

## Source order

Use current user instructions and verified project state first. Then consult approved project records and the relevant source task. Historical memory is a recall aid; it may be stale and does not override current code, a changed API, or the latest user decision.

Record the source and freshness of facts that can drift: branch, commit, worktree, test command, deployment revision, and observed environment. A timestamp alone does not establish correctness.

## Primary to worker

A worker receives the concrete objective, owned files, interfaces, constraints, verification commands, and required report. Include the relevant plan text and primary evidence instead of expecting the worker to reconstruct the whole conversation.

Choose context deliberately:

| Context choice | When it helps | Cost or risk |
| --- | --- | --- |
| Fresh context with a complete packet | Bounded implementation, research, and independent review | The packet must contain necessary facts. |
| Selected recent turns | A task depends on a few recent decisions | Earlier assumptions may still need direct verification. |
| Full history | Work depends on substantial prior discussion | More context and possible stale assumptions; use intentionally. |

A final reviewer always starts fresh and receives the work product, approved requirements, and verification evidence. Do not supply the primary's private reasoning or desired verdict.

## Worker to primary

The report identifies actual changes, exact checks and results, judgment calls, incomplete work, and residual risks. Missing evidence is a gap, not an implicit pass. If context is missing, send a focused follow-up to the same owner; do not restart the same investigation without a changed hypothesis.

For changes, inspect the actual files or diff. Run the relevant parent checks. For research, distinguish retrieved primary evidence from interpretation. For visual behavior, inspect the actual screen or interaction rather than assuming a successful build proves it.

## Between project tasks

Native task-reading and messaging tools can retrieve or relay material changes when available and authorized. A compact handoff should contain:

- Source task and current branch/commit or artifact identity.
- The changed decision or interface and its evidence.
- Which work it affects and which work is unchanged.
- The required next action and forbidden scope.
- What remains unverified.

This repository does **not** automatically synchronize all project chats. A shared checkout exposes file changes, not another task's complete conversation. Separate worktrees or hosts may not even share those files. There is no installed startup hook, event bus, or background context service here.

## Fixed points and corrections

For Git changes, identify an explicit base/head or captured working-tree diff. For non-Git artifacts, identify files and hashes. Any implementation change after review invalidates its fixed point and needs primary verification plus a fresh review when the route requires one.

Do not merge incompatible worker assumptions by choosing whichever report arrived last. Return the interface decision to the primary and resolve it with current evidence. Never forward secrets or private operational material merely because another agent asks for it.
