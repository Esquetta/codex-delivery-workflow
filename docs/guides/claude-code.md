# Claude Code compatibility

This adapter was checked against official documentation on 2026-09-29. It packages the same 120 specialists and two starter roles as native Claude Code Markdown definitions. It does not run Claude from Codex or provide a new orchestration service.

## Instructions and skills

The repository root `CLAUDE.md` imports `@AGENTS.md`, keeping shared rules in one place. To adopt them, review both files, merge them into the target project's existing instructions, and keep them together. Adapt the documentation link in `CLAUDE.md` if the target does not contain this documentation tree. Do not replace personal global instruction files.

The six shared skills branch on the actual host. Their existing `codex-delivery-workflow` name remains for compatibility; the name does not limit execution to Codex. Install the starter skill alone or all six together. Native Claude dispatch uses the installed subagent name and its native Agent interface, not Codex-specific delegation arguments.

## Models and permissions

| Purpose | Claude model | Tools |
| --- | --- | --- |
| Task execution with source write access or unspecified sandbox | `sonnet` | Read, Grep, Glob, Edit, Write, Bash |
| Source read-only specialist | `sonnet` | Read, Grep, Glob |
| `delivery-reviewer`, `reviewer`, `code-reviewer` | `opus` | Read, Grep, Glob |

These are workflow defaults, not performance benchmark results. Keep the user's primary model choice. Aliases resolve differently by provider, installed Claude Code version, and account configuration, and can change over time. Inspect the actual model before accepting a result. This adapter does not copy OpenAI's `high` reasoning setting into Claude; Claude effort follows its native configuration.

Every generated role uses `permissionMode: default`. A tool allowlist is not an operating-system sandbox. Parent permission settings and host policies can affect enforcement. Read-only profiles cannot run shell tests or browse via Bash; the primary supplies the relevant command output or gathered evidence. No MCP servers, hooks, permission bypass, credentials, or nested-agent tool access are bundled.

## Install and smoke test

Follow the [installation guide](installation.md). In a fresh Claude session, inspect the loaded instructions, discovered skills, selected agent, resolved model, and allowed tools. Try a read-only code-mapping task, then a bounded edit in a disposable project and a fresh review of its actual diff. Confirm that the reviewer cannot edit or execute shell commands and that the primary provides test results. File generation alone does not prove discovery or enforcement.

No live Claude Code smoke test was performed for this repository update because Claude Code was unavailable on the validation host. Static package checks and regression tests cover the adapter, not the Claude service.

## Maintaining the adapter

Codex TOMLs and their catalog are the source. After changing an approved source profile, run:

```sh
python -X utf8 scripts/export_claude.py
python -X utf8 scripts/export_claude.py --check
python -X utf8 scripts/validate.py
python -B -m unittest discover -s tests -v
```

Review the generated diff. The exporter does not install profiles or alter global settings. Model policy and tool mapping live in the exporter; do not hand-edit generated profiles. The check mode detects drift and unexpected generated files without writing.

## Official references

- [Subagent files, models, tools, and permission modes](https://code.claude.com/docs/en/sub-agents)
- [Shared project instructions and imports](https://code.claude.com/docs/en/memory)
- [Skill directories and discovery](https://code.claude.com/docs/en/skills)
- [Model aliases and native configuration](https://code.claude.com/docs/en/model-config)
