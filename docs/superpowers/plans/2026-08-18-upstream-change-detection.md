# Upstream Change Detection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 원문 `cppguide.html`이 바뀌면 어느 섹션이 어떻게 바뀌었고 그것이 어느 번역 파일에 해당하는지를 자동으로 이슈에 남긴다.

**Architecture:** 판단 로직 전부를 `scripts/upstream_sections.py` 한 파일에 담고, GitHub Actions 워크플로는 이 스크립트를 호출만 한다. 원문을 `<h2|h3 id="…">` 앵커 기준 113개 섹션으로 쪼개 정규화한 텍스트를 `upstream/`에 스냅샷으로 커밋해 두고, 매주 현재 원문과 비교한다. 차이가 있으면 스냅샷을 갱신하고 이슈를 하나 연다.

**Tech Stack:** Python 3.11 표준 라이브러리만 사용(`re`, `hashlib`, `html`, `json`, `difflib`, `urllib`, `unittest`). 테스트는 `python3 -m unittest`. CI는 GitHub Actions + `gh` CLI.

## Global Constraints

- 설계 근거는 `docs/superpowers/specs/2026-08-18-upstream-change-detection-design.md`. 충돌하면 스펙이 우선한다.
- **새 런타임 의존성을 추가하지 않는다.** `requirements.txt`는 mkdocs 전용이며 손대지 않는다. 스크립트와 테스트는 표준 라이브러리만 쓴다.
- 기존 `scripts/check_translation_coverage.py`의 스타일을 따른다: `#!/usr/bin/env python3`, `from __future__ import annotations`, 모듈 상수로 경로 정의.
- 섹션 최소 개수 임계값은 **90**. 이보다 적게 파싱되면 스냅샷을 건드리지 않고 실패한다.
- 커밋 규칙: Conventional Commits, 타입은 `feat`/`chore`/`docs`/`test`, 스코프는 `upstream`. `docs` 외 타입은 본문 필수(20자 이상). 한 줄 80자 이하. `Co-Authored-By`나 생성 푸터를 붙이지 않는다.
- 브랜치는 `feat/upstream-change-detection` (이미 생성되어 있고 스펙 커밋 `a87cfd0`이 올라가 있다).

---

### Task 1: 섹션 파싱과 정규화

원문 HTML을 섹션으로 쪼개고, 오탐 없이 비교할 수 있는 텍스트로 정규화한다. 이 태스크의 산출물이 나머지 전부의 토대다.

**Files:**
- Create: `scripts/upstream_sections.py`
- Test: `tests/test_upstream_sections.py`

**Interfaces:**
- Consumes: 없음
- Produces:
  - `Section` 데이터클래스 — 필드 `id: str`, `level: int`, `title: str`, `text: str`, 프로퍼티 `sha256 -> str`
  - `split_sections(document: str) -> list[Section]`
  - `normalize(fragment: str) -> str`
  - `slug_for(section_id: str) -> str`
  - 모듈 상수 `MIN_SECTIONS = 90`, `CPPGUIDE_URL`

- [ ] **Step 1: 실패하는 테스트를 작성한다**

`tests/test_upstream_sections.py`를 새로 만든다.

```python
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
```

- [ ] **Step 2: 테스트를 실행해 실패를 확인한다**

Run: `python3 -m unittest tests.test_upstream_sections -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'upstream_sections'`

- [ ] **Step 3: 최소 구현을 작성한다**

`scripts/upstream_sections.py`를 새로 만든다.

