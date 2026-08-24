"""Tests for scripts/upstream_sections.py."""
from __future__ import annotations

import json
import sys
import tempfile
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

    def test_inline_tags_do_not_introduce_spaces(self):
        result = us.normalize(
            "<code><i>&lt;PROJECT&gt;</i>_<i>&lt;PATH&gt;</i></code>"
        )
        self.assertEqual(result, "<PROJECT>_<PATH>")

    def test_prose_and_pre_together_are_both_normalized_correctly(self):
        fragment = (
            "<p>Example:</p>"
            "<pre>if (x) {\n  f();\n}</pre>"
            "<p>That is the pattern.</p>"
        )
        result = us.normalize(fragment)
        self.assertIn("Example:", result)
        self.assertIn("<pre>\nif (x) {\n  f();\n}\n</pre>", result)
        self.assertIn("That is the pattern.", result)
        self.assertLess(result.index("Example:"), result.index("<pre>"))
        self.assertLess(result.index("</pre>"), result.index("That is"))


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


class SnapshotTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self._saved = (us.SNAPSHOT_DIR, us.MANIFEST, us.SECTIONS_DIR)
        us.SNAPSHOT_DIR = root / "upstream"
        us.MANIFEST = us.SNAPSHOT_DIR / "manifest.json"
        us.SECTIONS_DIR = us.SNAPSHOT_DIR / "sections"

    def tearDown(self):
        us.SNAPSHOT_DIR, us.MANIFEST, us.SECTIONS_DIR = self._saved

    def make_sections(self, entries):
        return us.split_sections(build_document(entries))

    def test_round_trip_preserves_section_text(self):
        sections = self.make_sections([
            (3, "Casting", "Casting", "<p>alpha</p>"),
            (3, "0_and_nullptr/NULL", "0 and nullptr/NULL", "<p>beta</p>"),
        ])

        us.write_snapshot(sections, commit="abc1234", source="local")
        manifest, texts = us.load_snapshot()

        self.assertEqual(manifest["upstream_commit"], "abc1234")
        self.assertEqual(set(texts), {"Casting", "0_and_nullptr/NULL"})
        self.assertEqual(texts["Casting"], sections[0].text)

    def test_unsafe_id_is_stored_under_a_safe_filename(self):
        sections = self.make_sections([(3, "0_and_nullptr/NULL", "x", "<p>a</p>")])

        us.write_snapshot(sections, commit=None, source="local")

        self.assertTrue((us.SECTIONS_DIR / "0_and_nullptr_NULL.txt").exists())

    def test_removed_sections_leave_no_stale_file(self):
        first = self.make_sections([
            (3, "Boost", "Boost", "<p>a</p>"),
            (3, "Casting", "Casting", "<p>b</p>"),
        ])
        us.write_snapshot(first, commit=None, source="local")
        second = self.make_sections([(3, "Casting", "Casting", "<p>b</p>")])

        us.write_snapshot(second, commit=None, source="local")

        self.assertFalse((us.SECTIONS_DIR / "Boost.txt").exists())
        self.assertEqual(set(us.load_snapshot()[1]), {"Casting"})

    def test_missing_snapshot_reads_as_none(self):
        self.assertIsNone(us.load_snapshot())

    def test_filename_collision_prevents_write_and_leaves_snapshot_clean(self):
        # A+B and A,B both map to A_B via slug_for
        self.assertEqual(us.slug_for("A+B"), us.slug_for("A,B"))
        sections = self.make_sections([
            (3, "A+B", "A+B", "<p>a</p>"),
            (3, "A,B", "A,B", "<p>b</p>"),
        ])

        with self.assertRaises(SystemExit):
            us.write_snapshot(sections, commit=None, source="local")

        self.assertFalse(us.MANIFEST.exists())

    def test_tampered_section_file_raises_on_load(self):
        sections = self.make_sections([(3, "Casting", "Casting", "<p>alpha</p>")])
        us.write_snapshot(sections, commit=None, source="local")

        target = us.SECTIONS_DIR / "Casting.txt"
        target.write_text("tampered content\n", encoding="utf-8")

        with self.assertRaises(SystemExit):
            us.load_snapshot()

    def test_use_snapshot_dir_redirects_writes_elsewhere(self):
        before = (us.SNAPSHOT_DIR, us.MANIFEST, us.SECTIONS_DIR)
        other = Path(self.tmp.name) / "elsewhere"
        sections = self.make_sections([(3, "Casting", "Casting", "<p>a</p>")])

        try:
            us.use_snapshot_dir(other)
            us.write_snapshot(sections, commit=None, source="local")

            self.assertEqual(us.SNAPSHOT_DIR, other)
            self.assertTrue((other / "manifest.json").exists())
            self.assertTrue((other / "sections" / "Casting.txt").exists())
        finally:
            us.SNAPSHOT_DIR, us.MANIFEST, us.SECTIONS_DIR = before

        # The redirected directory must be distinct from the real repo's
        # snapshot location, and must be restored to the pre-redirect value.
        self.assertNotEqual(other, self._saved[0])
        self.assertEqual(us.SNAPSHOT_DIR, before[0])


class ParseOrDieTest(unittest.TestCase):
    def test_short_document_is_rejected(self):
        document = build_document([(3, "Only", "Only", "<p>a</p>")])

        with self.assertRaises(SystemExit):
            us.parse_or_die(document)

    def test_full_length_document_is_accepted(self):
        entries = [(3, f"Section{i}", f"Section {i}", "<p>a</p>") for i in range(95)]

        sections = us.parse_or_die(build_document(entries))

        self.assertEqual(len(sections), 95)


