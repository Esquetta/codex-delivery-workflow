# Claude Code project adapter

@AGENTS.md

Use the shared project rules above and the installed delivery workflow skill.

- Use native Claude Code subagents and their installed names; do not send Codex tool parameters to Claude.
- Profiles under `claude/agents/` are distribution files. They become available only after deliberate installation into a Claude agent directory.
- Select task owners from the Claude catalog. Preserve the user's chosen primary model. Specialists use `sonnet`; independent delivery/code reviewers use `opus`.
- Use the actual host model and tool metadata. Alias resolution and permissions depend on the running environment; static files are not runtime proof.
- Read-only reviewers receive explicit evidence packets and have only Read, Grep, and Glob. The primary runs verification and provides outputs. Do not grant extra tools merely to complete a review.
- Keep existing user authorization boundaries for outbound messages, commits, publication, and deployment.

See [Claude Code compatibility](docs/guides/claude-code.md) for model and permission details. When adopting these instructions into another project, adapt or remove this documentation link.