```python
#!/usr/bin/env python3
"""Track upstream Google C++ Style Guide sections and report changes."""
from __future__ import annotations

import hashlib
import html
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CPPGUIDE_URL = (
    "https://raw.githubusercontent.com/google/styleguide/gh-pages/cppguide.html"
)
MIN_SECTIONS = 90

HEADING_RE = re.compile(r'<h([23])\s+id="([^"]+)"[^>]*>(.*?)</h\1>', re.S)
PRE_RE = re.compile(r"(<pre\b[^>]*>.*?</pre>)", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")
UNSAFE_RE = re.compile(r"[^A-Za-z0-9._-]")


@dataclass(frozen=True)
class Section:
    id: str
    level: int
    title: str
    text: str

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()


def normalize(fragment: str) -> str:
    """Collapse prose whitespace but keep whitespace inside <pre> intact.

    Prose may be rewrapped upstream without any change in meaning, so it is
    folded to single spaces. Indentation inside a code sample is part of the
    style guide's content, so it is preserved verbatim.
    """
    parts = []
    for chunk in PRE_RE.split(fragment):
        if chunk[:4].lower() == "<pre":
            body = re.sub(r"^<pre\b[^>]*>", "", chunk, flags=re.S | re.I)
            body = re.sub(r"</pre>\s*$", "", body, flags=re.S | re.I)
            code = html.unescape(TAG_RE.sub("", body)).strip("\n")
            parts.append("<pre>\n" + code + "\n</pre>")
        else:
            prose = " ".join(html.unescape(TAG_RE.sub(" ", chunk)).split())
            if prose:
                parts.append(prose)
    return "\n".join(parts)


def split_sections(document: str) -> list[Section]:
    marks = list(HEADING_RE.finditer(document))
    sections = []
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(document)
        title = " ".join(html.unescape(TAG_RE.sub(" ", mark.group(3))).split())
        sections.append(
            Section(
                id=mark.group(2),
                level=int(mark.group(1)),
                title=title,
                text=normalize(document[mark.end():end]),
            )
        )
    return sections


def slug_for(section_id: str) -> str:
    """Section ids contain '/', ',' and '+', which are unusable in filenames."""
    return UNSAFE_RE.sub("_", section_id)
```

- [ ] **Step 4: 테스트를 실행해 통과를 확인한다**

Run: `python3 -m unittest tests.test_upstream_sections -v`
Expected: PASS (7 tests)

- [ ] **Step 5: 실제 원문으로 손검증한다**

Run:
```bash
curl -sL https://raw.githubusercontent.com/google/styleguide/gh-pages/cppguide.html \
  -o /tmp/cppguide.html
python3 -c "
import sys; sys.path.insert(0, 'scripts')
import upstream_sections as us
s = us.split_sections(open('/tmp/cppguide.html').read())
print(len(s), s[0].id, s[-1].id)
"
```
Expected: 첫 줄이 `113`으로 시작한다. 113이 아니면 `HEADING_RE`가 원문 마크업을 놓친 것이므로 다음 태스크로 넘어가기 전에 고친다.

- [ ] **Step 6: 커밋한다**

```bash
git add scripts/upstream_sections.py tests/test_upstream_sections.py
git commit -m "feat(upstream): add cppguide section parser

Split the upstream guide on its h2/h3 anchors and normalize each section
so that prose rewrapping does not register as a change while indentation
inside code samples does."
```

---

### Task 2: 스냅샷 읽기·쓰기와 `snapshot` 명령

파싱된 섹션을 `upstream/`에 기록하고 다시 읽어 들인다. 삭제된 섹션의 잔여 파일이 남지 않아야 하고, 파싱이 비정상일 때 스냅샷을 망가뜨리지 않아야 한다.

**Files:**
- Modify: `scripts/upstream_sections.py`
- Modify: `tests/test_upstream_sections.py`

**Interfaces:**
- Consumes: Task 1의 `Section`, `split_sections`, `slug_for`, `MIN_SECTIONS`
- Produces:
  - `parse_or_die(document: str) -> list[Section]` — 섹션이 `MIN_SECTIONS` 미만이면 `SystemExit`
  - `read_source(source: str) -> str` — `http(s)://`면 내려받고 아니면 파일로 읽음
  - `write_snapshot(sections, *, commit: str | None, source: str) -> None`
  - `load_snapshot() -> tuple[dict, dict[str, str]] | None` — `(manifest, id별 텍스트)`, 스냅샷이 없으면 `None`
  - 모듈 상수 `SNAPSHOT_DIR`, `MANIFEST`, `SECTIONS_DIR`
  - CLI: `python3 scripts/upstream_sections.py snapshot [--source X] [--commit SHA]`

- [ ] **Step 1: 실패하는 테스트를 작성한다**

`tests/test_upstream_sections.py`의 `if __name__ == "__main__":` 앞에 아래를 추가한다. 파일 맨 위 import에 `import json`과 `import tempfile`을 더한다.

```python
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


class ParseOrDieTest(unittest.TestCase):
    def test_short_document_is_rejected(self):
        document = build_document([(3, "Only", "Only", "<p>a</p>")])

        with self.assertRaises(SystemExit):
            us.parse_or_die(document)

    def test_full_length_document_is_accepted(self):
        entries = [(3, f"Section{i}", f"Section {i}", "<p>a</p>") for i in range(95)]

        sections = us.parse_or_die(build_document(entries))

        self.assertEqual(len(sections), 95)
```

