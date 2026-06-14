# 중괄호 초기화 목록 형식 (Braced Initializer List Format)

그 자리에서 함수 호출의 형식을 지정하는 것과 똑같이 중괄호 초기화 목록의 형식을 지정합니다.

중괄호로 묶인 목록이 이름(예: 유형 또는 변수 이름) 뒤에 오는 경우, {}가 해당 이름을 가진 함수 호출의 괄호인 것처럼 형식을 지정합니다. 이름이 없으면 길이가 0인 이름을 가정합니다.

```cpp
// Examples of braced init list on a single line.
return {foo, bar};
functioncall({foo, bar});
std::pair<int, int> p{foo, bar};

// When you have to wrap.
SomeFunction(
    {"assume a zero-length name before {"},
    some_other_function_parameter);
SomeType variable{
    some, other, values,
    {"assume a zero-length name before {"},
    SomeOtherType{
        "Very long string requiring the surrounding breaks.",
        some, other, values},
    SomeOtherType{"Slightly shorter string",
                  some, other, values}};
SomeType variable{
    "This is too long to fit all in one line"};
MyType m = {  // Here, you could also break before {.
    superlongvariablename1,
    superlongvariablename2,
    {short, interior, list},
    {interiorwrappinglist,
     interiorwrappinglist2}};
```

---

## 이해하기 쉽게 설명하기

### 핵심: 함수 호출처럼 형식을 맞춘다

중괄호 초기화 목록은 그 자리에서 **함수 호출과 똑같이** 형식을 지정합니다. 이름(타입·변수 이름) 뒤에 `{}`가 오면, 그 이름을 가진 함수 호출의 괄호처럼 다룹니다. 이름이 없으면 "길이 0짜리 이름"이 있다고 가정합니다.

```cpp
return {foo, bar};
functioncall({foo, bar});
std::pair<int, int> p{foo, bar};

// 래핑이 필요할 때
SomeType variable{
    some, other, values,
    {"assume a zero-length name before {"},
    SomeOtherType{"Slightly shorter string",
                  some, other, values}};
```
