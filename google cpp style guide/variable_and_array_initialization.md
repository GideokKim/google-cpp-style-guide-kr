# 변수와 배열 초기화 (Variable and Array Initialization)

## 원문 규칙 번역

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

또한 버팀대 형태는 일체형의 협소화를 방지합니다. 이렇게 하면 일부 유형의 프로그래밍 오류를 방지할 수 있습니다.

```cpp
int pi(3.14);  // OK -- pi == 3.
int pi{3.14};  // Compile error: narrowing conversion.
```

---

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 빈 중괄호 {}는 특별하며, 가능한 경우 기본 생성자를 호출합니다.

실제로 코드를 볼 때는 비어 있지 않은 중괄호 초기화 목록은 가능할 때마다

점검할 때는 특히 다음을 확인하세요:

- std::initializer_list 생성자가 있는 유형에 중괄호 초기화 목록 {...}을 사용할 때는 주의하세요.
- std::initializer_list 생성자가 아닌 생성자를 강제하려면 중괄호 대신 괄호를 사용하십시오.
