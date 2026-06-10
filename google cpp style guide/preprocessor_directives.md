# 전처리기 지시문 (Preprocessor Directives)

## 원문 규칙 번역

전처리기 지시문을 시작하는 해시 표시는 항상 줄의 시작 부분에 있어야 합니다.

전처리기 지시문이 들여쓰기된 코드 본문 내에 있는 경우에도 지시문은 줄의 시작 부분에서 시작해야 합니다.

```cpp
// Good - directives at beginning of line
  if (lopsided_score) {
#if DISASTER_PENDING      // Correct -- Starts at beginning of line
    DropEverything();
# if NOTIFY               // OK but not required -- Spaces after #
    NotifyClient();
# endif
#endif
    BackToNormal();
  }
```

```cpp
// Bad - indented directives
  if (lopsided_score) {
    #if DISASTER_PENDING  // Wrong!  The "#if" should be at beginning of line
    DropEverything();
    #endif                // Wrong!  Do not indent "#endif"
    BackToNormal();
  }
```

---

## 이해하기 쉽게 설명하기

전처리기 지시문 규칙을 적용할 때는 원문 규칙을 문자 그대로 외우기보다, 왜 이 선택이 독자에게 더 명확한지 살펴보면 쉽습니다. 코드 리뷰에서는 이 기능이 호출 지점에서 의도를 숨기지 않는지, 더 단순한 구조로 같은 목적을 달성할 수 없는지, 기존 코드와 섞였을 때 유지보수 비용이 커지지 않는지를 확인하세요.
