# 포인터/참조 표현식과 타입 (Pointer and Reference Expressions and Types)

## 원문 규칙 번역

마침표나 화살표 주위에는 공백이 없습니다. 포인터 연산자에는 후행 공백이 없습니다.

다음은 올바른 형식의 포인터 및 참조 표현식의 예입니다.

```cpp
x = *p;
p = &x;
x = r.y;
x = r->y;
```

참고 사항:

- 회원 접근 시 마침표나 화살표 주위에 공백이 없어야 합니다.
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

포인터/참조 표현식과 타입 규칙을 적용할 때는 원문 규칙을 문자 그대로 외우기보다, 왜 이 선택이 독자에게 더 명확한지 살펴보면 쉽습니다. 코드 리뷰에서는 이 기능이 호출 지점에서 의도를 숨기지 않는지, 더 단순한 구조로 같은 목적을 달성할 수 없는지, 기존 코드와 섞였을 때 유지보수 비용이 커지지 않는지를 확인하세요.
