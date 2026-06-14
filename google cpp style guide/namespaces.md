# 네임스페이스 (Namespaces)

몇 가지 예외를 제외하고, 코드는 네임스페이스 안에 배치하세요. 네임스페이스는 프로젝트 이름과 (가능하면) 경로에 기반한 고유한 이름을 가져야 합니다. using 지시문(_using-directive_, 예: `using namespace foo`)을 사용하지 마세요. 인라인 네임스페이스를 사용하지 마세요. 이름 없는 네임스페이스에 대해서는 내부 연결(Internal Linkage)을 참조하세요.

네임스페이스는 전역 범위를 별개의 명명된 범위로 세분화하므로, 전역 범위에서의 이름 충돌을 방지하는 데 유용합니다.

네임스페이스는 대규모 프로그램에서 이름 충돌을 방지하면서도, 대부분의 코드가 적당히 짧은 이름을 사용할 수 있게 해줍니다.

예를 들어, 서로 다른 두 프로젝트가 전역 범위에 각각 `Foo` 클래스를 가지고 있다면 이 심볼들은 컴파일 타임이나 런타임에 충돌할 수 있습니다. 각 프로젝트가 자신의 코드를 네임스페이스에 배치하면 `project1::Foo`와 `project2::Foo`는 충돌하지 않는 별개의 심볼이 되고, 각 프로젝트의 네임스페이스 안에서는 접두사 없이 계속 `Foo`를 참조할 수 있습니다.

인라인 네임스페이스는 그 이름을 바깥 범위에 자동으로 배치합니다. 예를 들어 다음 코드를 살펴보세요.

```cpp
namespace outer {
inline namespace inner {
  void foo();
}  // namespace inner
}  // namespace outer
```

`outer::inner::foo()`와 `outer::foo()` 표현식은 서로 바꿔 쓸 수 있습니다. 인라인 네임스페이스는 주로 버전 간 ABI 호환성을 위해 만들어졌습니다.

네임스페이스는 이름이 가리키는 정의를 파악하는 과정을 복잡하게 만들기 때문에 혼란스러울 수 있습니다.

특히 인라인 네임스페이스는 이름이 실제로 선언된 네임스페이스에 한정되지 않기 때문에 혼란스러울 수 있습니다. 인라인 네임스페이스는 대규모 버전 관리 정책의 일부로만 유용합니다.

어떤 상황에서는 심볼을 정규화된(fully-qualified) 이름으로 반복해서 참조해야 합니다. 깊게 중첩된 네임스페이스에서는 이 때문에 군더더기가 많이 늘어날 수 있습니다.

네임스페이스는 다음과 같이 사용해야 합니다.

- 네임스페이스 이름 규칙을 따르세요.
- 여러 줄에 걸친 네임스페이스는 예시처럼 주석으로 끝을 표시하세요.
- 네임스페이스는 include, gflags 정의/선언, 다른 네임스페이스의 클래스 전방 선언 뒤에서 소스 파일 전체를 감쌉니다.

```cpp
// .h 파일에서
namespace mynamespace {

// 모든 선언은 네임스페이스 범위 안에 있습니다.
// 들여쓰기를 하지 않는다는 점에 유의하세요.
class MyClass {
 public:
  ...
  void Foo();
};

}  // namespace mynamespace

// .cc 파일에서
namespace mynamespace {

// 함수 정의도 네임스페이스 범위 안에 있습니다.
void MyClass::Foo() {
  ...
}

}  // namespace mynamespace
```

  더 복잡한 `.cc` 파일에는 플래그나 using 선언 같은 추가 내용이 있을 수 있습니다.

```cpp
#include "a.h"

ABSL_FLAG(bool, someflag, false, "a flag");

namespace mynamespace {

using ::foo::Bar;

...code for mynamespace...    // 코드는 왼쪽 여백에 맞춥니다.

}  // namespace mynamespace
```

- 생성된 프로토콜 메시지 코드를 네임스페이스에 넣으려면 `.proto` 파일에서 `package` 지정자를 사용하세요. 자세한 내용은 Protocol Buffer Packages를 참조하세요.
- 표준 라이브러리 클래스의 전방 선언을 포함해, `std` 네임스페이스에는 아무것도 선언하지 마세요. `std` 네임스페이스에 엔터티를 선언하는 것은 정의되지 않은 동작(undefined behavior)이며 이식성이 없습니다. 표준 라이브러리의 엔터티를 사용하려면 적절한 헤더 파일을 포함하세요.
- using 지시문(_using-directive_)으로 네임스페이스의 모든 이름을 가져오지 마세요.

```cpp
// 금지 -- 네임스페이스를 오염시킵니다.
using namespace foo;
```

