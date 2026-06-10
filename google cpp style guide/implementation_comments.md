# 구현 주석 (Implementation Comments)

## 원문 규칙 번역

구현 시 까다롭거나, 명확하지 않거나, 흥미롭거나, 중요한 코드 부분에 대한 주석이 있어야 합니다.

까다롭거나 복잡한 코드 블록 앞에는 주석이 있어야 합니다.

함수 인수의 의미가 명확하지 않은 경우 다음 해결 방법 중 하나를 고려하세요.

- 인수가 리터럴 상수이고 동일한 상수가 암묵적으로 동일하다고 가정하는 방식으로 여러 함수 호출에서 사용되는 경우 명명된 상수를 사용하여 해당 제약 조건을 명시적으로 만들고 유지되도록 보장해야 합니다.
- bool 인수를 enum 인수로 바꾸려면 함수 서명을 변경하는 것이 좋습니다. 이렇게 하면 인수 값이 자체적으로 설명됩니다.
- 여러 구성 옵션이 있는 함수의 경우 모든 옵션을 보유하도록 단일 클래스 또는 구조체를 정의하고 해당 인스턴스를 전달하는 것을 고려하세요. 이 접근 방식에는 몇 가지 장점이 있습니다. 옵션은 호출 사이트에서 이름으로 참조되므로 의미가 명확해집니다. 또한 함수 인수 수를 줄여 함수 호출을 더 쉽게 읽고 쓸 수 있습니다. 추가 혜택으로는 다른 옵션을 추가할 때 호출 사이트를 변경할 필요가 없습니다.
- 크거나 복잡한 중첩 표현식을 명명된 변수로 바꿉니다.
- 최후의 수단으로 주석을 사용하여 호출 현장에서 인수 의미를 명확히 합니다.

```cpp
// What are these arguments?
const DecimalNumber product = CalculateProduct(values, 7, false, nullptr);
```

대:

```cpp
ProductOptions options;
options.set_precision_decimals(7);
options.set_use_cache(ProductOptions::kDontUseCache);
const DecimalNumber product =
    CalculateProduct(values, options, /*completion_callback=*/nullptr);
```

명백한 것을 말하지 마세요. 특히, C++를 잘 이해하는 독자에게 동작이 명확하지 않은 한, 코드가 수행하는 작업을 문자 그대로 설명하지 마세요. 대신 코드가 수행하는 작업을 설명하는 상위 수준 주석을 제공하거나 코드를 자체 설명하도록 만드세요.

```cpp
// Find the element in the vector.  <-- Bad: obvious!
if (std::find(v.begin(), v.end(), element) != v.end()) {
  Process(element);
}
```

```cpp
// Process "element" unless it was already processed.
if (std::find(v.begin(), v.end(), element) != v.end()) {
  Process(element);
}
```

자기 설명 코드에는 주석이 필요하지 않습니다. 위 예의 설명은 다음과 같습니다.

```cpp
if (!IsAlreadyProcessed(element)) {
  Process(element);
}
```

---

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 - 인수가 리터럴 상수이고 동일한 상수가 암묵적으로 동일하다고 가정하는 방식으로 여러 함수 호출에서 사용되는 경우 명명된 상수를 사용하여 해당 제약 조건을 명시적으로 만들고 유지되도록 보장해야 합니다.

실제로 코드를 볼 때는 구현 시 까다롭거나, 명확하지 않거나, 흥미롭거나, 중요한 코드 부분에 대한 주석이 있어야 합니다.

점검할 때는 특히 다음을 확인하세요:

- 함수 인수의 의미가 명확하지 않은 경우 다음 해결 방법 중 하나를 고려하세요.
- 특히, C++를 잘 이해하는 독자에게 동작이 명확하지 않은 한, 코드가 수행하는 작업을 문자 그대로 설명하지 마세요.
