"""Export the public role profiles as portable Claude Code subagents."""
from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CATALOG = "agents/catalog.json"
STARTERS = ("agents/delivery_worker.toml", "agents/delivery_reviewer.toml")
READ_TOOLS = ["Read", "Grep", "Glob"]
WRITE_TOOLS = [*READ_TOOLS, "Edit", "Write", "Bash"]
REVIEWERS = {"delivery-reviewer", "code-reviewer", "reviewer"}
SOURCE_NAME = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
GENERATED_PATH = re.compile(
    r"^claude/(?:catalog\.json|agents/[a-z0-9][a-z0-9-]*\.md|agents/specialists/[a-z0-9][a-z0-9-]*\.md)$"
)


def normalize_name(name: str) -> str:
    return name.replace("_", "-").replace(".", "-")


def parse_frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated frontmatter")
    fields: dict[str, object] = {}
    for line in text[4:end].splitlines():
        key, separator, value = line.partition(": ")
        if not separator or not key or key in fields:
            raise ValueError("invalid frontmatter field")
        fields[key] = json.loads(value)
    return fields


def source_sandbox(value: object) -> str:
    if value is None:
        return "unknown"
    if value == "read-only":
        return "read-only"
    if value == "workspace-write":
        return "write"
    raise ValueError(f"unsupported source sandbox mode: {value!r}")


def adapted_text(source_name: str, value: str) -> str:
    if source_name == "agent-installer":
        return (
            value.replace("Codex custom agents", "Claude Code custom agents")
            .replace("~/.codex/agents/", "the user-selected Claude Code agent directory")
            .replace(".codex/agents/", "the repository Claude Code agent directory")
            .replace("Codex agent directories", "Claude Code agent directories")
        )
    if source_name == "workflow-orchestrator":
        return (
            value.replace("Codex subagent workflow", "Claude Code subagent workflow")
            .replace("Codex executions", "Claude Code executions")
            .replace(
                "Codex auto-spawns, auto-synchronizes, or auto-integrates agents",
                "Claude Code automatically creates, coordinates, or integrates subagents",
            )
        )
    if source_name == "code-reviewer":
        return value.replace("Implement or recommend", "Recommend")
    return value


def source_notice(source: str) -> str:
    comments = []
    for line in source.splitlines():
        if line.startswith("#"):
            comments.append(line[1:].lstrip())
        elif line.strip():
            break
    if not comments:
        return ""
    return "<!--\n" + "\n".join(comments) + "\n-->\n\n"


def catalog_profile_paths(catalog: dict[str, object]) -> list[str]:
    entries = catalog.get("agents")
    if not isinstance(entries, list):
        raise ValueError("invalid source catalog entries")
    paths = []
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("invalid source catalog entry")
        name, path = entry.get("name"), entry.get("path")
        if not isinstance(name, str) or not SOURCE_NAME.fullmatch(name):
            raise ValueError("invalid source catalog name")
        expected = f"agents/specialists/{name}.toml"
        if path != expected:
            raise ValueError("invalid source catalog path")
        paths.append(path)
    if len(paths) != len(set(paths)):
        raise ValueError("duplicate source catalog path")
    return paths


def safe_target(root: Path, relative: str, *, generated: bool) -> Path:
    if generated and not GENERATED_PATH.fullmatch(relative):
        raise ValueError(f"invalid generated path: {relative}")
    target = root
    if target.is_symlink():
        raise ValueError(f"symlinked export root: {root}")
    for part in PurePosixPath(relative).parts:
        target /= part
        if target.is_symlink():
            raise ValueError(f"symlinked path is not allowed: {relative}")
    return target


def markdown(profile: dict[str, object], source_path: str, tools: list[str], notice: str) -> str:
    source_name = str(profile["name"])
    name = normalize_name(source_name)
    fields = {
        "name": name,
        "description": adapted_text(source_name, str(profile["description"])),
        "model": "opus" if name in REVIEWERS else "sonnet",
        "tools": tools,
        "permissionMode": "default",
    }
    frontmatter = "\n".join(
        f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in fields.items()
    )
    instructions = adapted_text(source_name, str(profile["developer_instructions"])).strip()
    if name in REVIEWERS:
        instructions += (
            "\n\nReview-only operating limits:\n"
            "- Never edit files or execute tests, builds, or other checks.\n"
            "- Base conclusions on the primary agent's supplied evidence and the fixed review scope."
        )
    return "---\n" + frontmatter + "\n---\n\n" + (
        f"<!-- Generated from public source profile: {source_path}. "
        "Attribution and license details are in NOTICE.md. Claude model aliases are intentionally unpinned. -->\n\n"
    ) + notice + instructions + "\n"


