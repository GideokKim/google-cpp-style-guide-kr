# 이름 선택하기 (Choosing Names)

새로운 독자, 심지어 소유자와 다른 팀에 속한 사람이 목적이나 의도를 이해할 수 있도록 이름을 지정하세요. 새로운 독자가 코드를 즉시 이해할 수 있도록 만드는 것이 훨씬 더 중요하므로 수평 공간을 절약하는 것에 대해 걱정하지 마세요.

이름이 사용될 상황을 고려하십시오. 이름은 사용 가능한 코드와 멀리 떨어져 사용되더라도 설명적이어야 합니다. 그러나 이름은 즉각적인 맥락에 존재하는 정보를 반복하여 독자의 주의를 산만하게 해서는 안 됩니다. 일반적으로 이는 설명성이 이름의 가시성 범위에 비례해야 함을 의미합니다. 헤더에 선언된 자유 함수는 헤더의 라이브러리를 언급해야 하지만 지역 변수는 그 안에 어떤 함수가 있는지 설명해서는 안 됩니다.

프로젝트 외부인이 알지 못할 약어(특히 약어 및 두문자어)의 사용을 최소화하세요. 단어 내의 문자를 삭제하여 축약하지 마세요. 약어가 사용되는 경우 단일 "단어"로 대문자로 시작하는 것이 좋습니다(예: StartRPC() 대신 StartRpc() ). 경험상 Wikipedia에 나열된 약어는 아마도 괜찮을 것입니다. 루프 인덱스의 경우 i, 템플릿 매개변수의 경우 T와 같이 널리 알려진 특정 약어는 괜찮습니다.

가장 자주 보는 이름은 대부분의 이름과 다릅니다. 소수의 "어휘" 이름이 너무 광범위하게 재사용되어 항상 문맥에 포함됩니다. 이러한 이름은 짧거나 축약되는 경향이 있으며, 전체 의미는 이름에 포함된 단어와 정의에 대한 설명이 아닌 명시적인 긴 형식의 문서에서 비롯됩니다. 예를 들어, absl::Status에는 적절한 사용을 문서화하는 전용 페이지가 devguide에 있습니다. 새로운 어휘 이름을 자주 정의하지는 않을 것입니다. 하지만 그렇게 한다면 추가 디자인 검토를 받아 선택한 이름이 널리 사용될 때 잘 작동하는지 확인하십시오.

```cpp
class MyClass {
 public:
  int CountFooErrors(const std::vector<Foo>& foos) {
    int n = 0;  // Clear meaning given limited scope and context
    for (const auto& foo : foos) {
      ...
      ++n;
    }
    return n;
  }
  // Function comment doesn't need to explain that this returns non-OK on
  // failure as that is implied by the `absl::Status` return type, but it
  // might document behavior for some specific codes.
  absl::Status DoSomethingImportant() {
    std::string fqdn = ...;  // Well-known abbreviation for Fully Qualified Domain Name
    return absl::OkStatus();
  }
 private:
  const int kMaxAllowedConnections = ...;  // Clear meaning within context
};
```

```cpp
class MyClass {
 public:
  int CountFooErrors(const std::vector<Foo>& foos) {
    int total_number_of_foo_errors = 0;  // Overly verbose given limited scope and context
    for (int foo_index = 0; foo_index < foos.size(); ++foo_index) {  // Use idiomatic `i`
      ...
      ++total_number_of_foo_errors;
    }
    return total_number_of_foo_errors;
  }
  // A return type with a generic name is unclear without widespread education.
  Result DoSomethingImportant() {
    int cstmr_id = ...;  // Deletes internal letters
  }
 private:
  const int kNum = ...;  // Unclear meaning within broad scope
};
```

---

## 이해하기 쉽게 설명하기

### 핵심: 새 독자가 의도를 이해할 수 있는 이름

이름은, 소유자와 다른 팀의 새 독자도 목적·의도를 이해할 수 있게 지으세요. 가로 공간을 아끼는 것보다 **즉시 이해되는 것**이 훨씬 중요합니다.

### 설명성은 가시 범위에 비례

- 넓은 범위(헤더의 자유 함수 등)일수록 더 설명적인 이름을.
- 좁은 범위(지역 변수)에서는 짧아도 됩니다 — 문맥이 의미를 채워줍니다. 즉각적 문맥에 이미 있는 정보를 이름에 반복하지 마세요.

```cpp
int CountFooErrors(const std::vector<Foo>& foos) {
  int n = 0;              // 좁은 범위 — 짧아도 명확
  for (const auto& foo : foos) { ...; ++n; }
  return n;
}
```

### 약어

- 외부인이 모를 약어(특히 두문자어)는 최소화하세요. 단어 중간 글자를 빼서 줄이지 마세요(`cstmr_id` ✗).
- 약어를 쓰면 한 "단어"처럼 첫 글자만 대문자: `StartRpc()`(✓) vs `StartRPC()`(✗).
- 널리 알려진 것(루프 인덱스 `i`, 템플릿 매개변수 `T`, `fqdn` 등)은 괜찮습니다.
