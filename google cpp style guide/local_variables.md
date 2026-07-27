# 지역 변수 (Local Variables)

함수의 변수를 가능한 한 가장 좁은 범위에 배치하고, 선언과 동시에 초기화하세요.

C++에서는 함수의 어느 위치에서나 변수를 선언할 수 있습니다. 가능한 한 로컬 범위에서 선언하고 첫 번째 사용에 최대한 가깝게 선언하는 것이 좋습니다. 이렇게 하면 독자가 선언을 더 쉽게 찾고 변수의 유형과 초기화된 내용을 확인할 수 있습니다. 특히 선언과 할당 대신 초기화를 사용해야 합니다. 예:

```cpp
int i;
i = f();      // Bad -- initialization separate from declaration.
```

```cpp
int i = f();  // Good -- declaration has initialization.
```

```cpp
int jobs = NumJobs();
// More code...
f(jobs);      // Bad -- declaration separate from use.
```

```cpp
int jobs = NumJobs();
f(jobs);      // Good -- declaration immediately (or closely) followed by use.
```

```cpp
std::vector<int> v;
v.push_back(1);  // Prefer initializing using brace initialization.
v.push_back(2);
```

```cpp
std::vector<int> v = {1, 2};  // Good -- v starts initialized.
```

if , while 및 for 문에 필요한 변수는 일반적으로 해당 문 내에서 선언되어야 하므로 해당 변수는 해당 범위로 제한됩니다. 예를 들어:

```cpp
while (const char* p = strchr(str, '/')) str = p + 1;
```

한 가지 주의 사항이 있습니다. 변수가 객체인 경우 변수가 범위에 들어가고 생성될 때마다 해당 생성자가 호출되고, 범위를 벗어날 때마다 소멸자가 호출됩니다.

```cpp
// Inefficient implementation:
for (int i = 0; i < 1000000; ++i) {
  Foo f;  // My ctor and dtor get called 1000000 times each.
  f.DoSomething(i);
}
```

해당 루프 외부의 루프에 사용되는 변수를 선언하는 것이 더 효율적일 수 있습니다.

```cpp
Foo f;  // My ctor and dtor get called once each.
for (int i = 0; i < 1000000; ++i) {
  f.DoSomething(i);
}
```

---

## 옮긴이 풀이

### 핵심 두 가지: 좁은 범위 + 선언 시 초기화

지역 변수는 (1) 가능한 한 좁은 범위에, (2) 처음 쓰이는 곳에 가깝게 선언하고, (3) 선언과 동시에 초기화하세요. 그래야 독자가 변수의 타입과 초깃값을 바로 확인할 수 있습니다.

```cpp
int i;
i = f();      // 나쁨 -- 선언과 초기화가 분리됨

int j = f();  // 좋음 -- 선언과 동시에 초기화
```

### 조건문·반복문 변수는 그 문 안에서 선언

`if`, `while`, `for`에만 필요한 변수는 해당 문 안에서 선언해 범위를 그 문으로 제한하세요.

```cpp
while (const char* p = strchr(str, '/')) str = p + 1;
```

### 예외: 루프 안의 비싼 객체

변수가 객체라면 범위에 들어올 때마다 생성자가, 나갈 때마다 소멸자가 호출됩니다. 루프 안에서 매번 생성·소멸하는 비용이 크다면, 그 변수만은 루프 밖에서 선언하는 편이 더 효율적입니다.

```cpp
// 비효율적: 생성자/소멸자가 100만 번씩 호출됨
for (int i = 0; i < 1000000; ++i) {
  Foo f;
  f.DoSomething(i);
}

// 효율적: 생성자/소멸자가 한 번씩만 호출됨
Foo f;
for (int i = 0; i < 1000000; ++i) {
  f.DoSomething(i);
}
```

단, 이는 어디까지나 예외입니다. 기본은 "가장 좁은 범위"이며, 성능이 실제로 문제될 때만 범위를 넓히세요.
