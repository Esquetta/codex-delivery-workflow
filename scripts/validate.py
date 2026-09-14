"""Static repository checks for the Codex Delivery Workflow reference.

This validator is intentionally small and uses Python 3.11+ standard library only.
Passing it is not a security guarantee or proof that Codex discovered, selected, or
enforced any installed skill, role, model, or sandbox.
"""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = {
    ".gitignore",
    "LICENSE",
    "NOTICE.md",
    "README.md",
    "agents/delivery_reviewer.toml",
    "agents/delivery_worker.toml",
    "examples/review-packet.md",
    "examples/task-packet.md",
    "scripts/validate.py",
    "skills/codex-delivery-workflow/SKILL.md",
}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
MACHINE_PATH = re.compile(r"(?:(?<![A-Za-z])[A-Za-z]:[\\/]|/(?:Users|home)/[^/]+/)")
CREDENTIAL_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)


def repository_files() -> set[str]:
    return {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts
    }


def check_file_set(errors: list[str]) -> None:
    actual = repository_files()
    missing = REQUIRED_FILES - actual
    unexpected = actual - REQUIRED_FILES
    for path in sorted(missing):
        errors.append(f"missing required file: {path}")
    for path in sorted(unexpected):
        errors.append(f"unexpected file: {path}")


def check_skill(errors: list[str]) -> None:
    skill = ROOT / "skills/codex-delivery-workflow/SKILL.md"
    text = skill.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        errors.append("skill frontmatter is missing")
        return
    fields = {
        key.strip(): value.strip().strip('"')
        for line in match.group(1).splitlines()
        if ":" in line
        for key, value in [line.split(":", 1)]
    }
    if fields.get("name") != "codex-delivery-workflow":
        errors.append("skill frontmatter name must be codex-delivery-workflow")
    if not fields.get("description", "").strip():
        errors.append("skill frontmatter description is missing")


def check_agents(errors: list[str]) -> None:
    expected = {
        "delivery_worker.toml": ("delivery_worker", "workspace-write"),
        "delivery_reviewer.toml": ("delivery_reviewer", "read-only"),
    }
    for filename, (name, sandbox) in expected.items():
        path = ROOT / "agents" / filename
        try:
            role = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as error:
            errors.append(f"invalid TOML in {filename}: {error}")
            continue
        for key, value in {
            "name": name,
            "model": "gpt-5.6-terra",
            "model_reasoning_effort": "high",
            "sandbox_mode": sandbox,
        }.items():
            if role.get(key) != value:
                errors.append(f"{filename} {key} must be {value!r}")
        if not isinstance(role.get("developer_instructions"), str) or not role["developer_instructions"].strip():
            errors.append(f"{filename} developer_instructions must be non-empty text")


def check_markdown_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for destination in MARKDOWN_LINK.findall(text):
            if "://" in destination or destination.startswith("#") or destination.startswith("mailto:"):
                continue
            target = destination.split("#", 1)[0]
            if target and not (path.parent / target).resolve().is_file():
                errors.append(f"broken local Markdown link in {path.relative_to(ROOT)}: {destination}")


def check_text_safety(errors: list[str]) -> None:
    for relative_path in repository_files():
        path = ROOT / relative_path
        text = path.read_text(encoding="utf-8")
        if MACHINE_PATH.search(text):
            errors.append(f"machine-specific source path in {relative_path}")
        if any(pattern.search(text) for pattern in CREDENTIAL_PATTERNS):
            errors.append(f"credential-shaped text in {relative_path}")


def main() -> int:
    errors: list[str] = []
    check_file_set(errors)
    if not errors:
        check_skill(errors)
        check_agents(errors)
        check_markdown_links(errors)
        check_text_safety(errors)
    if errors:
        print("FAIL: static validation")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PASS: 10 expected files; frontmatter, TOML, local links, and static text checks passed.")
    print("NOTE: this is static validation, not a security guarantee or runtime proof.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
