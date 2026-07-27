# 네임스페이스 (Namespaces)

몇 가지 예외를 제외하고, 코드는 네임스페이스 안에 배치하세요. 네임스페이스는 프로젝트 이름과, 경우에 따라서는 그 경로까지 반영한 고유한 이름을 가져야 합니다. using 지시문(_using-directive_, 예: `using namespace foo`)을 사용하지 마세요. 인라인 네임스페이스를 사용하지 마세요. 이름 없는 네임스페이스에 대해서는 [내부 연결](internal_linkage.md)을 참조하세요.

**정의:**

네임스페이스는 전역 범위를 별개의 명명된 범위로 세분화하므로, 전역 범위에서의 이름 충돌을 방지하는 데 유용합니다.

**장점:**

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

**단점:**

네임스페이스는 이름이 가리키는 정의를 파악하는 과정을 복잡하게 만들기 때문에 혼란스러울 수 있습니다.

특히 인라인 네임스페이스는 이름이 실제로 선언된 네임스페이스에 한정되지 않기 때문에 혼란스러울 수 있습니다. 인라인 네임스페이스는 대규모 버전 관리 정책의 일부로만 유용합니다.

어떤 상황에서는 심볼을 정규화된(fully-qualified) 이름으로 반복해서 참조해야 합니다. 깊게 중첩된 네임스페이스에서는 이 때문에 군더더기가 많이 늘어날 수 있습니다.

**결정:**

네임스페이스는 다음과 같이 사용해야 합니다.

