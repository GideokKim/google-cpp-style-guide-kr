# 반복문과 분기문 (Looping and branching statements)

## 원문 규칙 번역

상위 수준에서 루프 또는 분기 문은 다음 구성 요소로 구성됩니다.

- 하나 이상의 명령문 키워드(예: if , else , switch , while , do 또는 for ).
- 괄호 안에 하나의 조건 또는 반복 지정자.
- 하나 이상의 제어문 또는 제어문 블록입니다.

- 명령문의 구성요소는 단일 공백으로 구분되어야 합니다(줄바꿈이 아님).
- 조건 또는 반복 지정자 내에서 토큰이 닫는 괄호 또는 다른 세미콜론인 경우를 제외하고 각 세미콜론과 다음 토큰 사이에 하나의 공백(또는 줄 바꿈)을 넣습니다.
- 조건 또는 반복 지정자 내에서 여는 괄호 뒤나 닫는 괄호 앞에 공백을 넣지 마십시오.
- 제어되는 명령문을 블록 안에 넣으세요(예: 중괄호 사용).
- 제어되는 블록 내에서 여는 중괄호 바로 뒤에 한 줄 바꿈을 넣고, 닫는 중괄호 바로 앞에 한 줄 바꿈을 넣으세요.

```cpp
if (condition) {                   // Good - no spaces inside parentheses, space before brace.
  DoOneThing();                    // Good - two-space indent.
  DoAnotherThing();
} else if (int a = f(); a != 3) {  // Good - closing brace on new line, else on same line.
  DoAThirdThing(a);
} else {
  DoNothing();
}

// Good - the same rules apply to loops.
while (condition) {
  RepeatAThing();
}

// Good - the same rules apply to loops.
do {
  RepeatAThing();
} while (condition);

// Good - the same rules apply to loops.
for (int i = 0; i < 10; ++i) {
  RepeatAThing();
}
```

```cpp
if(condition) {}                   // Bad - space missing after `if`.
else if ( condition ) {}           // Bad - space between the parentheses and the condition.
else if (condition){}              // Bad - space missing before `{`.
else if(condition){}               // Bad - multiple spaces missing.

for (int a = f();a == 10) {}       // Bad - space missing after the semicolon.

// Bad - `if ... else` statement does not have braces everywhere.
if (condition)
  foo;
else {
  bar;
}

// Bad - `if` statement too long to omit braces.
if (condition)
  // Comment
  DoSomething();

// Bad - `if` statement too long to omit braces.
if (condition1 &&
    condition2)
  DoSomething();
```

역사적 이유로 위 규칙에 대한 한 가지 예외는 허용하지만 권장하지 않습니다. 결과적으로 전체 명령문이 한 줄(닫는 괄호와 제어 문 사이에 공백이 있는 경우) 또는 두 줄(닫는 괄호 뒤에 줄 바꿈이 있고 중괄호가 없는 경우)에 나타나는 경우 제어 문에 대한 중괄호 또는 중괄호 안의 줄 바꿈을 생략할 수 있습니다.

```cpp
// OK - fits on one line.
if (x == kFoo) { return new Foo(); }

// OK - braces are optional in this case.
if (x == kFoo) return new Foo();

// OK - condition fits on one line, body fits on another.
if (x == kBar)
  Bar(arg1, arg2, arg3);
```

이 예외는 if ... else 또는 do ... while 과 같은 다중 키워드 문에는 적용되지 않습니다.

```cpp
// Bad - `if ... else` statement is missing braces.
if (x) DoThis();
else DoThat();

// Bad - `do ... while` statement is missing braces.
do DoThis();
while (x);
```

명령문이 간단한 경우에만 이 스타일을 사용하고, 복잡한 조건이나 제어 명령문이 포함된 루프 및 분기 명령문은 중괄호를 사용하면 더 쉽게 읽을 수 있다는 점을 고려하세요. 일부 프로젝트에는 항상 중괄호가 필요합니다.

switch 문의 케이스 블록에는 기본 설정에 따라 중괄호가 있을 수도 있고 없을 수도 있습니다. 중괄호를 포함하는 경우 아래와 같이 배치해야 합니다.

```cpp
switch (var) {
  case 0: {  // 2 space indent
    Foo();   // 4 space indent
    break;
  }
  default: {
    Bar();
  }
}
```

빈 루프 본문은 빈 중괄호 쌍을 사용하거나 단일 세미콜론 대신 중괄호 없이 계속되어야 합니다.

```cpp
while (condition) {}  // Good - `{}` indicates no logic.
while (condition) {
  // Comments are okay, too
}
while (condition) continue;  // Good - `continue` indicates no logic.
```

```cpp
while (condition);  // Bad - looks like part of `do-while` loop.
```

---

## 이해하기 쉽게 설명하기

반복문과 분기문 규칙을 적용할 때는 원문 규칙을 문자 그대로 외우기보다, 왜 이 선택이 독자에게 더 명확한지 살펴보면 쉽습니다. 코드 리뷰에서는 이 기능이 호출 지점에서 의도를 숨기지 않는지, 더 단순한 구조로 같은 목적을 달성할 수 없는지, 기존 코드와 섞였을 때 유지보수 비용이 커지지 않는지를 확인하세요.
