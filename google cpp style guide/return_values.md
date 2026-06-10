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

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 불필요하게 반환 표현식을 괄호로 묶지 마십시오.

실제로 코드를 볼 때는 불필요하게 반환 표현식을 괄호로 묶지 마십시오.

점검할 때는 특히 다음을 확인하세요:

- 이 선택이 독자에게 숨은 전제나 비용을 만들지 않는지 확인하세요.
