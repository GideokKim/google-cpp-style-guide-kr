# 타입 이름 (Type Names)

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

### 핵심: 타입 이름은 PascalCase

클래스·구조체·타입 별칭·열거형·타입 템플릿 매개변수 등 **모든 타입**은 대문자로 시작하고 새 단어마다 대문자, 밑줄 없이 씁니다: `MyExcitingClass`, `MyExcitingEnum`.

```cpp
class UrlTable { ... };
struct UrlTableProperties { ... };
using PropertiesMap = hash_map<UrlTableProperties*, std::string>;
enum class UrlTableError { ... };
```
