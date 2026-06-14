# 변수와 배열 초기화 (Variable and Array Initialization)

= , () 및 {} 중에서 선택할 수 있습니다. 다음은 모두 정확합니다.

```cpp
int x = 3;
int x(3);
int x{3};
std::string name = "Some Name";
std::string name("Some Name");
std::string name{"Some Name"};
```

std::initializer_list 생성자가 있는 유형에 중괄호 초기화 목록 {...}을 사용할 때는 주의하세요. 비어 있지 않은 중괄호 초기화 목록은 가능할 때마다 std::initializer_list 생성자를 선호합니다. 빈 중괄호 {}는 특별하며, 가능한 경우 기본 생성자를 호출합니다. std::initializer_list 생성자가 아닌 생성자를 강제하려면 중괄호 대신 괄호를 사용하십시오.

```cpp
std::vector<int> v(100, 1);  // A vector containing 100 items: All 1s.
std::vector<int> v{100, 1};  // A vector containing 2 items: 100 and 1.
```

또한 중괄호 형태는 정수 타입의 축소 변환(narrowing)을 방지합니다. 이렇게 하면 일부 프로그래밍 오류를 방지할 수 있습니다.

```cpp
int pi(3.14);  // OK -- pi == 3.
int pi{3.14};  // Compile error: narrowing conversion.
```

---

## 이해하기 쉽게 설명하기

### 핵심: =, (), {} 중 선택 — 다만 {}의 함정에 주의

세 가지 초기화 형태 모두 맞습니다.

```cpp
int x = 3;   int x(3);   int x{3};
std::string name = "Some Name";  // (), {} 도 가능
```

### 중괄호 {}의 두 가지 함정

1. **`std::initializer_list` 생성자 우선**: 비어 있지 않은 `{...}`는 가능하면 `initializer_list` 생성자를 부릅니다. 다른 생성자를 부르려면 괄호 `()`를 쓰세요.

```cpp
std::vector<int> v(100, 1);  // 1이 100개
std::vector<int> v{100, 1};  // 100과 1, 두 개!
```

2. **빈 `{}`**는 특별 — 가능하면 기본 생성자를 부릅니다.

### 중괄호의 장점: 축소 변환 방지

중괄호 형태는 정수 타입의 축소 변환(narrowing)을 막아 일부 오류를 컴파일 단계에서 잡아줍니다.

```cpp
int pi(3.14);  // OK -- pi == 3 (조용히 잘림)
int pi{3.14};  // 컴파일 오류: 축소 변환
```
