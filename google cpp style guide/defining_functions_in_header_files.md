# 헤더 파일에서 함수 정의하기 (Defining Functions in Header Files)

함수의 정의가 짧을 때만 헤더 파일에서 선언 지점에 함수 정의를 포함하세요. 정의가 다른 이유로 헤더에 있어야 한다면, 파일의 내부 부분에 두세요. 정의를 ODR-safe하게 만들기 위해 필요하다면 `inline` 지정자를 표시하세요.

헤더 파일에 정의된 함수는 때때로 "인라인 함수"라고 불리는데, 이는 여러 개의 구별되지만 겹치는 상황을 가리키는 다소 과부하된 용어입니다:

- **텍스트적으로 인라인인 심볼(textually inline symbol)**: 정의가 선언 지점에서 독자에게 노출됩니다.
- **인라인 확장 가능한 함수 또는 변수**: 헤더 파일에 정의된 함수나 변수는 컴파일러가 인라인 확장할 수 있도록 정의가 사용 가능하므로 인라인 확장 가능하며, 이는 더 효율적인 객체 코드로 이어질 수 있습니다.
- **ODR-safe 엔티티**: "One Definition Rule"을 위반하지 않으며, 헤더 파일에 정의된 것들은 종종 `inline` 키워드가 필요합니다.

함수만큼 혼란의 원인이 되는 경우는 드물지만, 이러한 정의는 변수에도 적용되며, 여기서의 규칙도 마찬가지입니다.

함수를 텍스트적으로 인라인으로 정의하면 접근자(accessor)와 변경자(mutator)와 같은 간단한 함수의 보일러플레이트 코드를 줄일 수 있습니다.

위에서 언급한 대로, 헤더 파일의 함수 정의는 작은 함수의 경우 컴파일러의 인라인 확장으로 인해 더 효율적인 객체 코드로 이어질 수 있습니다.

함수 템플릿과 `constexpr` 함수는 일반적으로 선언하는 헤더 파일에 정의되어야 합니다(하지만 반드시 공개 부분일 필요는 없습니다).

공개 API에 함수 정의를 포함하면 API를 빠르게 훑어보기 어렵게 만들고, 해당 API를 읽는 사람에게 인지적 부담을 줍니다. 함수가 복잡할수록 비용이 높아집니다.

공개 정의는 최선의 경우 무해하고 종종 불필요한 구현 세부 사항을 노출합니다.

함수가 짧을 때만(예: 10줄 이하) 공개 선언 지점에 함수를 정의하세요. 더 긴 함수 본문은 성능이나 기술적 이유로 헤더에 있어야 하지 않는 한 `.cc` 파일에 두세요.

정의가 헤더에 있어야 하더라도, 이것이 공개 부분에 두기에 충분한 이유는 아닙니다. 대신 정의는 헤더의 내부 부분에 둘 수 있습니다. 예를 들어 클래스의 private 섹션, `internal`이라는 단어를 포함하는 네임스페이스 내부, 또는 `// Implementation details only below here`와 같은 주석 아래에 둘 수 있습니다.

정의가 헤더 파일에 있으면, `inline` 지정자를 가지거나 함수 템플릿이거나 클래스 본문에서 처음 선언될 때 정의되어 암시적으로 인라인으로 지정되어 ODR-safe해야 합니다.

```cpp
template <typename T>
class Foo {
 public:
  int bar() { return bar_; }

  void MethodWithHugeBody();

 private:
  int bar_;
};

// Implementation details only below here

template <typename T>
void Foo<T>::MethodWithHugeBody() {
  ...
}
```

---

## 옮긴이 풀이

### 헤더 파일에서 함수 정의하기란?

일반적으로 함수는 **선언(declaration)**과 **정의(definition)**로 나뉩니다:

- **선언**: 함수의 이름, 매개변수, 반환 타입을 알려줍니다.
- **정의**: 함수의 실제 구현 코드를 포함합니다.

헤더 파일에서 함수를 정의한다는 것은 선언뿐만 아니라 함수의 본문까지 헤더 파일에 작성하는 것을 의미합니다.

### "인라인 함수"라는 용어의 혼란

"인라인 함수"라는 용어는 여러 의미로 사용되어 혼란을 야기할 수 있습니다:

1. **텍스트적으로 인라인**: 함수 정의가 선언 지점에서 바로 보입니다.
2. **인라인 확장 가능**: 컴파일러가 함수 호출을 함수 본문으로 대체할 수 있습니다.
3. **ODR-safe**: One Definition Rule을 위반하지 않습니다.

이 세 가지는 서로 다른 개념이지만, 헤더 파일에 정의된 함수는 종종 세 가지 모두에 해당합니다.

### 헤더 파일에서 함수를 정의하는 이유

#### 장점

1. **보일러플레이트 코드 감소**: 접근자나 변경자 같은 간단한 함수의 경우, 헤더에 정의하면 별도의 `.cc` 파일에 작성할 필요가 없습니다.

```cpp
// 좋은 예: 짧은 접근자 함수
class Point {
 public:
  int x() const { return x_; }  // 헤더에 정의
  int y() const { return y_; }  // 헤더에 정의
 private:
  int x_, y_;
};
```

