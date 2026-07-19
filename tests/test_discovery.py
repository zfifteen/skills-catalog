import unittest
import tempfile
import json
import shutil
import subprocess
from pathlib import Path
from lumos.core import init_workspace, load_state
from lumos.discovery import get_git_info, load_rules, match_path_rules, perform_workspace_save

class TestLumosDiscovery(unittest.TestCase):
    def setUp(self):
        # Create a mock temporary workspace and initialize a git repo
        self.test_dir = Path(tempfile.mkdtemp())
        subprocess.run(["git", "init"], cwd=str(self.test_dir), capture_output=True, check=True)
        # Add basic git config so commits succeed in tests
        subprocess.run(["git", "config", "user.name", "Tester"], cwd=str(self.test_dir), check=True)
        subprocess.run(["git", "config", "user.email", "tester@test.com"], cwd=str(self.test_dir), check=True)

        # Seed an initial commit
        test_file = self.test_dir / "main.py"
        test_file.write_text("print('test')")
        subprocess.run(["git", "add", "main.py"], cwd=str(self.test_dir), check=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=str(self.test_dir), check=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_git_info_extraction(self):
        info = get_git_info(self.test_dir)
        self.assertNotEqual(info["git_commit_sha"], "")
        self.assertEqual(info["active_branch"], "main")
        self.assertEqual(len(info["dirty_files"]), 0)

        # Create modifications
        test_file = self.test_dir / "main.py"
        test_file.write_text("print('edited')")
        
        info_mod = get_git_info(self.test_dir)
        self.assertEqual(info_mod["dirty_files"], ["main.py"])

    def test_rules_loading_and_matching(self):
        # Initial status should return default rules since rules.json is missing
        rules = load_rules(self.test_dir)
        self.assertIn("path_mappings", rules)

        # Set up a mock rules.json
        init_workspace(self.test_dir)
        rules_file = self.test_dir / ".lumos" / "rules.json"
        
        custom_rules = {
            "path_mappings": {
                "src/python": {
                    "test_command": "pytest src/python/tests"
                }
            }
        }
        with open(rules_file, "w", encoding="utf-8") as f:
            json.dump(custom_rules, f)

        # Verify parsing
        rules_mod = load_rules(self.test_dir)
        self.assertEqual(rules_mod["path_mappings"]["src/python"]["test_command"], "pytest src/python/tests")

        # Verify matching
        matched = match_path_rules(self.test_dir, ["src/python/module.py"])
        self.assertEqual(matched.get("src/python"), "pytest src/python/tests")

    def test_workspace_save_integration(self):
        init_workspace(self.test_dir)
        state = load_state(self.test_dir)

        # Write rules.json first
        rules_file = self.test_dir / ".lumos" / "rules.json"
        with open(rules_file, "w", encoding="utf-8") as f:
            json.dump({"path_mappings": {"src/c": {"test_command": "make -C src/c test"}}}, f)

        # Create local modifications in mock C directory
        c_dir = self.test_dir / "src" / "c"
        c_dir.mkdir(parents=True)
        c_file = c_dir / "main.c"
        c_file.write_text("int main() {}")

        # Save workspace
        updated_state = perform_workspace_save(self.test_dir, state)
        self.assertIn("src/c/main.c", updated_state["workspace_map"]["key_paths"]["modified_files"])
        self.assertEqual(updated_state["operational_history"]["preferred_test_commands"]["src/c"], "make -C src/c test")

if __name__ == "__main__":
    unittest.main()
