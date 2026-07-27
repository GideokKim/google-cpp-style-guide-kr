# 열거자 이름 (Enumerator Names)

열거자(범위가 지정된 열거형과 범위가 지정되지 않은 열거형 모두)는 매크로가 아닌 상수와 같은 이름을 지정해야 합니다. 즉, ENUM_NAME이 아닌 kEnumName을 사용하십시오.

```cpp
enum class UrlTableError {
  kOk = 0,
  kOutOfMemory,
  kMalformedInput,
};
```

```cpp
enum class AlternateUrlTableError {
  OK = 0,
  OUT_OF_MEMORY = 1,
  MALFORMED_INPUT = 2,
};
```

2009년 1월까지는 매크로와 같은 열거형 값의 이름을 지정하는 것이 스타일이었습니다. 이로 인해 열거형 값과 매크로 간의 이름 충돌 문제가 발생했습니다. 따라서 상수 스타일 이름 지정을 선호하도록 변경되었습니다. 새 코드는 상수 스타일 이름을 사용해야 합니다.

---

## 옮긴이 풀이

### 핵심: 열거자는 상수처럼 (k 접두사)

열거자(scoped/unscoped 모두)는 매크로 스타일(`ENUM_NAME`)이 아니라 **상수 스타일**(`kEnumName`)로 씁니다.

```cpp
enum class UrlTableError {
  kOk = 0,
  kOutOfMemory,
  kMalformedInput,
};
```

(과거에는 매크로 스타일이었으나 매크로와의 이름 충돌 문제로 2009년에 상수 스타일로 바뀌었습니다. 새 코드는 상수 스타일을 쓰세요.)
