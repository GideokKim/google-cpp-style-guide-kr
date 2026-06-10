# 생성자 초기화 목록 (Constructor Initializer Lists)

## 원문 규칙 번역

생성자 이니셜라이저 목록은 모두 한 줄에 표시되거나 후속 줄에 4개의 공백이 들여쓰기될 수 있습니다.

이니셜라이저 목록에 허용되는 형식은 다음과 같습니다.

```cpp
// When everything fits on one line:
MyClass::MyClass(int var) : some_var_(var) {
  DoSomething();
}

// If the signature and initializer list are not all on one line,
// you must wrap before the colon and indent 4 spaces:
MyClass::MyClass(int var)
    : some_var_(var), some_other_var_(var + 1) {
  DoSomething();
}

// When the list spans multiple lines, put each member on its own line
// and align them:
MyClass::MyClass(int var)
    : some_var_(var),             // 4 space indent
      some_other_var_(var + 1) {  // lined up
  DoSomething();
}

// As with any other code block, the close curly can be on the same
// line as the open curly, if it fits.
MyClass::MyClass(int var)
    : some_var_(var) {}
```

---

---

## 이해하기 쉽게 설명하기

이 규칙의 핵심은 이니셜라이저 목록에 허용되는 형식은 다음과 같습니다.

실제로 코드를 볼 때는 생성자 이니셜라이저 목록은 모두 한 줄에 표시되거나 후속 줄에 4개의 공백이 들여쓰기될 수 있습니다.

점검할 때는 특히 다음을 확인하세요:

- 이 선택이 독자에게 숨은 전제나 비용을 만들지 않는지 확인하세요.
