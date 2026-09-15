"""In-memory mutations of the real package; no test fixture files are written."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate import ROOT, read_files, validate_files


class PackageValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline, errors = read_files(ROOT)
        if errors:
            raise AssertionError(errors)

    def mutated(self, transform):
        files = dict(self.baseline)
        transform(files)
        return validate_files(files)

    def test_current_package(self):
        self.assertEqual([], validate_files(self.baseline))

    def test_missing_profile(self):
        errors = self.mutated(lambda f: f.pop("agents/specialists/backend-developer.toml"))
        self.assertTrue(any("catalog/profile file set mismatch" in e for e in errors))

    def test_catalog_description_drift(self):
        def change(files):
            catalog = json.loads(files["agents/catalog.json"])
            catalog["agents"][0]["description"] = "Drifted metadata"
            files["agents/catalog.json"] = json.dumps(catalog)
        self.assertTrue(any("metadata mismatch" in e for e in self.mutated(change)))

    def test_wrong_reviewer_sandbox(self):
        def change(files):
            p = "agents/delivery_reviewer.toml"
            files[p] = files[p].replace('"read-only"', '"workspace-write"')
        self.assertTrue(any("starter sandbox mismatch" in e for e in self.mutated(change)))

    def test_invalid_sandbox_type_returns_error(self):
        def change(files):
            p = "agents/delivery_reviewer.toml"
            files[p] = files[p].replace('sandbox_mode = "read-only"', 'sandbox_mode = ["read-only"]')
        self.assertTrue(any("unexpected sandbox" in e for e in self.mutated(change)))

    def test_local_mcp_configuration_is_rejected(self):
        def change(files):
            p = "agents/specialists/backend-developer.toml"
            files[p] += '\n[mcp_servers.local]\ncommand = "example"\n'
        self.assertTrue(any("local integrations" in e for e in self.mutated(change)))

    def test_starter_cannot_depend_on_sibling_skill(self):
        def change(files):
            files["skills/codex-delivery-workflow/SKILL.md"] += "\n[Other](../writing-plans/SKILL.md)\n"
        self.assertTrue(any("not standalone" in e for e in self.mutated(change)))

    def test_pack_cannot_depend_on_repository_docs(self):
        def change(files):
            files["skills/executing-plans/SKILL.md"] += "\n[Repo](../../README.md)\n"
        self.assertTrue(any("leaves installed pack" in e for e in self.mutated(change)))

    def test_missing_relative_link(self):
        errors = self.mutated(lambda f: f.update({"README.md": f["README.md"] + "\n[Missing](not-here.md)\n"}))
        self.assertTrue(any("broken or escaping" in e for e in errors))

    def test_escaping_catalog_path(self):
        def change(files):
            catalog = json.loads(files["agents/catalog.json"])
            catalog["agents"][0]["path"] = "../outside.toml"
            files["agents/catalog.json"] = json.dumps(catalog)
        self.assertTrue(any("invalid or duplicate catalog path" in e for e in self.mutated(change)))

    def test_private_document_is_rejected(self):
        errors = self.mutated(lambda f: f.update({"docs/internal/notes.md": "Not public material"}))
        self.assertTrue(any("unexpected public package" in e for e in errors))

    def test_personal_path_marker(self):
        marker = "C:" + "/Users/" + "example/config"
        errors = self.mutated(lambda f: f.update({"README.md": f["README.md"] + marker}))
        self.assertTrue(any("machine-specific path" in e for e in errors))

    def test_credential_marker(self):
        marker = "gh" + "p_" + "a" * 36
        errors = self.mutated(lambda f: f.update({"README.md": f["README.md"] + marker}))
        self.assertTrue(any("credential-shaped text" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
