# 상수 이름 (Constant Names)

constexpr 또는 const 로 선언되고 해당 값이 프로그램 기간 동안 고정되는 변수의 이름은 앞에 "k" 뒤에 대소문자가 혼합되어 지정됩니다. 밑줄은 대문자를 구분에 사용할 수 없는 드문 경우에 구분 기호로 사용할 수 있습니다. 예를 들어:

```cpp
const int kDaysInAWeek = 7;
const int kAndroid8_0_0 = 24;  // Android 8.0.0
```

정적 저장 기간이 있는 모든 변수(예: 정적 변수 및 전역 변수, 자세한 내용은 저장 기간 참조)는 정적 상수 클래스 데이터 멤버인 변수와 템플릿의 다양한 인스턴스화가 다른 값을 가질 수 있는 템플릿의 변수를 포함하여 이 방식으로 이름을 지정해야 합니다. 이 규칙은 자동 변수와 같은 다른 저장소 클래스의 변수에 대해서는 선택 사항입니다. 그렇지 않으면 일반적인 변수 명명 규칙이 적용됩니다. 예를 들어:

```cpp
void ComputeFoo(absl::string_view suffix) {
  // Either of these is acceptable.
  const absl::string_view kPrefix = "prefix";
  const absl::string_view prefix = "prefix";
  ...
}
```

```cpp
void ComputeFoo(absl::string_view suffix) {
  // Bad - different invocations of ComputeFoo give kCombined different values.
  const std::string kCombined = absl::StrCat(kPrefix, suffix);
  ...
}
```

---

## 이해하기 쉽게 설명하기

### 핵심: 상수는 k 접두사 + PascalCase

`constexpr`/`const`로 선언되고 값이 프로그램 내내 고정되는 변수는 `k` 다음에 PascalCase로 씁니다.

```cpp
const int kDaysInAWeek = 7;
const int kAndroid8_0_0 = 24;  // 대문자로 구분 못 할 땐 밑줄 허용
```

### 어디에 적용되나

- **정적 저장 기간** 변수(전역·정적 변수, 정적 상수 클래스 멤버 등)는 **반드시** 이 규칙을 따릅니다.
- 지역 변수(자동 저장 기간)는 선택 — 일반 변수 명명을 써도 됩니다.

```cpp
void ComputeFoo(absl::string_view suffix) {
  const absl::string_view kPrefix = "prefix";  // 둘 다 허용
  const absl::string_view prefix = "prefix";

  // 나쁨: 호출마다 값이 달라지므로 k 접두사는 부적절
  const std::string kCombined = absl::StrCat(kPrefix, suffix);
}
```
