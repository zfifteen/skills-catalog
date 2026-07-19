import unittest
import tempfile
import json
import shutil
from pathlib import Path
from lumos.core import init_workspace, load_state, save_state, add_learning, get_state_file

class TestLumosCore(unittest.TestCase):
    def setUp(self):
        # Create a mock temporary workspace
        self.test_dir = Path(tempfile.mkdtemp())
        
    def tearDown(self):
        # Cleanup mock temporary workspace
        shutil.rmtree(self.test_dir)

    def test_init_workspace(self):
        # Check initial behavior
        msg = init_workspace(self.test_dir)
        self.assertIn("Successfully initialized", msg)

        state_file = get_state_file(self.test_dir)
        self.assertTrue(state_file.exists())

        # Verify gitignore has been updated
        gitignore = self.test_dir / ".gitignore"
        self.assertTrue(gitignore.exists())
        gitignore_content = gitignore.read_text(encoding="utf-8")
        self.assertIn(".lumos/", gitignore_content)

    def test_load_and_save_state(self):
        init_workspace(self.test_dir)
        state = load_state(self.test_dir)
        self.assertEqual(state["project_metadata"]["name"], self.test_dir.name)

        # Update metadata and save
        state["project_metadata"]["git_commit_sha"] = "test_sha_123"
        save_state(self.test_dir, state)

        # Reload and check values
        reloaded = load_state(self.test_dir)
        self.assertEqual(reloaded["project_metadata"]["git_commit_sha"], "test_sha_123")

    def test_add_learning(self):
        init_workspace(self.test_dir)
        
        # Test appending to logical_invariants
        add_learning(self.test_dir, "logical_invariants.port", "3000")
        state = load_state(self.test_dir)
        self.assertEqual(state["learnings_ledger"]["logical_invariants"]["port"], "3000")

        # Test appending to build_invariants
        add_learning(self.test_dir, "build_invariants.tool", "lake")
        state = load_state(self.test_dir)
        self.assertEqual(state["learnings_ledger"]["build_invariants"]["tool"], "lake")

if __name__ == "__main__":
    unittest.main()
