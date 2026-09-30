"""Contract tests for the deterministic portable Claude Code export."""
import json
import sys
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from export_claude import (
    build_outputs,
    check_outputs,
    main,
    parse_frontmatter,
    read_sources,
    write_outputs,
)


class ClaudeExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {
            path.relative_to(ROOT).as_posix(): path.read_text(encoding="utf-8")
            for path in (ROOT / "agents").rglob("*")
            if path.is_file()
        }

    def outputs(self, transform=None):
        files = dict(self.sources)
        if transform:
            transform(files)
        return build_outputs(files)

    def test_exports_catalog_and_all_profiles_deterministically(self):
        first = self.outputs()
        self.assertEqual(first, self.outputs())
        self.assertEqual(123, len(first))
        self.assertIn("claude/catalog.json", first)
        self.assertIn("claude/agents/delivery-worker.md", first)
        self.assertIn("claude/agents/delivery-reviewer.md", first)
        self.assertIn("claude/agents/specialists/code-reviewer.md", first)

        catalog = json.loads(first["claude/catalog.json"])
        self.assertEqual("anthropic", catalog["provider"])
        self.assertEqual({"default": "sonnet", "review": "opus"}, catalog["model_policy"])
        self.assertEqual(122, len(catalog["agents"]))
        self.assertEqual(
            sorted(entry["source_path"] for entry in catalog["agents"]),
            [entry["source_path"] for entry in catalog["agents"]],
        )

    def test_search_has_web_tools_without_write_or_shell_access(self):
        fields = parse_frontmatter(self.outputs()["claude/agents/specialists/search-specialist.md"])
        self.assertEqual(["Read", "Grep", "Glob", "WebSearch", "WebFetch"], fields["tools"])

    def test_browser_reports_unconfigured_mcp_without_guessing_tools(self):
        text = self.outputs()["claude/agents/specialists/browser-debugger.md"]
        fields = parse_frontmatter(text)
        self.assertIn("BLOCKED", text)
        self.assertIn("exact browser MCP tool names", text)
        self.assertNotIn("mcpServers", fields)
        self.assertFalse(any(tool.startswith("mcp__") for tool in fields["tools"]))

    def test_export_prunes_removed_and_renamed_owned_profiles(self):
        before = self.outputs()
        def rename(files):
            catalog = json.loads(files["agents/catalog.json"])
            catalog["agents"] = [e for e in catalog["agents"] if e["name"] != "search-specialist"]
            entry = next(e for e in catalog["agents"] if e["name"] == "browser-debugger")
            entry.update(name="browser-investigator", path="agents/specialists/browser-investigator.toml")
            files[entry["path"]] = files.pop("agents/specialists/browser-debugger.toml").replace('name = "browser-debugger"', 'name = "browser-investigator"')
            files["agents/catalog.json"] = json.dumps(catalog)
        after = self.outputs(rename)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_outputs(root, before)
            custom = root / "claude/agents/custom.md"
            custom.write_text("User-owned profile", encoding="utf-8")
            write_outputs(root, after)
            self.assertFalse((root / "claude/agents/specialists/search-specialist.md").exists())
            self.assertFalse((root / "claude/agents/specialists/browser-debugger.md").exists())
            self.assertTrue((root / "claude/agents/specialists/browser-investigator.md").exists())
            self.assertEqual("User-owned profile", custom.read_text(encoding="utf-8"))

    def test_user_file_at_new_output_path_is_preserved(self):
        outputs = self.outputs()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "claude/agents/delivery-worker.md"
            target.parent.mkdir(parents=True)
            target.write_text("User-owned profile", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "ownership"):
                write_outputs(root, outputs)
            self.assertEqual("User-owned profile", target.read_text(encoding="utf-8"))
            self.assertFalse((root / "claude/catalog.json").exists())

    def test_owned_profile_accepts_git_crlf_checkout(self):
        outputs = self.outputs()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_outputs(root, outputs)
            target = root / "claude/agents/delivery-worker.md"
            target.write_bytes(target.read_bytes().replace(b"\n", b"\r\n"))
            write_outputs(root, outputs)
            self.assertEqual([], check_outputs(root, outputs))

    def test_modified_current_profile_is_preserved(self):
        outputs = self.outputs()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_outputs(root, outputs)
            target = root / "claude/agents/specialists/search-specialist.md"
            target.write_text("User edits", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "modified"):
                write_outputs(root, outputs)
            self.assertEqual("User edits", target.read_text(encoding="utf-8"))

    def test_obsolete_legacy_profile_without_hash_is_preserved(self):
        outputs = self.outputs()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_outputs(root, outputs)
            catalog = json.loads(outputs["claude/catalog.json"])
            for entry in catalog["agents"]:
                entry.pop("content_sha256")
            (root / "claude/catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
            relative = "claude/agents/specialists/search-specialist.md"
            after = dict(outputs)
            after.pop(relative)
            with self.assertRaisesRegex(ValueError, "ownership"):
                write_outputs(root, after)
            self.assertTrue((root / relative).is_file())

    def test_obsolete_catalog_path_cannot_escape_export_root(self):
        outputs = self.outputs()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_outputs(root, outputs)
            path = root / "claude/catalog.json"
            catalog = json.loads(path.read_text(encoding="utf-8"))
            catalog["agents"][0]["path"] = "../outside.md"
            path.write_text(json.dumps(catalog), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid generated path"):
                write_outputs(root, outputs)
            self.assertEqual("../outside.md", json.loads(path.read_text(encoding="utf-8"))["agents"][0]["path"])

    def test_modified_obsolete_profile_blocks_export_before_writes(self):
        before = self.outputs()
        after = dict(before)
        relative = "claude/agents/specialists/search-specialist.md"
        after.pop(relative)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_outputs(root, before)
            target = root / relative
            target.write_text("User edits", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "modified|ownership"):
                write_outputs(root, after)
            self.assertEqual("User edits", target.read_text(encoding="utf-8"))
            self.assertEqual(before["claude/catalog.json"], (root / "claude/catalog.json").read_text(encoding="utf-8"))

    def test_source_metadata_drift_changes_generated_output(self):
        before = self.outputs()["claude/agents/specialists/backend-developer.md"]

        def drift(files):
            path = "agents/specialists/backend-developer.toml"
            files[path] = files[path].replace(
                "scoped backend implementation or backend bug fixes",
                "drifted backend implementation or backend bug fixes",
            )

        after = self.outputs(drift)["claude/agents/specialists/backend-developer.md"]
        self.assertNotEqual(before, after)
        self.assertIn("drifted backend implementation", after)

    def test_normalized_name_collisions_fail(self):
        def collision(files):
            catalog = json.loads(files["agents/catalog.json"])
            catalog["agents"].append({
                "name": "delivery.worker",
                "description": "Collision role.",
                "path": "agents/specialists/delivery.worker.toml",
                "sandbox_mode": "read-only",
            })
            files["agents/catalog.json"] = json.dumps(catalog)
            files["agents/specialists/delivery.worker.toml"] = (
                'name = "delivery.worker"\n'
                'description = "Collision role."\n'
                'model = "gpt-5.6-terra"\n'
                'model_reasoning_effort = "high"\n'
                'sandbox_mode = "read-only"\n'
                'developer_instructions = "Review only."\n'
            )

        with self.assertRaisesRegex(ValueError, "collision"):
            self.outputs(collision)

    def test_model_and_tools_follow_the_role_policy(self):
        outputs = self.outputs()
        reviewer = parse_frontmatter(outputs["claude/agents/delivery-reviewer.md"])
        worker = parse_frontmatter(outputs["claude/agents/delivery-worker.md"])
        specialist = parse_frontmatter(outputs["claude/agents/specialists/code-reviewer.md"])

        self.assertEqual("opus", reviewer["model"])
        self.assertEqual(["Read", "Grep", "Glob"], reviewer["tools"])
        self.assertEqual("default", reviewer["permissionMode"])
        self.assertEqual("sonnet", worker["model"])
        self.assertEqual(["Read", "Grep", "Glob", "Edit", "Write", "Bash"], worker["tools"])
        self.assertEqual("opus", specialist["model"])
        self.assertEqual(["Read", "Grep", "Glob"], specialist["tools"])

    def test_reviewer_lane_is_read_only_even_when_source_sandbox_allows_writes(self):
        def writable_reviewer(files):
            path = "agents/specialists/code-reviewer.toml"
            files[path] = files[path].replace('sandbox_mode = "read-only"', 'sandbox_mode = "workspace-write"')

        agent = parse_frontmatter(
            self.outputs(writable_reviewer)["claude/agents/specialists/code-reviewer.md"]
        )
        self.assertEqual(["Read", "Grep", "Glob"], agent["tools"])

    def test_catalog_entry_name_and_path_must_match_a_safe_profile_stem(self):
        def invalid_catalog(files):
            catalog = json.loads(files["agents/catalog.json"])
            catalog["agents"][0]["name"] = "../outside"
            files["agents/catalog.json"] = json.dumps(catalog)

        with self.assertRaisesRegex(ValueError, "catalog"):
            self.outputs(invalid_catalog)

    def test_profile_name_must_match_its_validated_source_path_stem(self):
        def mismatched_profile(files):
            path = "agents/specialists/backend-developer.toml"
            files[path] = files[path].replace('name = "backend-developer"', 'name = "other"')

        with self.assertRaisesRegex(ValueError, "profile name"):
            self.outputs(mismatched_profile)

    def test_openai_only_fields_are_omitted_and_source_sandbox_is_catalogued(self):
        outputs = self.outputs()
        agent = outputs["claude/agents/specialists/backend-developer.md"]
        self.assertNotIn("reasoning_effort", agent)
        self.assertNotIn("sandbox_mode", agent)
        self.assertNotIn("gpt-", agent)
        catalog = json.loads(outputs["claude/catalog.json"])
        entry = next(item for item in catalog["agents"] if item["source_name"] == "backend-developer")
        self.assertEqual("write", entry["source_sandbox_mode"])

    def test_adapted_profiles_do_not_instruct_claude_to_use_codex_apis(self):
        outputs = self.outputs()
        installer = outputs["claude/agents/specialists/agent-installer.md"]
        orchestrator = outputs["claude/agents/specialists/workflow-orchestrator.md"]
        self.assertNotIn("Codex", installer)
        self.assertNotIn("Codex", orchestrator)
        self.assertIn("Claude Code", installer)
        self.assertIn("Claude Code", orchestrator)

    def test_preserves_required_upstream_notices_after_frontmatter(self):
        outputs = self.outputs()
        for name in ("resume-refiner", "scientific-literature-researcher"):
            content = outputs[f"claude/agents/specialists/{name}.md"]
            frontmatter_end = content.index("---", 4) + 3
            self.assertIn("Copyright (c) 2026 VoltAgent", content[frontmatter_end:])
            self.assertIn("MIT License", content[frontmatter_end:])

    def test_read_sources_rejects_a_source_symlink(self):
        with patch.object(
            Path,
            "is_symlink",
            autospec=True,
            side_effect=lambda path: path.as_posix().endswith("agents/delivery_worker.toml"),
        ):
            with self.assertRaisesRegex(ValueError, "symlink"):
                read_sources(ROOT)

    def test_pruning_rejects_junction_before_any_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = self.outputs()
            write_outputs(root, outputs)
            with patch.object(
                Path, "is_junction", lambda path: path.name == "specialists", create=True,
            ), patch.object(Path, "write_text", autospec=True) as write_text, patch.object(
                Path, "unlink", autospec=True
            ) as unlink:
                with self.assertRaisesRegex(ValueError, "junction"):
                    write_outputs(root, {"claude/catalog.json": "{}\n"})
            write_text.assert_not_called()
            unlink.assert_not_called()
            self.assertEqual([], check_outputs(root, outputs))

    def test_write_outputs_rejects_symlink_escape_before_writing(self):
        with patch.object(
            Path,
            "is_symlink",
            autospec=True,
            side_effect=lambda path: path.as_posix().endswith("/claude"),
        ), patch.object(Path, "mkdir", autospec=True) as mkdir, patch.object(
            Path, "write_text", autospec=True
        ) as write_text:
            with self.assertRaisesRegex(ValueError, "symlink"):
                write_outputs(ROOT, {"claude/catalog.json": "{}\n"})
        mkdir.assert_not_called()
        write_text.assert_not_called()

    def test_check_reports_missing_stale_and_extra_files_without_writing(self):
        expected = {"claude/catalog.json": "current", "claude/agents/worker.md": "wanted"}

        def is_file(path):
            return path.name in {"catalog.json", "extra.md"}

        with patch.object(Path, "is_file", autospec=True, side_effect=is_file), patch.object(
            Path, "is_dir", autospec=True, return_value=True
        ), patch.object(Path, "read_text", autospec=True, return_value="stale"), patch.object(
            Path, "rglob", autospec=True, return_value=[ROOT / "claude" / "extra.md"]
        ):
            errors = check_outputs(ROOT, expected)
        self.assertIn("stale generated file: claude/catalog.json", errors)
        self.assertIn("missing generated file: claude/agents/worker.md", errors)
        self.assertIn("extra generated file: claude/extra.md", errors)

    def test_check_mode_never_calls_write_outputs(self):
        with patch("export_claude.write_outputs") as write:
            self.assertEqual(0, main(["--check"]))
        write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
