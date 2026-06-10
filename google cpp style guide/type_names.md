# 타입 이름 (Type Names)

## 원문 규칙 번역

유형 이름은 대문자로 시작하고 각각의 새로운 단어에 대해 밑줄 없이 대문자를 사용합니다: MyExcitingClass , MyExcitingEnum .

클래스, 구조체, 유형 별칭, 열거형, 유형 템플릿 매개변수 등 모든 유형의 이름은 동일한 명명 규칙을 따릅니다. 유형 이름은 대문자로 시작해야 하며 새 단어마다 대문자가 있어야 합니다. 밑줄이 없습니다. 예를 들어:

```cpp
// classes and structs
class UrlTable { ...
class UrlTableTester { ...
struct UrlTableProperties { ...

// typedefs
typedef hash_map<UrlTableProperties*, std::string> PropertiesMap;

// using aliases
using PropertiesMap = hash_map<UrlTableProperties*, std::string>;

// enums
enum class UrlTableError { ...
```

---

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 유형 이름은 대문자로 시작하고 각각의 새로운 단어에 대해 밑줄 없이 대문자를 사용합니다: MyExcitingClass , MyExcitingEnum .

실제로 코드를 볼 때는 유형 이름은 대문자로 시작해야 하며 새 단어마다

점검할 때는 특히 다음을 확인하세요:

- 클래스, 구조체, 유형 별칭, 열거형, 유형 템플릿 매개변수 등 모든 유형의 이름은 동일한 명명 규칙을 따릅니다.