- [ ] **Step 2: 테스트를 실행해 실패를 확인한다**

Run: `python3 -m unittest tests.test_upstream_sections -v`
Expected: FAIL — `AttributeError: module 'upstream_sections' has no attribute 'write_snapshot'`

- [ ] **Step 3: 최소 구현을 작성한다**

`scripts/upstream_sections.py`의 import에 `argparse`, `json`, `sys`, `urllib.request`, `from datetime import datetime, timezone`을 추가하고, `ROOT` 아래에 경로 상수를, 파일 끝에 아래 함수와 CLI를 추가한다.

```python
SNAPSHOT_DIR = ROOT / "upstream"
MANIFEST = SNAPSHOT_DIR / "manifest.json"
SECTIONS_DIR = SNAPSHOT_DIR / "sections"
TOPIC_MAP = ROOT / "scripts/upstream-topic-map.json"
```

```python
def read_source(source: str) -> str:
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source, timeout=60) as response:
            return response.read().decode("utf-8")
    return Path(source).read_text(encoding="utf-8")


def parse_or_die(document: str) -> list[Section]:
    sections = split_sections(document)
    if len(sections) < MIN_SECTIONS:
        raise SystemExit(
            f"parsed only {len(sections)} sections, expected at least "
            f"{MIN_SECTIONS}; refusing to touch the snapshot"
        )
    return sections


def write_snapshot(sections, *, commit: str | None, source: str) -> None:
    owners: dict[str, str] = {}
    for section in sections:
        slug = slug_for(section.id)
        if slug in owners:
            raise SystemExit(
                f"filename collision: '{section.id}' and '{owners[slug]}' "
                f"both map to {slug}.txt"
            )
        owners[slug] = section.id

    SECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    for stale in SECTIONS_DIR.glob("*.txt"):
        stale.unlink()
    for section in sections:
        target = SECTIONS_DIR / f"{slug_for(section.id)}.txt"
        target.write_text(section.text + "\n", encoding="utf-8")

    manifest = {
        "source": source,
        "upstream_commit": commit,
        "captured_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sections": [
            {
                "id": section.id,
                "level": section.level,
                "title": section.title,
                "file": f"{slug_for(section.id)}.txt",
                "sha256": section.sha256,
            }
            for section in sections
        ],
    }
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def load_snapshot():
    if not MANIFEST.exists():
        return None
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    texts = {
        row["id"]: (SECTIONS_DIR / row["file"]).read_text(encoding="utf-8").rstrip("\n")
        for row in manifest["sections"]
    }
    return manifest, texts


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    snapshot = sub.add_parser("snapshot", help="rewrite the stored snapshot")
    snapshot.add_argument("--source", default=CPPGUIDE_URL)
    snapshot.add_argument("--commit", default=None)

    args = parser.parse_args(argv)
    document = read_source(args.source)
    sections = parse_or_die(document)

    if args.command == "snapshot":
        write_snapshot(sections, commit=args.commit, source=args.source)
        print(f"wrote {len(sections)} sections to {SNAPSHOT_DIR}")
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: 테스트를 실행해 통과를 확인한다**

Run: `python3 -m unittest tests.test_upstream_sections -v`
Expected: PASS (13 tests)

- [ ] **Step 5: 커밋한다**

```bash
git add scripts/upstream_sections.py tests/test_upstream_sections.py
git commit -m "feat(upstream): store and load section snapshots