- [네임스페이스 이름](namespace_names.md) 규칙을 따르세요.
- 여러 줄에 걸친 네임스페이스는 예시처럼 주석으로 끝을 표시하세요.
- 네임스페이스는 include, [gflags](https://gflags.github.io/gflags/) 정의/선언, 다른 네임스페이스의 클래스 전방 선언 뒤에서 소스 파일 전체를 감쌉니다.

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
    ```

    ```cpp
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

- 생성된 프로토콜 메시지 코드를 네임스페이스에 넣으려면 `.proto` 파일에서 `package` 지정자를 사용하세요. 자세한 내용은 [Protocol Buffer Packages](https://protobuf.dev/reference/cpp/cpp-generated/#package)를 참조하세요.
- 표준 라이브러리 클래스의 전방 선언을 포함해, `std` 네임스페이스에는 아무것도 선언하지 마세요. `std` 네임스페이스에 엔터티를 선언하는 것은 정의되지 않은 동작(undefined behavior)이며 이식성이 없습니다. 표준 라이브러리의 엔터티를 사용하려면 적절한 헤더 파일을 포함하세요.
- using 지시문(_using-directive_)으로 네임스페이스의 모든 이름을 가져오지 마세요.

    ```cpp
    // 금지 -- 네임스페이스를 오염시킵니다.
    using namespace foo;
    ```

- 헤더 파일의 네임스페이스 범위에서는 네임스페이스 별칭(_namespace alias_)을 사용하지 마세요. 단, 명시적으로 내부 전용으로 표시된 네임스페이스는 예외입니다. 헤더 파일에서 네임스페이스로 가져온 것은 모두 그 파일이 내보내는 공개 API의 일부가 되기 때문입니다. 이 조건에 해당하지 않으면 네임스페이스 별칭을 사용할 수 있지만, [적절한 이름](naming_aliases.md)을 가져야 합니다.

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
    ```

    ```cpp
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

## 옮긴이 풀이

### 한눈에 보는 규칙

| 항목 | 규칙 |
| --- | --- |
| 코드 배치 | 몇 가지 예외를 빼고 **모두 네임스페이스 안에** |
| 네임스페이스 이름 | 프로젝트 이름 + (가능하면) 경로 기반의 고유한 이름 |
| `using namespace foo;` (지시문) | **금지** |
| `using ::foo::Bar;` (선언) | `.cc` 파일에서 허용 |
| 인라인 네임스페이스 | **금지** |
| `std`에 선언/전방 선언 | **금지** (정의되지 않은 동작) |
| 헤더의 네임스페이스 범위 별칭 | **금지** (`internal` 네임스페이스·함수 안은 예외) |
| 구현 세부사항 | 이름에 `internal`이 들어간 네임스페이스로 |
| 중첩 네임스페이스 | 한 줄 선언(`namespace a::b {`) 선호, 필수는 아님 |

### 왜 모든 코드를 네임스페이스에 넣는가?

C++의 전역 범위는 **프로그램 전체가 공유하는 단 하나의 공간**입니다. 여기에 이름을 그대로 두면, 내가 만든 이름과 다른 라이브러리의 이름이 같아지는 순간 충돌합니다.

```cpp
// project1/foo.h
class Foo { ... };   // 전역 범위

// project2/foo.h
class Foo { ... };   // 전역 범위 -- 위와 충돌!
```

문제는 이 충돌이 항상 친절한 컴파일 오류로 나타나지는 않는다는 점입니다. 두 정의가 서로 다른 `.cc` 파일에 들어가면 컴파일은 통과하고, 링커가 같은 심볼로 묶어 버려 **런타임에 엉뚱한 클래스 레이아웃으로 동작**할 수 있습니다(ODR 위반).

네임스페이스로 감싸면 이 문제가 사라집니다.

```cpp
namespace project1 { class Foo { ... }; }
namespace project2 { class Foo { ... }; }
// project1::Foo 와 project2::Foo 는 완전히 다른 심볼
```

핵심은 **"짧은 이름을 안전하게 쓰기 위한 장치"**라는 점입니다. 네임스페이스가 있으면 `project1` 안에서는 여전히 `Foo`라고만 써도 되고, 바깥에서 볼 때만 `project1::Foo`로 구분됩니다. 이름을 길게 만들어(`Project1Foo`) 충돌을 피하는 방식보다 훨씬 낫습니다.

### using 지시문(directive)과 using 선언(declaration)은 다릅니다

가장 자주 혼동되는 부분입니다. 이름이 비슷하지만 규칙상 취급이 정반대입니다.

```cpp
using namespace foo;   // using 지시문(directive)  -> 금지
using ::foo::Bar;      // using 선언(declaration)  -> .cc 파일에서 허용
```

- **using 지시문**은 `foo`의 **모든** 이름을 현재 범위로 끌어옵니다. 무엇이 들어왔는지 코드만 봐서는 알 수 없고, `foo`에 새 이름이 추가되는 것만으로 기존 코드가 조용히 다른 오버로드를 고르거나 컴파일이 깨질 수 있습니다.
- **using 선언**은 지정한 이름 하나만 가져옵니다. 무엇을 가져왔는지 파일 상단에 명시적으로 드러나고, 영향 범위도 예측 가능합니다.

```cpp
// 위험한 예: 지시문 때문에 어느 Sort가 불릴지 알기 어렵다
using namespace foo;   // foo::Sort(int*) 가 있다고 가정
using namespace bar;   // 나중에 bar::Sort(int*) 가 추가되면? -> 모호성 오류
Sort(data);
```

단, using 선언도 **헤더 파일의 네임스페이스 범위에서는 쓰지 않는 것이 원칙**입니다. 헤더에서 가져온 이름은 그 헤더를 포함하는 모든 파일에 딸려 들어가, 사실상 그 헤더의 공개 API가 되어 버리기 때문입니다.

### 인라인 네임스페이스를 금지하는 이유

인라인 네임스페이스는 안쪽 이름을 바깥 범위에 자동으로 노출합니다.

```cpp
namespace outer {
inline namespace inner {
  void foo();
}  // namespace inner
}  // namespace outer

outer::inner::foo();  // 둘은
outer::foo();         // 완전히 같은 함수
```

읽는 사람 입장에서는 `outer::foo`를 찾으려고 `outer` 안을 뒤져도 정의가 보이지 않습니다. **이름이 선언된 위치와 참조되는 위치가 어긋나기 때문에** 정의를 추적하기 어려워집니다.

원래 이 기능은 라이브러리가 버전 간 ABI 호환성을 유지하려고 만든 장치입니다(예: `absl::lts_20240116::` 같은 버전 네임스페이스를 인라인으로 두어, 사용자는 `absl::`로 쓰지만 심볼 이름에는 버전이 박히도록). 즉 **라이브러리 전체를 아우르는 버전 관리 정책이 있을 때만 의미가 있고**, 일반 애플리케이션 코드에서는 얻는 것 없이 혼란만 늘어납니다.

### 헤더에서 네임스페이스 별칭을 조심해야 하는 이유

```cpp
// bad.h -- 네임스페이스 범위의 별칭
namespace sidetable = ::pipeline_diagnostics::sidetable;   // 금지
```

이 헤더를 포함하는 **모든** 파일에 `sidetable`이라는 이름이 생깁니다. 헤더 작성자가 의도하지 않았어도 이 별칭은 헤더가 내보내는 공개 API의 일부가 되고, 나중에 이름을 바꾸거나 없애면 사용자 코드가 깨집니다. 사용자가 자기 `sidetable`을 정의하려 할 때 충돌하기도 합니다.

그래서 헤더에서는 별칭의 수명을 좁혀야 합니다.

```cpp
namespace librarian {

namespace internal {  // 내부 전용임이 이름으로 드러남
namespace sidetable = ::pipeline_diagnostics::sidetable;
}

inline void my_inline_function() {
  namespace baz = ::foo::bar::baz;  // 함수 안으로 한정 -> 밖으로 새지 않음
  ...
}

}  // namespace librarian
```

`.cc` 파일은 다른 파일이 포함하지 않으므로 네임스페이스 범위에서 자유롭게 별칭을 써도 됩니다.

### internal 네임스페이스 규약

라이브러리 구현 세부사항은 이름에 `internal`이 들어간 네임스페이스에 두어 **"사용자가 직접 쓰면 안 되는 부분"**임을 문서화합니다. 컴파일러가 막아 주지는 않지만, 코드 리뷰와 자동화 도구가 잡아낼 수 있는 명확한 신호가 됩니다.

```cpp
// absl이 아닌 코드에서 이 내부 이름을 사용하면 안 됩니다.
using ::absl::container_internal::ImplementationDetail;
```

주의할 점은 `internal`이라는 이름 자체가 흔하다는 것입니다. 같은 네임스페이스 아래 여러 헤더가 각자 `internal`을 쓰면 그 안에서 다시 충돌합니다. 그래서 **라이브러리(파일) 이름을 덧붙여** 고유하게 만듭니다.

```cpp
// gshoe/widget.h
namespace gshoe::internal_widget { ... }   // 좋음
namespace gshoe::internal { ... }          // 나쁨 -- 다른 헤더와 충돌 가능
```

### 형식 규칙: 들여쓰기하지 않고, 끝에 주석을 답니다

```cpp
namespace mynamespace {

// 네임스페이스 안이라고 해서 들여쓰지 않습니다.
class MyClass {
 public:
  void Foo();
};

}  // namespace mynamespace
```

- 네임스페이스 블록 안의 내용은 **들여쓰지 않습니다.** 파일 전체가 하나의 네임스페이스로 감싸이는 경우가 대부분이라, 들여쓰면 모든 줄이 통째로 밀려 가로 폭만 낭비됩니다.
- 여러 줄에 걸친 네임스페이스는 닫는 중괄호에 `// namespace 이름` 주석을 답니다. 파일 끝에 `}`만 여러 개 있으면 어떤 블록이 닫히는지 알 수 없기 때문입니다.
- 네임스페이스는 `#include`, gflags 정의/선언, 다른 네임스페이스의 전방 선언 **뒤에서** 시작합니다. `#include`를 네임스페이스 안에 넣으면 포함되는 헤더의 모든 이름이 그 네임스페이스 안에 들어가 버립니다.
- 새 코드에서는 중첩 네임스페이스를 한 줄로 선언하는 편이 선호됩니다(필수는 아님).

```cpp
namespace my_project::my_component {   // 선호
...
}  // namespace my_project::my_component

namespace my_project {                  // 허용되지만 장황함
namespace my_component {
...
}  // namespace my_component
}  // namespace my_project
```

### 하지 말아야 할 것 정리

- `using namespace foo;` — 네임스페이스 오염, 어떤 이름이 들어왔는지 추적 불가
- `std`에 무언가 선언 또는 전방 선언 — 정의되지 않은 동작. 표준 라이브러리 타입은 반드시 해당 헤더를 포함해서 사용
- 인라인 네임스페이스 — ABI 버전 관리 같은 특수 목적 외에는 사용하지 않음
- 헤더의 네임스페이스 범위에 별칭이나 using 선언 두기 — 의도치 않은 공개 API가 됨
- 여러 줄 네임스페이스에서 닫는 `}` 주석 빠뜨리기
- 이름 없는 네임스페이스를 `.h`에 두기 — [내부 연결](internal_linkage.md) 참조