2. **성능 향상**: 작은 함수의 경우 컴파일러가 인라인 확장을 통해 함수 호출 오버헤드를 제거할 수 있습니다.

3. **템플릿과 constexpr의 필수 요구사항**: 함수 템플릿과 `constexpr` 함수는 일반적으로 헤더에 정의되어야 합니다.

```cpp
// 함수 템플릿은 헤더에 정의해야 함
template <typename T>
T max(T a, T b) {
  return a > b ? a : b;
}

// constexpr 함수도 헤더에 정의해야 함
constexpr int square(int x) {
  return x * x;
}
```

#### 단점

1. **API 가독성 저하**: 공개 API에 함수 정의가 포함되면 API를 빠르게 훑어보기 어렵습니다.

```cpp
// 나쁜 예: 긴 함수가 공개 API에 노출됨
class DataProcessor {
 public:
  void ProcessData(const std::vector<int>& data) {
    // 50줄 이상의 복잡한 로직...
    // API 사용자가 이 모든 것을 봐야 함
  }
};
```

2. **구현 세부 사항 노출**: 공개 정의는 구현 세부 사항을 노출하여, 최선의 경우 무해하지만 종종 불필요한 정보입니다.

3. **인지적 부담**: 함수가 복잡할수록 API를 읽는 사람에게 더 큰 부담을 줍니다.

### 규칙 요약

#### 1. 짧은 함수만 공개 선언 지점에 정의

함수가 **10줄 이하**일 때만 공개 선언 지점에 정의하세요.

```cpp
// 좋은 예: 짧은 함수
class Widget {
 public:
  int value() const { return value_; }  // 1줄 - OK
  void set_value(int v) { value_ = v; }  // 1줄 - OK
 private:
  int value_;
};
```

```cpp
// 나쁜 예: 긴 함수를 공개 API에 정의
class Widget {
 public:
  void complex_operation() {
    // 30줄 이상의 복잡한 로직...
    // 이건 .cc 파일로 옮겨야 함
  }
};
```

#### 2. 긴 함수는 .cc 파일에

더 긴 함수 본문은 성능이나 기술적 이유로 헤더에 있어야 하지 않는 한 `.cc` 파일에 두세요.

```cpp
// widget.h
class Widget {
 public:
  void complex_operation();  // 선언만
};

// widget.cc
#include "widget.h"

void Widget::complex_operation() {
  // 30줄 이상의 복잡한 로직...
  // .cc 파일에 정의
}
```

#### 3. 헤더에 있어야 하는 경우 내부 부분에 정의

정의가 헤더에 있어야 하더라도(예: 템플릿 함수), 공개 부분에 두지 말고 내부 부분에 두세요.

```cpp
template <typename T>
class Foo {
 public:
  int bar() { return bar_; }  // 짧은 함수 - 공개 부분에 OK

  void MethodWithHugeBody();  // 선언만

 private:
  int bar_;
};

// Implementation details only below here
// (또는 namespace internal { ... } 내부)

template <typename T>
void Foo<T>::MethodWithHugeBody() {
  // 긴 구현은 내부 부분에
  // ...
}
```

내부 부분으로 사용할 수 있는 위치:
- 클래스의 `private` 섹션
- `internal`이라는 단어를 포함하는 네임스페이스 내부
- `// Implementation details only below here`와 같은 주석 아래

#### 4. ODR-safe 보장

헤더 파일에 정의된 함수는 ODR-safe해야 합니다. 다음 중 하나를 만족해야 합니다:

- `inline` 키워드를 명시적으로 사용
- 함수 템플릿인 경우 (자동으로 인라인)
- 클래스 본문에서 처음 선언될 때 정의된 경우 (자동으로 인라인)

```cpp
// 좋은 예: inline 키워드 사용
inline int helper_function(int x) {
  return x * 2;
}

// 좋은 예: 함수 템플릿 (자동으로 인라인)
template <typename T>
T max(T a, T b) {
  return a > b ? a : b;
}

// 좋은 예: 클래스 본문에서 정의 (자동으로 인라인)
class MyClass {
 public:
  int get_value() const { return value_; }  // 자동으로 인라인
 private:
  int value_;
};
```

### 변수에도 동일한 규칙 적용

이 규칙은 함수뿐만 아니라 변수에도 적용됩니다. 헤더 파일에 정의된 변수도 ODR-safe해야 합니다.

```cpp
// 헤더 파일에서
inline const int kMaxSize = 100;  // inline 키워드 필요

// 또는
constexpr int kMaxSize = 100;  // constexpr은 자동으로 인라인
```

### 정리

- **원칙**: 
  - 짧은 함수(10줄 이하)만 헤더의 공개 선언 지점에 정의
  - 긴 함수는 `.cc` 파일에 정의
  - 헤더에 있어야 하는 경우 내부 부분에 정의
  - ODR-safe 보장 (`inline` 키워드 또는 자동 인라인)

- **예외**:
  - 함수 템플릿과 `constexpr` 함수는 헤더에 정의해야 함
  - 성능상 중요한 작은 함수는 헤더에 정의 가능

- **효과**:
  - API 가독성 향상
  - 구현 세부 사항 숨김
  - 컴파일러 최적화 가능 (인라인 확장)

