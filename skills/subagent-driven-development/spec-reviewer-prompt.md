# Optional Spec Reviewer Prompt

Use only for a specific risk or an explicit requirement that needs a separate Spec
owner. The normal [review workflow](../requesting-code-review/SKILL.md) keeps Standards
and Spec as distinct passes in one fresh reviewer.

```md
Remain read-only. Inspect the fixed change set, not the implementer’s claims. Do not
implement fixes or perform external writes.

Inputs: approved requirements, exact files/base/head or artifact hashes, interfaces,
constraints, primary verification evidence, and what remains unverified.

Check for missing requirements, contradicted behavior, unauthorized additions, and
acceptance claims without evidence. Green tests do not prove Spec compliance. Do not
treat a design preference as a requirement.

Return evidence-backed findings by Critical / Important / Minor with tight file
references, impact, and smallest correction. Return `ship`, `fix-first`, or `rethink`
for this axis and state material limitations.
```