Write one text file per section plus a manifest of hashes, mapping ids
that contain '/' or ',' onto safe filenames. Refuse to write when the
parse yields fewer sections than expected, so a broken fetch cannot
destroy the baseline."
```

---

### Task 3: 변경 비교와 이슈 본문 렌더링

스냅샷과 현재 원문을 비교해 이슈 본문 마크다운을 만든다.

**Files:**
- Modify: `scripts/upstream_sections.py`
- Modify: `tests/test_upstream_sections.py`

**Interfaces:**
- Consumes: Task 2의 `load_snapshot`, `parse_or_die`, `read_source`, `TOPIC_MAP`
- Produces:
  - `Changes` 데이터클래스 — 필드 `changed: list[tuple[Section, str]]`, `added: list[Section]`, `removed: list[str]`, 진리값은 셋 중 하나라도 비어 있지 않으면 참
  - `compare(sections, previous_texts) -> Changes`
  - `load_topic_map() -> dict[str, str]` — 섹션 id → 번역 파일명
  - `diff_excerpt(previous_text: str, current_text: str) -> str`
  - `render_issue_title(commit: str | None, captured_at: str) -> str`
  - `render_issue_body(changes, topic_map, previous_commit, current_commit) -> str`
  - CLI: `python3 scripts/upstream_sections.py diff [--source X] [--title-out PATH]`

- [ ] **Step 1: 실패하는 테스트를 작성한다**

`tests/test_upstream_sections.py`의 `if __name__ == "__main__":` 앞에 추가한다.

```python
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
```

- [ ] **Step 2: 테스트를 실행해 실패를 확인한다**

Run: `python3 -m unittest tests.test_upstream_sections -v`
Expected: FAIL — `AttributeError: module 'upstream_sections' has no attribute 'compare'`

- [ ] **Step 3: 최소 구현을 작성한다**

import에 `difflib`을 추가하고, `MIN_SECTIONS` 옆에 `DIFF_LIMIT = 40`을 추가한다. `main` 앞에 아래를 넣는다.

````python
@dataclass
class Changes:
    changed: list
    added: list
    removed: list

    def __bool__(self) -> bool:
        return bool(self.changed or self.added or self.removed)


def compare(sections, previous_texts) -> Changes:
    changed, added = [], []
    for section in sections:
        if section.id not in previous_texts:
            added.append(section)
        elif previous_texts[section.id] != section.text:
            changed.append((section, previous_texts[section.id]))
    current_ids = {section.id for section in sections}
    removed = [key for key in previous_texts if key not in current_ids]
    return Changes(changed=changed, added=added, removed=removed)


def load_topic_map() -> dict[str, str]:
    rows = json.loads(TOPIC_MAP.read_text(encoding="utf-8"))
    return {row["id"]: row["file"] for row in rows}


def diff_excerpt(previous_text: str, current_text: str) -> str:
    lines = list(
        difflib.unified_diff(
            previous_text.splitlines(),
            current_text.splitlines(),
            fromfile="before",
            tofile="after",
            lineterm="",
            n=1,
        )
    )
    if len(lines) > DIFF_LIMIT:
        omitted = len(lines) - DIFF_LIMIT
        lines = lines[:DIFF_LIMIT] + [f"... ({omitted}줄 생략)"]
    return "\n".join(lines)


def render_issue_title(commit: str | None, captured_at: str) -> str:
    short = commit[:8] if commit else "unknown"
    return f"원문 변경 감지: {captured_at[:10]} ({short})"


def render_issue_body(changes, topic_map, previous_commit, current_commit) -> str:
    out = []
    if previous_commit and current_commit:
        out += [
            "원문 비교: https://github.com/google/styleguide/compare/"
            f"{previous_commit}...{current_commit}",
            "",
        ]

    if changes.changed:
        out += [
            "## 내용이 바뀐 섹션",
            "",
            "| 섹션 | 원문 제목 | 번역 파일 |",
            "| --- | --- | --- |",
        ]
        for section, _ in changes.changed:
            target = topic_map.get(section.id)
            cell = f"`google cpp style guide/{target}`" if target else "(매핑 없음)"
            out.append(f"| `{section.id}` | {section.title} | {cell} |")
        out += ["", "### 할 일", ""]
        for section, _ in changes.changed:
            target = topic_map.get(section.id, "(매핑 없음)")
            out.append(f"- [ ] `google cpp style guide/{target}`")
        out += ["", "### 변경 내용", ""]
        for section, previous_text in changes.changed:
            out += [
                "<details>",
                f"<summary>{section.title} (<code>{section.id}</code>)</summary>",
                "",
                "```diff",
                diff_excerpt(previous_text, section.text),
                "```",
                "",
                "</details>",
                "",
            ]

    if changes.added or changes.removed:
        out += [
            "## 섹션 구성 변경",
            "",
            "아래는 번역 본문뿐 아니라 `scripts/upstream-topic-map.json`과 "
            "`mkdocs.yml` nav도 함께 손봐야 합니다.",
            "",
        ]
        for section in changes.added:
            out.append(
                f"- [ ] 추가됨: `{section.id}` — {section.title} (새 `.md` 파일 필요)"
            )
        for section_id in changes.removed:
            out.append(f"- [ ] 삭제됨: `{section_id}` — 번역 파일과 nav 항목 정리 필요")
        out.append("")

    return "\n".join(out).rstrip() + "\n"
