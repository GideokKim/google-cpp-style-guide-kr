# 복사 가능 및 이동 가능 타입 (Copyable and Movable Types)

클래스의 공개 API는 클래스가 복사 가능인지, 이동 전용인지, 복사 가능하지도 이동 가능하지도 않은지 명확하게 밝혀야 합니다. 이러한 작업이 귀하의 유형에 명확하고 의미가 있는 경우 복사 및/또는 이동을 지원하십시오.

이동 가능 유형은 임시에서 초기화하고 할당할 수 있는 유형입니다.

복사 가능한 유형은 소스 값이 변경되지 않는다는 규정과 함께 동일한 유형의 다른 객체에서 초기화되거나 할당될 수 있는 유형입니다(따라서 정의에 따라 이동할 수도 있음). std::unique_ptr<int>는 이동 가능하지만 복사할 수 없는 유형의 예입니다(소스 std::unique_ptr<int>의 값은 대상에 할당하는 동안 수정되어야 하기 때문입니다). int 및 std::string은 복사도 가능한 이동 가능 유형의 예입니다. ( int 의 경우 이동 및 복사 작업이 동일합니다. std::string 의 경우 복사보다 비용이 적게 드는 이동 작업이 있습니다.)

사용자 정의 유형의 경우 복사 동작은 복사 생성자와 복사 할당 연산자에 의해 정의됩니다. 이동 동작은 이동 생성자와 이동 할당 연산자(있는 경우)에 의해 정의되고, 그렇지 않으면 복사 생성자와 복사 할당 연산자에 의해 정의됩니다.

복사/이동 생성자는 객체를 값으로 전달할 때와 같은 일부 상황에서 컴파일러에 의해 암시적으로 호출될 수 있습니다.

복사 가능 및 이동 가능 유형의 객체를 값으로 전달하고 반환할 수 있으므로 API가 더욱 단순하고 안전하며 일반화됩니다. 포인터나 참조로 객체를 전달할 때와는 달리 소유권, 수명, 가변성 및 유사한 문제에 대해 혼동할 위험이 없으며 계약에서 이를 지정할 필요가 없습니다. 또한 클라이언트와 구현 간의 비로컬 상호 작용을 방지하므로 컴파일러에서 이를 더 쉽게 이해하고 유지 관리하고 최적화할 수 있습니다. 또한 이러한 객체는 대부분의 컨테이너와 같이 값별 전달이 필요한 일반 API와 함께 사용할 수 있으며 유형 구성과 같은 추가적인 유연성을 허용합니다.

복사/이동 생성자 및 할당 연산자는 일반적으로 Clone() , CopyFrom() 또는 Swap() 과 같은 대안보다 올바르게 정의하기가 더 쉽습니다. 왜냐하면 암시적으로 또는 = default 를 사용하여 컴파일러에서 생성할 수 있기 때문입니다. 간결하며 모든 데이터 멤버가 복사되었는지 확인합니다. 복사 및 이동 생성자는 힙 할당이나 별도의 초기화 및 할당 단계가 필요하지 않고 복사 제거와 같은 최적화에 적합하기 때문에 일반적으로 더 효율적입니다.

이동 작업을 사용하면 rvalue 개체에서 리소스를 암시적이고 효율적으로 전송할 수 있습니다. 이를 통해 경우에 따라 더 단순한 코딩 스타일이 가능해집니다.

일부 유형은 복사할 필요가 없으며 이러한 유형에 대한 복사 작업을 제공하는 것은 혼란스럽고 무의미하거나 완전히 부정확할 수 있습니다. 싱글톤 개체( Registerer ), 특정 범위에 연결된 개체( Cleanup ) 또는 개체 ID에 밀접하게 연결된 개체( Mutex )를 나타내는 형식은 의미 있게 복사할 수 없습니다. 다형성으로 사용되는 기본 클래스 유형에 대한 복사 작업은 위험합니다. 복사 작업을 사용하면 객체 분할이 발생할 수 있기 때문입니다. 기본 설정되거나 부주의하게 구현된 복사 작업은 올바르지 않을 수 있으며, 결과적인 버그는 혼란스럽고 진단하기 어려울 수 있습니다.

복사 생성자는 암시적으로 호출되므로 호출을 놓치기 쉽습니다. 이는 참조에 의한 전달이 관례적이거나 필수인 언어에 익숙한 프로그래머에게 혼란을 야기할 수 있습니다. 또한 과도한 복사를 조장하여 성능 문제를 일으킬 수도 있습니다.

모든 클래스의 공개 인터페이스는 클래스가 지원하는 복사 및 이동 작업을 명확히 해야 합니다. 이는 일반적으로 선언의 공개 섹션에서 적절한 작업을 명시적으로 선언 및/또는 삭제하는 형식을 취해야 합니다.

특히 복사 가능한 클래스는 복사 작업을 명시적으로 선언해야 하고, 이동 전용 클래스는 이동 작업을 명시적으로 선언해야 하며, 복사 불가능/이동 가능한 클래스는 복사 작업을 명시적으로 삭제해야 합니다. 복사 가능한 클래스는 효율적인 이동을 지원하기 위해 이동 작업을 선언할 수도 있습니다. 네 가지 복사/이동 작업을 모두 명시적으로 선언하거나 삭제하는 것이 허용되지만 필수는 아닙니다. 복사 또는 이동 할당 연산자를 제공하는 경우 해당 생성자도 제공해야 합니다.

