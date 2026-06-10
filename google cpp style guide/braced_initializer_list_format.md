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

## 이해하기 쉽게 설명하기

중괄호 초기화 목록 형식 규칙을 적용할 때는 원문 규칙을 문자 그대로 외우기보다, 왜 이 선택이 독자에게 더 명확한지 살펴보면 쉽습니다. 코드 리뷰에서는 이 기능이 호출 지점에서 의도를 숨기지 않는지, 더 단순한 구조로 같은 목적을 달성할 수 없는지, 기존 코드와 섞였을 때 유지보수 비용이 커지지 않는지를 확인하세요.