````

그리고 `main`의 서브파서와 분기를 아래로 교체한다.

```python
    diff_cmd = sub.add_parser("diff", help="compare upstream against the snapshot")
    diff_cmd.add_argument("--source", default=CPPGUIDE_URL)
    diff_cmd.add_argument("--commit", default=None)
    diff_cmd.add_argument("--title-out", default=None)
```

```python
    if args.command == "diff":
        stored = load_snapshot()
        if stored is None:
            raise SystemExit(
                f"no snapshot at {MANIFEST}; run 'snapshot' once to create it"
            )
        manifest, previous_texts = stored
        changes = compare(sections, previous_texts)
        if not changes:
            return 0
        body = render_issue_body(
            changes, load_topic_map(), manifest.get("upstream_commit"), args.commit
        )
        if args.title_out:
            title = render_issue_title(
                args.commit, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            )
            Path(args.title_out).write_text(title + "\n", encoding="utf-8")
        sys.stdout.write(body)
        return 0
```

- [ ] **Step 4: 테스트를 실행해 통과를 확인한다**

Run: `python3 -m unittest tests.test_upstream_sections -v`
Expected: PASS (20 tests)

- [ ] **Step 5: 커밋한다**

```bash
git add scripts/upstream_sections.py tests/test_upstream_sections.py
git commit -m "feat(upstream): render a change report for the issue body

Compare the parsed guide against the snapshot and emit markdown naming
each changed section, the translated file it maps to, and a truncated
diff. Added and removed sections are listed separately because they also
require topic-map and nav updates."
```

---

### Task 4: 과거 릴리스 회귀 검증과 최초 스냅샷

스펙에 기록된 기준값(11 / 11+추가1+삭제1 / 1)이 실제로 재현되는지 확인하고, 재현되면 현재 원문으로 최초 스냅샷을 커밋한다.

**Files:**
- Create: `scripts/verify_upstream_history.sh`
- Modify: `docs/superpowers/specs/2026-08-18-upstream-change-detection-design.md` (측정 결과가 다를 경우에만)
- Create: `upstream/manifest.json`, `upstream/sections/*.txt` (스크립트가 생성)

**Interfaces:**
- Consumes: Task 2의 `snapshot`, Task 3의 `diff` CLI
- Produces: 커밋된 최초 스냅샷. 이후 모든 실행이 이 기준과 비교한다.

- [ ] **Step 1: 검증 스크립트를 작성한다**

`scripts/verify_upstream_history.sh`를 새로 만든다.

```bash
#!/usr/bin/env bash
# Replay past upstream releases through the detector and print what it finds.
#
# Expected, measured on 2026-08-18:
#   c885dc26 -> 11 changed, 0 added, 0 removed
#   3c5c895c -> 11 changed, 1 added, 1 removed
#   1809c769 ->  1 changed, 0 added, 0 removed
set -euo pipefail

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

for sha in c6f57a91 c885dc26 3c5c895c 1809c769; do
  curl -sL "https://raw.githubusercontent.com/google/styleguide/$sha/cppguide.html" \
    -o "$work/$sha.html"
done

python3 scripts/upstream_sections.py snapshot \
  --source "$work/c6f57a91.html" --commit c6f57a91 >/dev/null

for sha in c885dc26 3c5c895c 1809c769; do
  echo "=== $sha"
  python3 scripts/upstream_sections.py diff \
    --source "$work/$sha.html" --commit "$sha" \
    | grep -cE '^\| `' || true
  python3 scripts/upstream_sections.py diff \
    --source "$work/$sha.html" --commit "$sha" \
    | grep -E '^- \[ \] (추가됨|삭제됨)' || true
  python3 scripts/upstream_sections.py snapshot \
    --source "$work/$sha.html" --commit "$sha" >/dev/null
