# Installation and compatibility

Choose what to install. Browsing this repository installs nothing, and the 120-role catalog is not a recommendation to load every role.

The existing personal-root procedure below is for Codex. For Claude Code, use the project-scoped procedure at the end. Neither procedure installs or replaces global instruction files.

## Starter or full workflow pack

| Mode | Skills | Roles |
| --- | --- | --- |
| Starter | Only `codex-delivery-workflow` | `delivery_worker`, `delivery_reviewer` from the root agents folder |
| Full pack | All six skill directories | A small selection from `agents/specialists` |

The full pack links planning, execution, parallelism, and review. Copy all six folders together so their relative helper links survive installation. Its root-level examples and documentation remain repository references, not runtime dependencies.

The specialist snapshot and the starter roles are separate alternatives. In a run, choose a role that is actually available and appropriate; do not silently substitute another model when a configured role is missing.

## Check compatibility first

Use a Codex environment that supports personal skills and custom agent TOMLs. Model names in this repository reflect the source setup, not a promise of account availability. Verify available role/model/effort metadata on your host before delegation.

Check the active skill catalog before installing. Names such as `writing-plans` and `requesting-code-review` may already come from a personal folder or a plugin. Choose one authoritative version for a task. These commands do not disable plugins, alter global instructions, or overwrite existing files.

The scripts below cover default personal roots and an explicit `CODEX_HOME`. Project-local and other plugin skill roots may also exist; inspect the application's catalog. A collision in any active root should be resolved deliberately rather than hidden by a later copy.

## PowerShell: preflight, then copy

Run from the repository root. Choose `starter` or `full` and the specific roles before running this block. It changes only the selected skill and agent destinations.

```powershell
$ErrorActionPreference = 'Stop'
$deliveryRepo = (Get-Location).Path
$deliveryHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME '.codex' }
$deliveryMode = 'starter'
$deliveryRoleNames = @('code-mapper', 'fullstack-developer', 'reviewer')
$deliverySkillNames = if ($deliveryMode -eq 'starter') {
    @('codex-delivery-workflow')
} elseif ($deliveryMode -eq 'full') {
    @('codex-delivery-workflow', 'writing-plans', 'executing-plans',
      'subagent-driven-development', 'dispatching-parallel-agents', 'requesting-code-review')
} else { throw 'Choose starter or full.' }

$deliveryAgentNames = if ($deliveryMode -eq 'starter') {
    @('delivery_worker', 'delivery_reviewer')
} else { $deliveryRoleNames }
$deliveryAgentSource = if ($deliveryMode -eq 'starter') { 'agents' } else { 'agents/specialists' }
$deliveryCopies = @()

foreach ($deliveryName in $deliverySkillNames) {
    $deliverySource = Join-Path $deliveryRepo "skills/$deliveryName"
    $deliveryTarget = Join-Path $deliveryHome "skills/$deliveryName"
    $deliveryAlternate = Join-Path $HOME ".agents/skills/$deliveryName"
    if (-not (Test-Path -LiteralPath (Join-Path $deliverySource 'SKILL.md') -PathType Leaf)) {
        throw "Missing source skill: $deliveryName"
    }
    if ((Test-Path -LiteralPath $deliveryTarget) -or (Test-Path -LiteralPath $deliveryAlternate)) {
        throw "Existing personal skill: $deliveryName. Compare before installing."
    }
    $deliveryCopies += @{ Source = $deliverySource; Target = $deliveryTarget }
}
foreach ($deliveryName in $deliveryAgentNames) {
    if ($deliveryName -notmatch '^[a-z0-9][a-z0-9_.-]*$') { throw 'Invalid role name.' }
    $deliverySource = Join-Path $deliveryRepo "$deliveryAgentSource/$deliveryName.toml"
    $deliveryTarget = Join-Path $deliveryHome "agents/$deliveryName.toml"
    if (-not (Test-Path -LiteralPath $deliverySource -PathType Leaf)) { throw "Missing role: $deliveryName" }
    if (Test-Path -LiteralPath $deliveryTarget) { throw "Existing role: $deliveryName" }
    $deliveryCopies += @{ Source = $deliverySource; Target = $deliveryTarget }
}

foreach ($deliveryCopy in $deliveryCopies) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $deliveryCopy.Target) | Out-Null
    Copy-Item -LiteralPath $deliveryCopy.Source -Destination $deliveryCopy.Target -Recurse
}
```

This is a manually reviewed copy procedure, not a transaction-safe package manager. Do not run it concurrently with another installer.

## Other operating systems

The payload is text and uses relative paths. Copy the same selected folders/files to your Codex personal roots. Respect `CODEX_HOME` when configured. Preflight every source and destination before copying, and inspect other active skill roots for duplicate names. No operating-system-specific executable or runtime is bundled.

