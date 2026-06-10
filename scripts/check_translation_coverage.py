#!/usr/bin/env python3
"""Check local translation coverage against the recorded upstream topic map."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "scripts/upstream-topic-map.json"
DOCS = ROOT / "google cpp style guide"
NAV = ROOT / "mkdocs.yml"


def main() -> int:
    rows = json.loads(MAP.read_text(encoding="utf-8"))
    nav = NAV.read_text(encoding="utf-8")
    missing_files = []
    missing_nav = []
    missing_explanations = []
    duplicate_explanations = []
    generic_explanations = []
    explanation_bodies = {}

    for row in rows:
        filename = row["file"]
        path = DOCS / filename
        if not path.exists():
            missing_files.append(filename)
            continue
        if filename not in nav:
            missing_nav.append(filename)
        content = path.read_text(encoding="utf-8")
        if "이해하기 쉽게 설명하기" not in content:
            missing_explanations.append(filename)
        else:
            body = content.split("이해하기 쉽게 설명하기", 1)[1]
            normalized = " ".join(body.split())
            if "원문 규칙을 문자 그대로 외우기보다" in normalized:
                generic_explanations.append(filename)
            explanation_bodies.setdefault(normalized, []).append(filename)

    duplicate_explanations = [
        files for body, files in explanation_bodies.items()
        if body and len(files) > 1
    ]

    print(f"upstream_topics={len(rows)}")
    print(f"missing_files={len(missing_files)}")
    print(f"missing_nav={len(missing_nav)}")
    print(f"missing_explanations={len(missing_explanations)}")
    print(f"generic_explanations={len(generic_explanations)}")
    print(f"duplicate_explanation_bodies={len(duplicate_explanations)}")

    for label, values in (
        ("missing_files", missing_files),
        ("missing_nav", missing_nav),
        ("missing_explanations", missing_explanations),
        ("generic_explanations", generic_explanations),
    ):
        if values:
            print(f"{label}:")
            for value in values:
                print(f"  - {value}")

    if duplicate_explanations:
        print("duplicate_explanation_bodies:")
        for files in duplicate_explanations[:10]:
            print("  - " + ", ".join(files))

    return 1 if (missing_files or missing_nav or missing_explanations or generic_explanations or duplicate_explanations) else 0


if __name__ == "__main__":
    raise SystemExit(main())
