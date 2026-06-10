# 별칭 (Aliases)

## 원문 규칙 번역

공개 별칭은 API 사용자의 이익을 위한 것이며 명확하게 문서화되어야 합니다.

다른 엔터티의 별칭인 이름을 만드는 방법에는 여러 가지가 있습니다.

```cpp
using Bar = Foo;
typedef Foo Bar;  // But prefer `using` in C++ code.
using ::other_namespace::Foo;
using enum MyEnumType;  // Creates aliases for all enumerators in MyEnumType.
```

새 코드에서는 typedef보다 를 사용하는 것이 더 좋습니다. 왜냐하면 C++의 나머지 부분과 보다 일관된 구문을 제공하고 템플릿과 함께 작동하기 때문입니다.

다른 선언과 마찬가지로 헤더 파일에 선언된 별칭은 함수 정의, 클래스의 비공개 부분 또는 명시적으로 표시된 내부 네임스페이스에 있지 않는 한 해당 헤더의 공개 API의 일부입니다. 해당 영역이나 .cc 파일의 별칭은 구현 세부 정보(클라이언트 코드가 이를 참조할 수 없기 때문에)이며 이 규칙으로 제한되지 않습니다.

- 별칭은 길거나 복잡한 이름을 단순화하여 가독성을 향상시킬 수 있습니다.
- 별칭은 API에서 반복적으로 사용되는 유형의 이름을 한 곳에서 지정하여 중복을 줄일 수 있으며, 이를 통해 나중에 유형을 더 쉽게 변경할 수 있습니다.

- 클라이언트 코드가 참조할 수 있는 헤더에 별칭을 배치하면 해당 헤더의 API에 있는 엔터티 수가 늘어나 복잡성이 증가합니다.
- 클라이언트는 공개 별칭의 의도하지 않은 세부 정보에 쉽게 의존할 수 있으므로 변경이 어려워집니다.
- API나 유지 관리 가능성에 대한 영향을 고려하지 않고 구현에만 사용하도록 의도된 공개 별칭을 만들고 싶은 유혹이 있을 수 있습니다.
- 별칭은 이름 충돌의 위험을 초래할 수 있습니다.
- 별칭은 익숙한 구문에 익숙하지 않은 이름을 부여하여 가독성을 저하시킬 수 있습니다.
- 유형 별칭은 불분명한 API 계약을 생성할 수 있습니다. 별칭이 별칭이 지정된 유형과 동일하도록 보장되는지, 동일한 API를 갖는지, 지정된 좁은 방식으로만 사용할 수 있는지가 불분명합니다.

단지 구현 시 입력을 절약하기 위해 공개 API에 별칭을 넣지 마세요. 고객이 사용하도록 의도한 경우에만 그렇게 하십시오.

공개 별칭을 정의할 때 현재 별칭이 지정된 유형과 항상 동일하도록 보장되는지 또는 더 제한적인 호환성을 의도하는지 여부를 포함하여 새 이름의 의도를 문서화하세요. 이를 통해 사용자는 유형을 대체 가능한 것으로 처리할 수 있는지 또는 보다 구체적인 규칙을 따라야 하는지 여부를 알 수 있으며 구현 시 별칭을 변경할 수 있는 자유도를 유지하는 데 도움이 될 수 있습니다.

공개 API에 네임스페이스 별칭을 넣지 마세요. (네임스페이스도 참조하세요.)

예를 들어, 다음 별칭은 클라이언트 코드에서 사용되는 방법을 문서화합니다.

```cpp
namespace mynamespace {
// Used to store field measurements. DataPoint may change from Bar* to some internal type.
// Client code should treat it as an opaque pointer.
using DataPoint = ::foo::Bar*;

// A set of measurements. Just an alias for user convenience.
using TimeSeries = std::unordered_set<DataPoint, std::hash<DataPoint>, DataPointComparator>;
}  // namespace mynamespace
```

이러한 별칭은 의도된 용도를 문서화하지 않으며 그 중 절반은 클라이언트 사용을 위한 것이 아닙니다.

```cpp
namespace mynamespace {
// Bad: none of these say how they should be used.
using DataPoint = ::foo::Bar*;
using ::std::unordered_set;  // Bad: just for local convenience
using ::std::hash;           // Bad: just for local convenience
typedef unordered_set<DataPoint, hash<DataPoint>, DataPointComparator> TimeSeries;
}  // namespace mynamespace
```

그러나 함수 정의, 클래스의 전용 섹션, 명시적으로 표시된 내부 네임스페이스 및 .cc 파일에서는 로컬 편의 별칭이 문제가 없습니다.

```cpp
// In a .cc file
using ::foo::Bar;
```

---

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 - API나 유지 관리 가능성에 대한 영향을 고려하지 않고 구현에만 사용하도록 의도된 공개 별칭을 만들고 싶은 유혹이 있을 수 있습니다.

실제로 코드를 볼 때는 해당 영역이나 .cc 파일의 별칭은 구현 세부 정보(클라이언트 코드가 이를 참조할 수 없기 때문에)이며 이 규칙으로 제한되지 않습니다.

점검할 때는 특히 다음을 확인하세요:

- 이러한 별칭은 의도된 용도를 문서화하지 않으며 그 중 절반은 클라이언트 사용을 위한 것이 아닙니다.
- 공개 별칭은 API 사용자의 이익을 위한 것이며 명확하게 문서화되어야 합니다.
