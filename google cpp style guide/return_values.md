# 반환값 (Return Values)

## 원문 규칙 번역

불필요하게 반환 표현식을 괄호로 묶지 마십시오.

반환 expr에는 괄호를 사용하십시오. x = expr에서 사용할 경우에만; .

```cpp
return result;                  // No parentheses in the simple case.
// Parentheses OK to make a complex expression more readable.
return (some_long_condition &&
        another_condition);
```

```cpp
return (value);                // You wouldn't write var = (value);
return(result);                // return is not a function!
```

---

## 이해하기 쉽게 설명하기

반환값 규칙을 적용할 때는 원문 규칙을 문자 그대로 외우기보다, 왜 이 선택이 독자에게 더 명확한지 살펴보면 쉽습니다. 코드 리뷰에서는 이 기능이 호출 지점에서 의도를 숨기지 않는지, 더 단순한 구조로 같은 목적을 달성할 수 없는지, 기존 코드와 섞였을 때 유지보수 비용이 커지지 않는지를 확인하세요.
