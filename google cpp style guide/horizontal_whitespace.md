# 가로 공백 (Horizontal Whitespace)

가로 공백 사용은 위치에 따라 다릅니다. 줄 끝에 공백을 두지 마십시오.

```cpp
int i = 0;  // Two spaces before end-of-line comments.

void f(bool b) {  // Open braces should always have a space before them.
  ...
int i = 0;  // Semicolons usually have no space before them.
// Spaces inside braces for braced-init-list are optional.  If you use them,
// put them on both sides!
int x[] = { 0 };
int x[] = {0};

// Spaces around the colon in inheritance and initializer lists.
class Foo : public Bar {
 public:
  // For inline function implementations, put spaces between the braces
  // and the implementation itself.
  Foo(int b) : Bar(), baz_(b) {}  // No spaces inside empty braces.
  void Reset() { baz_ = 0; }  // Spaces separating braces from implementation.
  ...
```

후행 공백을 추가하면 기존 후행 공백을 제거할 수 있는 것처럼 다른 사람이 병합할 때 동일한 파일을 편집하는 데 추가 작업이 발생할 수 있습니다. 따라서 후행 공백을 도입하지 마세요. 해당 줄을 이미 변경하고 있는 경우 이를 제거하거나 별도의 정리 작업으로 수행하십시오(가급적이면 파일에 대해 작업 중인 사람이 없을 때).

```cpp
if (b) {          // Space after the keyword in conditions and loops.
} else {          // Spaces around else.
}
while (test) {}   // There is usually no space inside parentheses.
switch (i) {
for (int i = 0; i < 5; ++i) {
// Loops and conditions may have spaces inside parentheses, but this
// is rare.  Be consistent.
switch ( i ) {
if ( test ) {
for ( int i = 0; i < 5; ++i ) {
// For loops always have a space after the semicolon.  They may have a space
// before the semicolon, but this is rare.
for ( ; i < 5 ; ++i) {
  ...

// Range-based for loops always have a space before and after the colon.
for (auto x : counts) {
  ...
}
switch (i) {
  case 1:         // No space before colon in a switch case.
    ...
  case 2: break;  // Use a space after a colon if there's code after it.
```

```cpp
// Assignment operators always have spaces around them.
x = 0;

// Other binary operators usually have spaces around them, but it's
// OK to remove spaces around factors.  Parentheses should have no
// internal padding.
v = w * x + y / z;
v = w*x + y/z;
v = w * (x + z);

// No spaces separating unary operators and their arguments.
x = -5;
++x;
if (x && !y)
  ...
```

```cpp
// No spaces inside the angle brackets (< and >), before
// <, or between >( in a cast
std::vector<std::string> x;
y = static_cast<char*>(x);

// No spaces between type and pointer.
std::vector<char*> x;
```

---

## 옮긴이 풀이

### 핵심: 자리에 따라 다르게, 줄 끝 공백은 절대 금지

가로 공백은 위치마다 규칙이 다릅니다. 공통적으로 **줄 끝 공백(trailing whitespace)은 두지 마세요** — 병합·편집 때 불필요한 충돌을 만듭니다.

### 주요 규칙

```cpp
int i = 0;          // 줄 끝 주석 앞에는 공백 2칸
void f(bool b) {    // 여는 { 앞에는 항상 공백
x = 0;              // 대입 연산자 주위에는 항상 공백
v = w * x + y / z;  // 이항 연산자 주위 공백(인수 주위는 빼도 OK)
x = -5; ++x;        // 단항 연산자와 인수 사이엔 공백 없음
std::vector<std::string> x;     // <, > 안쪽엔 공백 없음
y = static_cast<char*>(x);      // 캐스트의 >( 사이 공백 없음
class Foo : public Bar { ... }; // 상속·초기화 목록의 : 주위엔 공백
for (auto x : counts) { ... }   // range-for의 : 양쪽엔 공백
```

- 조건·반복문 키워드 뒤(`if (`, `while (`)에는 공백. 괄호 **안쪽**은 보통 공백 없음(있어도 되지만 드묾 — 일관되게).
- `switch` case의 `:` 앞에는 공백 없음, 뒤에 코드가 있으면 공백.