done
```

- [ ] **Step 2: 검증을 실행한다**

Run:
```bash
chmod +x scripts/verify_upstream_history.sh
git stash list >/dev/null  # 스냅샷을 덮어쓰므로 작업 트리가 깨끗한지 확인
./scripts/verify_upstream_history.sh
```
Expected:
```
=== c885dc26
11
=== 3c5c895c
11
- [ ] 추가됨: `Third_party_Libraries` — ...
- [ ] 삭제됨: `Boost` — ...
=== 1809c769
1
```
표 행 수가 기준값과 다르면 정규화 규칙이 스펙과 어긋난 것이다. 실제 diff를 눈으로 확인해 원인을 판단하고, 정규화가 틀렸으면 Task 1로 돌아가 고친다. 원문이 실제로 그렇게 바뀐 것이면 스펙의 표를 실측값으로 갱신한다.

- [ ] **Step 3: 회귀 검증 결과로 남은 스냅샷을 버리고 현재 원문으로 다시 만든다**

Run:
```bash
git checkout -- upstream 2>/dev/null || rm -rf upstream
python3 scripts/upstream_sections.py snapshot \
  --commit "$(gh api 'repos/google/styleguide/commits?path=cppguide.html&sha=gh-pages&per_page=1' --jq '.[0].sha')"
python3 -c "
import json
m = json.load(open('upstream/manifest.json'))
print(len(m['sections']), m['upstream_commit'][:8])
"
```
Expected: `113`과 현재 원문 커밋의 짧은 sha가 출력된다.

- [ ] **Step 4: 스냅샷이 안정적인지 확인한다**

Run: `python3 scripts/upstream_sections.py diff`
Expected: 출력 없음, 종료 코드 0. 방금 만든 스냅샷과 현재 원문이 같으므로 아무것도 보고하지 않아야 한다.

- [ ] **Step 5: 커밋한다**

```bash
git add scripts/verify_upstream_history.sh upstream
git commit -m "chore(upstream): add history replay check and seed the snapshot

Replaying the last four upstream releases reproduces the section counts
recorded in the design, so the normalization rules hold. Seed the
baseline from the current guide; changes before this point are out of
reach of the detector by construction."
```

---

### Task 5: GitHub Actions 워크플로

주 1회 감지하고, 변경이 있으면 스냅샷을 커밋하고 이슈를 연다.

**Files:**
- Create: `.github/workflows/upstream-watch.yml`
- Modify: `README.md` (검증 섹션에 새 스크립트 안내 추가)

**Interfaces:**
- Consumes: Task 3의 `diff --title-out`, Task 2의 `snapshot --commit`
- Produces: 없음 (최종 산출물)

- [ ] **Step 1: 워크플로를 작성한다**

`.github/workflows/upstream-watch.yml`을 새로 만든다. 기존 `gh-pages.yml`과 같은 액션 버전을 쓴다.

```yaml
name: "Upstream watch"

on:
  workflow_dispatch:
  schedule:
    - cron: "0 0 * * 1"

permissions:
  contents: write
  issues: write

jobs:
  watch:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: 3.11
          architecture: x64

      - name: "Fetch upstream guide"
        id: fetch
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          set -euo pipefail
          curl -sSfL \
            https://raw.githubusercontent.com/google/styleguide/gh-pages/cppguide.html \
            -o cppguide.html
          sha="$(gh api \
            'repos/google/styleguide/commits?path=cppguide.html&sha=gh-pages&per_page=1' \
            --jq '.[0].sha')"
          echo "sha=$sha" >> "$GITHUB_OUTPUT"

      - name: "Detect changes"
        id: detect
        run: |
          set -euo pipefail
          python3 scripts/upstream_sections.py diff \
            --source cppguide.html \
            --commit "${{ steps.fetch.outputs.sha }}" \
            --title-out issue-title.txt > issue-body.md
          if [ -s issue-body.md ]; then
            echo "changed=true" >> "$GITHUB_OUTPUT"
          fi

      - name: "Refresh snapshot"
        if: steps.detect.outputs.changed == 'true'
        run: |
          set -euo pipefail
          python3 scripts/upstream_sections.py snapshot \
            --source cppguide.html \
            --commit "${{ steps.fetch.outputs.sha }}"
          git config user.name "github-actions[bot]"
          git config user.email \
            "41898282+github-actions[bot]@users.noreply.github.com"
          git add upstream
          git commit -m "chore(upstream): refresh section snapshot

          Detected an upstream change and recorded the new baseline. The
          translation work itself is tracked in the issue opened by the
          same workflow run."
          git push

      - name: "Open issue"
        if: steps.detect.outputs.changed == 'true'
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          set -euo pipefail
          gh issue create \
            --title "$(cat issue-title.txt)" \
            --body-file issue-body.md \
            --label documentation \
            --label enhancement

      - name: "Dump report on failure"
        if: failure() && steps.detect.outputs.changed == 'true'
        run: |
          echo "이슈 생성에 실패했습니다. 아래 본문으로 수동 생성하세요."
          cat issue-body.md
