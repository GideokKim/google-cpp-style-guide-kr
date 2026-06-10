# 함수 선언과 정의 형식 (Function Declarations and Definitions)

## 원문 규칙 번역

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

함수 선언과 정의 형식 규칙을 적용할 때는 원문 규칙을 문자 그대로 외우기보다, 왜 이 선택이 독자에게 더 명확한지 살펴보면 쉽습니다. 코드 리뷰에서는 이 기능이 호출 지점에서 의도를 숨기지 않는지, 더 단순한 구조로 같은 목적을 달성할 수 없는지, 기존 코드와 섞였을 때 유지보수 비용이 커지지 않는지를 확인하세요.
