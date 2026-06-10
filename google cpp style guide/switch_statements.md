# switch 문 (Switch Statements)

## 원문 규칙 번역

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

한 케이스 레이블에서 다른 케이스 레이블로의 폴스루는 [[fallthrough]]를 사용하여 주석을 달아야 합니다. 기인하다. [[폴스루]]; 다음 사례 레이블로 넘어갈 수 있는 실행 지점에 배치되어야 합니다. 일반적인 예외는 중간 코드가 없는 연속 케이스 레이블이며, 이 경우 주석이 필요하지 않습니다.

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

## 이해하기 쉽게 설명하기

switch 문 규칙을 적용할 때는 원문 규칙을 문자 그대로 외우기보다, 왜 이 선택이 독자에게 더 명확한지 살펴보면 쉽습니다. 코드 리뷰에서는 이 기능이 호출 지점에서 의도를 숨기지 않는지, 더 단순한 구조로 같은 목적을 달성할 수 없는지, 기존 코드와 섞였을 때 유지보수 비용이 커지지 않는지를 확인하세요.
