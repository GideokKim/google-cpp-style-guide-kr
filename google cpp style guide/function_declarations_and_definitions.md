# 함수 선언과 정의 형식 (Function Declarations and Definitions)

함수 이름과 같은 줄에 반환 유형이 있고, 맞는 경우 매개변수가 같은 줄에 있습니다. 함수 호출에서 인수를 래핑하는 것처럼 한 줄에 맞지 않는 매개변수 목록을 래핑합니다.

기능은 다음과 같습니다:

```cpp
ReturnType ClassName::FunctionName(Type par_name1, Type par_name2) {
  DoSomething();
  ...
}
```

한 줄에 들어갈 텍스트가 너무 많은 경우:

```cpp
ReturnType ClassName::ReallyLongFunctionName(Type par_name1, Type par_name2,
                                             Type par_name3) {
  DoSomething();
  ...
}
```

또는 첫 번째 매개변수조차 맞출 수 없는 경우:

```cpp
ReturnType LongClassName::ReallyReallyReallyLongFunctionName(
    Type par_name1,  // 4 space indent
    Type par_name2,
    Type par_name3) {
  DoSomething();  // 2 space indent
  ...
}
```

참고할 사항:

- 좋은 매개변수 이름을 선택하세요.
- 매개변수 이름은 함수 정의에 매개변수가 사용되지 않는 경우에만 생략할 수 있습니다.
- 반환 유형과 함수 이름을 한 줄에 맞출 수 없으면 둘 사이를 구분하십시오.
- 함수 선언이나 정의의 반환 유형 다음에 중단하는 경우 들여쓰기하지 마세요.
- 여는 괄호는 항상 함수 이름과 같은 줄에 있습니다.
- 함수 이름과 여는 괄호 사이에는 공백이 있어서는 안 됩니다.
- 괄호와 매개변수 사이에는 공백이 있어서는 안 됩니다.
- 여는 중괄호는 항상 다음 줄의 시작 부분이 아니라 함수 선언의 마지막 줄 끝에 있습니다.
- 닫는 중괄호는 단독으로 마지막 줄에 있거나 여는 중괄호와 같은 줄에 있습니다.
- 닫는 괄호와 여는 중괄호 사이에는 공백이 있어야 합니다.
- 가능하면 모든 매개변수를 정렬해야 합니다.
- 기본 들여쓰기는 공백 2개입니다.
- 래핑된 매개변수에는 4개의 공백 들여쓰기가 있습니다.

문맥상 명백히 사용되지 않는 매개변수는 이름을 생략할 수 있습니다:

```cpp
class Foo {
 public:
  Foo(const Foo&) = delete;
  Foo& operator=(const Foo&) = delete;
};
```

명확하지 않을 수 있는 사용되지 않는 매개변수는 함수 정의에서 변수 이름을 주석 처리해야 합니다.

```cpp
class Shape {
 public:
  virtual void Rotate(double radians) = 0;
};

class Circle : public Shape {
 public:
  void Rotate(double radians) override;
};

void Circle::Rotate(double /*radians*/) {}
```

```cpp
// Bad - if someone wants to implement later, it's not clear what the
// variable means.
void Circle::Rotate(double) {}
```

속성 및 속성으로 확장되는 매크로는 함수 선언 또는 정의의 맨 처음, 반환 유형 앞에 나타납니다.

```cpp
  ABSL_ATTRIBUTE_NOINLINE void ExpensiveFunction();
  [[nodiscard]] bool IsOk();
```

---

## 이해하기 쉽게 설명하기

### 핵심: 반환 타입은 함수 이름과 같은 줄, 넘치면 들여써서 래핑

```cpp
ReturnType ClassName::FunctionName(Type par_name1, Type par_name2) {
  DoSomething();
}
```

한 줄에 안 들어가면 매개변수를 래핑합니다 — 첫 매개변수에 맞춰 정렬하거나, 그것도 안 되면 4칸 들여쓰기로:

```cpp
ReturnType LongClassName::ReallyReallyReallyLongFunctionName(
    Type par_name1,  // 4칸 들여쓰기
    Type par_name2) {
  DoSomething();     // 본문은 2칸
}
```

### 주요 규칙

- 함수 이름과 여는 `(` 사이, `(`와 매개변수 사이에 공백 없음.
- 여는 `{`는 함수 선언 마지막 줄 **끝**에. 닫는 `)`와 `{` 사이에는 공백.
- 기본 들여쓰기 2칸, 래핑된 매개변수는 4칸.
- 속성/속성 매크로(`ABSL_ATTRIBUTE_NOINLINE`, `[[nodiscard]]`)는 반환 타입 **앞**에.

### 쓰지 않는 매개변수 이름

- 문맥상 자명하면 이름 생략 가능: `Foo(const Foo&) = delete;`
- 자명하지 않으면 이름을 주석 처리: `void Circle::Rotate(double /*radians*/) {}`