class CompareTest(unittest.TestCase):
    def sections(self, entries):
        return us.split_sections(build_document(entries))

    def test_reports_changed_added_and_removed(self):
        previous = {
            "Casting": us.normalize("<p>old</p>"),
            "Boost": us.normalize("<p>gone</p>"),
            "Naming": us.normalize("<p>same</p>"),
        }
        current = self.sections([
            (3, "Casting", "Casting", "<p>new</p>"),
            (3, "Naming", "Naming", "<p>same</p>"),
            (3, "Third_party_Libraries", "Third-party Libraries", "<p>fresh</p>"),
        ])

        changes = us.compare(current, previous)

        self.assertEqual([s.id for s, _ in changes.changed], ["Casting"])
        self.assertEqual([s.id for s in changes.added], ["Third_party_Libraries"])
        self.assertEqual(changes.removed, ["Boost"])
        self.assertTrue(changes)

    def test_identical_input_is_falsy(self):
        current = self.sections([(3, "Naming", "Naming", "<p>same</p>")])
        previous = {"Naming": current[0].text}

        self.assertFalse(us.compare(current, previous))


class RenderTest(unittest.TestCase):
    def build_changes(self):
        current = us.split_sections(build_document([
            (3, "Casting", "Casting", "<p>new wording</p>"),
            (3, "Third_party_Libraries", "Third-party Libraries", "<p>fresh</p>"),
        ]))
        previous = {
            "Casting": us.normalize("<p>old wording</p>"),
            "Boost": us.normalize("<p>gone</p>"),
        }
        return us.compare(current, previous)

    def test_body_names_the_translated_file_of_a_changed_section(self):
        body = us.render_issue_body(
            self.build_changes(),
            {"Casting": "casting.md"},
            "aaaaaaaa",
            "bbbbbbbb",
        )

        self.assertIn("casting.md", body)
        self.assertIn("- [ ]", body)

    def test_body_flags_added_and_removed_sections(self):
        body = us.render_issue_body(self.build_changes(), {}, None, None)

        self.assertIn("Third_party_Libraries", body)
        self.assertIn("Boost", body)
        self.assertIn("upstream-topic-map.json", body)

    def test_body_links_the_upstream_compare_view(self):
        body = us.render_issue_body(self.build_changes(), {}, "aaaaaaaa", "bbbbbbbb")

        self.assertIn(
            "https://github.com/google/styleguide/compare/aaaaaaaa...bbbbbbbb", body
        )

    def test_title_carries_the_date_and_short_sha(self):
        title = us.render_issue_title("1809c769abcdef", "2026-06-03T00:00:00Z")

        self.assertEqual(title, "원문 변경 감지: 2026-06-03 (1809c769)")

    def test_diff_excerpt_is_truncated(self):
        before = "\n".join(f"line {i}" for i in range(200))
        after = "\n".join(f"changed {i}" for i in range(200))

        excerpt = us.diff_excerpt(before, after)

        self.assertLessEqual(len(excerpt.splitlines()), us.DIFF_LIMIT + 1)
        self.assertIn("생략", excerpt)

    def test_section_title_with_pipe_escapes_in_table_row(self):
        current = us.split_sections(build_document([
            (3, "Casting", "Casting | Table", "<p>new content</p>"),
        ]))
        previous = {"Casting": us.normalize("<p>old content</p>")}
        changes = us.compare(current, previous)

        body = us.render_issue_body(changes, {"Casting": "casting.md"}, None, None)

        # The table cell should have the pipe escaped, and the structural separators
        # should still number 2 (for a 3-column table)
        table_line = [line for line in body.splitlines()
                      if "Casting" in line and "casting.md" in line][0]
        structural_separators = table_line.count(" | ")
        self.assertEqual(structural_separators, 2)
        self.assertIn("\\|", table_line)

    def test_section_title_with_angle_brackets_escapes_in_summary(self):
        # Use HTML entities so angle brackets survive parsing
        current = us.split_sections(build_document([
            (3, "Template", "Template &lt;T&gt;", "<p>new code</p>"),
        ]))
        previous = {"Template": us.normalize("<p>old code</p>")}
        changes = us.compare(current, previous)

        body = us.render_issue_body(changes, {}, None, None)

        # The title should be wrapped in backticks in the summary
        self.assertIn("`Template <T>`", body)
        # Ensure there's no raw unescaped angle bracket that would break HTML
        self.assertNotIn("<summary>Template <T>", body)

    def test_diff_excerpt_with_backticks_uses_safe_fence(self):
        before = "code with ``` marker"
        after = "different ``` marker"

        excerpt = us.diff_excerpt(before, after)
        fence = us.fence_for_content(excerpt)

        # Fence should be at least 4 backticks since excerpt contains 3
        self.assertGreaterEqual(len(fence), 4)
        # Content should survive unchanged within the fence
        wrapped = f"{fence}diff\n{excerpt}\n{fence}"
        self.assertIn("```", wrapped)

    def test_render_body_with_added_removed_but_no_changed(self):
        section = us.Section(
            id="New_Section",
            level=3,
            title="New Section",
            text="new content"
        )
        changes = us.Changes(changed=[], added=[section], removed=["Old_Section"])

        body = us.render_issue_body(changes, {}, None, None)

        # Should not include the "내용이 바뀐 섹션" heading
        self.assertNotIn("내용이 바뀐 섹션", body)
        # Should include the "섹션 구성 변경" block
        self.assertIn("섹션 구성 변경", body)
        # Should list both added and removed
        self.assertIn("New_Section", body)
        self.assertIn("Old_Section", body)


if __name__ == "__main__":
    unittest.main()
