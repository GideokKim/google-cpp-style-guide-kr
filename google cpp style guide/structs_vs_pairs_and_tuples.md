# 구조체와 쌍/튜플 (Structs vs. Pairs and Tuples)

요소에 의미 있는 이름이 있을 수 있으면 쌍이나 튜플 대신 구조체를 사용하는 것이 좋습니다.

쌍과 튜플을 사용하면 사용자 정의 유형을 정의할 필요가 없어 잠재적으로 코드 작성 시 작업이 절약될 수 있지만 코드를 읽을 때 의미 있는 필드 이름은 .first , .second 또는 std::get<X> 보다 거의 항상 훨씬 더 명확합니다. 인덱스(유형이 고유한 경우)가 아닌 유형별로 튜플 요소에 액세스하기 위한 C++14의 std::get<Type> 도입이 때때로 이 문제를 부분적으로 완화할 수 있지만 일반적으로 필드 이름은 유형보다 훨씬 더 명확하고 더 많은 정보를 제공합니다.

쌍과 튜플은 쌍이나 튜플의 요소에 대한 구체적인 의미가 없는 일반 코드에 적합할 수 있습니다. 기존 코드나 API와 상호 운용하려면 해당 기능을 사용해야 할 수도 있습니다.

---

## 이해하기 쉽게 설명하기

### 핵심: 이름 붙일 수 있으면 pair/tuple 대신 struct

`std::pair`나 `std::tuple`은 타입을 새로 정의하지 않아 **쓸 때**는 편하지만, **읽을 때**는 `.first`, `.second`, `std::get<0>` 같은 접근이 의미를 가립니다. 필드에 의미 있는 이름을 줄 수 있다면 거의 항상 struct가 더 명확합니다.

```cpp
// 읽기 어려움: .first가 뭐였더라?
std::pair<std::string, int> p = GetUser();
Use(p.first, p.second);

// 명확함
struct User {
  std::string name;
  int age;
};
User u = GetUser();
Use(u.name, u.age);
```

### pair/tuple이 맞는 경우

요소에 구체적 의미가 없는 **일반(generic) 코드**나, 기존 코드·API(예: `std::map`의 원소)와 맞춰야 할 때는 pair/tuple이 적절합니다.
