"""Validate the public workflow package; Python 3.11+, no external dependencies.

Static consistency and disclosure-marker checks are not a security audit or proof
of role discovery, model routing, sandbox enforcement, or application behavior.
"""
from __future__ import annotations

import json
import posixpath
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "codex-delivery-workflow", "writing-plans", "executing-plans",
    "subagent-driven-development", "dispatching-parallel-agents",
    "requesting-code-review",
}
REQUIRED = {
    ".gitignore", "LICENSE", "NOTICE.md", "README.md", "agents/catalog.json",
    "agents/delivery_worker.toml", "agents/delivery_reviewer.toml",
    "examples/task-packet.md", "examples/review-packet.md",
    "docs/architecture/system.md", "docs/architecture/workflows.md",
    "docs/architecture/context-and-handoffs.md",
    "docs/guides/agent-selection.md", "docs/guides/installation.md",
    "docs/guides/testing-and-debugging.md", "docs/guides/worked-examples.md",
    "scripts/validate.py", "tests/test_validate.py",
} | {f"skills/{name}/SKILL.md" for name in SKILLS}
ROLE_FIELDS = {
    "name", "description", "model", "model_reasoning_effort",
    "sandbox_mode", "developer_instructions",
}
LINK = re.compile(r'\[[^\]]+\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
PERSONAL_PATH = re.compile(r"(?:(?<![A-Za-z])[A-Za-z]:[\\/]|/(?:Users|home)/[^/\s]+/)")
CREDENTIALS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\bgh[opusr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)
EXCLUDED_DIRS = {".git", "__pycache__", ".pytest_cache"}
PRIVATE_DIRS = {"memories", "sessions", "automations", "internal", ".codex", ".agents"}
NAME = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")


def read_files(root: Path) -> tuple[dict[str, str], list[str]]:
    files, errors = {}, []
    # Do not traverse symlinked directories or read symlinked files.
    def walk(folder: Path) -> None:
        for path in sorted(folder.iterdir()):
            relative = path.relative_to(root).as_posix()
            if path.name in EXCLUDED_DIRS:
                continue
            if path.is_symlink():
                errors.append(f"symlink is not public package content: {relative}")
            elif path.is_dir():
                walk(path)
            elif path.is_file():
                try:
                    files[relative] = path.read_text(encoding="utf-8")
                except (UnicodeError, OSError) as error:
                    errors.append(f"cannot read UTF-8 file {relative}: {type(error).__name__}")
    walk(root)
    return files, errors


def allowed_path(path: str) -> bool:
    if path in REQUIRED:
        return True
    parts = path.split("/")
    return (
        len(parts) == 3 and parts[:2] == ["agents", "specialists"] and path.endswith(".toml")
        or len(parts) >= 3 and parts[0] == "skills" and parts[1] in SKILLS and path.endswith(".md")
        or len(parts) == 3 and parts[0] == "docs" and parts[1] in {"architecture", "guides"} and path.endswith(".md")
    )


def check_catalog(files: dict[str, str], errors: list[str]) -> dict[str, dict]:
    try:
        catalog = json.loads(files.get("agents/catalog.json", ""))
    except json.JSONDecodeError:
        errors.append("invalid or missing agents/catalog.json")
        return {}
    if not isinstance(catalog, dict):
        errors.append("catalog must be an object")
        return {}
    if catalog.get("model") != "gpt-5.6-terra" or catalog.get("reasoning_effort") != "high":
        errors.append("catalog model/effort must describe Terra/high")
    if not isinstance(catalog.get("source"), str) or not catalog["source"].strip():
        errors.append("catalog source is missing")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(catalog.get("snapshot_date", ""))):
        errors.append("catalog snapshot_date must use YYYY-MM-DD")
    entries = catalog.get("agents")
    if not isinstance(entries, list) or len(entries) != 120:
        errors.append("this snapshot requires exactly 120 catalog entries")
        return {}
    by_path = {}
    names = []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str) or not NAME.fullmatch(entry["name"]):
            errors.append("invalid catalog role entry")
            continue
        name = entry["name"]
        path = f"agents/specialists/{name}.toml"
        if entry.get("path") != path or path in by_path:
            errors.append(f"invalid or duplicate catalog path: {name}")
            continue
        by_path[path] = entry
        names.append(name)
    if names != sorted(names) or len(set(names)) != len(names):
        errors.append("catalog names must be unique and sorted")
    actual = {p for p in files if p.startswith("agents/specialists/") and p.endswith(".toml")}
    if actual != set(by_path):
        errors.append("catalog/profile file set mismatch")
    return by_path