- 헤더 파일의 네임스페이스 범위에서는 네임스페이스 별칭(_namespace alias_)을 사용하지 마세요. 단, 명시적으로 내부 전용으로 표시된 네임스페이스는 예외입니다. 헤더 파일에서 네임스페이스로 가져온 것은 모두 그 파일이 내보내는 공개 API의 일부가 되기 때문입니다. 이 조건에 해당하지 않으면 네임스페이스 별칭을 사용할 수 있지만, 적절한 이름을 가져야 합니다.

```cpp
// .h 파일에서 별칭은 별개의 API가 아니어야 하거나,
// 구현 세부사항으로 숨겨야 합니다.
namespace librarian {

namespace internal {  // 내부용, API의 일부가 아닙니다.
namespace sidetable = ::pipeline_diagnostics::sidetable;
}

inline void my_inline_function() {
  // 함수에 한정됩니다.
  namespace baz = ::foo::bar::baz;
  ...
}

}  // namespace librarian

// .cc 파일에서는 자주 쓰는 이름 중 흥미롭지 않은 부분을 줄입니다.
namespace sidetable = ::pipeline_diagnostics::sidetable;
```

- 인라인 네임스페이스를 사용하지 마세요.
- API 사용자가 언급하지 말아야 할 부분을 문서화하려면 이름에 "internal"이 포함된 네임스페이스를 사용하세요.

```cpp
// absl이 아닌 코드에서 이 내부 이름을 사용하면 안 됩니다.
using ::absl::container_internal::ImplementationDetail;
```

  중첩된 `internal` 네임스페이스 안에서도 라이브러리 간 충돌 위험이 여전히 남아 있으므로, 라이브러리 파일 이름을 덧붙여 네임스페이스 안의 각 라이브러리에 고유한 내부 네임스페이스를 부여하세요. 예를 들어 `gshoe/widget.h`는 그냥 `gshoe::internal`이 아니라 `gshoe::internal_widget`을 사용합니다.
- 새 코드에서는 한 줄로 된 중첩 네임스페이스 선언이 선호되지만, 필수는 아닙니다.

```cpp
namespace my_project::my_component {

  ...

}  // namespace my_project::my_component
```

---

## 이해하기 쉽게 설명하기

### 왜 모든 코드를 네임스페이스에 넣는가?

전역 범위에 이름을 그대로 두면, 다른 라이브러리나 프로젝트가 같은 이름을 쓸 때 충돌합니다. 네임스페이스로 감싸면 `project1::Foo`와 `project2::Foo`처럼 서로 구분되므로, 큰 코드베이스에서도 짧은 이름(`Foo`)을 안심하고 쓸 수 있습니다.

### using 지시문(using-directive)은 왜 금지인가?

`using namespace foo;`는 `foo`의 **모든** 이름을 현재 범위로 끌어옵니다. 이렇게 하면 어떤 이름이 어디서 왔는지 추적하기 어려워지고, 의도치 않은 이름 충돌이 생깁니다.

```cpp
// 금지: foo의 모든 이름이 쏟아져 들어옴
using namespace foo;

// 허용: 필요한 이름만 콕 집어서 (using 선언)
using ::foo::Bar;
```

`using namespace`(지시문, _directive_)는 금지지만, `using ::foo::Bar;`처럼 특정 이름 하나만 가져오는 **using 선언(_declaration_)**은 `.cc` 파일에서 허용됩니다. 둘을 혼동하지 마세요.

### 헤더에서 네임스페이스 별칭을 조심해야 하는 이유

헤더 파일에서 네임스페이스 범위에 별칭을 만들면, 그 별칭은 헤더를 포함하는 모든 사용자에게 공개 API처럼 노출됩니다. 그래서 헤더에서는 별칭을 함수 안이나 명시적 `internal` 네임스페이스 안으로 숨겨야 합니다. `.cc` 파일에서는 자유롭게 별칭을 써도 됩니다.

### internal 네임스페이스

라이브러리 구현 세부사항은 이름에 `internal`을 포함한 네임스페이스에 두어 "사용자가 직접 쓰면 안 되는 부분"임을 알립니다. 다만 `internal`이라는 이름은 흔해서 라이브러리끼리 충돌할 수 있으므로, `gshoe::internal_widget`처럼 파일 이름을 덧붙여 고유하게 만듭니다.

### 하지 말아야 할 것 정리

- `std` 네임스페이스에 무언가를 선언/전방 선언하기 → 정의되지 않은 동작
- 인라인 네임스페이스 사용 (ABI 버전 관리 같은 특수 목적 외)
- 여러 줄 네임스페이스에서 닫는 `}` 주석(`// namespace mynamespace`) 빠뜨리기
