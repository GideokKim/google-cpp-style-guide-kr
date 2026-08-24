# 구조체와 쌍/튜플 (Structs vs. Pairs and Tuples)

요소에 의미 있는 이름을 붙일 수 있다면 `pair`나 `tuple` 대신 `struct`를 사용하세요.

`pair`와 `tuple`을 쓰면 사용자 정의 타입을 정의할 필요가 없어 코드를 작성할 때는 일이 줄어들 수 있지만, 코드를 읽을 때는 의미 있는 필드 이름이 `.first`, `.second`, `std::get<X>`보다 거의 항상 훨씬 명확합니다. C++14에서 인덱스가 아니라 타입으로 튜플 요소에 접근하는 `std::get<Type>`이 도입되어(타입이 유일한 경우) 이 문제를 부분적으로 덜어 주기도 하지만, 대개 필드 이름이 타입보다 훨씬 명확하고 더 많은 정보를 줍니다.

`pair`와 `tuple`은 그 요소에 특정한 의미가 없는 제네릭 코드에서는 적절할 수 있습니다. 기존 코드나 API와 상호 운용하기 위해 사용해야 할 수도 있습니다.

---

## 옮긴이 풀이

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
