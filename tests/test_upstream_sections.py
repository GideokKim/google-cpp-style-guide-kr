"""Tests for scripts/upstream_sections.py."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import upstream_sections as us


def build_document(entries):
    """entries: list of (level, section_id, title, body_html)."""
    parts = ["<html><body>"]
    for level, section_id, title, body in entries:
        parts.append(f'<h{level} id="{section_id}">{title}</h{level}>')
        parts.append(body)
    parts.append("</body></html>")
    return "\n".join(parts)


class SplitSectionsTest(unittest.TestCase):
    def test_every_heading_becomes_one_section(self):
        document = build_document([
            (2, "Scoping", "Scoping", "<p>intro</p>"),
            (3, "Namespaces", "Namespaces", "<p>body</p>"),
            (3, "Internal_Linkage", "Internal Linkage", "<p>body</p>"),
        ])

        sections = us.split_sections(document)

        self.assertEqual([s.id for s in sections],
                         ["Scoping", "Namespaces", "Internal_Linkage"])
        self.assertEqual([s.level for s in sections], [2, 3, 3])
        self.assertEqual(sections[1].title, "Namespaces")

    def test_section_body_stops_at_the_next_heading(self):
        document = build_document([
            (3, "First", "First", "<p>alpha</p>"),
            (3, "Second", "Second", "<p>beta</p>"),
        ])

        sections = us.split_sections(document)

        self.assertIn("alpha", sections[0].text)
        self.assertNotIn("beta", sections[0].text)


class NormalizeTest(unittest.TestCase):
    def test_prose_line_breaks_do_not_change_the_text(self):
        one_line = us.normalize("<p>Avoid virtual method calls in constructors.</p>")
        wrapped = us.normalize(
            "<p>Avoid virtual method\n   calls in\n   constructors.</p>"
        )

        self.assertEqual(one_line, wrapped)

    def test_code_indentation_does_change_the_text(self):
        flat = us.normalize("<pre>if (x) {\n  f();\n}</pre>")
        indented = us.normalize("<pre>if (x) {\n    f();\n}</pre>")

        self.assertNotEqual(flat, indented)

    def test_entities_are_unescaped(self):
        self.assertIn("<int>", us.normalize("<p>vector&lt;int&gt;</p>"))


class SlugTest(unittest.TestCase):
    def test_characters_illegal_in_filenames_are_replaced(self):
        self.assertEqual(us.slug_for("0_and_nullptr/NULL"), "0_and_nullptr_NULL")
        self.assertEqual(us.slug_for("C++_Version"), "C___Version")
        self.assertEqual(
            us.slug_for("Nonmember,_Static_Member,_and_Global_Functions"),
            "Nonmember__Static_Member__and_Global_Functions",
        )

    def test_safe_ids_are_untouched(self):
        self.assertEqual(us.slug_for("Structs_vs._Classes"), "Structs_vs._Classes")


if __name__ == "__main__":
    unittest.main()
