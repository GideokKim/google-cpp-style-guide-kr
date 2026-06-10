# 중괄호 초기화 목록 형식 (Braced Initializer List Format)

## 원문 규칙 번역

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

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 중괄호로 묶인 목록이 이름(예: 유형 또는 변수 이름) 뒤에 오는 경우, {}가 해당 이름을 가진 함수 호출의 괄호인 것처럼 형식을 지정합니다.

실제로 코드를 볼 때는 그 자리에서 함수 호출의 형식을 지정하는 것과 똑같이 중괄호 초기화 목록의 형식을 지정합니다.

점검할 때는 특히 다음을 확인하세요:

- 이 선택이 독자에게 숨은 전제나 비용을 만들지 않는지 확인하세요.
