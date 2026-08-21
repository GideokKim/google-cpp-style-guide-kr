#!/usr/bin/env python3
"""Track upstream Google C++ Style Guide sections and report changes."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import html
import json
import re
import sys
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SNAPSHOT_DIR = ROOT / "upstream"
MANIFEST = SNAPSHOT_DIR / "manifest.json"
SECTIONS_DIR = SNAPSHOT_DIR / "sections"
TOPIC_MAP = ROOT / "scripts/upstream-topic-map.json"

CPPGUIDE_URL = (
    "https://raw.githubusercontent.com/google/styleguide/gh-pages/cppguide.html"
)
MIN_SECTIONS = 90
DIFF_LIMIT = 40

HEADING_RE = re.compile(r'<h([23])\s+id="([^"]+)"[^>]*>(.*?)</h\1>', re.S)
PRE_RE = re.compile(r"(<pre\b[^>]*>.*?</pre>)", re.S | re.I)
INLINE_TAG_RE = re.compile(
    r"</?(?:i|b|em|strong|code|a|span|tt|sub|sup)\b[^>]*>", re.I
)
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
            prose = " ".join(
                html.unescape(TAG_RE.sub(" ", INLINE_TAG_RE.sub("", chunk)))
                .split()
            )
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


def use_snapshot_dir(path: Path) -> None:
    """Point the snapshot at a different directory, for replays and tests."""
    global SNAPSHOT_DIR, MANIFEST, SECTIONS_DIR
    SNAPSHOT_DIR = path
    MANIFEST = SNAPSHOT_DIR / "manifest.json"
    SECTIONS_DIR = SNAPSHOT_DIR / "sections"


def slug_for(section_id: str) -> str:
    """Section ids contain '/', ',' and '+', which are unusable in filenames."""
    return UNSAFE_RE.sub("_", section_id)


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
    for section in sections:
        target = SECTIONS_DIR / f"{slug_for(section.id)}.txt"
        target.write_text(section.text + "\n", encoding="utf-8")

    new_files = {f"{slug_for(s.id)}.txt" for s in sections}
    for stale in SECTIONS_DIR.glob("*.txt"):
        if stale.name not in new_files:
            stale.unlink()

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


def escape_table_cell(text: str) -> str:
    """Escape pipe characters in a markdown table cell."""
    return text.replace("|", "\\|")


def fence_for_content(content: str) -> str:
    """Return a code fence marker that won't be prematurely closed by the content.

    Finds the longest run of consecutive backticks in the content and returns
    a fence marker with at least one more backtick, minimum three.
    """
    max_run = 0
    current_run = 0
    for char in content:
        if char == "`":
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 0
    fence_length = max(3, max_run + 1)
    return "`" * fence_length


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
            out.append(f"| `{section.id}` | {escape_table_cell(section.title)} | {cell} |")
        out += ["", "### 할 일", ""]
        for section, _ in changes.changed:
            target = topic_map.get(section.id, "(매핑 없음)")
            out.append(f"- [ ] `google cpp style guide/{target}`")
        out += ["", "### 변경 내용", ""]
        for section, previous_text in changes.changed:
            excerpt = diff_excerpt(previous_text, section.text)
            fence = fence_for_content(excerpt)
            out += [
                "<details>",
                f"<summary>`{section.title}` (<code>{section.id}</code>)</summary>",
                "",
                f"{fence}diff",
                excerpt,
                fence,
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


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    snapshot = sub.add_parser("snapshot", help="rewrite the stored snapshot")
    snapshot.add_argument("--source", default=CPPGUIDE_URL)
    snapshot.add_argument("--commit", default=None)
    snapshot.add_argument("--snapshot-dir", default=None)

    diff_cmd = sub.add_parser("diff", help="compare upstream against the snapshot")
    diff_cmd.add_argument("--source", default=CPPGUIDE_URL)
    diff_cmd.add_argument("--commit", default=None)
    diff_cmd.add_argument("--title-out", default=None)
    diff_cmd.add_argument("--snapshot-dir", default=None)

    args = parser.parse_args(argv)
    if args.snapshot_dir:
        use_snapshot_dir(Path(args.snapshot_dir))
    document = read_source(args.source)
    sections = parse_or_die(document)

    if args.command == "snapshot":
        write_snapshot(sections, commit=args.commit, source=args.source)
        print(f"wrote {len(sections)} sections to {SNAPSHOT_DIR}")
        return 0

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

    return 0


if __name__ == "__main__":
    sys.exit(main())