def load_profile(files: dict[str, str], path: str) -> dict[str, object]:
    try:
        profile = tomllib.loads(files[path])
    except KeyError as error:
        raise ValueError(f"missing source profile: {path}") from error
    except tomllib.TOMLDecodeError as error:
        raise ValueError(f"invalid source profile: {path}") from error
    required = {"name", "description", "developer_instructions"}
    if not required <= set(profile) or not all(isinstance(profile[key], str) for key in required):
        raise ValueError(f"invalid source profile fields: {path}")
    source_name = str(profile["name"])
    if not SOURCE_NAME.fullmatch(source_name) or source_name != PurePosixPath(path).stem:
        raise ValueError(f"profile name/path mismatch: {path}")
    profile.setdefault("sandbox_mode", None)
    return profile


def build_outputs(files: dict[str, str]) -> dict[str, str]:
    try:
        catalog = json.loads(files[SOURCE_CATALOG])
    except KeyError as error:
        raise ValueError(f"missing source catalog: {SOURCE_CATALOG}") from error
    except json.JSONDecodeError as error:
        raise ValueError("invalid source catalog") from error
    if not isinstance(catalog, dict):
        raise ValueError("invalid source catalog entries")

    sources = [*STARTERS, *catalog_profile_paths(catalog)]

    profiles = [(path, load_profile(files, path)) for path in sources]
    normalized: set[str] = set()
    outputs: dict[str, str] = {}
    entries = []
    for source_path, profile in profiles:
        source_name = str(profile["name"])
        name = normalize_name(source_name)
        if name in normalized:
            raise ValueError(f"normalized Claude agent name collision: {name}")
        normalized.add(name)
        sandbox = source_sandbox(profile["sandbox_mode"])
        tools = READ_TOOLS if name in REVIEWERS or sandbox == "read-only" else WRITE_TOOLS
        relative = (
            f"claude/agents/{name}.md"
            if source_path in STARTERS
            else f"claude/agents/specialists/{name}.md"
        )
        content = markdown(profile, source_path, tools, source_notice(files[source_path]))
        outputs[relative] = content
        entries.append({
            "source_name": source_name,
            "name": name,
            "source_path": source_path,
            "path": relative,
            "model": "opus" if name in REVIEWERS else "sonnet",
            "tools": tools,
            "permissionMode": "default",
            "source_sandbox_mode": sandbox,
        })

    entries.sort(key=lambda entry: entry["source_path"])
    outputs["claude/catalog.json"] = json.dumps({
        "snapshot_date": catalog.get("snapshot_date"),
        "provider": "anthropic",
        "model_policy": {"default": "sonnet", "review": "opus"},
        "agents": entries,
    }, indent=2, ensure_ascii=False) + "\n"
    return dict(sorted(outputs.items()))


def read_sources(root: Path) -> dict[str, str]:
    catalog_target = safe_target(root, SOURCE_CATALOG, generated=False)
    files = {SOURCE_CATALOG: catalog_target.read_text(encoding="utf-8")}
    catalog = json.loads(files[SOURCE_CATALOG])
    paths = [*STARTERS, *catalog_profile_paths(catalog)]
    for path in paths:
        files[path] = safe_target(root, path, generated=False).read_text(encoding="utf-8")
    return files


def check_outputs(root: Path, expected: dict[str, str]) -> list[str]:
    errors = []
    for path, content in expected.items():
        target = root / path
        if not target.is_file():
            errors.append(f"missing generated file: {path}")
        elif target.read_text(encoding="utf-8") != content:
            errors.append(f"stale generated file: {path}")
    directory = root / "claude"
    if directory.is_dir():
        for target in sorted(path for path in directory.rglob("*") if path.is_file()):
            path = target.relative_to(root).as_posix()
            if path not in expected:
                errors.append(f"extra generated file: {path}")
    return errors


def write_outputs(root: Path, outputs: dict[str, str]) -> None:
    targets = [(safe_target(root, path, generated=True), content) for path, content in outputs.items()]
    for target, content in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report stale, missing, or extra generated files")
    args = parser.parse_args(argv)
    expected = build_outputs(read_sources(ROOT))
    if args.check:
        errors = check_outputs(ROOT, expected)
        if errors:
            print("FAIL: Claude export is stale")
            for error in errors:
                print(f"- {error}")
            return 1
        print(f"PASS: {len(expected)} Claude Code export files are current.")
        return 0
    write_outputs(ROOT, expected)
    print(f"Wrote {len(expected)} Claude Code export files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
