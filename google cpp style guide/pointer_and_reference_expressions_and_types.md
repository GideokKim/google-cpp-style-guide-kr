# 포인터/참조 표현식과 타입 (Pointer and Reference Expressions and Types)

마침표나 화살표 주위에는 공백이 없습니다. 포인터 연산자에는 후행 공백이 없습니다.

다음은 올바른 형식의 포인터 및 참조 표현식의 예입니다.

```cpp
x = *p;
p = &x;
x = r.y;
x = r->y;
```

참고 사항:

- 멤버 접근 시 마침표나 화살표 주위에 공백이 없어야 합니다.
- 포인터 연산자에는 * 또는 & 뒤에 공백이 없습니다.

포인터나 참조(변수 선언이나 정의, 인수, 반환 유형, 템플릿 매개변수 등)를 참조할 때 별표/앰퍼샌드 앞에 공백을 두어서는 안 됩니다. 선언된 이름(있는 경우)과 유형을 구분하려면 공백을 사용하십시오.

```cpp
// These are fine.
char* c;
const std::string& str;
int* GetPointer();
std::vector<char*>  // Note no space between '*' and '>'
```

동일한 선언에서 여러 변수를 선언하는 것은 (비정상적인 경우) 허용되지만 포인터 또는 참조 장식이 있는 경우에는 허용되지 않습니다. 그러한 선언은 쉽게 잘못 읽힐 수 있습니다.

```cpp
// Fine if helpful for readability.
int x, y;
```

```cpp
int x, *y;  // Disallowed - no & or * in multiple declaration
int *x, *y;  // Disallowed - no & or * in multiple declaration
int *x;  // Disallowed - & or * must be left of the space
char * c;  // Bad - spaces on both sides of *
const std::string & str;  // Bad - spaces on both sides of &
```

---

## 이해하기 쉽게 설명하기

### 핵심: `.`/`->` 주위 공백 없음, `*`/`&`는 타입 쪽에 붙인다

- 멤버 접근의 `.`이나 `->` 주위에는 공백을 넣지 않습니다.
- 포인터 연산자 `*`, `&` 뒤에는 공백을 넣지 않습니다.

```cpp
x = *p;   p = &x;   x = r.y;   x = r->y;
```

### 선언에서의 `*`/`&` 위치

선언·인수·반환 타입·템플릿 매개변수 등에서 `*`/`&`는 **타입 쪽에 붙이고**(앞에 공백 없음), 이름과 타입은 공백으로 구분합니다.

```cpp
char* c;
const std::string& str;
int* GetPointer();
std::vector<char*>          // '*'와 '>' 사이 공백 없음

char * c;                   // 나쁨 - * 양쪽에 공백
const std::string & str;    // 나쁨
```

### 다중 선언 금지

한 선언에서 여러 변수를 선언하는 것은 가능하지만, **포인터·참조가 끼면 금지**입니다(오독하기 쉬움).

```cpp
int x, y;        // 가독성에 도움되면 OK
int x, *y;       // 금지
int *x, *y;      // 금지
```
