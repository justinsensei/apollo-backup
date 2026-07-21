#!/usr/bin/env python3
"""Tests for wiki_semantic_lint.py."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import wiki_semantic_lint as wsl


class WikiSemanticLintTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vault = Path(self.tmp.name)
        os.makedirs(self.vault / "Notebook", exist_ok=True)
        os.makedirs(self.vault / "Inputs" / "Readings", exist_ok=True)
        os.makedirs(self.vault / "Utilities", exist_ok=True)

        Path(self.vault / "Utilities" / "log.md").write_text(
            "# Wiki Log\n\n## 2026-06-01\n- 10:00 | slack | [[test]] | inbox/a.md | [[2026-06-01 Monday]]\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, rel: str, content: str):
        path = self.vault / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_maturity_orphan_detected(self):
        self._write(
            "Notebook/Orphan Concept.md",
            """---
category: "[[Concepts]]"
---
# Orphan Concept
Standalone idea with no inbound links.
""",
        )
        result = wsl.run_lint(vault=self.vault, since_last=False)
        orphans = result["findings"]["maturity_orphans"]
        self.assertEqual(len(orphans), 1)
        self.assertEqual(orphans[0]["path"], "Notebook/Orphan Concept.md")

    def test_maturity_orphan_not_detected_if_has_outgoing_links(self):
        self._write(
            "Notebook/Target.md",
            """---
category: "[[Concepts]]"
---
# Target
This note is linked to by another note.
""",
        )
        self._write(
            "Notebook/Source With Outgoing.md",
            """---
category: "[[Concepts]]"
---
# Source With Outgoing
Links to [[Target]].
""",
        )
        result = wsl.run_lint(vault=self.vault, since_last=False)
        orphans = result["findings"]["maturity_orphans"]
        self.assertEqual(len(orphans), 0)

    def test_stale_summary_detected(self):
        reading = self._write(
            "Inputs/Readings/Example Book.md",
            """---
category: "[[Readings]]"
---
# Example Book
""" + ("x" * 500),
        )
        source = self._write(
            "Notebook/Example Book.md",
            """---
category: "[[Sources]]"
---
# Example Book

## Summary
Old summary.

## Raw inputs
- [[Example Book]]
""",
        )
        reading_path = self.vault / "Inputs/Readings/Example Book.md"
        source_path = self.vault / "Notebook/Example Book.md"
        old = source_path.stat().st_mtime
        os.utime(reading_path, (old + 100, old + 100))

        result = wsl.run_lint(vault=self.vault, since_last=False)
        stale = result["findings"]["stale_summaries"]
        self.assertEqual(len(stale), 1)
        self.assertEqual(stale[0]["source"], "Notebook/Example Book.md")

    def test_promotion_opportunity_detected(self):
        self._write(
            "Inputs/Readings/Uncompiled Article.md",
            """---
category: "[[Readings]]"
---
# Uncompiled Article

## Highlights
- Important point one
- Important point two
""" + ("detail " * 80),
        )
        result = wsl.run_lint(vault=self.vault, since_last=False)
        promos = result["findings"]["promotion_opportunities"]
        self.assertEqual(len(promos), 1)
        self.assertIn("Uncompiled Article", promos[0]["reading"])

    def test_clean_vault_reports_zero_issues(self):
        self._write(
            "Notebook/Hub.md",
            """---
category: "[[Projects]]"
---
# Hub
See [[Linked Child]].
""",
        )
        self._write(
            "Notebook/Linked Child.md",
            """---
category: "[[Concepts]]"
---
# Linked Child
From [[Hub]].
""",
        )
        result = wsl.run_lint(vault=self.vault, since_last=False)
        self.assertEqual(result["issue_count"], 0)


if __name__ == "__main__":
    unittest.main()
