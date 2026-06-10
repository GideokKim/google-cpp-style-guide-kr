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

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 전처리기 지시문이 들여쓰기된 코드 본문 내에 있는 경우에도 지시문은 줄의 시작 부분에서 시작해야 합니다.

실제로 코드를 볼 때는 전처리기 지시문을 시작하는 해시 표시는 항상 줄의 시작 부분에 있어야 합니다.

점검할 때는 특히 다음을 확인하세요:

- 이 선택이 독자에게 숨은 전제나 비용을 만들지 않는지 확인하세요.