## Verify after installation

1. Reopen Codex and check the discovered skill names and chosen role names.
2. Read the installed core skill and relevant helper links. A copied file is not evidence that the app loaded it.
3. Verify the role's model/effort metadata and actual sandbox policy before accepting a delegated result.
4. Try a small read-only mapping task before using the pack on a real change. Record what actually ran.
5. If a model/role is unavailable, stop that lane and adapt the configuration intentionally.

The repository validator checks package consistency, not any of these runtime steps. Automated installation, background context synchronization, token benchmarking, and end-to-end host compatibility testing are not included.

## Claude Code: project-scoped installation

Choose an existing target project, then run from this distribution repository. This copies selected profiles into the target's `.claude/agents/` and skills into `.claude/skills/`. Starter names use hyphens. For the full pack, select names from [claude/catalog.json](../../claude/catalog.json).

Inspect active project, personal, and plugin catalogs for duplicate names first. The block checks the project destination and default personal roots; it cannot enumerate managed/plugin configuration. It intentionally does not overwrite files. Do not run concurrently with another installer.

```powershell
$ErrorActionPreference = 'Stop'
$deliveryRepo = (Get-Location).Path
$deliveryProject = Read-Host 'Existing target project directory'
if (-not (Test-Path -LiteralPath $deliveryProject -PathType Container)) { throw 'Target project must exist.' }
$deliveryProject = (Resolve-Path -LiteralPath $deliveryProject).Path
$deliveryMode = 'starter'
$deliveryRoleNames = @('code-mapper', 'fullstack-developer', 'reviewer')
$deliverySkillNames = if ($deliveryMode -eq 'starter') {
    @('codex-delivery-workflow')
} elseif ($deliveryMode -eq 'full') {
    @('codex-delivery-workflow', 'writing-plans', 'executing-plans',
      'subagent-driven-development', 'dispatching-parallel-agents', 'requesting-code-review')
} else { throw 'Choose starter or full.' }
$deliveryAgentNames = if ($deliveryMode -eq 'starter') {
    @('delivery-worker', 'delivery-reviewer')
} else { $deliveryRoleNames }
$deliveryAgentSource = if ($deliveryMode -eq 'starter') { 'claude/agents' } else { 'claude/agents/specialists' }
$deliveryCopies = @()
foreach ($deliveryName in $deliverySkillNames) {
    $deliverySource = Join-Path $deliveryRepo "skills/$deliveryName"
    $deliveryTarget = Join-Path $deliveryProject ".claude/skills/$deliveryName"
    if (-not (Test-Path -LiteralPath (Join-Path $deliverySource 'SKILL.md') -PathType Leaf)) { throw "Missing skill: $deliveryName" }
    if ((Test-Path -LiteralPath $deliveryTarget) -or
        (Test-Path -LiteralPath (Join-Path $HOME ".claude/skills/$deliveryName"))) { throw "Existing skill: $deliveryName" }
    $deliveryCopies += @{ Source = $deliverySource; Target = $deliveryTarget }
}
foreach ($deliveryName in $deliveryAgentNames) {
    if ($deliveryName -notmatch '^[a-z0-9][a-z0-9-]*$') { throw 'Use a Claude catalog name.' }
    $deliverySource = Join-Path $deliveryRepo "$deliveryAgentSource/$deliveryName.md"
    $deliveryTarget = Join-Path $deliveryProject ".claude/agents/$deliveryName.md"
    if (-not (Test-Path -LiteralPath $deliverySource -PathType Leaf)) { throw "Missing role: $deliveryName" }
    if ((Test-Path -LiteralPath $deliveryTarget) -or
        (Test-Path -LiteralPath (Join-Path $HOME ".claude/agents/$deliveryName.md"))) { throw "Existing role: $deliveryName" }
    $deliveryCopies += @{ Source = $deliverySource; Target = $deliveryTarget }
}
foreach ($deliveryCopy in $deliveryCopies) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $deliveryCopy.Target) | Out-Null
    Copy-Item -LiteralPath $deliveryCopy.Source -Destination $deliveryCopy.Target -Recurse
}
```

Review and merge the distribution's root [AGENTS.md](../../AGENTS.md) and [CLAUDE.md](../../CLAUDE.md) into the target project's instruction files separately. Keep `@AGENTS.md` in `CLAUDE.md` and keep both files at the same project root. Adapt its documentation link for the target. Existing project instructions must be reconciled, not overwritten. No personal global instruction file is involved.

On other operating systems, copy the same selected files and directories after equivalent collision checks. Users who intentionally prefer personal Claude installation can use `~/.claude/agents/` and `~/.claude/skills/`, but project instructions remain a separate adoption decision. Follow the [Claude smoke-test checklist](claude-code.md) after reopening the host.
