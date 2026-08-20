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
