from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from ipynbcleaner.cli import main
from ipynbcleaner.cleaner import CleanOptions, clean_notebook, clean_notebook_file

SAMPLE_NOTEBOOK = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {"kernelspec": {"name": "python3"}},
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {"tags": ["intro"]},
            "source": ["# Title\n", "Notebook body.\n"],
            "attachments": {"image.png": {"image/png": "abc"}},
        },
        {
            "cell_type": "code",
            "execution_count": 7,
            "metadata": {"collapsed": false},
            "source": ["print('hello')\n"],
            "outputs": [
                {"output_type": "stream", "name": "stdout", "text": ["first\n"]},
                {"output_type": "stream", "name": "stdout", "text": ["last\n"]},
            ],
            "id": "cell-1",
        },
    ],
}

class CleanerTests(unittest.TestCase):
    def test_clean_notebook_removes_noise_and_keeps_last_output(self) -> None:
        cleaned = clean_notebook(SAMPLE_NOTEBOOK)

        self.assertEqual(cleaned["metadata"], {})
        self.assertEqual(len(cleaned["cells"]), 2)

        markdown_cell = cleaned["cells"][0]
        self.assertEqual(markdown_cell["metadata"], {})
        self.assertNotIn("attachments", markdown_cell)

        code_cell = cleaned["cells"][1]
        self.assertIsNone(code_cell["execution_count"])
        self.assertEqual(code_cell["outputs"], [SAMPLE_NOTEBOOK["cells"][1]["outputs"][-1]])
        self.assertEqual(code_cell["metadata"], {})
        self.assertNotIn("id", code_cell)

    def test_clean_notebook_can_drop_outputs(self) -> None:
        cleaned = clean_notebook(SAMPLE_NOTEBOOK, CleanOptions(keep_last_output=False))

        self.assertEqual(cleaned["cells"][1]["outputs"], [])

    def test_clean_notebook_file_writes_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            input_file = tmp_path / "sample.ipynb"
            output_file = tmp_path / "sample_clean.ipynb"

            input_file.write_text(json.dumps(SAMPLE_NOTEBOOK), encoding="utf-8")

            result_path = clean_notebook_file(input_file, output_file)

            self.assertEqual(result_path, output_file)
            saved = json.loads(output_file.read_text(encoding="utf-8"))
            self.assertEqual(saved["cells"][1]["outputs"], [SAMPLE_NOTEBOOK["cells"][1]["outputs"][-1]])

    def test_cli_main_returns_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            input_file = tmp_path / "sample.ipynb"
            output_file = tmp_path / "out.ipynb"

            input_file.write_text(json.dumps(SAMPLE_NOTEBOOK), encoding="utf-8")

            exit_code = main([str(input_file), str(output_file), "--drop-outputs"])

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_file.exists())

if __name__ == "__main__":
    unittest.main()