```cpp
class Copyable {
 public:
  Copyable(const Copyable& other) = default;
  Copyable& operator=(const Copyable& other) = default;

  // The implicit move operations are suppressed by the declarations above.
  // You may explicitly declare move operations to support efficient moves.
};

class MoveOnly {
 public:
  MoveOnly(MoveOnly&& other) = default;
  MoveOnly& operator=(MoveOnly&& other) = default;

  // The copy operations are implicitly deleted, but you can
  // spell that out explicitly if you want:
  MoveOnly(const MoveOnly&) = delete;
  MoveOnly& operator=(const MoveOnly&) = delete;
};

class NotCopyableOrMovable {
 public:
  // Not copyable or movable
  NotCopyableOrMovable(const NotCopyableOrMovable&) = delete;
  NotCopyableOrMovable& operator=(const NotCopyableOrMovable&)
      = delete;

  // The move operations are implicitly disabled, but you can
  // spell that out explicitly if you want:
  NotCopyableOrMovable(NotCopyableOrMovable&&) = delete;
  NotCopyableOrMovable& operator=(NotCopyableOrMovable&&)
      = delete;
};
```

이러한 선언/삭제는 명백한 경우에만 생략할 수 있습니다.

- 클래스에 구조체 또는 인터페이스 전용 기본 클래스와 같은 비공개 섹션이 없는 경우 복사 가능성/이동 가능성은 공개 데이터 멤버의 복사 가능성/이동 가능성에 의해 결정될 수 있습니다.
- 기본 클래스가 복사 가능하거나 이동 가능하지 않은 경우 파생 클래스도 당연히 그렇지 않습니다. 이러한 작업을 암시적으로 남겨두는 인터페이스 전용 기본 클래스만으로는 구체적인 하위 클래스를 명확하게 만드는 데 충분하지 않습니다.
- 복사에 대한 생성자 또는 할당 작업을 명시적으로 선언하거나 삭제하면 다른 복사 작업은 명확하지 않으므로 선언하거나 삭제해야 합니다. 이동 작업도 마찬가지입니다.

일반 사용자에게 복사/이동의 의미가 명확하지 않거나 예상치 못한 비용이 발생하는 경우 유형을 복사/이동할 수 없어야 합니다. 복사 가능한 유형에 대한 이동 작업은 엄격하게 성능 최적화이며 잠재적인 버그 및 복잡성 소스이므로 해당 복사 작업보다 훨씬 더 효율적인 경우가 아니면 정의하지 마세요. 유형이 복사 작업을 제공하는 경우 해당 작업의 기본 구현이 올바르도록 클래스를 디자인하는 것이 좋습니다. 다른 코드와 마찬가지로 기본 작업의 정확성을 검토하는 것을 잊지 마세요.

조각화 위험을 제거하려면 생성자를 보호하거나 소멸자를 보호한다고 선언하거나 하나 이상의 순수 가상 멤버 함수를 제공하여 기본 클래스를 추상화하는 것이 좋습니다. 구체적인 클래스에서 파생되는 것을 피하는 것이 좋습니다.

---

## 옮긴이 풀이

### 핵심: 공개 API가 복사/이동 가능 여부를 "명시"해야 한다

클래스를 보는 사람이 그 클래스를 값으로 복사할 수 있는지, 이동만 되는지, 둘 다 안 되는지 **선언만 보고** 알 수 있어야 합니다. 그래서 해당 연산을 public 섹션에서 명시적으로 선언하거나 `= delete`합니다.

```cpp
// 복사 가능: 복사 연산을 명시적으로 선언
class Copyable {
 public:
  Copyable(const Copyable&) = default;
  Copyable& operator=(const Copyable&) = default;
};

// 이동 전용: 이동을 선언하면 복사는 암시적으로 삭제됨
class MoveOnly {
 public:
  MoveOnly(MoveOnly&&) = default;
  MoveOnly& operator=(MoveOnly&&) = default;
};

// 복사·이동 불가: 복사를 명시적으로 삭제
class NotCopyableOrMovable {
 public:
  NotCopyableOrMovable(const NotCopyableOrMovable&) = delete;
  NotCopyableOrMovable& operator=(const NotCopyableOrMovable&) = delete;
};
```

### 언제 복사를 막아야 하나?

복사의 의미가 불분명하거나 예상치 못한 비용이 드는 타입은 복사 가능하게 만들지 마세요. 싱글톤(`Registerer`), 특정 스코프에 묶인 객체(`Cleanup`), 정체성이 중요한 객체(`Mutex`)가 그렇습니다. 특히 **다형적으로 쓰이는 기본 클래스**는 복사 시 객체 슬라이싱(object slicing)이 발생하므로 위험합니다.

### 슬라이싱 방지

기본 클래스는 추상으로 만드세요 — 생성자나 소멸자를 `protected`로 두거나, 순수 가상 함수를 하나 이상 두는 방법이 있습니다. 구체 클래스에서 파생하는 것은 피하세요.

### 복사 가능 타입의 이동 연산

복사 가능한 타입에 이동 연산을 추가하는 것은 **순전히 성능 최적화**이며 버그·복잡성의 원천입니다. 복사보다 확실히 훨씬 빠를 때만 정의하세요.
