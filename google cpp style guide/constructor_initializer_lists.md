# 생성자 초기화 목록 (Constructor Initializer Lists)

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

## 이해하기 쉽게 설명하기

### 핵심: 한 줄에, 안 되면 콜론 앞에서 줄바꿈하고 4칸 들여쓰기

```cpp
// 한 줄에 다 들어가면
MyClass::MyClass(int var) : some_var_(var) { DoSomething(); }

// 안 들어가면 콜론(:) 앞에서 줄바꿈 + 4칸 들여쓰기
MyClass::MyClass(int var)
    : some_var_(var), some_other_var_(var + 1) {
  DoSomething();
}

// 여러 줄이면 멤버마다 한 줄씩, 정렬
MyClass::MyClass(int var)
    : some_var_(var),             // 4칸 들여쓰기
      some_other_var_(var + 1) {  // 정렬
  DoSomething();
}
```
