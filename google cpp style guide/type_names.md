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

## 이해하기 쉽게 설명하기

타입 이름 규칙을 적용할 때는 원문 규칙을 문자 그대로 외우기보다, 왜 이 선택이 독자에게 더 명확한지 살펴보면 쉽습니다. 코드 리뷰에서는 이 기능이 호출 지점에서 의도를 숨기지 않는지, 더 단순한 구조로 같은 목적을 달성할 수 없는지, 기존 코드와 섞였을 때 유지보수 비용이 커지지 않는지를 확인하세요.