def check_roles(files: dict[str, str], catalog: dict[str, dict], errors: list[str]) -> None:
    starters = {"delivery_worker": "workspace-write", "delivery_reviewer": "read-only"}
    for path, content in files.items():
        if not path.startswith("agents/") or not path.endswith(".toml"):
            continue
        try:
            role = tomllib.loads(content)
        except tomllib.TOMLDecodeError:
            errors.append(f"invalid TOML: {path}")
            continue
        name = Path(path).stem
        if set(role) - ROLE_FIELDS:
            errors.append(f"unexported role fields or local integrations in {path}")
        if role.get("name") != name or role.get("model") != "gpt-5.6-terra" or role.get("model_reasoning_effort") != "high":
            errors.append(f"role name/model/effort mismatch: {path}")
        for field in ("description", "developer_instructions"):
            if not isinstance(role.get(field), str) or not role[field].strip():
                errors.append(f"missing role {field}: {path}")
        sandbox = role.get("sandbox_mode")
        if sandbox not in (None, "read-only", "workspace-write"):
            errors.append(f"unexpected sandbox: {path}")
        if path == f"agents/{name}.toml" and sandbox != starters.get(name):
            errors.append(f"starter sandbox mismatch: {path}")
        if path in catalog:
            entry = catalog[path]
            if entry.get("description") != role.get("description") or entry.get("sandbox_mode") != sandbox:
                errors.append(f"catalog/profile metadata mismatch: {path}")


def check_skills(files: dict[str, str], errors: list[str]) -> None:
    for name in sorted(SKILLS):
        path = f"skills/{name}/SKILL.md"
        match = re.match(r"\A---\n(.*?)\n---\n", files.get(path, ""), re.S)
        if not match:
            errors.append(f"missing skill frontmatter: {path}")
            continue
        fields = {}
        for line in match[1].splitlines():
            key, separator, value = line.partition(":")
            if not separator or key in fields or key not in {"name", "description"}:
                errors.append(f"invalid two-scalar skill frontmatter: {path}")
                continue
            fields[key] = value.strip().strip('"').strip("'")
        if fields.get("name") != name or not fields.get("description"):
            errors.append(f"skill name/description mismatch: {path}")


def check_links(files: dict[str, str], errors: list[str]) -> None:
    for path, content in files.items():
        if not path.endswith(".md"):
            continue
        for destination in LINK.findall(content):
            if "://" in destination or destination.startswith(("#", "mailto:")):
                continue
            target = unquote(destination.split("#", 1)[0])
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target))
            if resolved.startswith(("../", "/")) or not (
                resolved in files or any(p.startswith(resolved + "/") for p in files)
            ):
                errors.append(f"broken or escaping local link: {path} -> {destination}")
                continue
            if path.startswith("skills/"):
                if not resolved.startswith("skills/"):
                    errors.append(f"skill runtime link leaves installed pack: {path} -> {destination}")
                elif path.startswith("skills/codex-delivery-workflow/") and not resolved.startswith("skills/codex-delivery-workflow/"):
                    errors.append(f"starter skill is not standalone: {destination}")


def validate_files(files: dict[str, str]) -> list[str]:
    errors = [f"missing required file: {p}" for p in sorted(REQUIRED - set(files))]
    for path, content in files.items():
        if not allowed_path(path) or set(path.split("/")) & PRIVATE_DIRS:
            errors.append(f"unexpected public package file: {path}")
        if PERSONAL_PATH.search(content):
            errors.append(f"machine-specific path: {path}")
        if any(pattern.search(content) for pattern in CREDENTIALS):
            errors.append(f"credential-shaped text: {path}")
    catalog = check_catalog(files, errors)
    check_roles(files, catalog, errors)
    check_skills(files, errors)
    check_links(files, errors)
    return errors


def main() -> int:
    files, errors = read_files(ROOT)
    errors.extend(validate_files(files))
    if errors:
        print("FAIL: static package validation")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1
    print(f"PASS: {len(files)} files; 120 specialist profiles, 2 starter roles, 6 skills.")
    print("Catalog, metadata, package links, and installed-skill links are consistent.")
    print("NOTE: static disclosure checks are not a security audit or runtime proof.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
