# Google C++ Style Guide - 한글 번역

이 저장소는 [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)의 한글 번역본을 제공합니다.
Google C++ Style Guide는 C++ 코드 작성 시 권장되는 스타일과 모범 사례를 정의한 문서입니다.
이 번역 프로젝트는 한국어 사용자들이 스타일 가이드를 더 쉽게 이해하고 활용할 수 있도록 돕기 위해 시작되었습니다.

---

## 📌 프로젝트 개요

- **원작**: [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- **라이선스**: [Apache License 2.0](./LICENSE)
- **번역 목적**: 한국어 사용자들이 Google의 C++ 스타일 가이드를 보다 쉽게 접근할 수 있도록 지원.

---

## 📂 디렉토리 구조

```text
repository/
├── LICENSE                         # 라이선스 파일
├── NOTICE                          # 원작 정보 고지
├── README.md                       # 프로젝트 소개
├── mkdocs.yml                      # MkDocs 사이트 설정
└── google cpp style guide/         # MkDocs 문서 루트 및 번역본 파일
```

---

## 🚀 진행 상황

| 작업 내용               | 상태 | 완료 날짜  | 업데이트 날짜 |
| ----------------------- | ---- | ---------- | ------------- |
| 저장소 생성             | ✅   | 2025-01-12 | -             |
| 기본 설정 진행          | ✅   | 2025-01-12 | -             |
| GitHub Pages 설정       | ✅   | 2025-01-12 | -             |
| C++ Version             | ✅   | 2025-11-19 | 2026-06-14    |
| Header Files            | ✅   | 2025-12-31 | 2026-06-14    |
| Scoping                 | ✅   | 2026-06-10 | 2026-07-28    |
| Classes                 | ✅   | 2026-06-10 | 2026-08-26    |
| Functions               | ✅   | 2026-06-10 | 2026-06-14    |
| Google-Specific Magic   | ✅   | 2026-06-10 | 2026-06-14    |
| Other C++ Features      | ✅   | 2026-06-10 | 2026-06-14    |
| Inclusive Language      | ✅   | 2026-06-10 | 2026-06-14    |
| Naming                  | ✅   | 2026-06-10 | 2026-06-14    |
| Comments                | ✅   | 2026-06-10 | 2026-06-14    |
| Formatting              | ✅   | 2026-06-10 | 2026-06-15    |
| Exceptions to the Rules | ✅   | 2026-06-10 | 2026-06-16    |

> **Note:** 번역 상태는 공식 원문 변경에 따라 계속 업데이트될 수 있습니다.
> `완료 날짜`는 해당 섹션의 번역이 처음 완료된 날짜, `업데이트 날짜`는 이후 원문 반영이나
> 번역 개선이 마지막으로 이루어진 날짜입니다.

## 🧪 번역 범위 검증

이 저장소는 `scripts/upstream-topic-map.json`을 현재 번역 범위의 기준 목록으로 사용합니다. 이 파일은 공식 Google C++ Style Guide의 주요 제목과 하위 제목을 기록한 manifest입니다.

새 원문 주제가 추가되거나 문서 구조가 바뀌면 다음을 함께 갱신하세요.

1. `scripts/upstream-topic-map.json`
2. 대응하는 번역 Markdown 파일
3. `mkdocs.yml` navigation
4. 각 페이지의 `옮긴이 풀이` 섹션

로컬 검증 명령:

```bash
python3 scripts/check_translation_coverage.py
mkdocs build --strict
```

원문 변경 감지는 `.github/workflows/upstream-watch.yml`이 매주 수행합니다. 로컬에서 직접 확인하려면 다음을 실행하세요.

```bash
python3 scripts/upstream_sections.py diff   # 변경이 있으면 이슈 본문용 마크다운을 출력
python3 scripts/upstream_sections.py snapshot  # 기준 스냅샷 갱신
```

기준 스냅샷은 `upstream/`에 있으며, 워크플로가 변경을 감지할 때마다 자동으로 갱신됩니다.

## 📖 참고 자료

- [Google C++ Style Guide (원문)](https://google.github.io/styleguide/cppguide.html)
- [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)
