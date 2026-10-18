"""Regression tests for PyMC guide imports, without modifying repository posts."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import import_pymc_guides as importer


class ImporterHeroTests(unittest.TestCase):
    def test_hero_renders_once_even_if_source_already_has_it(self):
        cover = importer.POST_CONFIG["pymc-marketing-01.md"]["heroImage"]
        cases = [
            ("Body stays intact", "Body stays intact"),
            (f"![Existing cover]({cover})\n\nBody stays intact", "Body stays intact"),
        ]
        for body, expected_body in cases:
            with self.subTest(body=body), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                input_dir = root / "input"
                output_dir = root / "output"
                input_dir.mkdir()
                output_dir.mkdir()
                source = f"---\ntitle: Example\npubDatetime: 2026-10-17T00:00:00Z\ndraft: true\n---\n\n{body}\n"
                (input_dir / "pymc-marketing-01.md").write_text(source, encoding="utf-8")
                with patch.object(importer, "DEST_DIR", output_dir):
                    importer.process_file("pymc-marketing-01.md", input_dir)
                content = (output_dir / "pymc-marketing-01.md").read_text(encoding="utf-8")
                self.assertIn(f'heroImage: "{cover}"', content)
                self.assertIn("ogImage:", content)
                self.assertIn("draft: false", content)
                rendered_body = content.split("---", 2)[2].strip()
                self.assertEqual(rendered_body, expected_body)
                self.assertNotIn(f"]({cover})", rendered_body)


if __name__ == "__main__":
    unittest.main()