```

마지막 스텝은 스펙의 오류 처리 항목을 만족시키기 위한 것이다. 스냅샷 커밋은 이미 이루어졌을 수 있으므로 재실행해도 변경이 감지되지 않는다. 이때 유일한 복구 수단이 실행 로그에 남은 본문이다.

- [ ] **Step 2: 워크플로 문법을 확인한다**

Run:
```bash
python3 -c "
import json, sys
try:
    import yaml
except ImportError:
    sys.exit('pyyaml 없음 - 이 단계는 건너뛰고 Step 4의 실제 실행으로 검증한다')
d = yaml.safe_load(open('.github/workflows/upstream-watch.yml'))
print(sorted(d['jobs']['watch']['steps'][0]))
"
```
Expected: 파싱 성공 또는 pyyaml 부재 메시지. 파싱 오류가 나면 들여쓰기를 고친다.

- [ ] **Step 3: README에 안내를 추가한다**

`README.md`의 "🧪 번역 범위 검증" 섹션 끝에 아래 문단을 추가한다.

```markdown
원문 변경 감지는 `.github/workflows/upstream-watch.yml`이 매주 수행합니다. 로컬에서 직접 확인하려면 다음을 실행하세요.

```bash
python3 scripts/upstream_sections.py diff   # 변경이 있으면 이슈 본문용 마크다운을 출력
python3 scripts/upstream_sections.py snapshot  # 기준 스냅샷 갱신
```

기준 스냅샷은 `upstream/`에 있으며, 워크플로가 변경을 감지할 때마다 자동으로 갱신됩니다.
```

- [ ] **Step 4: 커밋하고 PR을 올린 뒤 수동 실행으로 검증한다**

```bash
git add .github/workflows/upstream-watch.yml README.md
git commit -m "feat(upstream): watch the upstream guide weekly

Run the detector every Monday, refresh the snapshot when it reports a
change, and open one issue per upstream release listing the affected
translation files."
git push -u origin feat/upstream-change-detection
gh pr create --base main --fill
```

PR을 머지한 뒤 `main`에서 수동 실행한다.

```bash
gh workflow run "Upstream watch"
sleep 60
gh run list --workflow "Upstream watch" --limit 1
```
Expected: 결론이 `success`이고, 스냅샷이 현재 원문과 같으므로 **이슈가 생성되지 않는다.**

- [ ] **Step 5: 감지 경로가 실제로 동작하는지 확인한다**

스냅샷 파일 하나를 일부러 훼손해 감지·이슈 생성 경로를 실제로 태운다.

```bash
git checkout main && git pull
python3 -c "
from pathlib import Path
p = Path('upstream/sections/Casting.txt')
p.write_text('의도적으로 훼손한 내용\n', encoding='utf-8')
"
git add upstream && git commit -m "test(upstream): perturb one section to exercise the watcher

Verify end to end that a differing snapshot produces an issue and a
refreshed baseline. Reverted immediately after the run."
git push
gh workflow run "Upstream watch"
sleep 90
gh issue list --limit 1
```
Expected: `원문 변경 감지: …` 제목의 이슈가 열리고, 본문에 `Casting` 행과 `google cpp style guide/casting.md`가 보이며, 워크플로가 스냅샷을 원래대로 되돌리는 커밋을 푸시한다.

확인한 뒤 검증용 이슈를 닫는다.

```bash
gh issue close <번호> --comment "감지 경로 검증용 이슈입니다. 실제 원문 변경이 아니므로 닫습니다."
```

---

## 완료 조건

- `python3 -m unittest tests.test_upstream_sections -v` 전부 통과
- `./scripts/verify_upstream_history.sh`가 스펙의 기준값(11 / 11+1+1 / 1)을 재현
- `python3 scripts/upstream_sections.py diff`가 현재 원문에 대해 아무것도 출력하지 않음
- `Upstream watch` 워크플로 수동 실행이 성공하고, 스냅샷을 훼손했을 때 이슈가 실제로 열림
