# 전처리기 지시문 (Preprocessor Directives)

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

### 핵심: `#`은 항상 줄 맨 앞에

전처리기 지시문의 `#`은 들여쓰기된 코드 안에 있더라도 **항상 줄 맨 앞**에서 시작해야 합니다.

```cpp
  if (lopsided_score) {
#if DISASTER_PENDING      // 맞음 - 줄 맨 앞에서 시작
    DropEverything();
# if NOTIFY               // # 뒤 공백은 OK(필수 아님)
    NotifyClient();
# endif
#endif
    BackToNormal();
  }
```

`#if`/`#endif`를 코드 들여쓰기에 맞춰 들여쓰는 것은 잘못입니다.
