import unittest
import tempfile
import shutil
from pathlib import Path
from lumos.core import init_workspace, load_state, save_state
from lumos.scrub import should_ignore_path, scrub_string, filter_dirty_files
from lumos.format import format_state_to_markdown

class TestLumosScrubAndFormat(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_secret_scrub_paths(self):
        # Verify sensitive files are blocked
        self.assertTrue(should_ignore_path(".env"))
        self.assertTrue(should_ignore_path("src/key/id_rsa"))
        self.assertFalse(should_ignore_path("src/python/main.py"))

        # Verify dirty files filtering
        files = [".env", "src/main.py", "secret/private_key.pem"]
        filtered = filter_dirty_files(files)
        self.assertEqual(filtered, ["src/main.py"])

    def test_secret_scrub_strings(self):
        # Slack token
        raw_slack = "slack_key = 'xoxb-1234567890-abcdef'"
        self.assertIn("[REDACTED_SECRET]", scrub_string(raw_slack))

        # AWS key
        raw_aws = "aws_key = 'AKIA1234567890ABCDEF'"
        self.assertIn("[REDACTED_SECRET]", scrub_string(raw_aws))

        # Generic password assignment
        raw_pw = "db_password = 'MySecretPassword123'"
        scrubbed_pw = scrub_string(raw_pw)
        self.assertIn("[REDACTED_CREDENTIAL]", scrubbed_pw)
        self.assertNotIn("MySecretPassword123", scrubbed_pw)

    def test_markdown_formatter(self):
        init_workspace(self.test_dir)
        state = load_state(self.test_dir)

        # Populate mock state data
        state["project_metadata"]["git_commit_sha"] = "test_commit_sha_123"
        state["project_metadata"]["active_branch"] = "feature/test-format"
        state["learnings_ledger"]["logical_invariants"]["test_gotcha"] = "gotcha insight string"
        state["handoff_state"]["last_completed_step"] = "Completed Step A"
        state["handoff_state"]["pending_tasks"] = ["Task B", "Task C"]
        save_state(self.test_dir, state)

        # Generate markdown output
        markdown_output = format_state_to_markdown(self.test_dir)
        self.assertIn("test_commit_sha_123", markdown_output)
        self.assertIn("feature/test-format", markdown_output)
        self.assertIn("test_gotcha", markdown_output)
        self.assertIn("gotcha insight string", markdown_output)
        self.assertIn("Completed Step A", markdown_output)
        self.assertIn("- [ ] Task B", markdown_output)

if __name__ == "__main__":
    unittest.main()
