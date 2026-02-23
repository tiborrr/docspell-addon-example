from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path

import version

# Fixtures path: mirrors Docspell's addon invocation structure
FIXTURES = Path(__file__).parent / "fixtures"
WORK_DIR = FIXTURES / "work"
OUTPUT_DIR = FIXTURES / "output"
CACHE_DIR = FIXTURES / "cache"


def _chmod_for_container(work: Path) -> None:
    """Ensure container (non-root) can read bind-mounted files.

    The addon runs as appuser (uid 5678) in the container, while fixtures are owned
    by the host user. Restrictive permissions cause permission denied. Chmod to 755/644
    allows others to read so the container can access the test data.
    """
    for root, dirs, files in os.walk(work, topdown=True):
        os.chmod(root, 0o755)
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o755)
        for f in files:
            os.chmod(os.path.join(root, f), 0o644)


class TestDocspellAddonInterface(unittest.TestCase):
    def test_addon_uses_all_docspell_data(self) -> None:
        _ = subprocess.run(["docker", "compose", "build"], check=True, capture_output=True)

        # Ensure addon dir exists (ADDON_DIR = addons/name-version)
        addon_dir = WORK_DIR / version.ADDON_DIR
        addon_dir.mkdir(parents=True, exist_ok=True)

        # Ensure container can read fixtures (same as temp dirs)
        _chmod_for_container(FIXTURES)

        result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--network", "none",
                "--mount", f"type=bind,source={WORK_DIR.resolve()},target=/mnt/work",
                "--mount", f"type=bind,source={OUTPUT_DIR.resolve()},target=/mnt/output",
                "--mount", f"type=bind,source={CACHE_DIR.resolve()},target=/mnt/cache",
                "--env", f"ADDON_DIR={version.ADDON_DIR}",
                "--env", "ITEM_DATA_JSON=item/item-data.json",
                "--env", "ITEM_DIR=item",
                "--env", "TMP_DIR=temp",
                "--env", "TMPDIR=temp",
                "--env", "CACHE_DIR=/mnt/cache",
                "--env", "ITEM_ARGS_JSON=item/given-data.json",
                "--env", "ITEM_ORIGINAL_JSON=item/source-files.json",
                "--env", "ITEM_PDF_JSON=item/pdf-files.json",
                "--env", "OUTPUT_DIR=/mnt/output",
                "--env", "ITEM_ORIGINAL_DIR=item/originals",
                "--env", "ITEM_PDF_DIR=item/pdfs",
                "--env", "DSC_DOCSPELL_URL=http://localhost:7880",
                "--env", "DSC_SESSION=test-session-token",
                "-w", "/mnt/work",
                "tiborrr/docspell-addon-example:latest",
                "arguments/user-input",
            ],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")

        # stdout must be valid JSON (addon instructions)
        output = result.stdout.strip()
        self.assertTrue(output, "Addon should output JSON to stdout")
        parsed = json.loads(output)
        self.assertIsInstance(parsed, dict)

        # stderr shows all Docspell-provided data
        stderr = result.stderr
        self.assertIn("User input file: arguments/user-input", stderr)
        self.assertIn("John", stderr)
        self.assertIn("ADDON_DIR", stderr)
        self.assertIn("TMP_DIR", stderr)
        self.assertIn("OUTPUT_DIR", stderr)
        self.assertIn("CACHE_DIR", stderr)
        self.assertIn("ITEM_DIR", stderr)
        self.assertIn("yearly report 2021", stderr)
        self.assertIn("tag-1", stderr)
        self.assertIn("invoice", stderr)
        self.assertIn("Acme AG", stderr)
        self.assertIn("Derek Jeter", stderr)
        self.assertIn("given-tag-1", stderr)
        self.assertIn("ITEM_ORIGINAL_JSON", stderr)
        self.assertIn("ITEM_PDF_JSON", stderr)
        self.assertIn("ITEM_ORIGINAL_DIR", stderr)
        self.assertIn("ITEM_PDF_DIR", stderr)


if __name__ == "__main__":
    _ = unittest.main()
