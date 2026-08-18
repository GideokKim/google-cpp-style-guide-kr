# thread_local 변수 (thread_local Variables)

함수 안에서 선언되지 않은 `thread_local` 변수는 진짜 컴파일 타임 상수로 초기화되어야 하며, 이는 [`constinit`](https://en.cppreference.com/w/cpp/language/constinit) 특성(attribute)을 사용해 강제해야 합니다. 스레드 지역 데이터를 정의하는 다른 방법보다 `thread_local`을 선호하세요.

**정의:**

변수는 `thread_local` 지정자를 붙여 선언할 수 있습니다.

```cpp
thread_local Foo foo = ...;
```

이런 변수는 사실 객체들의 모음이어서, 서로 다른 스레드가 이 변수에 접근하면 실제로는 서로 다른 객체에 접근하게 됩니다. `thread_local` 변수는 여러 면에서 [정적 저장 기간 변수](static_and_global_variables.md)와 매우 비슷합니다. 예를 들어 네임스페이스 범위, 함수 안, 클래스의 정적 멤버로는 선언할 수 있지만, 일반 클래스 멤버로는 선언할 수 없습니다.

`thread_local` 변수의 인스턴스는 정적 변수와 매우 비슷하게 초기화되지만, 프로그램 시작 시 한 번이 아니라 스레드마다 따로 초기화되어야 한다는 점이 다릅니다. 따라서 함수 안에 선언된 `thread_local` 변수는 안전하지만, 그 밖의 `thread_local` 변수는 정적 변수와 똑같은 초기화 순서 문제를(그리고 그 이상의 문제도) 겪습니다.

`thread_local` 변수에는 미묘한 소멸 순서 문제가 있습니다. 스레드가 종료될 때 `thread_local` 변수는 (C++에서 대체로 그렇듯이) 초기화의 역순으로 소멸됩니다. 어떤 `thread_local` 변수의 소멸자가 실행시킨 코드가 같은 스레드에서 이미 소멸된 `thread_local`을 참조하면, 특히 진단하기 어려운 use-after-free가 발생합니다.

**장점:**

- 스레드 지역 데이터는 (보통 한 스레드만 접근할 수 있으므로) 본질적으로 경합에서 안전하며, 그래서 `thread_local`은 동시성 프로그래밍에 유용합니다.
- `thread_local`은 스레드 지역 데이터를 만드는 유일한 표준 지원 방법입니다.

**단점:**

- `thread_local` 변수에 접근하면, 스레드가 시작될 때나 특정 스레드에서 처음 사용할 때 예측할 수도 제어할 수도 없는 양의 다른 코드가 실행될 수 있습니다.
- `thread_local` 변수는 사실상 전역 변수이며, 스레드 안전성이 부족하다는 점을 제외한 전역 변수의 모든 단점을 그대로 가집니다.
- `thread_local` 변수가 소비하는 메모리는 (최악의 경우) 실행 중인 스레드 수에 비례해 늘어나며, 프로그램에서 그 양이 상당히 커질 수 있습니다.
- 데이터 멤버는 `static`이기도 하지 않으면 `thread_local`이 될 수 없습니다.
- `thread_local` 변수에 복잡한 소멸자가 있으면 use-after-free 버그를 겪을 수 있습니다. 특히 그런 변수의 소멸자는 이미 소멸되었을 수 있는 `thread_local`을 참조하는 코드를 (간접적으로라도) 호출해서는 안 됩니다. 이 성질은 강제하기 어렵습니다.
- 전역/정적 맥락에서 use-after-free를 피하려고 쓰던 방법은 `thread_local`에는 통하지 않습니다. 구체적으로, 전역 변수와 정적 변수의 소멸자를 건너뛰는 것은 그 수명이 프로그램 종료와 함께 끝나기 때문에 허용됩니다. 따라서 "누수"가 있더라도 OS가 메모리와 그 밖의 리소스를 정리하면서 곧바로 처리됩니다. 반면 `thread_local` 변수의 소멸자를 건너뛰면, 프로그램이 도는 동안 종료된 전체 스레드 수에 비례해 리소스 누수가 발생합니다.

**결정:**

- 클래스 범위나 네임스페이스 범위의 `thread_local` 변수는 진짜 컴파일 타임 상수로 초기화되어야 합니다(즉, 동적 초기화가 없어야 합니다). 이를 강제하기 위해 클래스 범위나 네임스페이스 범위의 `thread_local` 변수에는 [`constinit`](https://en.cppreference.com/w/cpp/language/constinit)을 붙여야 합니다(`constexpr`도 가능하지만 그런 경우는 드물어야 합니다).

    ```cpp
    constinit thread_local Foo foo = ...;
    ```

- 함수 안의 `thread_local` 변수는 초기화 문제는 없지만, 스레드 종료 중에 use-after-free가 발생할 위험은 여전히 있습니다. 함수 범위의 `thread_local`을 노출하는 함수나 정적 메서드를 정의하면, 클래스 범위나 네임스페이스 범위의 `thread_local`을 흉내 낼 수 있다는 점을 알아 두세요.

    ```cpp
    Foo& MyThreadLocalFoo() {
      thread_local Foo result = ComplicatedInitialization();
      return result;
    }
    ```

- `thread_local` 변수는 스레드가 종료될 때마다 소멸된다는 점에 유의하세요. 그런 변수의 소멸자가 (이미 소멸되었을 수 있는) 다른 `thread_local`을 참조하면 진단하기 어려운 use-after-free 버그를 겪게 됩니다. 다른 `thread_local`에 접근할 가능성을 최소화하려면, 자명한 타입이나 소멸 시 사용자 제공 코드를 실행하지 않는다고 증명할 수 있는 타입을 선호하세요.

스레드 지역 데이터를 정의하는 다른 메커니즘보다 `thread_local`을 선호해야 합니다.

---

## 옮긴이 풀이

### thread_local이란?

`thread_local` 변수는 스레드마다 별도의 인스턴스를 가집니다. 같은 변수 이름이라도 스레드 A와 스레드 B는 서로 다른 객체에 접근합니다. 덕분에 별도의 락 없이도 스레드 간 데이터 경합에서 안전합니다.

```cpp
thread_local Foo foo = ...;
```

### 핵심 규칙: 클래스·네임스페이스 범위는 "진짜 컴파일 타임 상수"로

함수 **밖**(클래스·네임스페이스 범위)에 선언한 `thread_local`은 동적 초기화가 없어야 하며, 이를 `constinit`로 강제해야 합니다.

```cpp
constinit thread_local Foo foo = ...;
```

함수 **안**의 `thread_local`은 초기화 순서 문제가 없으므로, 복잡한 초기화가 필요하면 함수로 감싸 노출하는 패턴이 안전합니다.

```cpp
Foo& MyThreadLocalFoo() {
  thread_local Foo result = ComplicatedInitialization();
  return result;
}
```

### 주의: 소멸 순서와 use-after-free

`thread_local`은 **스레드가 끝날 때마다** 소멸됩니다. 어떤 `thread_local`의 소멸자가 이미 파괴된 다른 `thread_local`을 참조하면 진단하기 어려운 use-after-free가 됩니다. 그래서 소멸 시 사용자 코드를 실행하지 않는 간단한 타입을 선호하세요.

또한 전역/정적 변수에서 쓰던 "소멸자 건너뛰기(의도적 누수)" 기법은 `thread_local`에는 통하지 않습니다. 전역은 프로그램 종료 시 OS가 한꺼번에 정리하지만, `thread_local`은 스레드가 끝날 때마다 누수가 쌓여 종료된 스레드 수에 비례해 리소스가 새기 때문입니다.

### 단점 요약

- 접근 시 스레드 시작/첫 사용 중 예측 불가한 양의 코드가 실행될 수 있음
- 사실상 전역 변수라, 스레드 안전성만 빼면 전역의 단점을 그대로 가짐
- 메모리 사용량이 실행 중인 스레드 수에 비례해 커짐
