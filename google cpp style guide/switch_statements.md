# switch 문 (Switch Statements)

열거된 값에 대한 조건이 아닌 경우 스위치 문에는 항상 기본 사례가 있어야 합니다(열거된 값의 경우 값이 처리되지 않으면 컴파일러에서 경고합니다). 기본 사례가 실행되지 않아야 하는 경우 이를 오류로 처리합니다. 예를 들어:

```cpp
switch (var) {
  case 0: {
    ...
    break;
  }
  case 1: {
    ...
    break;
  }
  default: {
    LOG(FATAL) << "Invalid value in switch statement: " << var;
  }
}
```

한 케이스 레이블에서 다른 케이스 레이블로의 폴스루(fallthrough)는 `[[fallthrough]];`로 표시해야 합니다. `[[fallthrough]];`는 다음 케이스 레이블로 넘어갈 수 있는 실행 지점에 배치되어야 합니다. 일반적인 예외는 중간 코드가 없는 연속 케이스 레이블이며, 이 경우 주석이 필요하지 않습니다.

```cpp
switch (x) {
  case 41:  // No annotation needed here.
  case 43:
    if (dont_be_picky) {
      // Use this instead of or along with annotations in comments.
      [[fallthrough]];
    } else {
      CloseButNoCigar();
      break;
    }
  case 42:
    DoSomethingSpecial();
    [[fallthrough]];
  default:
    DoSomethingGeneric();
    break;
}
```

---

## 옮긴이 풀이

### 핵심: default를 두고, fallthrough는 명시하라

`switch` 문에는 항상 `default` 케이스를 두세요(단, enum 값에 대한 분기는 예외 — 처리 안 된 값이 있으면 컴파일러가 경고). 도달하면 안 되는 `default`는 오류로 처리하세요.

```cpp
switch (var) {
  case 0: { ...; break; }
  case 1: { ...; break; }
  default: {
    LOG(FATAL) << "Invalid value in switch statement: " << var;
  }
}
```

### fallthrough 주석

한 `case`에서 다음 `case`로 넘어가는 폴스루(fallthrough)는 `[[fallthrough]];`로 명시하세요. 단, 중간 코드 없이 연속된 `case` 레이블은 주석이 필요 없습니다.

```cpp
switch (x) {
  case 41:  // 연속 레이블 — 주석 불필요
  case 43:
    DoWork();
    [[fallthrough]];  // 다음 case로 의도적으로 넘어감
  default:
    DoDefault();
    break;
}
```
