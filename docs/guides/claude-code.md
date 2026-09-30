# Claude Code compatibility

This adapter was checked against official documentation on 2026-09-30. It packages the same 120 specialists and two starter roles as native Claude Code Markdown definitions. It does not run Claude from Codex or provide a new orchestration service.

## Instructions and skills

The repository root `CLAUDE.md` imports `@AGENTS.md`, keeping shared rules in one place. To adopt them, review both files, merge them into the target project's existing instructions, and keep them together. Adapt the documentation link in `CLAUDE.md` if the target does not contain this documentation tree. Do not replace personal global instruction files.

The six shared skills branch on the actual host. Their existing `codex-delivery-workflow` name remains for compatibility; the name does not limit execution to Codex. Install the starter skill alone or all six together. Native Claude dispatch uses the installed subagent name and its native Agent interface, not Codex-specific delegation arguments.

## Models and permissions

| Purpose | Claude model | Tools |
| --- | --- | --- |
| Task execution with source write access or unspecified sandbox | `sonnet` | Read, Grep, Glob, Edit, Write, Bash |
| `search-specialist` | `sonnet` | Read, Grep, Glob, WebSearch, WebFetch |
| Other source read-only specialist | `sonnet` | Read, Grep, Glob |
| `delivery-reviewer`, `reviewer`, `code-reviewer` | `opus` | Read, Grep, Glob |

These are workflow defaults, not performance benchmark results. Keep the user's primary model choice. Aliases resolve differently by provider, installed Claude Code version, and account configuration, and can change over time. Inspect the actual model before accepting a result. This adapter does not copy OpenAI's `high` reasoning setting into Claude; Claude effort follows its native configuration.

Every generated role uses `permissionMode: default`. A tool allowlist is not an operating-system sandbox. Parent permission settings and host policies can affect enforcement. Read-only profiles cannot run shell tests or browse via Bash; the primary supplies the relevant command output or gathered evidence. No MCP servers, hooks, permission bypass, credentials, or nested-agent tool access are bundled.

## Role-specific prerequisites

Checked against official documentation on **2026-09-30**:

- [Subagent tools](https://code.claude.com/docs/en/sub-agents#available-tools): `tools` is an allowlist covering built-in and MCP tools. Omitting it inherits available tools; this pack keeps explicit lists. Denials still apply. Reviewers keep only Read, Grep, and Glob.
- [Web tools](https://code.claude.com/docs/en/tools-reference#websearch-tool-behavior): `search-specialist` adds only `WebSearch` and `WebFetch`, not shell or write tools. Availability depends on provider and policy; unavailable external research is reported as BLOCKED, not simulated.
- [MCP permissions](https://code.claude.com/docs/en/permissions#mcp) and [subagent MCP scope](https://code.claude.com/docs/en/sub-agents#scope-mcp-servers-to-a-subagent): browser MCP names depend on the installation. The distribution configures no server and cannot perform live browser work as shipped. For an installed copy, select an already-authorized server and add only its observed, required tool names to `tools`. If a server reference is needed, `mcpServers` can name an existing configured server. Do not guess identifiers, inherit all tools, or create authentication as an incidental setup step.
- [MCP tool search](https://code.claude.com/docs/en/mcp#scale-with-mcp-tool-search): deferred tools may also require `ToolSearch`. Verify discovery and authorization in the actual host before dispatch; the browser role reports BLOCKED when prerequisites are absent and must not bypass them through Bash.
- [Model aliases](https://code.claude.com/docs/en/model-config#model-aliases): retain `sonnet` and `opus`; provider and account overrides affect resolution. These files do not establish the model that actually ran.
- [Memory imports](https://code.claude.com/docs/en/memory#import-additional-files): imports inside code spans or fenced blocks are literal examples. This package requires a standalone `@AGENTS.md` outside code; its current root import remains valid. This is a package convention, not a complete implementation of Claude's import parser.

## Install and smoke test

Follow the [installation guide](installation.md). In a fresh Claude session, inspect the loaded instructions, discovered skills, selected agent, resolved model, and allowed tools. Try a read-only code-mapping task, then a bounded edit in a disposable project and a fresh review of its actual diff. Confirm that the reviewer cannot edit or execute shell commands and that the primary provides test results. File generation alone does not prove discovery or enforcement.

No live Claude Code smoke test was performed for this update. Verification is limited to official documentation and local deterministic tests; no Claude subscription, login, installation, or new authorization was used.

When Claude access is available, manually check in a disposable project:

1. Inspect loaded instructions and unique agent names from the installed scope. If the agents directory was created during the session, restart. Confirm the resolved model rather than only the alias.
2. Run a read-only mapping task and verify the actual tools and evidence returned.
3. Ask `search-specialist` for a small cited web lookup. Confirm WebSearch/WebFetch availability or an honest BLOCKED result; no shell/write tools should be granted.
4. Before browser dispatch, inspect the authorized MCP server and exact tools. With no browser capability, expect BLOCKED. With deliberately configured tools, verify one browser reproduction and its evidence.
5. Make a bounded disposable edit, provide primary test output to a fresh reviewer, and confirm the reviewer has no write, shell, or MCP tools. Record host version, resolved model, observed tools, and results.

## Maintaining the adapter

Codex TOMLs and their catalog are the source. After changing an approved source profile, run:

```sh
python -X utf8 scripts/export_claude.py
python -X utf8 scripts/export_claude.py --check
python -X utf8 scripts/validate.py
python -B -m unittest discover -s tests -v
```

Review the generated diff. The catalog records SHA-256 hashes of generated UTF-8 profile content (normalized LF line endings). On subsequent exports, an obsolete profile is removed only when its prior catalog path is within the export layout and its normalized content still matches that hash. Unlisted files are preserved; modified owned files block export before any write. Hashes establish generation ownership, not a security boundary against a maliciously rewritten catalog.

Legacy catalogs without hashes cannot authorize deletion. Regenerate a reviewed, clean legacy export before removing or renaming source roles; if a legacy obsolete file already exists, reconcile it manually. Existing files without an ownership hash can be adopted only when they already match the desired output; otherwise export stops for manual reconciliation. Files colliding with new output paths receive the same protection. Export is not transactional; do not run it concurrently with an editor or another exporter. `--check` remains read-only and reports extra files, including preserved user files.

The exporter does not install profiles or alter global settings. Model policy and tool mapping live in the exporter; do not hand-edit generated profiles. The check mode detects drift and unexpected generated files without writing.

## Official references

- [Subagent files, models, tools, and permission modes](https://code.claude.com/docs/en/sub-agents)
- [Shared project instructions and imports](https://code.claude.com/docs/en/memory)
- [Skill directories and discovery](https://code.claude.com/docs/en/skills)
- [Model aliases and native configuration](https://code.claude.com/docs/en/model-config)
