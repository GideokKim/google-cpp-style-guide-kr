#!/usr/bin/env python3
"""Check local translation coverage against the recorded upstream topic map."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / ".omx/ultragoal/upstream-topic-map.json"
DOCS = ROOT / "google cpp style guide"
NAV = ROOT / "mkdocs.yml"


def main() -> int:
    rows = json.loads(MAP.read_text(encoding="utf-8"))
    nav = NAV.read_text(encoding="utf-8")
    missing_files = []
    missing_nav = []
    missing_explanations = []

    for row in rows:
        filename = row["file"]
        path = DOCS / filename
        if not path.exists():
            missing_files.append(filename)
            continue
        if filename not in nav:
            missing_nav.append(filename)
        if "이해하기 쉽게 설명하기" not in path.read_text(encoding="utf-8"):
            missing_explanations.append(filename)

    print(f"upstream_topics={len(rows)}")
    print(f"missing_files={len(missing_files)}")
    print(f"missing_nav={len(missing_nav)}")
    print(f"missing_explanations={len(missing_explanations)}")

    for label, values in (
        ("missing_files", missing_files),
        ("missing_nav", missing_nav),
        ("missing_explanations", missing_explanations),
    ):
        if values:
            print(f"{label}:")
            for value in values:
                print(f"  - {value}")

    return 1 if missing_files or missing_nav or missing_explanations else 0


if __name__ == "__main__":
    raise SystemExit(main())
