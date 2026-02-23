from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


def _chmod_for_container(work: Path) -> None:
    """Ensure container (non-root) can read bind-mounted files.

    tempfile.TemporaryDirectory() creates dirs with mode 700 (owner-only). The addon
    runs as appuser (uid 5678) in the container, while the temp dir is owned by the
    host user. With 700, the container process gets permission denied. Chmod to 755/644
    allows others to read so the container can access the test data.
    """
    for root, dirs, files in os.walk(work, topdown=True):
        os.chmod(root, 0o755)
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o755)
        for f in files:
            os.chmod(os.path.join(root, f), 0o644)


def _build_docspell_work_dir(work: Path) -> None:
    """Create directory structure matching Docspell's addon invocation."""
    (work / "arguments").mkdir()
    item_dir = work / "item"
    item_dir.mkdir()
    (item_dir / "originals").mkdir()
    (item_dir / "pdfs").mkdir()

    # User input from web UI
    (work / "arguments" / "user-input").write_text(
        json.dumps({"name": "John", "customField": "value"}), encoding="utf-8"
    )

    # Item data (ITEM_DATA_JSON)
    (item_dir / "item-data.json").write_text(
        json.dumps({
            "id": "UyZ-item-id",
            "name": "yearly report 2021",
            "collective": 1,
            "source": "webapp",
            "tags": ["tag-1"],
            "assumedTags": ["invoice"],
            "attachments": [
                {
                    "id": "Apa-attach-id",
                    "name": "report_year_2021.pdf",
                    "position": 0,
                    "content": "extracted text…",
                    "language": "eng",
                    "pages": 2,
                }
            ],
            "assumedCorrOrg": {"id": "yf7XiqWp", "name": "Acme AG"},
            "assumedConcPerson": {"id": "7XLiAkeY", "name": "Derek Jeter"},
        }),
        encoding="utf-8",
    )

    # Item args from upload (ITEM_ARGS_JSON)
    (item_dir / "given-data.json").write_text(
        json.dumps({
            "collective": 1,
            "language": "eng",
            "tags": ["given-tag-1"],
            "skipDuplicate": True,
            "customData": {"my-id": 42},
        }),
        encoding="utf-8",
    )

    # Original files metadata (ITEM_ORIGINAL_JSON)
    (item_dir / "source-files.json").write_text(
        json.dumps([
            {
                "id": "2M8JwSdbE",
                "name": "report_year_2021.pdf",
                "position": 0,
                "language": "eng",
                "mimetype": "application/pdf",
                "length": 454654,
            }
        ]),
        encoding="utf-8",
    )

    # PDF files metadata (ITEM_PDF_JSON)
    (item_dir / "pdf-files.json").write_text(
        json.dumps([
            {
                "id": "2M8JwSdbE",
                "name": "report_year_2021.pdf",
                "position": 0,
                "language": "eng",
                "mimetype": "application/pdf",
                "length": 123456,
            }
        ]),
        encoding="utf-8",
    )


class TestDocspellAddonInterface(unittest.TestCase):
    def test_addon_uses_all_docspell_data(self) -> None:
        subprocess.run(["docker", "compose", "build"], check=True, capture_output=True)

        with tempfile.TemporaryDirectory() as work_dir:
            work = Path(work_dir)
            _build_docspell_work_dir(work)
            _chmod_for_container(work)

            result = subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",
                    "--mount", f"type=bind,source={work_dir},target=/mnt/work",
                    "--env", "ADDON_DIR=addons/docspell-addon-example-1.2.0",
                    "--env", "TMP_DIR=/mnt/work/temp",
                    "--env", "TMPDIR=/mnt/work/temp",
                    "--env", "OUTPUT_DIR=/mnt/output",
                    "--env", "CACHE_DIR=/mnt/cache",
                    "--env", "ITEM_DIR=/mnt/work/item",
                    "--env", "ITEM_DATA_JSON=/mnt/work/item/item-data.json",
                    "--env", "ITEM_ARGS_JSON=/mnt/work/item/given-data.json",
                    "--env", "ITEM_ORIGINAL_JSON=/mnt/work/item/source-files.json",
                    "--env", "ITEM_PDF_JSON=/mnt/work/item/pdf-files.json",
                    "--env", "ITEM_ORIGINAL_DIR=/mnt/work/item/originals",
                    "--env", "ITEM_PDF_DIR=/mnt/work/item/pdfs",
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
    unittest.main()
