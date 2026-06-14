# 반환값 (Return Values)

불필요하게 반환 표현식을 괄호로 묶지 마십시오.

`return expr;`에서는 `x = expr;`에 괄호를 쓸 만한 경우에만 괄호를 사용하세요.

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

### 핵심: 반환값을 불필요하게 괄호로 감싸지 마라

`return expr;`에서는 `x = expr;`에 괄호를 쓸 만한 경우(복잡한 표현식의 가독성)에만 괄호를 쓰세요. `return`은 함수가 아닙니다.

```cpp
return result;                  // 단순한 경우엔 괄호 없이
return (some_long_condition &&  // 복잡한 표현식의 가독성을 위해서는 OK
        another_condition);

return (value);                 // 나쁨 - var = (value)라고 쓰지 않듯이
return(result);                 // 나쁨 - return은 함수가 아님
```
