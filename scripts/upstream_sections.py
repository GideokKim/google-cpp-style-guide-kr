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
