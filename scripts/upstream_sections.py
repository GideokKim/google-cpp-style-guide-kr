#!/usr/bin/env python3
"""Track upstream Google C++ Style Guide sections and report changes."""
from __future__ import annotations

import argparse
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
